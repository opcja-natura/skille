# Ewidencja zwrotów: arkusz „Korekty paragonów 2025 zwroty”

Arkusz: https://docs.google.com/spreadsheets/d/16okHTxX5zvn2HZxUtnn-na2n2I6jomFzc1Kzibow_aU/edit. Mimo „2025” w nazwie ma zakładki 2026: `listopad 2026`, `październik_2026`, `wrzesien_2026`… (nazwy niejednolite, szukaj po miesiącu). Ewidencja idzie do księgowości jako podstawa korekt paragonów, więc liczby muszą się zgadzać z paragonem.

Agent pomaga osobie prowadzącej zwroty (podpis w uwagach, np. `Ka:`): z numeru zamówienia przygotowuje wiersz z danych paragonu w BL, a osoba uzupełnia powód, kwotę zwrotu i uwagi. Zasady rozliczania zwrotów (kiedy wpis jest, a kiedy nie, P24, pobranie, Allegro): `przeplywy.md`, sekcja 5, a krok po kroku `hub-manufaktura`, gdy ma rozdział o zwrotach (do tego czasu osoba od zwrotów). Najważniejsze: **stara paczka po wysyłce nowej za 0 zł nie dostaje wpisu.**

## Układ zakładki

Wiersz 1: objaśnienia, wiersz 2: nagłówki, dane od wiersza 3, pod danymi wiersze z formułami (suma E, netto, VAT), których nie ruszasz. Przed wpisem odczytaj nagłówki i znajdź pierwszy wiersz z formułą: wpis idzie w pierwszy pusty wiersz nad nim. Nagłówki inne niż w tabeli niżej albo brak wolnego wiersza → zgłoś, nie przesuwaj formuł.

| Kol. | Nagłówek | Skąd (BL) | Jak wpisać |
| :-- | :-- | :-- | :-- |
| A | data wystawienia paragonu | `getReceipt` z `order_id` → `date_add` | data paragonu, nie zamówienia ani zwrotu; wpis zostaje w miesiącu rozliczenia, nawet gdy paragon jest starszy |
| B | nazwa wszystkich zwracanych pozycji | `getReceipt` → `items` | jedna linia na pozycję, jak na paragonie: `Nazwa q x cena= wartość A` (A = VAT 23%), np. `Atop stop 1 x 49.90= 49.90 A`; razem z liniami rabatu (`Rabat23 1 x -36.82= -36.82 A`), pakowania i dostawy (`Pobranie InPost 1 x 18.00= 18.00 A`). Przy częściowym zwrocie tylko zwracane pozycje |
| C | kiedy zwrócono pieniądze | osoba | P24: data wykonania zwrotu; nieodebrane pobranie: data wpisu (to nie dowód wypłaty) |
| D | tylko wartość kosmetyków | z B | suma pozycji kosmetyków po rabatach, bez dostawy i pobrania |
| E | cała kwota zwracana | osoba (agent proponuje) | to, co faktycznie wraca: kosmetyki i ewentualnie przesyłka. Nie zakładaj, że przesyłka zawsze wraca |
| F | nr paragonu | `getReceipt` → `external_receipt_number` (numer z drukarki, np. `89844`) | nie `receipt_full_nr` (to numer BL, np. `1025/11/2026`) |
| G | dlaczego zwracamy | osoba | np. `zwrot`, `anulowała zamówienie`, `reklamacja uzgodniona z Agatą`, `anulacja - uzgodniona z księgowym` |
| H | mail klienta | `getOrders` → `email` | przy braku e-maila zespół wpisuje `Zamówienie <ID BL>` |
| I | numer zwrotu z bramki płatności | osoba | ID zwrotu w P24; Allegro: `allegro zwraca`; pobranie: puste |
| J | komentarz | osoba (agent szkicuje) | podpis i przebieg: `Ka: pop, pop, kontakt tel - klientka rezygnuje`. Liczba prób kontaktu jest rozliczana, więc wpisuj ją dokładnie |

Zamówienie znajdziesz po numerze sklepu `ON-…`, e-mailu (`getOrdersByEmail`) albo ID BL (`zapytania.md`, sekcje 1 i 3). Brak paragonu w BL (`getReceipt` zwraca błąd) → zamówienie mogło mieć fakturę albo paragon wystawiony ręcznie: zapytaj, nie zgaduj.

## Zapis

- Przygotuj wiersz i pokaż go osobie (bez całego e-maila klientki w rozmowie, jeśli nie trzeba). Wpisz dopiero po „tak”.
- Zapis w konkretne komórki pierwszego pustego wiersza (np. `<zakładka>!A13:J13`), jako wartości wpisywane ręcznie (`USER_ENTERED`), daty i kwoty jako liczby. Bez dopisywania wierszy metodą „append”.
- Nie poprawiasz istniejących wpisów, także gdy widać w nich błąd (np. D z dostawą). Zgłaszasz osobie.
- Brak narzędzia z zapisem do Sheets → podaj gotowy wiersz do wklejenia.
- W BL agent może po wpisie najwyżej dopisać uwagę do zamówienia (`zapisy.md`, zapis 1). Statusy zwrotów i przywrócenie stanów robi człowiek w panelu.
