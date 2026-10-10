---
name: przelewy-powracajace
description: >
  Odnotowanie opłaconych płatności powracających (wypłaty, ZUS, podatki, czynsze, abonamenty, kurierzy, stałe faktury) w arkuszu Google „003_przelewy powracajace” Opcja Natura. Używaj, gdy ktoś wrzuca listę przelewów (plik CSV z iPKO, wyciąg z banku, wklejoną tabelkę, PDF) i prosi „zaznacz opłacone”, „odnotuj płatności”, „wpisz wypłaty do systemu”, „co z tego jest w przelewach powracających”, albo pyta „czy X jest już zapłacone w tym miesiącu”, „kiedy ostatnio płaciliśmy za Y”. NIE do generowania plików przelewów do banku ani do księgowania.
---

# Przelewy powracające: co zostało opłacone

Arkusz: **003_przelewy powracajace**
https://docs.google.com/spreadsheets/d/1sg_GF_ujKiSSncFFcgpv8nynQRNXgur1ZjUf6e5r3GU/edit

Dostajesz listę przelewów. Część z nich to płatności powracające z arkusza, a część to zwykłe zakupy, które arkusza nie dotyczą. Twoje zadanie: rozpoznać, które przelewy są powracające, przygotować gotowe wiersze do wklejenia i wypisać operatorowi wszystko, czego nie da się rozstrzygnąć bez człowieka.

**Arkusza nie edytujesz.** Czytasz go przez podłączony Google Drive, a wynik podajesz jako wiersze do wklejenia. Jeśli Drive nie jest podłączony albo widzisz tylko jedną zakładkę, poproś o wklejenie zawartości zakładek `payments_list` i `payments_logs` (wystarczą wpisy z ostatnich 3 miesięcy).

## Zakładki

| Zakładka | Co w niej jest | Do czego ci służy |
|---|---|---|
| `payments_list` | Katalog płatności powracających, jeden wiersz na płatność | dopasowanie przelewu do `id_platnosci` |
| `payments_logs` | Dziennik opłat, jeden wiersz na jeden opłacony przelew | tu idą twoje wiersze; tu też sprawdzasz duplikaty |
| `payments_companies` | Firmy: `company_id`, nazwa rozliczeniowa, NIP | dopasowanie po nazwie firmy i NIP-ie |
| `payment_list-new`, `helper`, `config` | Widoki i słowniki liczone formułami | nie ruszać |

**`payments_list`, kolumny:** A `id_platnosci` · B `typ` (wynagrodzenie, wynajem, usługa obca, abonament, zus, podatek, VAT, kurier, leasing / rata, reklama, ubezpieczenie, b2b pozostale) · C `nazwa` (często potoczna, np. „wypłata kamilla”) · D `wlascicel` · E `active` (tak/nie) · F `podmiot` (sp zoo / jdg) · G `czestotliwosc` · H `sposob platnosci` (przelew, blik, karta, auto) · I `potrzebna fv` · J `data ostatniej płatności` (formuła) · L `notka` · P `recurring company` (nazwa z `payments_companies`).

**`payments_logs`, kolumny do wypełnienia (tylko A–G):**

| Kol. | Pole | Jak wypełnić |
|---|---|---|
| A | `id_platnosci` | id z `payments_list` |
| B | `data` | data przelewu z pliku/wyciągu, format `RRRR-MM-DD`. Gdy różni się od tego, co mówi operator („dziś poszły”), bierzesz datę z pliku i mówisz o tym w podsumowaniu. Gdy plik jest starszy niż tydzień, ostrzeż, że te przelewy mogły już zostać odnotowane |
| C | `nazwa fv` | numer faktury z tytułu przelewu; przy split payment ten z `/TXT/` (np. `A3/6/2026`), a gdy go tam nie ma, wartość `/INV/`; przy wypłatach, ZUS-ie i podatkach zostaw puste |
| D | `kwota netto` | **netto z faktury**, z kropką dziesiętną, bez spacji i „zł” (np. `6568.88`). Jak je ustalić: tabela „Kwota netto” niżej |
| E | `user` | e-mail osoby, która odnotowuje (`daniel@opcjanatura.pl` albo `operacje@opcjanatura.pl`). Jeśli nie wiesz, zapytaj raz |
| F | `comment` | krótko i tylko gdy coś wnosi, np. `Wynagrodzenie za okres 09/2026`, `rata 2/3`, `zapłacono 50 zł więcej` |
| G | `local_id` | 8 znaków `0-9a-f`, losowe, **zawsze zaczynające się od litery a, b, c, d lub f** (inaczej np. `578e1234` arkusz zamieni na liczbę `5.78E+07`) |

### Kwota netto

| Przelew | Co wpisać w D |
|---|---|
| Wypłata z listy płac, ZUS, podatek, VAT, opłata urzędowa | kwota przelewu (nie ma VAT-u) |
| Odbiorca oznaczony w słowniku „bez VAT” | kwota przelewu |
| Split payment (kod `53`, `/VAT/…` w tytule) | kwota przelewu − VAT z tytułu, dokładnie. Przykład: 1537.50 − 287.50 = `1250.00` |
| Pozostałe faktury od firm (VAT nieznany z przelewu) | kwota przelewu ÷ 1,23, zaokrąglona do grosza, **i wątpliwość** „netto policzone przy 23% VAT, sprawdź z fakturą”. Wiersz i tak dajesz do wklejenia |
| Osoba lub JDG, której nie ma w słowniku | kwota przelewu i wątpliwość „czy faktura ma VAT? jeśli tak, netto = przelew ÷ 1,23” |

Starsze wpisy w dzienniku bywają brutto (np. kurierzy). Nie traktuj ich jako wzoru i nie poprawiaj wstecz.

Kolumny H–L (`helper payment type`, udziały B2B/B2C) liczą się same z formuł. Nie wklejaj w nie niczego, bo zablokujesz formułę.

## Jak czytać listę przelewów

**Plik CSV z iPKO (import przelewów)**, kodowanie ISO-8859-2, jeden przelew na linię, pola po przecinku:
`110, data RRRRMMDD, kwota w groszach, …, rachunek nadawcy, rachunek odbiorcy, "nadawca", "Odbiorca||ulica|kod miasto", 0, …, "tytuł (linie rozdzielone |)", "", "", "51" lub "53"`.
Kwota `656888` to 6 568,88 zł. Kod `53` oznacza split payment, a tytuł ma wtedy postać `/VAT/287,50/IDC/<NIP>/INV/<nr faktury>/TXT/…`: NIP służy do dopasowania firmy, VAT do policzenia netto, a numer faktury bierzesz jak w kolumnie C.
**To jest zlecenie, nie potwierdzenie.** Plik importu pokazuje, co miało pójść, a nie to, co bank wykonał. Zawsze dopisz to w uwagach dla operatora.

**Wyciąg/historia rachunku, wklejona tabelka, PDF:** bierz datę księgowania, kwotę obciążenia, odbiorcę i tytuł. Wpływy na konto pomijasz.

Konto nadawcy `91 1020 2267 0000 4902 0224 3202` należy do **Opcja Natura Sp. z o.o.** Płatność spółki nie trafia na id z `podmiot = jdg`.

## Jak rozpoznać płatność powracającą

Dla każdego przelewu, po kolei:

1. **Szukaj odbiorcy** w słowniku niżej, w `payments_companies` (nazwa albo NIP) i w `nazwa` w `payments_list`. Porównuj bez wielkości liter, form prawnych i polskich znaków. Nazwa w banku bywa skrócona do 35 znaków.
2. **Przelew bez dopasowania** to zwykły zakup (surowce, opakowania, jednorazowe usługi, urzędy). Trafia do „Pominięte”. Wyjątek: odbiorca wygląda na stały koszt (prąd, wypłata nowej osoby, stały podwykonawca), a nie ma go na liście. Wtedy idzie do „Do decyzji” jako propozycja dopisania do `payments_list`.
3. **Przelew dopasowany sprawdź** pod kątem warunków z tabeli. Każde „tak” przenosi pozycję do „Do decyzji”.

| Sprawdzenie | Kiedy to wątpliwość |
|---|---|
| Kilka id pasuje do jednego odbiorcy | zawsze, chyba że tytuł albo kwota jednoznacznie wskazują jedno (patrz słownik) |
| `active = nie` | zawsze |
| `podmiot = jdg` przy przelewie z konta spółki | zawsze |
| W `payments_logs` jest już wpis tego id w tym samym miesiącu (dla wypłat: za ten sam okres) | zawsze. Dla typu `kurier` i przy ratach/kilku fakturach to normalne, ale i tak to zaznacz |
| Kwota netto różni się o ponad 30% od ostatniego wpisu tego id | tylko informacyjnie, wiersz i tak podajesz |
| Ta sama osoba ma i wypłatę, i faktury | wpisz na to samo id, w komentarzu napisz, czego dotyczy |

Nie zgaduj. Jeśli nie wiesz, który id wybrać, pozycja idzie do „Do decyzji” razem z twoją propozycją. Nie wpisujesz jej do bloku do wklejenia.

## Słownik odbiorców (stan 10.2026)

Nazwy w `payments_list` są potoczne, a w banku pełne. Ten słownik to podpowiedź; rozstrzyga zawsze aktualny `payments_list`. Gdy id ze słownika zniknęło z listy albo jest nieaktywne, to jest wątpliwość.

**Wypłaty z listy płac** (tytuł „Wynagrodzenie za okres MM/RRRR”, bez faktury):

| Odbiorca w banku | id | nazwa w arkuszu |
|---|---|---|
| Kamilla Pługowska | `ssuck_001` | wypłata kamilla |
| Maciej Jerczak | `ssuck_003` | wypłata maciek |
| Krystian Konieczny | `3e13b2a7` | wyplata krystian |
| Tomasz Parysek | `9c281b0a` | wypłata Parys |
| Karina Orwat | `d72804a4` | wypłata Karina |
| Urszula Mierzwa-Pakuła | `7b539526` | Urszula Mierzwa (też faktury „Grafika”, to samo id) |
| Łukasz Jakubiec | `934c8ab1` | Łukasz Jakubiec |
| Daniel Suliga | `3a79ce28` | wynagrodzenie Daniel Suliga |
| Maria Maćków | `19c0d6a3` | umowa zlecenie |
| Agata Cierzniak | `43d13e84` | umowa o dzieło |
| Kalina Barańska | `07826d4d` | umowa o dzieło |
| Aleksandra Szczodry, Monika Kwiecień-Gonda | `9527c3b7`, `375ae33e` | nieaktywne, więc wątpliwość |
| Antonina Zaleska | brak na liście | wątpliwość: dopisać do `payments_list`? |

**Faktury i stałe koszty:**

| Odbiorca w banku | id | Uwaga |
|---|---|---|
| Katarzyna Malińska Życiodajnia | `ssuck_002` | „wyplata kaśka”, faktury FVS, bywa kilka w miesiącu, bez VAT |
| Systemy Informatyczne Marek Szewczyk | `ssuck_005` | „wypłata grubby” |
| Daria Szczygieł | `fd6f461a` | fotograf, bez VAT |
| Konrad Orzechowski (TATTOO) | `d3f488cc` | |
| Zuzanna Litawińska | `7259cb91` | bez VAT |
| Jakub Biernacki / USEME | `2fc728b1` | |
| Biuro Obrotu Nieruchomościami Inwestor | `ssuck_006` | czynsz biuro + magazyn |
| Biuro Rachunkowe Joanna Tomaszewska | `ssuck_009` | |
| Piotr Jerzak | `ssuck_010` | księgowość |
| EMTE Mateusz Bőhm | `ssuck_012` | internet (sp zoo), z VAT |
| P4 sp. z o.o. (Play) | `ssuck_013` | `ssuck_014` to Play na jdg |
| FedEx Express Poland | `ssuck_022` lub `84bc8dde` | dwa konta, więc wątpliwość, chyba że historia jednoznaczna |
| ORLEN Paczka | `ssuck_023` | |
| InPost | `ssuck_024` lub `ssuck_025` | dwa konta, więc wątpliwość |
| Mpg Info Sp. z o.o. | `e7564707` | konsultacje B2B Grzegorza Gęsiarka (faktury „FV nn/RRRR”) |
| MPG Grzegorz Gęsiarek | `ssuck_028` | magazyn Kobierno, ok. 360 zł netto. Inna kwota oznacza wątpliwość (może to być konsultacja `e7564707` albo coś spoza listy) |
| Tomasz Wirbał | `ssuck_029` | reklamy, z VAT |
| Erste Leasing | `5ec2db47` | Volvo_spZoo (w arkuszu firma: Santander, raty idą do Erste) |
| DHL eCommerce | `98d7f7f7` | |
| BRW Control | `38580ab8` | BHP, płatność co 2 miesiące |
| Radosław Rubiński | `c5111627` | SEO, zwykle split payment |
| Opcja Natura Agata Suliga | `87f9cd87` | faktura JDG dla spółki, z VAT |
| ZUS, Urząd Skarbowy (mikrorachunek) | `ssuck_016` / `ssuck_017` CIT / `ssuck_018` VAT / `ce726857` PIT-4 | typ z tytułu (`/TI/`, symbol formularza); jdg-owe id tylko z konta JDG |

Typowo **pomijane** (zakupy, nie płatności powracające): OQEMA, Strzelczyk, Fabpack, Chemes, Heinz-Plastics, Pakmar, Emcor, Biomus, Orcideo, BL Logistics, urzędy (opłaty skarbowe, Urząd Patentowy). Energa nie ma jej na liście; jeśli się pojawi, zapytaj, czy dopisać.

## Wynik: zawsze w tym układzie

**1. Podsumowanie:** jedno–dwa zdania, np. „14 przelewów: 8 do odnotowania, 4 pominięte, 2 do decyzji. Suma przelewów do odnotowania: 50 985,07 zł.” Plus data z pliku, jeśli różni się od „dziś”.

**2. Do wklejenia w `payments_logs`:** czytelna tabela (odbiorca · id · nazwa w arkuszu · data · kwota · nr FV), a pod nią blok kodu z wierszami rozdzielonymi **tabulatorami**, kolumny A–G, bez nagłówka:

```
934c8ab1	2026-10-06		6568.88	daniel@opcjanatura.pl	Wynagrodzenie za okres 09/2026	a4c19e07
ssuck_024	2026-10-06	59596/2026/F/06	12179.44	daniel@opcjanatura.pl		d02b7f13
```

Instrukcja dla operatora (podaj ją zawsze, jednym zdaniem): skopiuj blok, kliknij komórkę A w pierwszym pustym wierszu zakładki `payments_logs` i wklej. Jeśli na dole nie ma pustych wierszy, najpierw dodaj wiersze („Dodaj … wierszy u dołu”). Po wklejeniu kolumna `data ostatniej płatności` w `payments_list` zaktualizuje się sama.

**3. Do decyzji operatora:** numerowana lista. Wszystkie netto policzone ÷ 1,23 zbierz w **jednym** punkcie („sprawdź netto z fakturami: Wirbał 8300.00, Orlen 5148.88…”); te wiersze i tak są w bloku do wklejenia. Każda pozostała pozycja ma postać: przelew (odbiorca, kwota, tytuł), w czym problem i twoja propozycja z gotowym wierszem do wklejenia po akceptacji. Na końcu zawsze, jeśli źródłem był plik importu z iPKO: „Lista to zlecenie do banku. Wklej wiersze dopiero, gdy przelewy są wykonane.”

**4. Pominięte:** krótka lista „odbiorca, kwota, powód” (np. „zakup surowca, nie ma na liście powracających”).

Jeśli któraś sekcja jest pusta, napisz „brak”. Odpowiadaj po polsku, krótko, bez wykładu o systemie.

## Pytania typu „czy X zapłacone?”

Znajdź id w `payments_list` i podaj kolumnę `data ostatniej płatności`. Na pytanie o konkretny miesiąc odpowiadaj z wpisów `payments_logs` z tego miesiąca, z kwotą i numerem faktury. Jeśli id jest `active = nie`, powiedz to.
