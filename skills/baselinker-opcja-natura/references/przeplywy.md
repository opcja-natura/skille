# Przepływy zamówień

1. Skąd zamówienie przychodzi
2. Statusy: kto ustawia i co uruchamiają
3. Rozchód magazynu
4. Trzy osobne potwierdzenia
5. Ponowna wysyłka i nowe zamówienie

ID statusów i źródeł: `konto.md`.

## 1. Skąd zamówienie przychodzi

| Kanał | Kto zakłada | Status startowy | Charakterystyczne dane |
| :-- | :-- | :-- | :-- |
| sklep www | sklep, po opłaceniu (pobranie: od razu) | `10454` do wysyłki, `9890` odbiór osobisty | numer `ON-…` w `user_login`, UUID w `77620`, newsletter i kupon w polach dodatkowych, bony i pakowanie na prezent w uwagach; płatność `p24` albo `COD` |
| B2B | handlowiec wysyła z arkusza zamówień B2B (pozycje z formularza klienta albo z maila przez automat) | `9886` B2B, `313961` on hold, `294244` rozliczenie komisu | numer `ON-B2B__…`, klient `77836`, typ `77837`, termin płatności `78687`, uwagi handlowca |
| marketingowe | ręcznie | `341571` | powód wysyłki za 0 zł `77977` |
| Allegro, Amazon, TikTok Shop, Temu, Kaufland, Ceneo | integracje BL | kolejka kanału (`konto.md`); Kaufland i Ceneo nie mają osobnej kolejki, status sprawdź w `getOrders`; Allegro nieopłacone `355182` | `external_order_id`; Amazon FBA: status `338916`, magazyn firmy go pomija |
| InPost Fresh | integracja | `350558` | |
| dropshipping | Base Connect | `343182`, `348497` | |

## 2. Statusy: kto ustawia i co uruchamiają

Automatyczne akcje BL ustawia się w panelu. API ich nie pokazuje, więc opis poniżej wynika z tego, jak działają odbiorcy (backoffice, Bigin, Slack) i z procedur hubu.

| Etap | Status | Kto ustawia | Co uruchamia |
| :-- | :-- | :-- | :-- |
| wejście | kolejka wejściowa | sklep, integracja, arkusz B2B | B2B: zamówienie w Biginie (etap „Przekazano do realizacji”); wiadomość „wymagane działanie” na `#baselinker-bot`; wiadomości o zamówieniach na kanałach powiadomień |
| wstrzymanie | `313961` on hold | handlowiec albo hub | B2B: też zakłada zamówienie w Biginie |
| pakowanie | `10476` / `10475` Spakowano | hub, przy pakowaniu ze skanowaniem | rozchód w magazynie firmy (sekcja 3) |
| etykieta | `10455` Wydrukowano etykietę | hub, moduł kuriera w zamówieniu | paczka z `tracking_status` 1; Bigin: „Spakowano” |
| wysyłka | `9888` Wysłane; komis `294156` | automat BL | wiadomość do klientki; Bigin: „Wysłane” |
| koniec | `17910` Dostarczone, `10468` Odebrane/dostarczone | automat BL z trackingu | sklep (m.in. potwierdzenie zapisu do programu lojalnościowego); Bigin zakłada zamówienie na nowo z kwotą faktury i datą doręczenia |
| rozliczenie komisu | `294244` | handlowiec | faktura ręczna; „Ściągnij z magazynu” zdejmuje towar z magazynu komisanta |
| nieodebrana | `9888` dłużej niż 2 pełne dni robocze | nikt (to nie zdarzenie) | automat zwrotów zakłada sprawę „Nie doręczone” dla osoby od zwrotów |
| zwrot w drodze | `284070` | automat z trackingu | alarm po 7 dniach bez ruchu |
| zwrot u nas | `320111` zwrot - wysłany @ | hub: „Przyjęto paczkę zwrotu” | mail i SMS do klientki z propozycją płatnej ponownej wysyłki |
| deklaracja dopłaty | `320503` | hub | |
| rozliczenie | `320112` środki do zwrotu | automat BL po 60 h bez reakcji (wg procedury hubu) | dwa tory: magazyn i pieniądze |
| koniec zwrotu | `324032` wypakowano | hub po rozliczeniu obu torów | sprawa zamknięta |
| archiwum | `325481` | automat po kilku dniach | |
| problem | `284310` reklamowane, `9889` Anulowane, `341284` duplikaty | hub, lider | |

## 3. Rozchód magazynu

Magazyn firmy prowadzi backoffice, połączony z BL webhookami. Stan magazynu w BL to osobna ewidencja.

- **Rozchód:** przy pakowaniu automat BL „Ściągnij z magazynu” wywołuje webhook magazynu firmy. Sprzedaż (także B2B `DIRECT_SALE`) schodzi z Central. Komis (`SHIPMENT`) przesuwa towar z Central na magazyn komisanta. Amazon FBA jest pomijany.
- **Udany webhook:** automat BL zaznacza `77969` „zrealizowano magazyn spZoo” = TAK. W historii widać to jako `log_type` 16 kilka sekund po zmianie na Spakowano.
- **Nieudany webhook:** `77969` puste, brak `log_type` 16 po zmianie statusu, produkty zostają w magazynie BL jako zarezerwowane (klepsydra w panelu), w historii automatycznych akcji wykrzyknik przy „Ściągnij z magazynu”, alert „błąd wywołania URL magazynu” na `#baselinker-bot`. Rezerwację per zamówienie widać tylko w panelu; API pokazuje ją zbiorczo na produkcie (`getInventoryProductsStock`, `reservations`).
- **Zwrot stanów:** „Przywróć stany produktów” wywołuje webhook zwrotu i przywraca **całą** zawartość na Central; po sukcesie automat zaznacza `77970` = TAK. Przy częściowym zwrocie ta akcja jest błędem.

## 4. Trzy osobne potwierdzenia

Magazyn (`77969`), przekazanie kurierowi (kod w historii paczki inny niż 0, 1, 10) i doręczenie (kod 5 i status `17910` / `10468`) sprawdzasz osobno: każde może zawieść niezależnie.

## 5. Ponowna wysyłka i nowe zamówienie

| Sytuacja | W BL | Rozliczenie |
| :-- | :-- | :-- |
| paczka wróciła, stany nieprzywrócone, klientka dopłaca | to samo zamówienie wraca do `10454` i dostaje nowy list | paragon tylko na dopłatę |
| paczka jeszcze wraca, zamówienie opłacone, wysyłamy nową | **nowe** zamówienie: produkty 0 zł, `77056` „nie wystawiaj paragonu”, `77977` powód | stara paczka po powrocie: tylko magazyn, bez wpisu do ewidencji zwrotów |
| stany już przywrócone, klientka chce towar | **nowe** zamówienie z nowym rozchodem | najpierw sprawdź, co już zwrócono klientce |

Szczegóły procedury: `hub-manufaktura`, gdy ma rozdział o zwrotach; do tego czasu osoba od zwrotów albo lider hubu.
