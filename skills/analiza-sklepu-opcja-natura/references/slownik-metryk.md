# Słownik metryk sklepu opcjanatura.pl (wersja 1.2, 25.11.2026)

> Jedyne obowiązujące definicje. Te same definicje stosują dashboardy Metabase (Sklep · Puls, Kupony influ, Program lojalnościowy + newsletter). Zmiany zatwierdza Daniel.

## Po co i zasady

Każda karta w Metabase i każda analiza sklepu www liczy według tego słownika. Gdy definicja się zmienia, najpierw zmieniamy słownik (wpis w „Historia zmian”), dopiero potem karty. Karta, która liczy inaczej, jest błędem, nawet jeśli wynik wygląda rozsądnie.

- **Status definicji:** `USTALONE` (decyzja Daniela, z datą) · `DO ZATWIERDZENIA` (propozycja, do akceptacji).
- **Baza:** Supabase sklep `nmgxsrkxbbkutqucedmm`, schemat `prod` (+ `marketing`, `ads`). Tylko SELECT.
- **Weryfikacja:** po każdej zmianie kart niezależny weryfikator (inny model, bez wglądu w SQL kart) liczy kluczowe liczby z tego słownika i porównuje je z dashboardem. 

## 1. Zamówienia i przychód

| Pojęcie | Definicja | SQL | Status |
|---|---|---|---|
| **Zamówienie zrealizowane** | opłacone (nowa era) albo doręczone (stara era, do 03.2024); anulowane nigdy | `status IN ('PAID','DELIVERED')` | USTALONE (07.2026) |
| **Przychód netto** | wartość kosmetyków bez VAT i **bez wysyłki** | `(grand_total - tax_total) - coalesce(shipment_total,0)/1.23` | USTALONE (08.08.2026) |
| **Koszyk brutto** (do progu dostawy) | wartość kosmetyków z VAT, bez dostawy | `grand_total - coalesce(shipment_total,0)` | USTALONE (25.11.2026) |
| **AOV / średni koszyk** | przychód netto ÷ liczba zamówień zrealizowanych | | USTALONE |
| **Doba / dzień / miesiąc** | doba polska dla **wszystkich** znaczników czasu w bazie (zamówienia, punkty, newsletter); tak samo cięcie tygodni i miesięcy. Znaczniki w bazie są w UTC | `(kolumna at time zone 'UTC' at time zone 'Europe/Warsaw')` | USTALONE (09.10.2026; rozszerzone 25.11.2026) |
| **Wpływy z wysyłki** | opłaty za dostawę bez VAT; po stronie przychodu NIE wliczamy | `coalesce(shipment_total,0)/1.23` | USTALONE |
| **COGS** | koszt kosmetyków + 2 zł/szt. (pakowanie, wahania cen) | `quantity * (coalesce(product.cost_price_net,0) + 2)` | USTALONE (08.2026) |
| **Zysk po reklamie** | przychód netto − COGS − wydatek reklamowy (górne oszacowanie: bez kosztu kuriera, obsługi, zwrotów) | | USTALONE |
| **Wydatek reklamowy** | Meta + Google netto, dzień po dniu (TikTok Ads jeszcze nie) | `ads.spend_daily.koszt` | USTALONE (11.08.2026) |
| **MER** | przychód netto ÷ cały wydatek reklamowy, w tym samym oknie | | USTALONE |
| **Zamówienia B2B** | `baselinker_order*` NIE wchodzą do sklepu www | | USTALONE |

## 2. Klientki

| Pojęcie | Definicja | SQL | Status |
|---|---|---|---|
| **Klientka** | osoba = e-mail (68 % zamówień to zakupy bez konta) | `lower(email)` | USTALONE |
| **Pierwsze zamówienie** | najwcześniejsze **zrealizowane** zamówienie na ten e-mail (historia od 09.2022) | `min(date_created)` po `lower(email)` wśród zrealizowanych | USTALONE |
| **Nowa klientka (w okresie)** | jej pierwsze zamówienie wypada w okresie | | USTALONE |
| **Powracająca** | zamówienie zrealizowane, które nie jest jej pierwszym | | USTALONE |
| **% nowych** (przy kodzie, kanale, okresie) | udział zamówień, które są pierwszym zamówieniem klientki, w zamówieniach danej grupy | | USTALONE (25.11.2026) |
| **CAC** | wydatek reklamowy ÷ nowe klientki w tym samym oknie | | USTALONE |
| **Powrót w N dni** | drugie zrealizowane zamówienie najpóźniej N × 24 h po pierwszym. Kohorty miesięczne pokazujemy tylko pełne (cały miesiąc ma już N dni). Przy podziale członkinie / reszta: członkostwo to stan dzisiejszy, więc to związek, nie dowód skutku programu | | USTALONE (doprecyzowane 25.11.2026) |

## 3. Program lojalnościowy Moja Opcja Natura (od 03.06.2025)

| Pojęcie | Definicja | SQL | Status |
|---|---|---|---|
| **Członkini** | konto w programie, **stan dzisiejszy** (baza nie trzyma historii członkostwa) | `account.is_loyalty_member` | USTALONE |
| **Zamówienie członkini** („stała w programie”) | zamówienie, którego e-mail należy do konta członkini (także zakup bez logowania na ten e-mail) — spójnie z „klientka = e-mail”. Stan dzisiejszy, więc dla dawnych okresów zawyżone | `lower(order.email) IN (SELECT lower(email) FROM account WHERE is_loyalty_member)` | USTALONE (25.11.2026, po weryfikacji) |
| **Zgoda członkini** | zapis do programu = zgoda na **komunikację programu** (np. przypomnienie o wygasających punktach). To NIE jest zgoda na newsletter: newsletter idzie wyłącznie do `email_optin` | | USTALONE (Daniel, 25.11.2026) |
| **Data zapisu** | zapis potwierdzony = doręczenie paczki z pierwszym zamówieniem w programie. Gdy punkty wygasły (fala od 06.2026), zapis ma status DELETED, a jego `date_updated` to data wygaśnięcia, więc data zapisu = `date_updated − 1 rok`. 5 zapisów DELETED sprzed 06.2026 pomijamy (inny mechanizm, nie wygaśnięcie) | `status = 'CONFIRMED'` → `date_updated`; `status = 'DELETED' AND date_updated >= '2026-06-01'` → `date_updated - interval '1 year'`; doba PL | USTALONE (17.09.2026; doprecyzowane 25.11.2026) |
| **Liczba członkiń w czasie** | narastająco po dacie zapisu, z zapisami CONFIRMED i DELETED; konta bez eventu zapisu opisujemy osobno | | USTALONE |
| **Zakup z punktami** | zamówienie zrealizowane z realizacją punktów | `loyalty_points_used > 0` | USTALONE |
| **Powrót z zarobionymi punktami** (dawniej „powrót po punkty”) | zakup z punktami, przed którym klientka miała już na koncie co najmniej jedno zrealizowane zamówienie **nagrodzone punktami w programie**. Nie liczymy pierwszego zakupu z punktami, który jest tylko odebraniem zniżki (np. 50 pkt bonusu powitalnego). Główny wskaźnik programu. | `loyalty_points_used > 0` i istnieje zrealizowane zamówienie tego `account_id` o wcześniejszym `date_created`, z `loyalty_points_item` `item_type='ORDER'`, `status IN ('CONFIRMED','DELETED')` | USTALONE (Daniel, 25.11.2026); XI 2026: 149 z 365 zakupów z punktami |
| **Wartość punktu** | 1 pkt = 0,05 zł | `loyalty_points_used * 0.05` | USTALONE (sprawdzone w `discount_item`) |
| **Koszt programu** | wartość zrealizowanych punktów w zł, **ze wszystkich** zakupów z punktami (także pierwszego odebrania bonusu); zestawiany z przychodem z powrotów, co trzeba napisać przy karcie | `sum(loyalty_points_used) * 0.05` | USTALONE (doprecyzowane 25.11.2026) |
| **Zobowiązanie** | niewykorzystane punkty × 0,05 zł; na dashboardach pokazujemy **w zł** (saldo w punktach tylko pomocniczo). Obejmuje też saldo kont, którym termin minął, a system jeszcze punktów nie skasował (ok. 40 zł) | `sum(account.loyalty_points) * 0.05` | USTALONE |
| **Wygasanie punktów** | 12 mies. bez aktywności; aktywność = **zrealizowane** zamówienie złożone **na koncie** albo potwierdzony event punktowy (zakup bez konta na ten e-mail nie przedłuża). Okna „wygaśnie w N dni” = pełne doby PL od dziś do dziś + N | `greatest(max zrealizowane zamówienie po account_id, max event CONFIRMED) + 12 mies.` | USTALONE (07.2026; doprecyzowane 25.11.2026) |

## 4. Kody rabatowe

| Pojęcie | Definicja | SQL | Status |
|---|---|---|---|
| **Kod → rodzaj, influencerka** | widok `marketing.kody_mapa` (arkusz INFLU app → opis kuponu z apki Slack → klasyfikacja ręczna → reguły), z edycjami kodu | `join marketing.kody_mapa c on c.kod = upper(trim(cr.code)) and cr.date_created >= c.edycja_od and cr.date_created < c.edycja_do` | USTALONE (25.11.2026) |
| **Kody influ** | rodzaj `influencer` lub `wspolpraca_reklamowa` | `c.rodzaj in ('influencer','wspolpraca_reklamowa')` | USTALONE (25.11.2026) |
| **Wewnętrzne** | rodzaj `wewnetrzny` (pracownicze, GIGGS): nie pokazujemy | `c.rodzaj <> 'wewnetrzny'` | USTALONE (25.11.2026) |
| **Użycie kodu** | jedno zamówienie z kodem, liczone raz. Karty „wszystkie kody” (bez wewnętrznych) i „kody influ” mają inne sumy — tytuł karty musi mówić, który zakres | `count(distinct order_id)` | USTALONE |
| **Rabat z kodu procentowego na produkt** | `coupon_redemption.value_redeemed` = 0, kwota tylko w `discount_item` | | USTALONE |

## 5. Okresy i porównania

| Pojęcie | Definicja | Status |
|---|---|---|
| **Okres z filtra** | field filter `{{okres}}` na `prod."order".date_created` (pole 308); granice = pierwszy i ostatni dzień zamówień w zakresie; wyczyszczony filtr = cała historia | USTALONE (25.11.2026) |
| **Porównanie** | poprzedni okres tej samej długości; „rok temu” = te same dni tygodnia 364 dni wcześniej | USTALONE (25.11.2026) |
| **Domyślne okno operacyjne** | 7 pełnych dni do wczoraj (dziś−7 … dziś−1) | USTALONE (25.11.2026) |
| **Reklama w oknie** | okno tej samej długości kończące się na ostatnim dniu z kompletem Meta + Google | USTALONE |
| **Niepełny miesiąc** | bieżący miesiąc nie jest porównywany z pełnym poprzednim. Porównanie: te same dni miesiąca albo okno kroczące | USTALONE (25.11.2026) |
| **Przełomy w danych** | nowa strona 02.11.2026 (punkty, kasa); skala wartości Ads od 02.11.2026; migracja platformy 29.03.2024 | USTALONE |

## 6. Newsletter B2C

| Pojęcie | Definicja | SQL | Status |
|---|---|---|---|
| **Kampania** | `email_campaign`, `event_type = 'B2C'`, nie testowa | `NOT "isTestCampaign"` | USTALONE |
| **Kampania wysłana i data wysyłki** | pierwszy dzień (doba PL), w którym kampania miała **≥ 20 unikalnych otwarć**; wcześniejsze pojedyncze otwarcia to wysyłki testowe; kampania bez takiego dnia = jeszcze niewysłana. Dla kampanii z 10.02.2026 data = początek danych o otwarciach | | USTALONE (Daniel, 25.11.2026) |
| **Otwarcia / kliknięcia** | unikalne e-maile na kampanię, wszystkie zdarzenia kampanii (otwarcia testowe sprzed dnia wysyłki wchodzą, różnica 0–3) ; kliknięcia bez linku „wypisz się” | `count(distinct email)` | USTALONE (doprecyzowane 25.11.2026) |
| **Wypis** | kliknięcie linku `/unsubscribe` | | USTALONE |
| **Zamówienie po kliknięciu** | zamówienia (nie osoby) zrealizowane na e-mail, który kliknął w kampanii (bez kliknięcia „wypisz się”), w ciągu 7 × 24 h od jego **pierwszego** kliknięcia; przychód netto bez wysyłki | | USTALONE (doprecyzowane 25.11.2026) |
| **Baza newslettera** | osoby ze zgodą na newsletter. Członkostwo w programie nie daje zgody na newsletter. **W bazie sklepu widać tylko część:** konta z `email_optin` (ok. 8 000). Osoby zapisane bez konta są poza tą bazą — w 90 dniach do 25.11.2026 ok. połowa otwierających (3 623 z 7 129) nie miała konta. Pełna liczba odbiorców: z systemu wysyłki (do ustalenia z devem) | `account.email_optin` (tylko część z kontem) | USTALONE z luką (25.11.2026) |
| **Aktywna czytelniczka (90 dni)** | otworzyła albo kliknęła newsletter w ostatnich 90 dniach i nie wiemy o utracie zgody: odpada konto z `email_optin = false` i osoba, której ostatnim zdarzeniem jest kliknięcie „wypisz się”; osoby bez konta zostają | | USTALONE (Daniel, 25.11.2026) |
| **Zasięg %** | unikalne otwarcia ÷ szacowana baza w dniu wysyłki (konta z optin, z korektą o nowe konta i wypisy po wysyłce). **Zawyżony**: w liczniku są też osoby bez konta, których nie ma w mianowniku. Do czasu pełnej liczby odbiorców z systemu wysyłki traktować jako wskaźnik trendu, nie prawdziwy zasięg | | USTALONE z zastrzeżeniem (25.11.2026) |

## 7. Wygląd liczb

- Kwoty: „47 871 zł” (separator tysięcy spacja, „zł” po liczbie), bez „PLN” i „zł” z przodu.
- Procenty: „8,1 %”, przecinek dziesiętny.
- Etykiety serii i kolumn po polsku. Nie zostawiamy nazw z SQL (`przychod_netto`, `nowi_b`).
- Okresy bez danych (przed startem programu, przyszłe miesiące) są puste, nie „0”.

## Historia zmian

- 25.11.2026 — aktywna czytelniczka zatwierdzona; odkryta luka: ok. połowa otwierających newsletter nie ma konta w sklepie, więc „baza optin” to tylko zapisani z kontem, a zasięg % jest zawyżony (do ustalenia z devem, gdzie jest pełna lista odbiorców).

- 25.11.2026 — wersja 1.2 po rundzie 2 weryfikacji: powrót w N dni = N × 24 h i tylko pełne kohorty; okna wygasania = pełne doby PL (kafel „wygaśnie w 30 dni” = suma listy); przedłuża tylko zamówienie zrealizowane; zobowiązanie obejmuje saldo po terminie; koszt programu ze wszystkich zakupów z punktami.

- 25.11.2026 — wersja 1.1 po niezależnej weryfikacji (Fable 5.2, protokół `weryfikacja/2026-11-25_protokol.md`): doba PL dla wszystkich znaczników czasu, zamówienie członkini po e-mailu, 5 zapisów DELETED sprzed 06.2026 pomijane, zobowiązanie w zł, zasięg % wg szacowanej bazy w dniu wysyłki, zamówienie po kliknięciu (zamówienia, 7 × 24 h od pierwszego kliknięcia), % nowych.

- 25.11.2026 — wersja 1: zebrane definicje z decyzji 07–11.2026 i z tej sesji. Decyzje Daniela tego dnia: powrót = zakup z punktami zarobionymi na wcześniejszych zakupach; wysyłka kampanii = dzień z ≥ 20 otwarciami; newsletter tylko `email_optin` (zgoda z programu to inna zgoda). Aktywna czytelniczka = tylko obecna zgoda (zatwierdzone tego samego dnia).
