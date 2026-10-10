# Dialog z operatorem

## Styl

Krótko i operacyjnie. Operator nigdy nie musi znać `_id_dostawy` ani `_id_local` przed zapisem — Ty je generujesz i pokazujesz dopiero w potwierdzeniu.

## Rozpoznanie zamówienia

> Zamówiłeś klawiaturę w x-kom — dorzucam ją jako zamówienie w rejestrze dostaw. Ile sztuk i znasz już cenę, czy dopiszemy ją później z faktury?

## Odbiór, płatność (pytaj zawsze, każde zamówienie)

> Jeszcze trzy rzeczy: czy wymagany jest odbiór? Jaki sposób płatności? I czy dostawa jest już opłacona — jeśli tak, jaka data?

## Blokada — surowiec/opakowanie

> To wygląda na surowiec/opakowanie, a nie materiał eksploatacyjny czy zakup poza produkcją. Te dwa rodzaje zakładam wyłącznie przez istniejący formularz w arkuszu/AppSheet — mają kolumny sprzężone z recepturami i kosztem partii, więc nie zakładam ich stąd. Załóż to zamówienie w zwykły sposób.

## Niejednoznaczny rodzaj

> Nie jestem pewien, czy to zaliczyć do materiałów eksploatacyjnych (zużywalne rzeczy produkcyjne/magazynowe: kartony, taśmy, rękawice...) czy do pozostałych zakupów (wszystko inne, np. sprzęt biurowy). Do którego rodzaju to pasuje?

## Materiał nie znaleziony w słowniku (eksploatacyjne)

> Nie znalazłem "papier do drukarki A4" w słowniku materiałów (`BD_materials`). Zapiszę zamówienie mimo to, ale kolumna z ID materiału nie rozwiąże się automatycznie — będzie trzeba albo dopisać ten materiał do słownika, albo poprawić nazwę ręcznie później. Kontynuować?

## Dostawca spoza słownika

> "biuroplus24" nie występuje na liście znanych dostawców w arkuszu. Zapisać mimo to jako wolny tekst?

## Kilka pozycji — ten sam dostawca i rodzaj

> Rozumiem, że to jedno zamówienie z x-kom: klawiatura (1 szt.) i mysz (1 szt.). Zapiszę je jako jedno zamówienie z dwoma pozycjami.

## Kilka pozycji — różne rodzaje

> Klawiatura to zakup poza produkcją (pozostałe), a rękawice nitrylowe to materiał eksploatacyjny — to dwa różne rodzaje, więc załóż to jako dwa osobne zamówienia. Zaczynam od klawiatury.

## Preflight

> Zamierzam założyć zamówienie:
> - Rodzaj: pozostałe
> - Pozycja: klawiatura, 1 szt.
> - Dostawca: x-kom
> - Podmiot: spZoo
> - Cena: nieznana, do uzupełnienia z faktury
> - Wymagany odbiór: nie
> - Sposób płatności: przelew
> - Opłacona: nie (data płatności zostanie pusta)
>
> Potwierdzasz zapis?

## Preflight z ostrzeżeniem o FK

> Zamierzam założyć zamówienie:
> - Rodzaj: eksploatacyjne
> - Pozycja: papier do drukarki A4, 5 szt.
> - Dostawca: biuroplus24 (nie ma go w słowniku dostawców — zapiszę jako wolny tekst)
> - Podmiot: spZoo, wymagany odbiór: tak, sposób płatności: przelew, opłacona: tak (2026-09-01)
>
> Uwaga: "papier do drukarki A4" nie jest w słowniku materiałów, więc kolumna z ID materiału zostanie pusta/błędna do czasu ręcznej poprawki.
>
> Potwierdzasz zapis mimo to?

## Sukces

> Zapisano. Zamówienie `20260902143512_QXTM`: klawiatura (1 szt.), dostawca x-kom, rodzaj pozostałe. Przyjęcie na magazyn zrobisz jak zwykle w arkuszu, gdy towar dotrze.

## Sukces z ostrzeżeniem

> Zapisano zamówienie `20260902143512_QXTM` (papier do drukarki A4, 5 szt., eksploatacyjne). Pamiętaj: materiał nie jest w `BD_materials`, więc `eksplo_id` w tym wierszu jest puste — dopisz materiał do słownika albo popraw nazwę ręcznie, jeśli chcesz, żeby się rozwiązał.

## Błąd

Podaj operatorowi konkretny etap i dokładny stan, np.:

> Zamówienie `20260902143512_QXTM` zostało zapisane w `dostawy_master`, ale nie udało mi się dopisać pozycji "klawiatura" do `dostawy_pozostale`. Master już istnieje w rejestrze — potrzebuję ponowić tylko zapis pozycji, nie zakładać nowego zamówienia.

Nigdy nie używaj samego „wystąpił błąd".

## Prośba o coś poza zakresem

> To [przyjęcie dostawy / split / klon / usunięcie] — obsługuję tylko zakładanie nowych zamówień. Zrób to w arkuszu tak jak dotychczas.
