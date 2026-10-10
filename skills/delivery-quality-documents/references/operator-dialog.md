# Dialog z operatorem

## Styl

Krótko i operacyjnie. Operator nigdy nie musi znać `id_dostawy` ani `_id_local` — Ty je ustalasz i tylko pokazujesz do potwierdzenia.

## Niejednoznaczny surowiec

> Znalazłem kilka surowców pasujących do "algi". Który wybierasz?
> 1. Algi brunatne [SUR__001]
> 2. Algi czerwone [SUR__014]

## Wybór pozycji dostawy — kilka kandydatek

> Dla "Algi brunatne" mam kilka niedawnych dostaw. Której dotyczy ten dokument?
> 1. Dostawa 2026-08-20, dostawca: Alg-Borje AB [id_dostawy: 20260820_A31F]
> 2. Dostawa 2026-08-05, dostawca: Alg-Borje AB [id_dostawy: 20260805_9C02]

## Wybór pozycji dostawy — jedna oczywista kandydatka

> Znalazłem jedną niedawną dostawę Alg brunatnych: 2026-08-20, dostawca Alg-Borje AB. Tej dotyczy dokument?

## Brak pasującej dostawy

> Nie znalazłem żadnej dostawy Alg brunatnych w rejestrze `dostawy_surowce`. Nie mogę podpiąć dokumentu do nieistniejącej dostawy — czy dostawa na pewno została już wprowadzona do systemu?

## Ostrzeżenie o duplikacie

> Dla tej pozycji dostawy już jest zapisany dokument: `SUR__001__CoA_2026-08__20260820_A31F` ([link]). Czy ten nowy plik to dodatkowy dokument (np. osobny MSDS), czy pomyłka?

## Preflight

> Zamierzam podpiąć dokument:
> - Surowiec: Algi brunatne [SUR__001]
> - Dostawa: 20260820_A31F, przyjęta 2026-08-20, dostawca Alg-Borje AB
> - Plik: `CoA_algi_sierpien.pdf` → w Drive jako `SUR__001__CoA_algi_sierpien__20260820_A31F`
> Potwierdzasz zapis?

## Sukces

> Zapisano. Plik: `SUR__001__CoA_algi_sierpien__20260820_A31F` w folderze archiwum ([link]). Wiersz dodany do `dokumentacja_surowce`.

## Podgląd — brak wyników

> Nie znalazłem żadnych dokumentów jakościowych dla tej dostawy/surowca w `dokumentacja_surowce`.

## Błąd

Podaj operatorowi konkretny etap i dokładny stan, np.:

> Plik został zapisany w Drive jako `SUR__001__CoA_algi_sierpien__20260820_A31F` ([link]), ale nie udało mi się dopisać wiersza do `dokumentacja_surowce`. Arkusz nie ma jeszcze tego wpisu — potrzebuję ponowić zapis wiersza, nie ponownie uploadować pliku.

Nigdy nie używaj samego „wystąpił błąd”.
