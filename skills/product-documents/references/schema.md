# Schemat bazy

## Model

```text
DB_products_internal
  sercet_id (= product_id)
    |
    v
link_product_document
    |
    v
BD_documents
    |-- BD_document_versions
    |-- BD_document_change_requests
    |-- link_document_type --> BD_document_types
    `-- link_document_area --> BD_document_areas
```

Nie joinuj po nazwach. Używaj ID. Kolumny typu `document_name`/`type_name`/`area_name`/`product_name` w tabelach relacyjnych bywają same formułami `XLOOKUP`/`VLOOKUP` — patrz niżej.

## Kolumny chronione `ARRAYFORMULA` — czytaj to PRZED jakimkolwiek zapisem do tabel relacyjnych

`link_document_type`, `link_document_area` (workbook `BD_documents`) i `link_product_document` (workbook `BD_produkty`) mają po jednej-dwie kolumny wypełniane **jedną, rozlaną `ARRAYFORMULA`** zakotwiczoną w wierszu 2, liczącą wartość dla wszystkich wierszy w dół naraz (nie osobną formułą per wiersz).

**Zapisanie do takiej kolumny czegokolwiek — łącznie z pustym stringiem `""` — blokuje dalsze rozlewanie się formuły dla wszystkich kolejnych wierszy.** To nie jest teoretyczne ryzyko: zweryfikowany, realny sposób, w jaki tego typu tabele w tym systemie się psują. Zablokowanie nie daje widocznego błędu w wyświetlanej wartości — pusta komórka wygląda identycznie, czy jest zdrowym wynikiem formuły, czy zablokowanym literałem. Jedyny pewny sposób odróżnienia: odczyt na poziomie API z polem `userEnteredValue` — w zdrowej kolumnie występuje wyłącznie w komórce-kotwicy (np. `C2`), nigdzie indziej.

**Zasada bezwzględna**: przy dopisywaniu wiersza do którejkolwiek z tych trzech tabel, zakres zapisu **w ogóle nie obejmuje** kolumny formułowej — nie zapisuje się tam pustego stringa "dla kompletności wiersza", tylko pomija się tę kolumnę całkowicie w wywołaniu zapisu (np. zapisz `A2:B2` + `D2`, nie `A2:E2`). Dokładny, bezpieczny zakres zapisu dla każdej tabeli — patrz sekcje niżej i `references/workflows.md`.

## BD_documents

Kolumny A:H:

1. `document_id` — `DOC_NN` (obecnie 2 cyfry, do `DOC_46`; po przekroczeniu 99 przejdź na 3 cyfry)
2. `name` — konwencja `<TYP> — <nazwa produktu>`
3. `language` — `PL` / `EN`
4. `market` — np. `EU`, pole informacyjne
5. `owner` — e-mail
6. `folder_url` — folder Drive dokumentu: `typ_<TYP>/` dla nowych dokumentów nie-PIF, `_PL_`/`_EN_` dla PIF (patrz `project-resources.md`)
7. `status` — `active` / `archived`
8. `notes`

Nie ma tu kolumny na "aktualną wersję" — to zawsze `MAX(version_no)` z `BD_document_versions` dla danego `document_id`.

## BD_document_versions

Kolumny A:H:

1. `version_id` — `VER_000nnn`, globalny licznik (nie per-dokument), 6 cyfr, do `VER_000047`
2. `document_id`
3. `version_no` — liczba całkowita, **wartość statyczna zapisana przy tworzeniu rekordu**, nie formuła — nie zakładaj, że przeliczy się sama
4. `version_name` — `<document_id>_v<NN zero-padded do 2 cyfr>_<YYYY-MM-DD>`
5. `source_url` — **opcjonalne, wyłącznie informacyjne**: niezmieniona kopia oryginalnego pliku wejściowego (dowolny format), ustawiana TYLKO gdy to wejście nie było już PDF-em. Jeśli wejściem był bezpośrednio PDF, kolumna zostaje pusta — to poprawny stan, nie brak danych. Nigdy nie jest edytowana po zapisaniu i nigdy nie musi być natywnym Google Doc — nie twórz takiego dokumentu specjalnie w tym celu (zaobserwowany błąd 2026-09-16: konwersja gotowego PDF-a na DOCX pod błędnym założeniem, że `source_url` musi być edytowalny).
6. `pdf_url` — **wymagane zawsze**: zamrożony PDF na Drive — kopia 1:1 (jeśli wejście już było PDF-em) albo wynik konwersji (jeśli nie było)
7. `approved_at` — data
8. `approved_by` — e-mail operatora zatwierdzającego

**Brak** kolumny `is_current` (w odróżnieniu od `raw-material-documents`) i **brak** `valid_until`. Nie próbuj ich ustawiać ani szukać.

Aktualna wersja = `MAX(version_no)` per `document_id`.

## BD_document_change_requests

Kolumny A:K:

1. `request_id` — `DOCCR_` + 8 znaków hex, np. `DOCCR_07af04fe`
2. `document_id`
3. `product_id` — opcjonalne (FK → `DB_products_internal.sercet_id`)
4. `requested_at`
5. `requested_by` — e-mail
6. `request` — co zmienić
7. `reason` — dlaczego
8. `owner` — kto odpowiada za rozliczenie
9. `status` — `open` / `implemented` / `rejected`
10. **`implemented_in_version_id`** — FK → `BD_document_versions.version_id`, puste przy `open`/`rejected`. **UWAGA**: Google Doc README nazywa to pole `target_version_id` — to nieaktualna nazwa, żywy nagłówek arkusza (zweryfikowany 2026-09-15) to `implemented_in_version_id`. Używaj nazwy z arkusza.
11. `closed_at`

Stan live 2026-09-15: jeden rekord, testowy (`DOCCR_07af04fe`). Nie traktuj tego jako reprezentatywnej próbki formatu `request`/`reason` — to był test, nie realne zgłoszenie.

## link_document_type

1. `link_id` — **wzorzec `LDT_<CODE_TYPU>_NN`** (np. `LDT_PIF_01`, `LDT_PIF_02`) — licznik jest per-typ, nie globalny. Przy generowaniu kolejnego ID policz istniejące ID z tym samym prefiksem kodu typu.
2. `document_id`
3. `document_name` — **formuła** `XLOOKUP(document_id, BD_documents!A:A, BD_documents!B:B)`, rozlana z komórki C2 (`ARRAYFORMULA`). **Nigdy nie zapisuj tu żadnej wartości, także pustego stringa.**
4. `type_id`
5. `type_name` — **formuła** `XLOOKUP(type_id, BD_document_types!A:A, BD_document_types!C:C)`, analogicznie zakotwiczona w E2. **Nigdy nie zapisuj tu żadnej wartości.**

**Zapis nowego wiersza: tylko kolumny A, B, D.** Kolumny C i E pomijasz całkowicie w zapisie.

## link_document_area

1. `link_id` — **wzorzec `LDA_NN`**, globalny licznik (bez segmentu kodu obszaru — inaczej niż `link_document_type`)
2. `document_id`
3. `document_name` — **formuła**, jak wyżej. **Nigdy nie zapisuj.**
4. `area_id`
5. `area_name` — **formuła**, jak wyżej. **Nigdy nie zapisuj.**

`area_id` jest wyłącznie klasyfikacją prezentacyjną (filtr `per_dzial`). Nie jest częścią żadnego klucza dopasowania.

**Zapis nowego wiersza: tylko kolumny A, B, D.** Kolumny C i E pomijasz całkowicie w zapisie.

## BD_document_types

Słownik. Odczytuj live przed każdym użyciem `type_id`. Stan 2026-09-15 (13 wierszy, pełny):

| type_id | code | name |
|---|---|---|
| `DT_PIF` | `PIF` | PIF |
| `DT_SDS` | `SDS` | Karta charakterystyki (SDS) |
| `DT_ROB` | `ROB` | ROB |
| `DT_PRODUCT_MARKETING_CARD` | `PRODUCT_MARKETING_CARD` | Karta opisowa marketingowa |
| `DT_QUALITY_SPEC` | `QUALITY_SPEC` | Specyfikacja jakościowa |
| `DT_TECH_CARD` | `TECH_CARD` | Karta technologiczna |
| `DT_INSTRUCTION` | `INSTRUCTION` | Instrukcja |
| `DT_REGULATORY` | `REGULATORY` | Dokument regulacyjny |
| `DT_OTHER` | `OTHER` | Inny dokument |
| `DT_DERMATOLOGICAL_TEST` | `DERMATOLOGICAL_TEST` | Badanie dermatologiczne |
| `DT_INSTRUMENTAL_TEST` | `INSTRUMENTAL_TEST` | Badanie aparaturowe |
| `DT_CONSUMER_TEST` | `CONSUMER_TEST` | Badanie konsumenckie |
| `DT_NATURAL_ORIGIN_INDEX` | `NATURAL_ORIGIN_INDEX` | Indeks pochodzenia naturalnego |

Nie konstruuj `type_id` z kodu — odczytaj właściwy rekord z tabeli.

## BD_document_areas

Słownik. Stan 2026-09-15 (8 wierszy, pełny):

| area_id | code | name |
|---|---|---|
| `AREA_SALES` | `SALES` | Sprzedaż |
| `AREA_EXPORT` | `EXPORT` | Eksport |
| `AREA_PRODUCTION` | `PRODUCTION` | Produkcja |
| `AREA_QUALITY` | `QUALITY` | Jakość |
| `AREA_RND` | `RND` | R&D / Rozwój produktu |
| `AREA_REGULATORY` | `REGULATORY` | Regulacje / Dokumentacja |
| `AREA_MARKETING` | `MARKETING` | Marketing |
| `AREA_LOGISTICS` | `LOGISTICS` | Logistyka |

Nie konstruuj `area_id` z kodu — odczytaj właściwy rekord z tabeli.

## DB_products_internal (w BD_produkty)

Kolumny istotne:

1. `sercet_id` — literówka w nagłówku, semantycznie **`product_id`**. Stabilny klucz produktu (np. `616fce762e22f6789aafdb6f`)
4. `name` — nazwa produktu

Nie poprawiaj literówki `sercet_id` samodzielnie — inne miejsca w systemie odwołują się do niej po tej dokładnej nazwie kolumny.

## link_product_document (w BD_produkty)

1. `link_id` — wzorzec `LINK_NNNN` (4 cyfry, zero-padded), globalny licznik
2. `product_id` — FK → `DB_products_internal.sercet_id`
3. `product_name` — **formuła** `ARRAYFORMULA(IF(B2:B="","",IFERROR(VLOOKUP(B2:B,DB_products_internal!A:D,4,0),"")))`, rozlana z komórki C2. **Nigdy nie zapisuj tu żadnej wartości, także pustego stringa** — dokładnie ten sam mechanizm i to samo ryzyko co `document_name`/`type_name`/`area_name` w `link_document_type`/`link_document_area` wyżej. (Wcześniejsza wersja tej dokumentacji błędnie opisywała tę kolumnę jako zwykłe pole pomocnicze — poprawione 2026-09-15.)
4. `document_id` — FK → `BD_documents`
5. `document_name` — zwykła (nieformułowa) kolumna, obecnie nieużywana — w próbce danych live pusta dla wszystkich sprawdzonych wierszy. W odróżnieniu od C nie ma tu ryzyka blokady, ale i tak nie ma potrzeby jej wypełniać.
6. `required` — TRUE/FALSE

**Zapis nowego wiersza: tylko kolumny A, B, D, F.** Kolumnę C pomijasz całkowicie w zapisie (nigdy jej nie dotykaj); kolumnę E możesz pominąć (nieużywana).

Relacja zawsze wskazuje `document_id`, nigdy `version_id`.

## Generowanie ID

Dla liczników numerycznych (`BD_documents`, `BD_document_versions`, `link_document_area`, `link_product_document`, oraz per-typ dla `link_document_type`):

1. Odczytaj wszystkie istniejące ID danej tabeli (dla `link_document_type` — tylko ID z tym samym prefiksem kodu typu).
2. Wybierz największą numeryczną końcówkę.
3. Dodaj 1.
4. Zachowaj dotychczasową liczbę cyfr (zero-padding); po przekroczeniu pojemności zwiększ liczbę cyfr.

Dla `request_id` (`DOCCR_` + 8 znaków hex): wygeneruj losowy, nie sekwencyjny, hex string — sprawdź tylko, że nie koliduje z istniejącym.

Nie generuj ID na podstawie liczby wierszy — mogą być puste wiersze pośrodku.

Prefiksy:

- `DOC_`
- `VER_000`
- `DOCCR_`
- `LDT_<CODE>_`
- `LDA_`
- `LINK_`
