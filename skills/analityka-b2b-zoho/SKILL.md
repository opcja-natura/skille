---
name: analityka-b2b-zoho
description: Liczenie sprzedaży B2B Opcji Natury w Zoho Analytics (workspace „Analityka B2B", kopia Bigina odświeżana codziennie rano) — obroty za okres, miesiące i kwartały, porównania r/r, rankingi klientów i produktów, koszyk klienta, klienci spadający/zamilkli, RFM, należności w sumie. Gotowe org-id i workspace-id, mapa kolumn Analytics↔Bigin, sprawdzone zapytania SQL i pułapki. Używaj ZAWSZE, gdy odpowiedź wymaga zsumowania lub porównania więcej niż kilkunastu zamówień — zamiast ciągnąć rekordy z Bigina. NIE do rekordów z dzisiaj, pojedynczych zamówień, kontaktów i zapisu (to skill bigin-opcja-natura).
---

# Analityka B2B – Zoho Analytics

Bigin przez MCP nie sumuje (brak `SUM/COUNT/GROUP BY`), więc każda suma to pobranie wszystkich rekordów do rozmowy. Zoho Analytics ma **kopię tych samych danych z Bigina** i liczy SQL-em po swojej stronie — do rozmowy wraca kilka wierszy wyniku. Nazwy potoków i etapów są takie jak w Biginie (lista w skillu `bigin-opcja-natura`).

Sprawdzone na żywych danych 25.09.2026, w tym spójność: wrzesień 1–24 w Analytics i w Biginie = 92 zamówienia, 153 040 zł (zgodne co do złotówki).

## Kiedy które źródło

| Pytanie | Źródło |
|---|---|
| sprzedaż / obrót za okres, miesiące, porównania r/r, średnie | **Analytics** |
| ranking klientów lub produktów, udziały, segmenty, trendy | **Analytics** |
| co klient kupuje (produkty, ilości) | **Analytics** (`Associated Products`) |
| klienci spadający, zamilkli, RFM, „kto odbiega od normy" | **Analytics** (`DATA Client new`, `Dynamika klientow`) |
| co wpadło **dziś**, stan konkretnego zamówienia, faktura, dane kontaktowe, warunki klienta | **Bigin** |
| rozmowy, zadania, notatki, zapis czegokolwiek | **Bigin** |

⚠️ **Analytics jest aktualne do wczoraj.** Synchronizacja z Biginem idzie raz dziennie, rano (ostatnia 25.09 o 6:05). Zamówień z dzisiaj tam nie ma. Przy pytaniu o bieżący tydzień podaj sumę z Analytics i dopisz dzisiejsze rekordy z Bigina — albo powiedz wprost, że wynik jest do wczoraj.

## Stałe (nie ma narzędzia do ich wyszukania — używaj tych)
- org-id: `20105203197`
- workspace-id („Analityka B2B"): `263383000000002011`

## Narzędzia i kolejność
1. `createExportJobSQLQuery` z org-id, workspace-id i zapytaniem SQL (MySQL-owe) → zwraca job-id. Jeśli narzędzie pyta o format, wybierz **CSV** (lżejszy niż JSON).
2. `downloadExportedData` z org-id, workspace-id i job-id → wynik. Jeśli job jeszcze nie gotowy, ponów za chwilę.
3. `getViewDetails` / `getQueryTableDetails` — **tylko** gdy kolumny nie ma w tym skillu (błąd „nieprawidłowa kolumna"). Nie na rozgrzewkę.
4. `exportDataView` eksportuje **cały widok naraz** — nigdy na tabelach bazowych (`Pipelines` ma 14 tys. wierszy, `Associated Products` więcej). Tylko do małych, gotowych widoków.

**Zasada:** eksport SQL zwraca **wszystkie** wiersze wyniku. Zawsze agreguj (`GROUP BY`) i ograniczaj (`LIMIT`) w SQL — nigdy `SELECT *` z tabeli bazowej.

## Tabele (nazwy w SQL w cudzysłowach)

**`Pipelines`** — ten sam moduł co w Biginie, ale kolumny mają **inne nazwy**:

| Analytics | = Bigin | Uwaga |
|---|---|---|
| `"Id"` | `id` | |
| `"Pipeline Nazwa Rekordu"` | `Deal_Name` | |
| `"Account Name"` | `Account_Name` | **liczba = id klienta**, nie nazwa → join z `"Klienci"."Id"` |
| `"Potok podrzędny"` | potok | **tu filtr po potoku działa**: `'Zamówienia'`, `'Faktury Standardowy'`, `'Akcje Promo i Marketing Standardowy'`, `'Pozyskiwanie klientów Standardowy'`, `'Rozliczenia retro'`, `'standy Standardowy'`… |
| `"Stage"` | `Stage` | nazwy jak w Biginie |
| `"Amount"` | `Amount` | netto, CURRENCY — sumuj wprost. ⚠️ Wypełniony tylko w zamówieniach i fakturach: w `Rozliczenia retro` jest pusty (kwota w Biginie w `Warto_c_wpisywana_z_apy`, wpisywana ręcznie, bez wyliczenia — skill `bigin-opcja-natura`, `references/rozliczenia-retro.md`); sprawdź, czy ta kolumna jest w tabeli, zanim policzysz retro |
| `"Closing Date"` | `Closing_Date` | **oś czasu sprzedaży** (data zamówienia); na fakturach = termin płatności |
| `"Czas Utworzenia"` | `Created_Time` | ⚠️ **nie do okresów** — historia 2023–24 ma datę importu (2025) |
| `"Klient Handlowiec"` | handlowiec | ⚠️ tekst z **cudzysłowami w wartości** (`"Łukasz"`) → filtruj `LIKE '%Łukasz%'`, nie `=` |
| `"cel akcji"`, `"Data rozpoczęcia akcji"`, `"Data zakończenia akcji"`, `"całkowity koszt akcji waluta"`, `"Wartość sprzedaży netto"` | pola akcji | koszt akcji licz **tylko** z `"całkowity koszt akcji waluta"` (CURRENCY); `"Całkowity koszt akcji"` to tekst |
| `"baselinkerOrderId"` | `baselinkerOrderId` | łącznik zamówienie↔faktura |

**`Associated Products`** — pozycje zamówień: `"Deal Id"` (= `Pipelines."Id"`), `"Product Id"` (= `Produkty."Id"`), `"Quantity"`, `"wartość netto"` (CURRENCY, po rabacie), `"Discount"`.
**`Produkty`** — `"Id"`, `"Produkt - nazwa"`, `"Product Category"`, `"Cena netto"`.
**`Klienci`** — `"Id"`, `"Klient - nazwa"`, `"Segment"`, `"Klient Handlowiec Human"` (imię handlowca), `"Klient - status"`, `"Klient - ostatnie zamówienie"`, `"Wartość klienta PLN"` (CURRENCY — **tu wartość jest liczbą**, sortuje się poprawnie), `"wartość rabatu"`, `"Termin płatności - dni"`.
**`DATA Client new`** — gotowy RFM na klienta (nie licz od zera): `"Client ID"`, `"Client Name"`, `"Client Merchant Id"` (= id handlowca), `"Segment"` (kanał), `"Value Segment"` (Premium/High Value/Medium Value/Low Value/Minimal), `"Total Revenue"`, `"Last Order Date"`, `"Avg Days Between Orders"`, `"Orders 2025 Q1"`…`"Orders 2026 Q4"`, `"Orders Last 3 Months"`, `"Growth Trend"`, `"Client Status"`, `"Status aktywności"`.
**`Dynamika klientow`** — kto zachował się inaczej niż zwykle: `"Klient ID"`, `"Klient"`, `"Kanal"`, `"Segment wartosci"`, `"Obrot 3M"`, `"Norma 3M"`, `"Sygnal"` (`01_ZALAMANIE`, `02_WYSKOK`…), `"Obrot 12M"`, `"Obrot 12M rok temu"`, `"Trend proc"`. Nie ma kolumny handlowca → portfel przez join z `"Klienci"` po `"Klient ID"` = `"Id"`.

## Sprawdzone zapytania

**Sprzedaż handlowca po miesiącach:**
```sql
SELECT YEAR("Closing Date") AS rok, MONTH("Closing Date") AS mc,
       count(*) AS zamowienia, ROUND(sum("Amount"),2) AS netto,
       count(DISTINCT "Account Name") AS klienci
FROM "Pipelines"
WHERE "Potok podrzędny" = 'Zamówienia' AND "Stage" <> 'Zamknięty, utracony'
  AND "Klient Handlowiec" LIKE '%Łukasz%' AND "Closing Date" >= '2026-01-01'
GROUP BY YEAR("Closing Date"), MONTH("Closing Date") ORDER BY rok, mc
```

**Kwartały r/r (cała sprzedaż B2B):**
```sql
SELECT YEAR("Closing Date") AS rok, QUARTER("Closing Date") AS q, count(*) AS zam,
       ROUND(sum("Amount"),0) AS netto, count(DISTINCT "Account Name") AS klienci
FROM "Pipelines"
WHERE "Potok podrzędny" = 'Zamówienia' AND "Stage" <> 'Zamknięty, utracony'
  AND "Closing Date" >= '2024-01-01'
GROUP BY YEAR("Closing Date"), QUARTER("Closing Date") ORDER BY rok, q
```

**Miesiące „te same dni" (uczciwe porównanie niepełnego miesiąca):**
```sql
SELECT MONTH("Closing Date") AS mc, count(*) AS zam, ROUND(sum("Amount"),0) AS netto,
       count(DISTINCT "Account Name") AS klienci
FROM "Pipelines"
WHERE "Potok podrzędny" = 'Zamówienia' AND "Stage" <> 'Zamknięty, utracony'
  AND "Closing Date" >= '2026-04-01' AND DAY("Closing Date") <= 24
GROUP BY MONTH("Closing Date") ORDER BY mc
```

**Kto odpowiada za spadek miesiąca** (średnia miesięczna vs bieżący miesiąc):
```sql
SELECT k."Klient - nazwa" AS klient,
  ROUND(sum(CASE WHEN p."Closing Date" BETWEEN '2026-01-01' AND '2026-08-31' THEN p."Amount" ELSE 0 END)/8,0) AS sr_mc,
  ROUND(sum(CASE WHEN MONTH(p."Closing Date")=9 THEN p."Amount" ELSE 0 END),0) AS biezacy,
  max(p."Closing Date") AS ostatnie
FROM "Pipelines" p JOIN "Klienci" k ON p."Account Name" = k."Id"
WHERE p."Potok podrzędny" = 'Zamówienia' AND p."Stage" <> 'Zamknięty, utracony'
  AND p."Closing Date" BETWEEN '2026-01-01' AND '2026-09-24'
GROUP BY k."Klient - nazwa" ORDER BY sr_mc DESC LIMIT 20
```
Potem dla podejrzanych klientów rozpisz miesiące (`GROUP BY klient, MONTH(...)`), żeby odróżnić **rytm** (duże zamówienie co 2–3 miesiące) od **erozji** (spadek kilka miesięcy z rzędu).

**Na tle kanałów:** join z `"Klienci"` i `GROUP BY k."Segment"` z tymi samymi `CASE WHEN`.

**Należności po terminie per klient:**
```sql
SELECT k."Klient - nazwa" AS klient, count(*) AS fv, ROUND(sum(p."Amount"),0) AS netto,
       min(p."Closing Date") AS najstarszy_termin
FROM "Pipelines" p JOIN "Klienci" k ON p."Account Name" = k."Id"
WHERE p."Potok podrzędny" = 'Faktury Standardowy'
  AND p."Stage" IN ('Wystawiono Fakture','Faktura po terminie platnosci')
  AND p."Closing Date" < '2026-09-25'
GROUP BY k."Klient - nazwa" ORDER BY netto DESC LIMIT 15
```

**Top produkty w okresie:**
```sql
SELECT pr."Produkt - nazwa" AS produkt, sum(ap."Quantity") AS szt,
       ROUND(sum(ap."wartość netto"),2) AS netto
FROM "Associated Products" ap
JOIN "Pipelines" p ON ap."Deal Id" = p."Id"
JOIN "Produkty" pr ON ap."Product Id" = pr."Id"
WHERE p."Potok podrzędny" = 'Zamówienia' AND p."Klient Handlowiec" LIKE '%Łukasz%'
  AND p."Closing Date" >= '2026-09-01'
GROUP BY pr."Produkt - nazwa" ORDER BY netto DESC LIMIT 15
```
Koszyk jednego klienta: zamień filtr handlowca na `p."Account Name" = <id klienta>`.

**Top klienci w okresie (z nazwą):**
```sql
SELECT k."Klient - nazwa" AS klient, count(*) AS zamowienia, ROUND(sum(p."Amount"),2) AS netto
FROM "Pipelines" p JOIN "Klienci" k ON p."Account Name" = k."Id"
WHERE p."Potok podrzędny" = 'Zamówienia' AND p."Klient Handlowiec" LIKE '%Łukasz%'
  AND p."Closing Date" >= '2026-07-01'
GROUP BY k."Klient - nazwa" ORDER BY netto DESC LIMIT 20
```

**Klienci z sygnałem (spadek/wyskok):**
```sql
SELECT d."Klient", d."Sygnal", d."Obrot 3M", d."Norma 3M", d."Trend proc"
FROM "Dynamika klientow" d JOIN "Klienci" k ON d."Klient ID" = k."Id"
WHERE k."Klient Handlowiec Human" LIKE '%Łukasz%' AND d."Sygnal" LIKE '01%'
LIMIT 30
```

## Pułapki
- **Oś czasu = `"Closing Date"`.** Historia z lat 2023–2024 była importowana w 2025, więc po `"Czas Utworzenia"` porównania r/r wychodzą bzdurne.
- **Porównując niepełny miesiąc, porównuj te same dni:** `DAY("Closing Date") <= 24` dla wszystkich miesięcy, inaczej „wrzesień do 24." przegra z pełnym sierpniem.
- **Stare faktury „po terminie" (termin w 2025) mogą być nieaktualne** — status nieprzestawiony po zapłacie. Przy należnościach starszych niż ~3 miesiące pisz „do sprawdzenia w wFirmie".
- **`query` może odpowiedzieć „queue processing is slow"** — to kolejka po stronie Zoho, ponów to samo zapytanie.
- Jako opiekun (`"Klient Handlowiec"`) występuje praktycznie tylko Łukasz (~95% obrotu) i Daniel (mniejsze konta) — suma „wszystkich handlowców" ≈ cały B2B.
- **Sumy CURRENCY wychodzą jako długie ułamki** (`315221.39999999997`) → zawsze `ROUND(sum(...),2)`.
- **W CSV wartości z przecinkiem rozjeżdżają się na kilka kolumn**: `Segment` („Drogeryjny (punkty, zrzeszenia, hurtownie)"), kwoty w formacie `PLN 3,087.59`, daty `28 May, 2024`. To jedna wartość — czytaj ostrożnie albo wybieraj mniej takich kolumn.
- **`"kol"+0` skleja tekst** zamiast dodawać. Liczby tylko z kolumn CURRENCY/NUMBER.
- **`ORDER BY`/`GROUP BY` nie przyjmą agregatu wprost** — użyj aliasu (`ORDER BY netto`).
- Najwyżej **jeden poziom podzapytania**.
- Zamówienia i faktury są oddzielnymi rekordami także tutaj — sprzedaż licz z `'Zamówienia'`, należności z `'Faktury Standardowy'`.
