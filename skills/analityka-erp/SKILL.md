---
name: analityka-erp
description: Odpowiadanie na pytania o dane z arkuszy ERP Opcji Natury w Google Sheets — stan wyrobów gotowych na magazynie, sprzedaż kosmetyków w sztukach po miesiącach, kwartałach i latach, średnia sprzedaż, na ile dni starczy zapasu, co i kiedy jest zaplanowane do produkcji, statusy zleceń produkcyjnych, ostatnia produkcja i partie, stan surowców i opakowań. Daje mapę plików i zakładek, znaczenie kolumn, skąd idzie sprzedaż i pułapki (kwartał bieżący to tylko zamknięte miesiące, stan to kopia z backoffice, helper planowania nie jest pełną listą). Używaj, gdy ktoś pyta „ile sprzedaliśmy X w Q3”, „jaki mamy stan Y”, „na ile starczy”, „kiedy produkcja Z”, „co jest w toku”, „ile mamy słoików/surowca”. NIE do sprzedaży w złotówkach B2B (skill analityka-b2b-zoho), NIE do dokumentów surowców i produktów, dostaw ani zapisu czegokolwiek w arkuszach.
---

# Analityka ERP – arkusze Google

ERP to kilkadziesiąt arkuszy Google połączonych formułami. Większość liczb, które ludzie widzą, to **kopie i przeliczenia** z dwóch źródeł: **backoffice sklepu** (stan i sprzedaż wyrobów gotowych) i **bazy produkcji** (zlecenia, statusy, partie). Zanim podasz liczbę, wiedz, z której kopii ją bierzesz i czego w niej nie ma.

Arkuszy **nie edytujesz**. Wszystkie kolumny opisane w tym skillu liczą się formułami; ręczna zmiana zepsuje cały arkusz.

Mapa plików, zakładek i kolumn (z linkami): `references/mapa-arkuszy.md`. Stan opisu: 20.11.2026, sprawdzony na żywych arkuszach.

## Jak czytać arkusze

1. Otwórz plik przez podłączony Google Drive po ID z mapy.
2. Narzędzie Drive często pokazuje **tylko pierwszą zakładkę**. Potrzebujesz konkretnej (np. `produkty_magazyn`) → pobierz cały plik jako arkusz (XLSX) i czytaj właściwą zakładkę. Jeśli się nie da, poproś osobę o otwarcie zakładki i wklejenie wierszy albo wyeksportowanie jej do CSV.
3. Nie masz dostępu do pliku → powiedz to wprost. Nie zgaduj liczb i nie podawaj ich z wcześniejszej rozmowy.
4. Przy odpowiedzi podaj, skąd jest liczba (plik → zakładka → kolumna) i z jakiego dnia są dane.

## Które źródło do którego pytania

| Pytanie | Gdzie | Uwagi |
|---|---|---|
| ile mamy na magazynie (wyroby gotowe) | `03_magazyn_produkty` → `produkty_magazyn`, kol. E | kopia z backoffice, patrz pułapka 4 |
| ile sprzedaliśmy w roku / kwartale, średnia, rekordowy miesiąc | `03_magazyn_produkty` → `produkty_magazyn`, kol. P–AN | jeden wiersz na kosmetyk |
| sprzedaż miesiąc po miesiącu | `sprzedaz_2026` (albo `sprzedaz_2025`) → `wyrobGotowy_MoM` | kolumny styczeń–grudzień |
| sprzedaż w rozbiciu na kanał (B2C/B2B/POS), zwroty, wysyłki marketingowe | `Warehouse Sale - PROD`, zakładka miesiąca `2026_10` itd. | surowe ruchy, ~10 tys. wierszy na miesiąc |
| co jest zaplanowane / w produkcji, ile sztuk, od kiedy | `03_magazyn_produkty` → `produkty_rezerwacje_new` | tylko zlecenia niezakończone |
| historia wszystkich zleceń, statusy | `BD_produkcyjna` → `BD_productionOrder` | ~10 tys. wierszy |
| ostatnia produkcja, partie, daty ważności | `03_magazyn_produkty` → `produkty_wyprodukowanePartie_2026` (i `_2025`), kol. J–K w `produkty_magazyn` | |
| na ile dni starczy, co trzeba zaplanować | `00_planowanieProdukcji--2.0` → `produkcja_operacyjka` | wyłącznie lista do decyzji, patrz pułapka 6 |
| ile mamy surowca (w gramach) | `01_magazyn__surowce` → `magazyn__surowce` | |
| ile mamy opakowań (w sztukach) | `02_magazyn__opakowanie` → `magazyn__opakowanie` | |
| sprzedaż w złotówkach B2B, klienci, handlowcy | **nie ERP** → skill `analityka-b2b-zoho` | |

Arkusz z „NIE UZYWAC” w nazwie (np. `00_planowanieProdukcji --NIE UZYWAC--`, `01_produkcja -2025`) to stara wersja. Nie bierz z niego liczb.

## Skąd idzie sprzedaż

Backoffice sklepu zapisuje każdy ruch towaru. Ostatniego dnia miesiąca wieczorem (ok. 22:30) automat zrzuca ruchy całego miesiąca do pliku `Warehouse Sale - PROD` jako nową zakładkę `RRRR_M` (np. `2026_10`). Kolumny zrzutu: magazyn, id produktu, nazwa, nr zamówienia, ilość (sprzedaż jest **ujemna**), cena, typ ruchu, kanał.

Arkusz `sprzedaz_2026` sumuje z tych zakładek sprzedaż na produkt i miesiąc: **sztuki**, magazyn `C`, typy ruchu `SALE` i `SHIP_FROM`, znak odwrócony na dodatni. `produkty_magazyn` liczy z tego sumy roczne, średnie i kwartały.

Co to oznacza dla liczby „sprzedaż”:
- **wszystkie kanały razem**: sklep (B2C), hurt (B2B), sprzedaż stacjonarna (POS); w październiku 2026 ok. 77% wierszy to B2C, 15% B2B, 2% POS,
- **zwroty nie są odjęte** (`RETURNED` pomijane),
- **nie liczą się** wysyłki marketingowe, testery, zużycie własne, braki i nadwyżki inwentaryzacyjne, nowe przyjęcia,
- **nie liczą się** magazyny inne niż `C` (`WD…`, `O`, …), tj. drobna sprzedaż z magazynów zewnętrznych,
- to **sztuki, nie złotówki**. Wartość sprzedaży B2B → `analityka-b2b-zoho`.

Rozbicie na kanał albo zwroty policz sam z zakładki miesiąca w `Warehouse Sale - PROD` (kolumna typu ruchu i kanału), z tymi samymi filtrami.

## Pułapki

1. **Kwartał i rok bieżący to tylko zamknięte miesiące.** Zakładka miesiąca powstaje dopiero ostatniego dnia miesiąca. 20 listopada 2026 „Q4 2026” zawiera **tylko październik**, a „suma sprzedaż 2026” to styczeń–październik. Porównując z Q4 2025 (pełny kwartał), porównuj te same miesiące (październik do października) albo wprost napisz, że kwartał jest niepełny.
2. **„sprzedaż poprzedni mies”** to ostatni zamknięty miesiąc. Na przełomie miesiąca (zanim powstanie zakładka) potrafi pokazać pusto.
3. **Średnie liczą się różnie w zależności od roku.** 2026: suma ÷ liczba zamkniętych miesięcy (w listopadzie ÷ 10). 2025: suma ÷ 12. 2024: liczby wpisane na sztywno, nie przeliczają się.
4. **Stan to kopia z backoffice, nie stan na żywo.** `produkty_magazyn` kol. E pochodzi z pliku `Warehouse Inventory PROD`, który automat odświeża ok. dwa razy dziennie (po południu i wieczorem). Liczy wyłącznie magazyn centralny `C`. Do stanu wchodzi tylko to, co magazyn przyjął w backoffice: partia w produkcji albo w kontroli jakości jeszcze w nim nie jest. Gdy ktoś widzi w backoffice inną liczbę, **wygrywa backoffice**. W odpowiedzi podaj datę odświeżenia, jeśli ją znasz.
5. **„stan po produkcji zaplanowanych” (kol. G) to plan, nie wykonanie.** To stan + pełna zarezerwowana ilość wszystkich niezakończonych zleceń. Jeśli część partii jest już przyjęta na magazyn, a zlecenie jeszcze otwarte, te sztuki liczą się dwa razy. **„planowana data ukończenia” (kol. H) to w rzeczywistości data startu produkcji** z harmonogramu. Wartość `niezaplanowo` oznacza brak otwartego zlecenia.
6. **Helper planowania nie jest pełną listą produktów.** `planowanie_produkcji__helper` pokazuje tylko kosmetyki, których stan jest mniejszy niż mnożnik (komórka A1, teraz **3**) × średnia miesięczna sprzedaż 2026. Brak produktu na liście oznacza, że zapasu jest dużo, a nie że produkt nie istnieje. Kolumny podpisane „2M”/„minimum 2M” liczą się dziś z mnożnikiem 3, więc „min” i „opt” wychodzą prawie równe.
7. **Kolumna „status produkcji” w helperze bywa fałszywa** (stan 20.11.2026). Bierze **pierwsze w historii** zlecenie produktu, więc pokazuje „🟡 zakończono” albo samo „🟡” i oznacza produkt jako „⚪ ignoruj - w toku”, choć nic nie jest w produkcji. Przykład z 20.11: szampon z lasu (stan 46 szt., sprzedaż ok. 440 szt./mies.) oznaczony „ignoruj”. Zanim powiesz „jest w toku”, sprawdź, czy produkt ma wiersz w `produkty_rezerwacje_new`. Tak samo oceniaj zrzut `produkcja_operacyjka`.
8. **Łącz po ID, nie po nazwie.** Ten sam kosmetyk ma różne nazwy w różnych miejscach („eliskir młodości” / „Eliksir młodości”, „peeling detox” / „peeling detox pomarańcza”, w backoffice SKU typu „anty tartka”). Klucz produktu to `sercet_id` (literówka w nagłówku, w bazie produkcji `secret_id`, w backoffice `productId`); identyczny we wszystkich arkuszach. Drugi klucz: EAN.
9. **Surowce i opakowania liczą się po nazwie.** Stan = przyjęcia − zejścia, sumowane po nazwie pozycji. Surowce w **gramach**, opakowania w **sztukach**. „stan magazynowy po rezerwacjach” = stan minus to, co zarezerwowały otwarte zlecenia. Kolumny „2025: śr mies zużycie” dotyczą 2025, nie bieżącego roku.
10. **Liczby z formatowaniem.** W eksporcie liczby mają przecinek tysięcy (`16,173` = 16 173), daty bywają w formacie amerykańskim (`1/11/2027` = 11 stycznia 2027). Błędy formuł (`#N/A`, `error`) w kolumnach ostatniej produkcji oznaczają brak danych, nie zero.

## Statusy zlecenia produkcyjnego

Zlecenie (`production_id`, np. `20261007083705-uotu`) ma pięć statusów: masa, etykietowanie, kontrola jakości (KJ), całość, magazyn WG.

| Status całości (`status_produkcji`) | Co znaczy |
|---|---|
| `w_rezerwacji` | zaplanowane, surowce i opakowania zarezerwowane, produkcja nie ruszyła |
| `w_toku` | trwa produkcja masy albo etykietowanie |
| `oczekuje_zakonczenia` | masa i etykietowanie skończone, zlecenie czeka na zamknięcie (KJ i przyjęcie na magazyn mają własne statusy) |
| `zakończono` | zamknięte, materiały zdjęte z magazynu |

`status_magazyn_wg`: `niedostępny` → `dostepny_czesciowo`/`oczekuje` (KJ puściła część albo całość) → `w_toku` (magazyn przyjął część) → `zakończono` (przyjęte w całości). „Ilość wyprodukowana” liczy się z zamkniętych wsadów, „magazyn_wg_dodana_ilość” to sztuki przyjęte na magazyn.

## Jak liczyć typowe rzeczy

- **Na ile dni starczy:** stan (E) ÷ średnia sprzedaż 2026 (AI) × 30. Zaznacz, że średnia z całego roku nie widzi sezonu (np. dezodoranty latem), więc dla krótkich okresów podaj też ostatni miesiąc (AN).
- **Kwartał do kwartału r/r:** weź miesiące z `wyrobGotowy_MoM` obu lat i zsumuj te same miesiące; nie porównuj niepełnego Q z pełnym.
- **Czy jest produkcja w drodze:** wiersze produktu w `produkty_rezerwacje_new`: ilość (C), start (U), statusy (M–Q).
- **Wynik podawaj** w tabeli: produkt, liczba, okres, źródło. Liczby zaokrąglaj do sztuk.

## Czego ten skill nie robi

- Nie zapisuje niczego w arkuszach.
- Nie liczy sprzedaży w złotówkach ani marży B2B (`analityka-b2b-zoho`; CRM i zamówienia klientów: `bigin-opcja-natura`).
- Dokumenty surowców, produktów i dostaw: skille `raw-material-documents`, `product-documents`, `delivery-quality-documents`. Zakładanie zamówień do dostaw: `delivery-order-intake`.
- Jak działa proces produkcji krok po kroku: zapytaj Daniela albo zajrzyj do dokumentacji ERP (repo `erp-docs`), jeśli masz do niej dostęp.
