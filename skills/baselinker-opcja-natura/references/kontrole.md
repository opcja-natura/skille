# Kontrole: nieprawidłowe przepływy

Każda kontrola: **reguła → jak sprawdzić → wyjątki → komu przekazać** (role w `SKILL.md`). Najpierw liczby i numery przez `ask_agent`, potem szczegóły pojedynczych zamówień. Dni robocze liczysz w kalendarzu polskim (bez weekendów i świąt), od `date_in_status`. Kontrole robisz na prośbę; ich wyniki nie trafiają same do arkuszy hubu.

Wynik: tabela `order_id | numer (ON-… / ON-B2B__…) | kanał | status od kiedy | co jest nie tak | dowód | do kogo`, bez adresów i telefonów. Oddziel „błąd” (reguła złamana, dowód w danych) od „do sprawdzenia” (sygnał). Niczego nie poprawiasz w trakcie kontroli.

## A. Magazyn

| # | Reguła | Jak sprawdzić | Wyjątki | Do kogo |
| :-- | :-- | :-- | :-- | :-- |
| A1 | Zamówienie spakowane lub dalej (`10476`, `10475`, `10455`, `9888`, `294156`, `17910`, `10468`) ma rozchód | kandydaci: `ask_agent` „order_id w statusie X bez pola 77969 = TAK”; potwierdzenie: w historii brak `log_type` 16 kilka sekund po zmianie na Spakowano (ostatnie 3 dni). Agent niczego nie ponawia. Lider hubu może raz ponowić „Ściągnij z magazynu” w panelu, tylko gdy produkty są nadal zarezerwowane (klepsydra), a historia akcji pokazuje błąd. Bez tych dwóch śladów ponowienie grozi podwójnym rozchodem | Amazon FBA (`338916`); zamówienia bez pozycji; same próbki za 0 zł; rozliczenie komisu `294244` | lider hubu; gdy ponowienie nie pomoże albo nie ma klepsydry → właściciel systemów |
| A2 | Zwrot zamknięty (`324032`, `325481`) ma `77970` = TAK | pole w `getOrders` | paczka zaginiona (nie wróciła) | zwroty |
| A3 | Zwrot wysłany ponownie tym samym zamówieniem nie ma przywróconych stanów | zamówienie po statusie zwrotu znów w kolejce wejściowej albo `9888` (historia, `log_type` 18) z `77970` = TAK | | zwroty: po przywróceniu stanów wysyłka musi iść nowym zamówieniem |
| A4 | Częściowy zwrot nie przywraca całej paczki | `77970` = TAK przy zwrocie, w którego uwagach jest mowa o części albo uszkodzeniu | | zwroty, właściciel systemów |
| A5 | Zamówienie cofnięte po rozchodzie ma wyjaśniony towar | `77969` = TAK, a zamówienie wróciło do `313961`, kolejki wejściowej albo `9889`; w historii `log_type` 10 (usunięta paczka) | wstrzymanie z towarem odłożonym, opisane w uwagach | lider hubu: towar zszedł ze stanu firmy, a nie wyjechał; anulowanie wymaga przywrócenia stanów |

## B. Wysyłka i tracking

| # | Reguła | Jak sprawdzić | Wyjątki | Do kogo |
| :-- | :-- | :-- | :-- | :-- |
| B1 | Rano brak niewyjaśnionych zamówień w `10455` z poprzedniego dnia roboczego | `ask_agent` o order_id w `10455` sprzed dziś; `getOrderPackages`: kod 1 = kurier nie zabrał | paleta z uzgodnionym odbiorem; paczki spakowane po ostatnim odbiorze | lider hubu |
| B2 | `9888` krócej niż 2 pełne dni robocze | jak wyżej dla `9888`; pilne kody: 3, 7, 8, 9, 12 | komis `294156`; zagranica | zwroty (kontakt z klientką) |
| B3 | Status zgodny z trackingiem | `9888` przy kodzie 5 albo `17910` / `10468` przy kodzie innym niż 5 | odbiór osobisty (bez trackingu) | właściciel systemów |
| B4 | Zamówienie w `9888` ma list w BL | `delivery_package_nr` pusty i brak paczek w `getOrderPackages` | odbiór osobisty, dowóz własny | lider hubu: paczka nadana poza zamówieniem, automatyczne wiadomości nie poszły |
| B5 | Kurier zgodny z wymaganiami klienta B2B | wymagania klienta (Bigin / wiadomość na `#baselinker-bot`) vs `courier_code` paczki | | lider hubu przed nadaniem |
| B6 | Paleta spakowana w 3 dni robocze | B2B w `9886` z dostawą paletową starsze niż 3 dni robocze | termin uzgodniony z klientem | lider hubu |
| B7 | Sklep: złożone do 12:00 wychodzi tego dnia | `10454` z `date_add` dziś przed 12:00, po południu nadal bez paczki | brak towaru w uwagach, weekend, święto | lider hubu |

## C. Zwroty

| # | Reguła | Jak sprawdzić | Do kogo |
| :-- | :-- | :-- | :-- |
| C1 | `284070` nie stoi ponad 7 dni bez ruchu | paczka zwrotna: data ostatniego statusu w `getOrderPackages` | zwroty (reklamacja u przewoźnika) |
| C2 | `320112` nie czeka bez decyzji | `ask_agent`: order_id w `320112` starsze niż 3 dni robocze | zwroty; pieniądze: właściciel systemów |
| C3 | Nowa paczka za 0 zł ma `77977` i `77056` przed spakowaniem | zamówienia z sumą pozycji 0 zł w kolejkach wejściowych | zwroty / pakowanie |
| C4 | Nieopłacone pobranie nie trafia do wypłaty | `320112` z `payment_method_cod` = 1 i `payment_done` = 0 | zwroty: rozliczenie tylko magazynowe |
| C5 | Zwrot z Allegro rozlicza Allegro | `320112` z `order_source` = `allegro` | zwroty: zwrot w panelu Allegro |

## D. B2B

| # | Reguła | Jak sprawdzić | Do kogo |
| :-- | :-- | :-- | :-- |
| D1 | Każde zamówienie B2B z BL ma rekord w Biginie | numery B2B z BL (źródło `39943`, ostatnie 30 dni) vs Bigin po `baselinkerOrderId` (jeśli masz Bigin). Najczęstsza przyczyna braku: kosmetyk z zamówienia nie istnieje w produktach Bigina | właściciel systemów |
| D2 | Numer `ON-B2B__n` jest unikalny | dwa zamówienia z tym samym numerem w `extra_field_2` | właściciel systemów |
| D3 | Waluta, VAT i kraj spójne | `currency` EUR przy `tax_rate` 23 albo kraj inny niż PL przy PLN | handlowiec przed fakturą |
| D4 | Typ transakcji zgodny ze ścieżką | `77837` = `SHIPMENT` z fakturą albo poza ścieżką komisu; `SALE` bez `294244` | handlowiec |
| D5 | Awizacja wysłana na czas | `awizacje.md`, „Przegląd zaległych awizacji” | lider hubu |
| D6 | `313961` on hold nie wisi bez powodu | order_id w `313961` starsze niż 5 dni roboczych; powód w uwagach | handlowiec |
| D7 | Klient wymagający XML faktury ma fakturę | wymóg z Bigina / wiadomości na kanale + `getInvoices` po `order_id` | lider hubu |
| D8 | Etap w Biginie zgodny ze statusem BL | dla zamówień B2B z ostatnich dni: status BL vs `Stage` rekordu w Biginie po `baselinkerOrderId` (mapowanie: `przeplywy.md`, sekcja 2a). Typowy rozjazd: BL `313961` on hold, Bigin „Spakowano” albo „Przekazano do realizacji” | właściciel systemów (rekord trzeba poprawić w Biginie albo ponowić webhook) |

## E. Sklep

| # | Reguła | Jak sprawdzić | Do kogo |
| :-- | :-- | :-- | :-- |
| E1 | `341284` duplikaty rozstrzygnięte w ciągu dnia | liczba i wiek w statusie | pakowanie |
| E2 | Opłacone P24 ma pełną płatność | `payment_method` = `p24`, `payment_done` mniejsze niż pozycje + dostawa; pomiń zamówienia z bonami lub kuponami (uwagi „BONY”, kod kuponu w `extra_field_2`) | właściciel systemów |
| E3 | Zamówienie ze sklepu ma numer i UUID | brak `user_login` `ON-…` albo pola `77620` | właściciel systemów |
