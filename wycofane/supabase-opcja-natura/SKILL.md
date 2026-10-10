---
name: supabase-opcja-natura
description: >
  Obsługa dwóch projektów Supabase dla Opcja Natura przez MCP.
  Używaj gdy Daniel pyta o dane ze sklepu e-commerce (zamówienia, klienci, sprzedaż, lojalność)
  lub o dane social media (posty, reakcje, komentarze).
  Triggeruje na: "sprawdź w supabase", "zapytaj bazę", "ile zamówień", "ile postów",
  "dane o klientach", "reakcje na posty", "program lojalnościowy", "sprawdź tabelę".
  NIGDY nie modyfikuj struktury baz — tylko SELECT. Produkcja.
---

# Supabase — Opcja Natura: dwa projekty

## Projekty

| Projekt | ID | Opis |
|---|---|---|
| **store** | `nmgxsrkxbbkutqucedmm` | Sklep e-commerce — zamówienia, klienci, produkty |
| **socialAutomation** | `thvvzdbhqtklehhwsffi` | Social media — posty, reakcje, komentarze |

Zawsze używaj `Supabase:execute_sql` z odpowiednim `project_id`.

---

## PROJEKT 1 — store (`nmgxsrkxbbkutqucedmm`)

**Schemat: `prod`** — wszystkie tabele wymagają prefixu `prod.`

### Tabele i ich rola

#### `prod.order` — zamówienia (~87 000 rekordów)
Główna tabela sprzedaży e-commerce (sklep opcjanatura.pl).

| Kolumna | Typ | Opis |
|---|---|---|
| `id` | text PK | Unikalny ID zamówienia |
| `order_id` | text | Alternatywny ID (używany jako FK w innych tabelach) |
| `email` | text | Email klienta — klucz do identyfikacji nowy/powracający |
| `account_id` | text FK | Powiązanie z kontem (NULL = zakup bez rejestracji) |
| `date_created` | timestamp | Data złożenia zamówienia |
| `status` | enum | NEW / PAID / SHIPPED / DELIVERED / CANCELLED / REPLACED |
| `grand_total` | numeric | Wartość zamówienia **z VAT** (brutto) |
| `tax_total` | numeric | Kwota VAT |
| `discount_total` | numeric | Suma rabatów |
| `shipping_service_id` | text FK | Metoda dostawy |
| `coupon_code` | text | Użyty kupon |
| `loyalty_points_used` | integer | Użyte punkty lojalnościowe |

> **Przychód netto = grand_total - tax_total** — zawsze tak liczymy.

#### `prod.order_item` — pozycje zamówień (~233 000 rekordów)

| Kolumna | Typ | Opis |
|---|---|---|
| `id` | text PK | ID pozycji |
| `order_order_id` | text FK | Łączy z `prod.order.order_id` |
| `product_id` | text | ID produktu |
| `name` | text | Nazwa produktu w momencie zakupu |
| `sku` | text | SKU produktu |
| `quantity` | integer | Ilość sztuk |
| `unit_price` | numeric | Cena jednostkowa |
| `price_total` | numeric | Wartość pozycji |
| `tax_rate` | numeric | Stawka VAT |

#### `prod.account` — konta klientów (~22 700 rekordów)

| Kolumna | Typ | Opis |
|---|---|---|
| `id` | text PK | ID konta |
| `email` | text | Email (klucz do łączenia z order) |
| `email_optin` | boolean | Zgoda na newsletter |
| `is_loyalty_member` | boolean | Uczestnik programu lojalnościowego |
| `loyalty_membership_status` | enum | BRONZE / SILVER / GOLD |
| `loyalty_points` | integer | Aktualne saldo punktów |
| `date_created` | timestamp | Data rejestracji konta |

#### `prod.loyalty_points_item` — historia programu lojalnościowego (~8 000 rekordów)

| Kolumna | Typ | Opis |
|---|---|---|
| `PK` | text PK | Unikalny klucz (uwaga: wielka litera!) |
| `account_id` | text FK | Łączy z `prod.account.id` |
| `item_type` | enum | ORDER / ENROLLMENT / RECOMMENDATION / REVIEW |
| `loyalty_points_granted` | integer | Przyznane punkty |
| `loyalty_points_used` | integer | Użyte punkty |
| `status` | enum | CONFIRMED / BLOCKED / DELETED |
| `date_updated` | timestamp | Data zdarzenia |
| `order_id` | text | Powiązane zamówienie (jeśli dotyczy) |
| `email` | text | Email konta |

#### `prod.email_campaign` — kampanie newsletterowe

| Kolumna | Typ | Opis |
|---|---|---|
| `campaign_id` | text PK | ID kampanii |
| `name` | text | Nazwa kampanii |
| `subject` | text | Temat emaila |
| `event_type` | enum | B2C lub B2B |
| `isTestCampaign` | boolean | Czy kampania testowa |
| `date_updated` | timestamp | Data wysyłki |

#### `prod.email_campaign_tracking_event` — reakcje na kampanie (~3 500 rekordów)

| Kolumna | Typ | Opis |
|---|---|---|
| `campaign_id` | text FK | Łączy z `email_campaign` |
| `email` | text | Kto zareagował |
| `event_type` | enum | OPEN lub CLICK |
| `link` | text | Kliknięty link (tylko dla CLICK) |
| `date_updated` | timestamp | Czas zdarzenia |

#### `prod.product` — katalog produktów

| Kolumna | Typ | Opis |
|---|---|---|
| `product_id` | text PK | ID produktu |
| `name` | text | Nazwa |
| `sku` | text | SKU |
| `ean` | text | Kod EAN |
| `price_net` | numeric | Cena netto |
| `cost_price_net` | numeric | Koszt zakupu netto |
| `vat_rate` | numeric | Stawka VAT |

#### Tabele pomocnicze (store)
- `prod.shipping_service` — metody dostawy (7 rekordów)
- `prod.cart` — koszyki (usuwane po 30 dniach, ~9 000 aktualnych)
- `prod.discount_item` — pozycje rabatów
- `prod.baselinker_order` / `prod.baselinker_order_line` — zamówienia marketplace (marginalne)

### Wzorce zapytań — store

**Przychód netto MoM:**
```sql
SELECT
  TO_CHAR(date_created, 'YYYY-MM') AS okres,
  SUM(grand_total - tax_total) AS przychod_netto,
  COUNT(*) AS liczba_zamowien,
  ROUND(AVG(grand_total - tax_total), 2) AS aov_netto
FROM prod.order
WHERE status NOT IN ('CANCELLED', 'REPLACED')
GROUP BY 1
ORDER BY 1 DESC;
```

**Nowi vs powracający klienci MoM:**
```sql
SELECT
  TO_CHAR(o.date_created, 'YYYY-MM') AS okres,
  COUNT(CASE WHEN o.date_created = first_order.first_date THEN 1 END) AS nowi,
  COUNT(CASE WHEN o.date_created > first_order.first_date THEN 1 END) AS powracajacy
FROM prod.order o
JOIN (
  SELECT email, MIN(date_created) AS first_date
  FROM prod.order
  GROUP BY email
) first_order ON o.email = first_order.email
WHERE o.status NOT IN ('CANCELLED', 'REPLACED')
GROUP BY 1
ORDER BY 1 DESC;
```

**Newsletter — open i click rate per kampania:**
```sql
SELECT
  c.campaign_id,
  c.name,
  c.date_updated AS data_wysylki,
  COUNT(CASE WHEN t.event_type = 'OPEN' THEN 1 END) AS otwarcia,
  COUNT(CASE WHEN t.event_type = 'CLICK' THEN 1 END) AS klikniecia
FROM prod.email_campaign c
LEFT JOIN prod.email_campaign_tracking_event t USING (campaign_id)
WHERE c.event_type = 'B2C'
GROUP BY 1, 2, 3
ORDER BY 3 DESC;
```

---

## PROJEKT 2 — socialAutomation (`thvvzdbhqtklehhwsffi`)

**Schemat: `public`** — tabele bez prefixu schematu (lub z `public.`).

> ⚠️ Nazwy tabel i kolumn używają **polskich nazw z wielkimi literami i spacjami** — wymagają podwójnych cudzysłowów: `"Posty"`, `"Data Utworzenia"`.

### Tabele kluczowe

#### `"Posty"` — posty social media (347 rekordów)

| Kolumna | Typ | Opis |
|---|---|---|
| `"ID"` | text PK | ID posta (format platformy: np. `17883232785483732`) |
| `"Platforma"` | enum | INSTAGRAM / FACEBOOK / INNA |
| `"Opis"` | text | Treść/caption posta |
| `"Permalink"` | text | Link do posta |
| `"Zdjęcie URL"` | text | URL zdjęcia |
| `"Data Utworzenia"` | timestamp | Kiedy opublikowano |
| `"Data Aktualizacji"` | timestamptz | Ostatnia synchronizacja |
| `"Ilość komentarzy"` | integer | Liczba komentarzy |

#### `reactions` — reakcje na posty (2 112 rekordów)

| Kolumna | Typ | Opis |
|---|---|---|
| `id` | text PK | Generowany: `from_id + '_' + post_id` |
| `post_id` | text | Łączy z `"Posty"."ID"` |
| `from_id` | text | ID użytkownika który zareagował |
| `from_name` | text | Nazwa użytkownika |
| `reaction_type` | text | like / love / haha / care / wow / angry / sad |
| `created_time` | timestamptz | Czas reakcji |
| `parent_id` | text | Jeśli reakcja na komentarz (nullable) |

**Rozkład reaction_type (aktualne dane):**
- `like` — 1 772 (84%)
- `love` — 318 (15%)
- `haha / care / wow / angry / sad` — marginalne

### Tabele pomocnicze (socialAutomation)
- `"Komentarze"` — komentarze pod postami z workflow odpowiadania AI (2 513 rekordów)
- `"Odpowiedzi"` — wygenerowane odpowiedzi AI (1 465 rekordów)
- `products` — dane produktów do kontekstu AI (73 rekordy)
- `"Limity"` — limity API (1 583 rekordów)
- `flags` — flagi do komentarzy (4 rekordy)
- `"Maile"` — obsługa emaili (19 rekordów)

### Wzorce zapytań — socialAutomation

**Posty z liczbą reakcji:**
```sql
SELECT
  p."ID",
  p."Platforma",
  p."Data Utworzenia",
  p."Opis",
  COUNT(r.id) AS liczba_reakcji,
  COUNT(CASE WHEN r.reaction_type = 'like' THEN 1 END) AS like_count,
  COUNT(CASE WHEN r.reaction_type = 'love' THEN 1 END) AS love_count
FROM public."Posty" p
LEFT JOIN public.reactions r ON r.post_id = p."ID"
GROUP BY 1, 2, 3, 4
ORDER BY p."Data Utworzenia" DESC;
```

**Posty MoM per platforma:**
```sql
SELECT
  TO_CHAR("Data Utworzenia", 'YYYY-MM') AS okres,
  "Platforma",
  COUNT(*) AS liczba_postow
FROM public."Posty"
GROUP BY 1, 2
ORDER BY 1 DESC;
```

---

## Zasady ogólne

1. **NIGDY nie modyfikuj struktury** — tylko `SELECT`. Oba projekty to produkcja.
2. **store**: zawsze prefix `prod.` przed nazwą tabeli
3. **socialAutomation**: polskie nazwy z cudzysłowami: `"Posty"`, `"Data Utworzenia"`, `"Ilość komentarzy"`
4. **Łączenie projektów**: nie ma bezpośredniego FK między projektami — można łączyć przez wspólne klucze biznesowe (np. `product_id` / `ean`) w logice aplikacji
5. **Daty w store**: kolumna `date_created` (timestamp bez strefy)
6. **Daty w socialAutomation**: `"Data Utworzenia"` (timestamp), `"Data Aktualizacji"` (timestamptz)
