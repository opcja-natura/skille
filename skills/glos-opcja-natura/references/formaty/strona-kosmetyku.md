# Opis kosmetyku na stronę sklepu

Opisy kosmetyków powstają na Dysku Google. **Budowa strony, sekcje, długości, przykład i
checklista są w szablonie opisu.** Ten plik ich nie powtarza, żeby nie było dwóch źródeł prawdy.
Przed pisaniem otwórz szablon i pracuj według niego.

| Co | Gdzie |
| :-- | :-- |
| **Szablon opisu** (sekcje, długości, wzorcowy opis Anty Tarki, checklista) | [00 szablon] szablon opisu na opcjanatura.pl: https://docs.google.com/document/d/1sP6ntnFyl2tdmQshjb7T32SharetrJMsmkd6UvfoD50/edit |
| **Arkusz zmian opisów** (aktualna wersja każdego opisu, zgłoszenia zmian, historia wersji) | [000] Opisy_produktow, zakładka „aktualne”: https://docs.google.com/spreadsheets/d/1qNyeNaQwSCPW_dBjVVAHS2BCY_7BwK3XPetA8LHS38A/edit?gid=177679068 |
| **Folder z opisami** (jeden dokument na kosmetyk i wersję) | https://drive.google.com/drive/folders/1a4HqnTA0Y7NlBGV9w8jmj7-Y9VPL74E_ |

Gdy szablon i ten plik mówią co innego o budowie opisu, **wygrywa szablon.** Ten plik daje
tylko głos, źródła danych i prawo.

## Jak pracujemy

Arkusz ma trzy zakładki:
- **aktualne**: tu sprawdzasz, który dokument jest aktualnym opisem kosmetyku i czy są do niego
  otwarte zmiany (żółty wiersz). Liczy się sama, nic w niej nie wpisujesz.
- **zmiany**: zgłoszenia poprawek. Jedno zgłoszenie = jeden wiersz.
- **wersje**: każdy nowy dokument opisu to jeden wiersz.

**Poprawka istniejącego opisu**
1. Zgłoś ją w „zmiany”: data, kosmetyk, sekcja opisu, co zmienić, kto zgłasza. Kolumnę
   „Weszło w wersję” zostaw pustą: zgłoszenie jest otwarte.
2. Gdy nanosisz poprawki: otwórz aktualny dokument (link w „aktualne”), zrób jego kopię
   w folderze z opisami (podfolder bieżącego miesiąca `RRRR-MM`), nazwij ją
   `[opis RRRR-MM-DD] <nazwa kosmetyku>__<EAN>__` z dzisiejszą datą i popraw kopię.
   Starych wersji nie nadpisujesz.
3. Dodaj wiersz w „wersje”: kosmetyk, data, link do nowego dokumentu, co się zmieniło, kto.
4. Zamknij zgłoszenia: w „zmiany” wybierz w „Weszło w wersję” wersję, w której poprawka weszła.
   Lista pokazuje tylko wersje tego kosmetyku (aktualną w dniu zgłoszenia i pierwszą nowszą).

**Nowy kosmetyk**
1. W arkuszu wybierz z menu **Opisy → Wygeneruj nowy opis** i wskaż kosmetyk. Skrypt sam zrobi
   kopię szablonu w folderze z opisami (podfolder `RRRR-MM`), nazwie ją
   `[opis RRRR-MM-DD] <nazwa kosmetyku>__<EAN>__`, wpisze nazwę kosmetyku i dopisze kosmetyk
   w „aktualne”. Kosmetyku nie ma na liście = nie ma go jeszcze w bazie produktów: zapytaj Daniela.
2. Napisz opis według szablonu (szare teksty to przykład, nadpisz je) i dodaj wiersz w „wersje”.

Starej zakładki „Opisy produktów” (kto pisze, status) już nie używamy: to archiwum pisania
opisów z 2026.

Aktualny dokument z zakładki „aktualne” jest też źródłem dla tłumaczenia na angielski
(`tlumaczenia-opcja-natura`).

## Zanim zaczniesz: dane

- **Nazwa i podtytuł** z etykiety: decyduje projektowanie, nie Ty.
- **Skład, przeznaczenie, ostrzeżenia, pojemność**: z bazy (`produkty-lookup`). Składu nie
  piszesz ani nie poprawiasz.
- **Co go wyróżnia** (kluczowy składnik, stężenie, mechanizm) i **historia powstania**: od Agaty.
  Nie zgaduj stężeń ani mechanizmów.
- **Dla jakiej skóry, jak stosować, z czym łączyć**: z karty kosmetyku (`produkty-lookup`: typ skóry, sposób użycia, rytuały) albo od Agaty.

Brakuje czegoś z tej listy, zapytaj, zanim zaczniesz pisać.

## Głos na stronie kosmetyku

Zasady z `SKILL.md` i `warsztat-prozy.md`, a tu najważniejsze dla tego formatu:

- Opis główny zaczyna się od sytuacji klientki, nie od nazwy kosmetyku. Ma być miejsce, gdzie
  czytelniczka pomyśli "to o mnie".
- Mechanizm zamiast przymiotnika: "lanolina spowalnia parowanie wody z naskórka", nie
  "lanolina intensywnie nawilża".
- Każda sekcja robi co innego. Ta sama fraza w korzyściach, opisie i "Jak działa" to trzy razy
  to samo. To samo słowo ("otula", "nawilża") użyj raz, celowo.
- Składniki nie mogą brzmieć jednakowo ("wspiera odnowę" przy każdym). Podobne oleje opisz
  razem. Nie pisz "kompleks olejów", wymień je.
- "Kosmetyk", nie "produkt"; zero myślników.

## Prawo na stronie kosmetyku

Strona kosmetyku jest punktem odniesienia dla wszystkich innych tekstów (blog, SEO, posty muszą
się z nią zgadzać), więc tu ostrożność jest największa. Przed oddaniem przejdź audyt z
`compliance.md` (sekcja 6), szczególnie:

- **Gwarancje efektu i terminy** ("efekt po tygodniu", "pomaga") tylko z dokumentem (wzorzec 4).
- **Choroby i stany medyczne** (także w historii klientki albo w "Kosmetycznych historiach"):
  opowieść jest w porządku, obietnica leczenia nie (wzorzec 1 i 6).
- **Mazidło Opatrunkowe, Atop Stop, kosmetyki do tatuażu**: szczególnie ostrożnie.
- **Ostrzeżenia i przeciwwskazania** muszą być wpisane, bo inne teksty się na nie powołują
  (wzorzec 5).
