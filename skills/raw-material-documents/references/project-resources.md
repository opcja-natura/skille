# Zasoby projektu

## Source of truth

### Baza dokumentów surowców
- Nazwa: `BD_surowiec_dokumenty`
- Spreadsheet ID: `1jPGq47sgSVsBRpcB_WGzIIKO2gC9dGdWjBd13BoRIaQ`
- URL: `https://docs.google.com/spreadsheets/d/1jPGq47sgSVsBRpcB_WGzIIKO2gC9dGdWjBd13BoRIaQ/edit`

Tabele:
- `BD_documents`
- `BD_document_versions`
- `BD_document_types`
- `BD_document_areas`
- `link_raw_material_document`
- `link_document_type`
- `link_document_area`

`BD_document_change_requests` pozostaje fizycznie w arkuszu jako nieużywana pozostałość po module Change Request (usunięty z modelu 2026-08-31). Nie czytaj ani nie zapisuj tej tabeli.

### Baza surowców
- Nazwa: `BD_produkcyjna`
- Spreadsheet ID: `1jUSESWqYJapu5BrrKMdRk5CMR2cEOXChYKBmtOIsR3A`
- Zakładka: `BD_surowce`
- Klucz surowca: `_id` / `raw_material_id`, np. `SUR__001`
- Nazwa: `name`

### Drive — dokumenty
- Folder aktywnych dokumentów (nazwa `dokumenty`): `1xL1m7jSD-R9ZFrzSDqZqX1hlvwxsJidP`
- Folder archiwum `_archive` (podfolder powyższego): `1ntRjgBusEJjDsg4p680do9otp8GnSMl4`

**Oba foldery leżą na Dysku współdzielonym** `[002] OpcjaNatura - dokumentacjaSurowcow` (`driveId` `0ANRTLuZYHCEpUk9PVA`), nie na „Moim dysku”. Wywołania Drive API bez `supportsAllDrives=true` (a przy listowaniu także `includeItemsFromAllDrives=true`) zwracają dla nich `404 File not found` — to nie znaczy, że foldery nie istnieją. Zweryfikowane 2026-09-17. Na tym samym Dysku leży folder `dokumentacja dostaw/` (surowe pliki od dostawców, m.in. `karty charakterystki olejki/`) — to **wejście**, nie miejsce zarządzane: pliki stamtąd kopiuje się do `dokumenty/` pod nazwą zarządzaną, nigdy nie linkuje bezpośrednio w `approved_file_url`.

## Warstwa operacyjna

- Arkusz: `arkusz_operacyjny_surowiec_dokumenty_v2`
- Spreadsheet ID: `1Sj-ec9hKyiaFbJluIp1aFIYZLnpoN1k65D7E3-H5FnY`

Skill nie powinien wymagać od operatora ręcznego klikania w tym arkuszu. AI ma wykonywać operacje bezpośrednio na źródłowych tabelach i Drive. Arkusz operacyjny może służyć do diagnostyki/podglądu, ale nie jest source of truth.

## Dokumentacja historyczna projektu

- `README_BD_surowiec_dokumenty.md`
- `INSTRUKCJA_AI_OPERATOR.md`

W razie konfliktu stosuj zasady zapisane w tym skillu jako nowszą wersję workflow: PDF-only, brak obsługi `valid_until`, brak Change Request, dopasowanie nowy dokument/nowa wersja wyłącznie po `(raw_material_id, type_id)`.

## Poza zakresem

Dokument jakościowy surowca (certyfikat jakości / specyfikacja jakościowa dostawy) nie jest obsługiwany przez ten skill. Żyje w zupełnie innym systemie: spreadsheet `11caP8XxVKVO2tzEH4UFl1VJihX_rcyGYGxiBJev0Ak0`, tab `dokumentacja_surowce`. Obsługuje go osobny skill **`delivery-quality-documents`** — przełącz się na niego, nie próbuj wykonać tej operacji tutaj.
