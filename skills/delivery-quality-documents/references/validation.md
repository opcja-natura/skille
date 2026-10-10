# Walidacja i bezpieczeństwo

## Przed każdą mutacją

- Odczytaj stan live z `dostawy_surowce` i `dokumentacja_surowce`, nie polegaj wyłącznie na wcześniejszym wyniku w rozmowie — inne kanały (n8n, AppSheet webhook) piszą do tej samej tabeli równolegle.
- Sprawdź, że wybrana pozycja dostawy (`_id_local`) faktycznie istnieje w `dostawy_surowce` w momencie zapisu.
- Sprawdź dostęp do pliku źródłowego.
- Sprawdź, czy wymagane dane są kompletne (surowiec, pozycja dostawy, plik).

## Klucz dopasowania

`_id_local` (kol. M `dostawy_surowce`) = `id_surowiec_local` (kol. D `dokumentacja_surowce`) jest jedynym kluczem łączącym dokument z konkretną pozycją dostawy. Nie dopasowuj po samej nazwie surowca ani po samym `id_dostawy` — jeden surowiec może wystąpić w tej samej dostawie więcej niż raz jako osobne pozycje.

## Duplikat wiersza dokumentacji

Duplikat = istniejący wiersz `dokumentacja_surowce` z tym samym `id_surowiec_local`.

To **ostrzeżenie, nie blokada**: jedna pozycja dostawy może mieć więcej niż jeden dokument (np. CoA i osobno MSDS). Pokaż operatorowi, co już jest zapisane, i zapytaj, czy kontynuować.

## Duplikat pliku

Jeśli operator próbuje podpiąć plik, który wygląda identycznie jak już zapisany dla tej samej pozycji (ta sama nazwa źródłowa, ten sam rozmiar) — zwróć na to uwagę przed uploadem, żeby uniknąć przypadkowego zdublowania tego samego dokumentu.

## PDF-only

Zatwierdzony plik ma być PDF-em w folderze archiwum. Jeśli źródło jest Google Doc/Sheet/Slide lub innym formatem możliwym do eksportu, eksportuj do PDF. Jeśli nie można uzyskać poprawnego PDF-u, przerwij operację.

Konwencja nazwy:

```text
<surowiec_id>__<oryginalna_nazwa_bez_rozszerzenia>__<id_dostawy>
```

Nie zmieniaj tego formatu — musi pozostać spójny z tym, co zapisują n8n i webhook AppSheet do tej samej tabeli.

## Kolejność zapisu

Dozwolona:

```text
walidacja -> upload PDF do Drive -> potwierdzenie sukcesu uploadu -> append wiersza w dokumentacja_surowce -> read-back
```

Niedozwolona:

```text
append wiersza -> próba uploadu pliku
```

Jeśli upload się powiedzie, ale append się nie powiedzie: nie próbuj automatycznie kasować pliku z Drive ani ponawiać uploadu. Zgłoś operatorowi dokładny stan (plik zapisany pod jaką nazwą/linkiem, wiersz w arkuszu — brak) i poproś o decyzję.

## No delete

Nie usuwaj:
- wierszy z `dokumentacja_surowce`,
- plików z folderu archiwum.

Ten skill nie ma operacji "usuń dokument". Jeśli operator prosi o usunięcie, powiedz, że to wymaga ręcznej interwencji poza tym skillem.

## Brak pola na operatora

Schemat `dokumentacja_surowce` (A:H) nie ma kolumny na osobę wykonującą zapis. Nie dopisuj własnej kolumny ani nie zapisuj tożsamości operatora w istniejących polach (`notes`-podobnego pola tu nie ma). Jeśli to problem dla Daniela, to zmiana schematu do osobnej decyzji, nie coś do obejścia przez ten skill.
