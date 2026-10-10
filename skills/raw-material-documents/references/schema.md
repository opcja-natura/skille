# Schemat bazy

## Model

```text
BD_surowce
  _id
    |
    v
link_raw_material_document
    |
    v
BD_documents
    |-- BD_document_versions
    |-- link_document_type --> BD_document_types
    `-- link_document_area --> BD_document_areas
```

Nie joinuj po nazwach. Używaj ID.

## BD_documents

Kolumny A:H:

1. `document_id` — `DOC_RM_nnn`
2. `name`
3. `language` — `PL`, `EN`, `N/A`
4. `issuer` — wystawca dokumentu; uzupełniaj, gdy możliwy do ustalenia. Gdy nie jest jednoznaczny, potwierdź z operatorem; często jest równy `supplier_name`, ale nie zakładaj tego bez potwierdzenia.
5. `supplier_name`
6. `owner`
7. `status` — `active` / `archived`
8. `notes`

## BD_document_versions

Kolumny A:K:

1. `version_id` — `VER_RM_nnn`
2. `document_id`
3. `version_no`
4. `version_name`
5. `approved_file_url`
6. `issued_at`
7. `valid_until` — pole historyczne; dla nowych operacji pozostaw puste
8. `approved_at`
9. `approved_by`
10. `notes`
11. `is_current` — wyliczane przez istniejącą `ARRAYFORMULA`; TRUE dla najwyższego `version_no`. Kolumna tylko do odczytu: zapis wersji obejmuje wyłącznie A:J.

Aktualna konwencja `version_name`:

```text
<document_id>_vNN_YYYY-MM-DD
```

Przykład:

```text
DOC_RM_004_v03_2026-08-28
```

## link_raw_material_document

1. `link_id` — `LRM_nnn`
2. `raw_material_id`
3. `document_id`
4. `required` — TRUE/FALSE

## link_document_type

1. `link_id` — `LDT_RM_nnn`
2. `document_id`
3. `type_id`

**Obowiązkowa: każdy dokument ma tu co najmniej jeden wiersz.** `type_id` wyłącznie ze słownika `BD_document_types` (SSOT), nigdy kod ani nazwa.

`(raw_material_id, type_id)` — dopasowany przez `link_raw_material_document` + `link_document_type` — jest jedynym kluczem, po którym rozstrzygamy „nowy dokument czy nowa wersja”. Patrz `workflows.md`.

## link_document_area

1. `link_id` — `LDA_RM_nnn`
2. `document_id`
3. `area_id`

**Obowiązkowa: każdy dokument ma tu co najmniej jeden wiersz** (od 2026-09-17; wcześniej błędnie opisywana jako opcjonalna, przez co część dokumentów nie miała obszaru). `area_id` wyłącznie ze słownika `BD_document_areas` (SSOT).

`area_id` służy do klasyfikacji/prezentacji (filtr „Obszar” w widoku operacyjnym). Nie jest częścią klucza dopasowania nowy-dokument-vs-nowa-wersja, ale jego brak jest błędem kompletności dokumentu.

## BD_document_types

Słownik, **SSOT dla typów** — odczytuj live przed każdym zapisem, nie dopisuj pozycji samodzielnie. Kolumny: `type_id`, `code`, `name`, `notes`, **`typ_surowca`**.

`typ_surowca` (kolumna E) mówi, **dla jakich surowców dany typ dokumentu obowiązuje**:

- `all` — dokument obowiązuje dla każdego surowca (stan live: SDS, certyfikat pochodzenia, deklaracja pochodzenia naturalnego),
- `essential_oil` — dokument obowiązuje tylko dla olejków eterycznych (stan live: deklaracja alergenów, IFRA),
- `n/d` — nie dotyczy, typ bez reguły obowiązywania (stan live: `OTHER`).

Używaj tego przy podglądzie i diagnostyce: dla surowca wylicz zestaw obowiązujących typów (`all` + `essential_oil`, jeśli surowec jest olejkiem eterycznym) i pokaż, których aktywnych dokumentów brakuje. Nie używaj `typ_surowca` do blokowania zapisu — operator może świadomie dodać dokument typu `essential_oil` innemu surowcowi, ale zaznacz to w preflight.

Jak rozpoznać olejek eteryczny: `BD_surowce` **nie ma** osobnego pola typu surowca. Rozpoznaj po nazwie (`Olejek eteryczny …`) i potwierdź z operatorem przy wątpliwości — nie zgaduj po samym `function`.

Znane kody (stan po przycięciu 2026-08-31, zweryfikowane live 2026-09-17, z `typ_surowca`):

| type_id | code | name | typ_surowca |
|---|---|---|---|
| `DT_SDS` | `SDS` | Karta charakterystyki (SDS) | `all` |
| `DT_ORIGIN_CERTIFICATE` | `ORIGIN_CERTIFICATE` | Certyfikat pochodzenia | `all` |
| `DT_ALLERGEN_STATEMENT` | `ALLERGEN_STATEMENT` | Deklaracja alergenów | `essential_oil` |
| `DT_NATURAL_ORIGIN` | `NATURAL_ORIGIN` | Deklaracja pochodzenia naturalnego | `all` |
| `DT_IFRA` | `IFRA` | Certyfikat / deklaracja IFRA | `essential_oil` |
| `DT_OTHER` | `OTHER` | Inny dokument | `n/d` |

Dokument jakościowy surowca (dawne `QUALITY_CERTIFICATE` / `QUALITY_SPEC`) nie jest już obsługiwany w tym skillu — patrz `SKILL.md`, „Poza zakresem”. Usunięto też `TDS`, `COA`, `GMO_STATEMENT`, `REACH` jako nieużywane.

Nie konstruuj `type_id` z kodu. Odczytaj właściwy `type_id` z tabeli.

## BD_document_areas

Słownik, **SSOT dla obszarów** — odczytuj live przed każdym zapisem, nie dopisuj pozycji samodzielnie. Kolumny: `area_id`, `code`, `name`, `notes`. Znane kody (zweryfikowane live 2026-09-17, 6 pozycji):

- `QUALITY`
- `PROCUREMENT`
- `RND`
- `DOCUMENTATION`
- `PRODUCTION`
- `LOGISTICS`

Nie konstruuj `area_id` z kodu. Odczytaj właściwy `area_id` z tabeli.

## Generowanie ID

Dla każdej tabeli:

1. Odczytaj wszystkie ID z odpowiedniej kolumny.
2. Wybierz największą numeryczną końcówkę dla danego prefiksu.
3. Dodaj 1.
4. Użyj minimum 3 cyfr; po 999 zwiększ długość.

Prefiksy:

- `DOC_RM_`
- `VER_RM_`
- `LRM_`
- `LDT_RM_`
- `LDA_RM_`
