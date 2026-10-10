# Zasoby projektu

## Source of truth

### Baza dokumentacji jakościowej dostaw
- Nazwa: `dokumentacja_surowce`
- Spreadsheet ID: `11caP8XxVKVO2tzEH4UFl1VJihX_rcyGYGxiBJev0Ak0`
- Tab: GID `0`

### Baza dostaw (do wyszukania pozycji dostawy)
- Spreadsheet ID: `1N07AWra-pFjcKPPoirZPVK8O1F-iwuzJYmJq9uYZ088`
- Tab pozycji surowców: `dostawy_surowce`, GID `871950676`
- Tab nagłówków dostaw: `dostawy_master`
- Pełna struktura: `delivery/STRUCTURE.md` w repo (moduł `delivery/`)

### Baza surowców (do rozpoznania nazwy surowca)
- Spreadsheet ID: `1jUSESWqYJapu5BrrKMdRk5CMR2cEOXChYKBmtOIsR3A`
- Tab: `BD_surowce`
- Klucz: `_id` / `surowiec_id`, np. `SUR__001` — ta sama pula ID co `raw_material_id` w skillu `raw-material-documents`

### Drive
- Folder archiwum dokumentów jakościowych dostaw: `1rgo4UHMiwhDasq2j7fohcls3qIOw9ipx`

### Config (opcjonalnie, do potwierdzenia lokalizacji)
- `12GVEiCpFaL9XJCJjXcXXwNyHGomDdDyzHChaDC7aHE4`, arkusz `config`, wiersz 53 (`F53`=ssId, `H53`=GID `dokumentacja_surowce`), wiersz 55 (lokalizacja mastera dostaw)

## Inne systemy piszące do tej samej tabeli

- **n8n workflow `rlQMTUIDAtHlwiAn`** (`Get drive quality documents, interpret, input to sheets`) — mail z PDF-em na `dostawy.opcjanatura@gmail.com` → AI dopasowuje dostawę → human-in-the-loop mailowy → upload + append. Dokumentacja: `/home/daniel/Claude_praca/n8n/Get drive quality documents, interpret, input to sheets/STATUS.md`.
- **AppSheet webhook `wJxjzMrb1IU0gSJu`** (`Quality Document Upload - AppSheets Webhook`) — bezpośredni upload z formularza AppSheet.
- **`delivery/splitDelivery`** — nie tworzy nowych wierszy, tylko przepina `id_dostawy` (kol. C) przy splicie dostawy, dopasowując po `id_surowiec_local` (kol. D).

Ten skill jest czwartym punktem styku z tą tabelą (trzecim punktem *zapisu* obok n8n i AppSheet). Format zapisu (kolumny, konwencja nazwy pliku, metadata properties) musi być identyczny z tym, co robią tamte dwa kanały — patrz `references/schema.md`.

## Granica z `raw-material-documents`

Osobny skill, osobny arkusz (`BD_surowiec_dokumenty`, `1jPGq47sgSVsBRpcB_WGzIIKO2gC9dGdWjBd13BoRIaQ`). Dokument stały surowca (SDS, certyfikat pochodzenia, deklaracja alergenów, IFRA, inne) → tamten skill. Dokument jakościowy konkretnej dostawy → ten skill. Patrz `SKILL.md`, „Granica z raw-material-documents”.
