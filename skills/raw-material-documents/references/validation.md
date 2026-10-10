# Walidacja i bezpieczeństwo

## Przed każdą mutacją

- Odczytaj stan live z source of truth, nie polegaj wyłącznie na wcześniejszym wyniku w rozmowie.
- Sprawdź istnienie wszystkich FK.
- Sprawdź status obiektów.
- Sprawdź relację surowiec-dokument.
- Sprawdź, że dokument będzie miał co najmniej jeden `type_id` i co najmniej jeden `area_id` ze słowników (patrz niżej).
- Sprawdź duplikaty.
- Sprawdź dostęp do pliku.
- Sprawdź, czy wymagane dane są kompletne.


## Słowniki i tabele linkujące — obowiązkowe dla każdego dokumentu

`BD_document_types` i `BD_document_areas` są jedynym źródłem prawdy o dopuszczalnych typach i obszarach. Reguły:

- każdy dokument logiczny ma **co najmniej jeden** wiersz w `link_document_type` i **co najmniej jeden** w `link_document_area` — brak któregokolwiek to błąd kompletności, nie „opcja pominięta”,
- przed zapisem odczytaj oba słowniki live i dopasuj po `type_id` / `area_id`; nigdy nie wpisuj kodu ani nazwy do tabeli linkującej, nigdy nie konstruuj ID z kodu, nigdy nie dopisuj pozycji do słownika bez osobnej decyzji operatora,
- jeśli operator nie podał obszaru, zaproponuj go (na podstawie typu i treści dokumentu) i pokaż w preflight; zapis dopiero po potwierdzeniu,
- jeśli żadna pozycja słownika nie pasuje — zatrzymaj się i zapytaj, nie zapisuj dokumentu bez linku,
- po zapisie read-back obu tabel linkujących należy do obowiązkowego zestawu (razem z `is_current`).

Zaobserwowany błąd (2026-09-17): dokumenty zapisywane bez `link_document_area`, bo obszar był opisany jako opcjonalny. Skutek: pusty „Obszar” w widoku operacyjnym i dokument niewidoczny dla filtrów po obszarze. Diagnostyka (workflow 6) ma to wykrywać.

## `BD_document_versions.is_current` — kolumna tylko do odczytu

Kolumna K (`is_current`) jest zarządzana przez istniejącą `ARRAYFORMULA`.

- Nigdy nie zapisuj, nie czyść, nie nadpisuj ani nie wstawiaj wartości/formuł do K.
- Przy tworzeniu wersji zapisuj tylko A:J.
- Nie używaj bezpośredniego append-row / `appendCells` dla `BD_document_versions`, jeżeli mechanizm append wyznacza koniec tabeli na podstawie całej siatki: rozlana formuła w K może spowodować zapis na końcu arkusza.
- Wyznacz pierwszy wolny fizyczny wiersz na podstawie kolumny A (`version_id`) i zapisz A:J w tym wierszu.
- Po zapisie odczytaj K i zweryfikuj wynik `is_current`; dla nowej najwyższej wersji oczekuj `TRUE`.

## Klucz dopasowania i decyzja o archiwizacji

Klucz dopasowania „czy to nowy dokument, czy nowa wersja” to wyłącznie `(raw_material_id, type_id)`. `area_id` i `supplier_name` do niego nie należą — patrz `workflows.md`, workflow 2.

Przed dodaniem pliku policz aktywne dokumenty pasujące do klucza:

- 0 -> nowy dokument, bez pytania o archiwizację.
- 1 -> nowa wersja istniejącego dokumentu; zapytaj o archiwizację starej wersji, domyślnie **TAK**.
- 2+ -> pokaż wszystkich kandydatów operatorowi (z `supplier_name`); zapytaj, którego dotyczy zmiana; domyślnie **NIE** archiwizuj automatycznie, dopóki operator jawnie nie wskaże dokumentu.

## Duplikat pliku

Dla tego samego `document_id` nie twórz nowej wersji, jeśli nowy plik jest tym samym PDF-em co istniejąca wersja.

Preferowane sprawdzenia w kolejności możliwości narzędzia:

1. ten sam Drive file ID / ten sam approved file,
2. identyczny hash zawartości PDF, jeśli narzędzie pozwala pobrać bytes,
3. jeśli nie można wiarygodnie porównać zawartości, przynajmniej zablokuj identyczny source file ID i poinformuj o ograniczeniu.

Nie używaj samej nazwy pliku jako dowodu identyczności.

## PDF-only i zasada kopii

Nowa wersja zatwierdzona przez system ma być **osobnym** zarządzanym PDF-em w folderze aktywnym `dokumenty/`. Jeśli źródło jest Google Doc/Sheet/Slide lub formatem możliwym do eksportu, eksportuj do PDF. Jeśli nie można uzyskać poprawnego PDF-u, przerwij operację.

Nazwa zarządzanego PDF:

```text
<raw_material_id>__<version_name>.pdf
```

Skąd bierze się ten plik (pełna tabela: `workflows.md` §0):

- operator podał **link z Google Drive** → **kopia** do `dokumenty/`; oryginał zostaje tam, gdzie był, pod swoją nazwą, nietknięty (nie `move`, nie rename, nie delete),
- operator **załączył plik w rozmowie** → **upload** oryginału do `dokumenty/` pod nazwą zarządzaną,
- w żadnym przypadku `approved_file_url` **nie wskazuje pliku poza `dokumenty/`** ani pliku o niezarządzanej nazwie. Przed read-back sprawdź, że plik z `approved_file_url` ma rodzica `1xL1m7jSD-R9ZFrzSDqZqX1hlvwxsJidP` i nazwę równą `<raw_material_id>__<version_name>.pdf`; jeśli nie — operacja nie jest zakończona.

Diagnostyka (workflow 6) sprawdza to samo dla wszystkich istniejących wersji.

## Archiwizacja plików

### Nowa wersja

1. Utwórz nowy PDF w aktywnym folderze.
2. Zapisz wersję i wykonaj read-back.
3. Dopiero po potwierdzeniu operatora (patrz „Klucz dopasowania i decyzja o archiwizacji”) przenieś poprzedni current PDF do `_archive`.
4. Jeśli przeniesienie starego PDF nie powiedzie się, zgłoś błąd i nie zmieniaj statusu poprzedniego dokumentu/wersji, dopóki stan nie będzie spójny.

### Archiwizacja dokumentu

1. Przenieś current PDF do `_archive`.
2. Dopiero potem ustaw dokument `archived`.

## Kolejność przy nowej wersji

Dozwolona:

```text
walidacja -> nowy PDF -> nowy rekord wersji -> read-back -> (jeśli potwierdzone) archiwizacja starego PDF -> read-back
```

Niedozwolona:

```text
archiwizacja starego PDF -> próba stworzenia wersji
```

## No delete

Nie usuwaj:
- dokumentów logicznych,
- wersji,
- linków historycznych,
- plików zatwierdzonych.

Archiwizuj zamiast usuwać.

## valid_until

Kolumna pozostaje w bazie dla zgodności z historią. Nowy workflow nie obsługuje tego pola:

- nie pytaj operatora,
- nie używaj do decyzji,
- przy nowych rekordach wersji wpisuj pustą wartość.

## Owner i pola osobowe

- nowy dokument: `owner = operator`,
- nowa wersja: `approved_by = operator`,
- nigdy nie wpisuj AI jako osoby.
