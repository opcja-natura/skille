# Magazyn i planowanie produkcji — konektor „analityk”

Stan na 26.11.2026. Dotyczy pytań: „ile mamy na stanie”, „na ile wystarczy”, „ile doprodukować”, „kto z B2B już zamówił”.

## Dostęp

Konektor MCP **analityk** (claude.ai, tylko odczyt). Narzędzia:

| Narzędzie | Do czego |
| :-- | :-- |
| `analityk_schemat` | lista widoków z opisami kolumn i regułami; wywołaj raz na początku |
| `analityk_produkt` | rozpoznanie produktu po nazwie, SKU albo EAN; zwraca też cenę regularną i promocyjną, daty promocji, stan |
| `analityk_stan_i_zapas` | stan, sprzedaż 30/90 dni, zapas w dniach, zlecenia w toku |
| `analityk_tempo_sprzedazy` | sprzedaż w oknach dni, per kanał (B2C, B2B, POS) i osobno sklep www |
| `analityk_zapytanie` | jeden SELECT na widokach `mcp_analityk.v_*`, z podanym celem (trafia do dziennika) |

Konektor **nie zawiera** kosztów, receptur ani marż. Gdy go nie masz, powiedz to; nie licz stanów z bazy sklepu „po swojemu”.

## Co jest w danych

- **Stan** (`v_stany`) — na żywo, domyślnie magazyn `C` (centralny). Wersje EN produktów nie mają ruchów.
- **Sprzedaż sklepu www** (`v_sprzedaz_sklep_dzienna`) — wg dnia **zamówienia**, klienci zamawiają 24/7. Źródło do dziennego tempa i kształtu sezonu.
- **Sprzedaż z magazynu** (`v_sprzedaz_dzienna`) — wg dnia **pakowania**, kanały B2B / B2C / POS. Źródło do łącznego zejścia ze stanu.
- **B2B per klient** (`v_sprzedaz_b2b_klient`, `v_klienci_b2b`) — kto, co i kiedy; status klienta z CRM. Historia od 20.03.2025.
- **Produkcja** (`v_zlecenia`, `v_harmonogram`, `v_partie`, `v_przyjecia_produkcji`, `v_wsady`) — zlecenia w toku, terminy, przyjęte partie.
- **Promocje** — w `v_produkty`: czy promocja w sklepie trwa i do kiedy. Tylko bieżąca lub zaplanowana; historii promocji nie ma.
- Stany, partie, ERP i klienci są na żywo. Sprzedaż to kopia odświeżana ok. 04:30 i 13:00; każda odpowiedź narzędzia podaje, do kiedy sięga.

## Pułapki (każda już raz dała zły wynik)

1. **Sklep i magazyn to te same sztuki w innym dniu.** Magazyn pakuje w dni robocze; zamówienia po ok. 13:00 schodzą następnego dnia roboczego, a z piątku po południu i z weekendu w poniedziałek. Różnica dzień do dnia to rytm pracy, nie dodatkowy kanał. Porównuj tylko sumy z pełnego tygodnia lub dłużej. Marketplace'y to ok. 2 % B2C.
2. **Kształt sezonu bierz ze sklepu, nie z magazynu.** W 2025 zejścia B2C były dodatkowo przesunięte i Black Week 2025 widać w magazynie częściowo w grudniu.
3. **Tempo z promocji nie jest tempem bazowym.** Sprawdź w `analityk_produkt`, czy promocja trwa, zanim przeniesiesz bieżące tempo w przyszłość. Nie mnoż tempa z Black Week przez „mnożnik Black Week”.
4. **Sprzedaż = powód `SALE`.** Wysyłki marketingowe mają typ sprzedażowy, ale nie są sprzedażą; narzędzia już je pomijają, własny SQL musi filtrować `powod = 'SALE'`.
5. **B2B: tylko klienci aktywni.** Klient ze statusem „nieaktywny”, „współpraca zakończona” albo „działalność zamknięta” nie domówi; pokaż go osobno jako popyt utracony.
6. **`v_partie` to przyjęcia, nie stan.** Sprzedaż nie niesie numeru partii.
7. **Wszystko netto.** Wartość sprzedaży sklepu jest po cenie pozycji; kupon na całe zamówienie nie jest odjęty.

## Jak liczyć „ile doprodukować”

1. **Produkt.** `analityk_produkt` → podaj w odpowiedzi pełną nazwę, SKU, EAN i product_id.
2. **Podaż.** Stan w C + zlecenia w toku (ilość, termin, status masy).
3. **Tempo bazowe ze sklepu**, z nazwanego okresu. Jeśli trwa promocja, powiedz to i nie przenoś tego tempa dalej.
4. **Wzorzec na przyszłość** z produktu o podobnym charakterze (sezonowy z sezonowego rok wcześniej), nie z całego sklepu.
5. **B2B osobno:** kto już zamówił w tym sezonie, kto rok temu domawiał; tylko aktywni.
6. **Pozostałe zejścia:** POS, marketing, testery (z 90 dni).
7. **Horyzont.** Dla produktów świątecznych do ostatnich wysyłek przed Wigilią (ok. 20–21.12); potem sprzedaż spada prawie do zera.
8. **Wynik w trzech wariantach** (ostrożny / bazowy / wysoki), z założeniem „bez nowych promocji i akcji”.
9. **Kontrola:** porównaj prognozę z pełnym sezonem produktu-wzorca i z dotychczasową sprzedażą. Wynik wielokrotnie wyższy wymaga wyjaśnienia.
10. **Na końcu zapytaj** (jeśli pytający sam nie podał): planowane promocje i terminy, umówione zamówienia B2B, czy produkt zostaje w ofercie po sezonie.

## Przykład: Boski Peeling z Cynamonem, 26.11.2026

Nie przepisuj liczb; to wzór toku liczenia.

- **Produkt:** Boski Peeling z Cynamonem, SKU `peeling-cynamon`, EAN 5903766418445, product_id `OgM7jr9OSf`. Promocja Black Week trwa do 1.12.
- **Podaż:** stan ok. 230 szt. + zlecenie 300 szt. na 30.11–1.12 = ok. 530.
- **Sklep, dziennie od 20.11:** 13, 9, 23, 29, 44, 30. Skok od 22.11 to Black Week, więc ok. 30 szt./dzień to tempo promocyjne.
- **Kontrola źródeł:** 19–26.11 sklep 159 szt., B2C z magazynu 155 szt. — to samo. (Z samych dni 23–26.11 wyszłoby mylące 1,3×, bo w poniedziałek zeszły zamówienia z weekendu.)
- **Wzorzec:** Świąteczny Sztos 2025 w sklepie: Black Week 99 szt. (ok. 14/dzień), 1–24.12 186 szt. (ok. 8/dzień, czyli ok. 55 % tempa z Black Week), po świętach 16 szt.
- **Popyt do świąt:** reszta Black Week 120–165; grudzień przy 40–55 % tempa z Black Week 290–400; dokładki B2B 100–150 (listopad: 258 szt., z tego 241 od 23 aktywnych klientów, po jednym zamówieniu); POS i marketing 40–60. Razem ok. 550–780.
- **Wniosek:** brakuje ok. 20–250 szt.; zlecenie podnieść z 300 do ok. 450–500. Powyżej tego towar zostaje po świętach.
- **Błędy z tego dnia, których unikać:** krzywa sezonu z magazynu (wynik 600), mnożnik Black Week nałożony na tempo z Black Week i wzorzec z całego sklepu (wynik 1 100 ponad plan), mnożnik 1,3× z czterech dni (wynik 400 ponad plan).
