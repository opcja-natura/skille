# Mapa arkuszy ERP – pliki, zakładki, kolumny

Stan: 20.11.2026, sprawdzony na żywych arkuszach. Przy rozbieżności z arkuszem wygrywa arkusz. Link do pliku: `https://docs.google.com/spreadsheets/d/<ID>`.

## Przepływ danych

```
backoffice sklepu ──(automat ~2×/dzień)──► Warehouse Inventory PROD ──► 03_magazyn_produkty: produkty_magazyn (kol. E stan)
backoffice sklepu ──(automat, ostatni dzień miesiąca)──► Warehouse Sale - PROD (zakładka RRRR_M)
        └──► sprzedaz_2026 / sprzedaz_2025: wyrobGotowy_MoM (sztuki/miesiąc) ──► produkty_magazyn (kol. X–AN)
BD_produkcyjna: BD_productionOrder (zlecenia) ──► 03_magazyn_produkty: produkty_rezerwacje_new (otwarte) ──► produkty_magazyn (kol. G–H)
BD_produkcyjna: BD_partieProdukcji (partie) ──► produkty_magazyn (kol. J–N), produkty_wyprodukowanePartie_RRRR
produkty_magazyn ──► 00_planowanieProdukcji--2.0: planowanie_produkcji__helper ──► produkcja_operacyjka
```

Przyjęcie gotowego wyrobu na magazyn (stacja „kontrola magazynu WG”) wysyła sztuki do backoffice; dopiero wtedy pojawiają się w stanie.

## 03_magazyn_produkty – główny arkusz wyrobów gotowych

ID `1ec0g25QXtqUHv4kM3XMPBwGhqAB9MQX32OjuynjHn_I`

### `produkty_magazyn` – jeden wiersz na kosmetyk

| Kol. | Nagłówek | Znaczenie |
|---|---|---|
| A | `sercet_id` | ID produktu (klucz; literówka w nagłówku) |
| B | `baslinker_id` | ID w Baselinkerze |
| C | `ean` | EAN |
| D | `name` | nazwa |
| E | magazyn centralny stan | sztuki na magazynie `C` w backoffice (kopia, ~2×/dzień) |
| G | stan po produkcji zaplanowanych | E + zarezerwowana ilość wszystkich niezakończonych zleceń |
| H | planowana data ukończenia zaplanowanej produkcji | **faktycznie data startu** najbliższego otwartego zlecenia; `niezaplanowo` = brak zlecenia |
| J | poprzednia produkcja – ilość | ostatnia partia (sztuki) |
| K | poprzednia produkcja data | data ostatniej partii |
| M, N | suma produkcji 2024, 2025 | sztuki wyprodukowane w roku |
| P–V | 2024: suma, najwyższy miesiąc, średnia, Q1–Q4 | wpisane na sztywno |
| X–AE | 2025: suma, najwyższy miesiąc, średnia (÷12), Q1–Q4, sprzedaż poprzedni mies. | z `sprzedaz_2025` |
| AG–AN | 2026: suma, najwyższy miesiąc, średnia (÷ zamknięte miesiące), Q1–Q4, sprzedaż poprzedni mies. | z `sprzedaz_2026`; bieżący kwartał niepełny |

Kolumny F, I, L, O, W, AF są puste (separatory). Kwartały: Q1 = sty–mar, Q2 = kwi–cze, Q3 = lip–wrz, Q4 = paź–gru.

### `produkty_rezerwacje_new` – zlecenia niezakończone

Kopia `BD_productionOrder` z filtrem `status_produkcji ≠ zakończono`, posortowana po dacie rezerwacji. Kolumny jak w `BD_productionOrder` (niżej). Najważniejsze: B nazwa, C zarezerwowana ilość (szt), F `secret_id`, K wyprodukowane sztuki, M–Q statusy, R przyjęte na magazyn, U `data_produkcji_start`.

### `produkty_wyprodukowanePartie_2026` (i `_2025`) – partie

A `_id_partia`, B data ważności / nr partii (RRRR-MM-DD), C nazwa, D `id_produktu`, E wyprodukowana ilość, F data produkcji, G data transferu, H wersja formulacji, I plik etykiety, J tabela użytych surowców (link), K komentarz produkcyjny, L liczba wsadów, M data kontroli jakości, N data przyjęcia na magazyn WG (backoffice).

Pozostałe zakładki (`centralWarehouse_helper`, `productionBatches_helper`, `BD_productionOrder--helper`, `produkty_rezerwacje` stara, ukryte) to kopie techniczne. Nie czytaj z nich.

## sprzedaz_2026 / sprzedaz_2025 – sprzedaż miesięczna w sztukach

- `sprzedaz_2026` ID `1CgnJQD3AFHuGFjJ2ZzDyirRths1Iip99fUDpbTp5SfU`
- `sprzedaz_2025` ID `1zZwyBDQvpStC9SonPBRO3T41VBypADktg0sqLTvcR4Y`

Zakładka `wyrobGotowy_MoM`: A `sercet_id`, B `baslinker_id`, C `ean`, D `name`, F–Q styczeń…grudzień (nagłówki po angielsku: January…December). Pusta komórka miesiąca = miesiąc jeszcze niezamknięty (albo brak sprzedaży). Filtr: magazyn `C`, typ `SALE` lub `SHIP_FROM`.

## Warehouse Sale - PROD – surowe ruchy magazynowe

ID `1UShuRmSk82hoYPzd7autR_WpmtKUb-ksHvbBrqNixiY`. Zakładki `2025_1` … `2026_10` (kolejna powstaje ostatniego dnia miesiąca), ~8–14 tys. wierszy każda, **bez nagłówka**.

| Kol. | Znaczenie | Wartości |
|---|---|---|
| A | magazyn | `C` (centralny), `WD…`, `O`, … |
| B | ID produktu (`sercet_id`) | |
| C | nazwa | |
| D | nr zamówienia / dokumentu | |
| E | ilość | ujemna = wydanie |
| F | cena jednostkowa | |
| G | typ ruchu | `SALE`, `SHIP_FROM`, `SHIP_TO`, `RETURNED`, `MARKETING_SHIPMENT`, `TESTER/EXHIBITION`, `OWN_USE`, `QA`, `NEW_STOCK`, `UNFAULTY_DEFICIENCY`, `UNFAULTY_SURPLUS`, `ARCHIVED`, `DAMAGED_PRODUCT_REPLACEMENT` |
| H | kanał | `B2C`, `B2B`, `POS`, puste |

Zakładka `Sheet1`: miesięczne zestawienie z wartością sprzedaży (RRRR-MM, zakładka, liczby i kwoty) – pomocnicze, sprawdź nagłówki przed użyciem.

## Warehouse Inventory PROD – stan magazynu z backoffice

ID `1Ir5niBILr6KU9rTXTyoXTtbr_ucMK6niROAdR6-Qw2M`. `substitute_numbers`: stan per magazyn i produkt (`warehouseId`, `productId`, `productSku`, `productName`, `productEan`, `version`, `quantity`, `price`). `modifiedData_centralWarehouseState`: to samo zawężone do magazynu `C`. Odświeżany automatycznie, mniej więcej po południu i wieczorem.

## BD_produkcyjna – baza produkcji

ID `1jUSESWqYJapu5BrrKMdRk5CMR2cEOXChYKBmtOIsR3A`

### `BD_productionOrder` – zlecenia produkcyjne (jeden wiersz = jedno zlecenie)

| Kol. | Nagłówek | Znaczenie |
|---|---|---|
| A | `production_id` | ID zlecenia, np. `20261007083705-uotu` |
| B | nazwa produktu | |
| C | zarezerwowana ilość (szt) | ilość planowana |
| D | ilość masy (g) | |
| E | data złożenia rezerwacji | |
| F | `secret_id` | ID produktu |
| G | nr partii / data ważności | z harmonogramu |
| J | ilość wykonanych wsadów | |
| K | ilość wyprodukowanych sztuk | suma z zamkniętych wsadów |
| L | ilość wyprodukowanej masy (g) | |
| M | `status_produkcji_masy` | oczekuje / w_toku / zakończono |
| N | `status_etykietowania` | oczekuje / w_toku / zakończono |
| O | `status_qc` | niedostępny / oczekuje / w_toku / dostepny_czesciowo / zakończono |
| P | `status_produkcji` | w_rezerwacji / w_toku / oczekuje_zakonczenia / zakończono |
| Q | `status_magazyn_wg` | niedostępny / dostepny_czesciowo / oczekuje / w_toku / zakończono |
| R | `magazyn_wg_dodana_ilość` | sztuki przyjęte na magazyn |
| S | `data_zakonczenia_produkcji` | |
| U | `data_produkcji_start` | najwcześniejsza data z harmonogramu |
| V | `rzeczywista_wyprod_ilosc` | ilość ostateczna po zamknięciu |

Zlecenia sprzed nowego ERP (2024–2025) mają ID w formacie `20241123-118f` i część pól pustych.

## 00_planowanieProdukcji--2.0 – planowanie produkcji

ID `1sIRi5ZfibRIXe_8pxDtgj-BNAh3rxgQFH1KQ-5trsF4`

### `planowanie_produkcji__helper`

Tylko kosmetyki ze stanem < A1 × średnia miesięczna sprzedaż 2026 (A1 = 3 na 20.11.2026). Kolumny:

| Kol. | Nagłówek | Znaczenie |
|---|---|---|
| A, B, C | id, produkt, obecny stan magazyn | |
| D | w planowaniu | ✅ gdy jest otwarte zlecenie |
| E | status produkcji | **zawodne** (pierwsze zlecenie w historii; patrz pułapka 7 w SKILL.md) |
| F | AVG MONTH SELL 2026 * mnożnik | próg minimum |
| G | różnica | C − F |
| H | za ile dni koniec zapasów | C ÷ O × 30 |
| I | do kiedy produkcja | dziś + H |
| J | stan po wyprodukowaniu | = `produkty_magazyn` G |
| K | data przewidzianej produkcji | = `produkty_magazyn` H (data startu) |
| L | last month sale | |
| M, N | ostatnia produkcja: ilość, data | |
| O | avg 2026 month sells | |
| P | optimal qty to plan | O × 3, w górę do 50 |
| Q–S | max partia, max wydajność, ilość pożądana | parametry produkcyjne |
| U | sort_priority | 1–4 pilne, 7 OK, 8 niepilne, 9 ignoruj |
| V | decyzja | 🔴/🟠/🟡 USTAL DATĘ, 🔴 DATA ZA PÓŹNO, 🟢 OK, ⚪ ignoruj - w toku |
| W | zakres produkcji | „min … / opt …” |
| X | powód | uzasadnienie decyzji |
| Z | ilość zaplanowana | J − C |
| AA | komentarz ilości | czy po planie zapas ≥ progu |

Wyszukiwania po nazwie w kolumnach J, L, Q sięgają tylko wierszy 2–33.

### `produkcja_operacyjka`

Widok z helpera: decyzja, produkt, dni zapasu, zapas kończy się, stan, data produkcji, min/opt, ilość zaplanowana, stan po planie, ocena ilości, powód. Sortowanie po dniach zapasu.

## Magazyny surowców i opakowań

### 01_magazyn__surowce – ID `1T_QxAliHiZSsefBw7KyKSQisGUNVfze0uLYzhO5qBJQ`

`magazyn__surowce`: A `_id` (`SUR__001`), B nazwa, C używany w produktach, E stan (g), F stan po rezerwacjach, H–J zużycie 2025 (całkowite, śr. miesięczne, śr. kwartalne), L zużycie 2024, O cena 1 g (ostatnia), S średnia cena, W dostawca, Z–AB dostawcy 1–3, AC uwagi zakupowe, AE–AF ostatnie zamówienie (ilość, dostawca), AJ INCI, AK CAS. Zakładki ruchów: `surowce__przyjecia`, `surowce__odjecia`, `surowce__rezerwacje`.

### 02_magazyn__opakowanie – ID `1YPF0KGfe2VX1mji5zPtE76Q8eGdaL5lvoobZk2otT-M`

`magazyn__opakowanie`: A `_id` (`OPAK_001`), B nazwa, C używane w produktach, E stan (szt), F stan po rezerwacjach, H–J zużycie 2025, L zużycie 2024, O cena 1 szt (ostatnia), S–T średnie ceny 2024/2023, W uwagi, Y dostawca, AA–AC dostawcy 1–3, AE–AF ostatnie zamówienie. Zakładki ruchów: `opakowanie__przyjecia`, `opakowanie__odjecia`, `opakowanie__rezerwacje`.

## Baza produktów

`BD_produkty` – ID `1r22doIQDQDhYaZh1f3eWr8b1gj3gGBlbcjq41hf-ino`, zakładka `DB_products_internal`: produkt, EAN, receptura, opakowania. Dane o kosmetykach dla klientów (skład, ceny) bierz ze skilla `produkty-lookup`, nie stąd.
