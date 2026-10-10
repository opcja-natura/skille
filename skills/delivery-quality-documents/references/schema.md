# Schemat bazy

## Model

```text
BD_surowce (_id / surowiec_id, SUR__nnn)
    |
    v
dostawy_master (_id_dostawy)
    |
    v
dostawy_surowce (pozycja, _id_local w kol. M)
    |
    v  match po _id_local
dokumentacja_surowce (dokument jakościowy tej pozycji)
```

Nie joinuj po nazwach. Klucz dopasowania dokumentu do pozycji dostawy to zawsze `_id_local` / `id_surowiec_local`.

## `dostawy_surowce` (źródło pozycji dostaw)

Spreadsheet dostaw: `1N07AWra-pFjcKPPoirZPVK8O1F-iwuzJYmJq9uYZ088`, tab `dostawy_surowce` (GID `871950676`). Kolumny A:M:

| Kol | Pole | Uwaga |
|---|---|---|
| A | `_id_dostawy` | FK → `dostawy_master` |
| B | `data_przyjecia` | puste = pozycja jeszcze nie przyjęta |
| C | `surowiec_nazwa` | |
| D | `surowiec_id` | formuła; ARRAYFORMULA, **nie edytuj** |
| E | `surowiec_dostawca` | formuła; ARRAYFORMULA, **nie edytuj** |
| F | `surowiec_iloscFv_gramy` | |
| G | `surowiec_IloscRealna_gramy` | |
| H | `surowiec_wartosc_netto` | |
| I | `surowiec_cenaRalnaGram_netto` | formuła |
| J | `surowiec_data_waznosci` | |
| K | `surowiec_wewnetrzne_oznaczenie` | formuła |
| L | `przyjmujacy` | |
| M | `_id_local` | **klucz dopasowania dokumentacji** — globalnie unikalny per pozycja |

Ten skill tylko **czyta** `dostawy_surowce` (żeby znaleźć `_id_dostawy` + `_id_local` właściwej pozycji). Nigdy tu nie zapisuje.

## `dostawy_master` (kontekst dostawy)

Ten sam spreadsheet, tab `dostawy_master`. Kolumny istotne dla tego skilla:

| Kol | Pole |
|---|---|
| A | `_id_dostawy` |
| B | `data_zamowienia` |
| F | `dostawca` |
| K | `dostawa_przyjeta` (TRUE/FALSE) |

Używaj do pokazania operatorowi kontekstu (dostawca, data) przy wyborze kandydata i w podsumowaniu preflight.

## `dokumentacja_surowce` (source of truth tego skilla)

Spreadsheet `11caP8XxVKVO2tzEH4UFl1VJihX_rcyGYGxiBJev0Ak0`, tab GID `0`. Jeden wiersz = jeden dokument podpięty do pary (surowiec, dostawa). Nagłówek w wierszu 1, dane od 2. Kolumny A:H:

| Kol | Pole | Uwaga |
|---|---|---|
| A | `surowiec_id` | np. `SUR__016` — równe `surowiec_id` (kol. D) w `dostawy_surowce`, ta sama pula co `raw_material_id` w skillu `raw-material-documents` |
| B | `surowiec_name` | |
| C | `id_dostawy` | uwaga: `delivery/splitDelivery` przepina tę kolumnę przy splicie dostawy — nie traktuj jej jako niezmiennej |
| D | `id_surowiec_local` | = `_id_local` pozycji (kol. M `dostawy_surowce`) — **klucz dopasowania**; bywa puste w starych wpisach |
| E | `dokumentacja_name` | nazwa pliku w Drive, konwencja `<surowiec_id>__<nazwa_bez_rozszerzenia>__<id_dostawy>` |
| F | `dokumentacja_link` | link do pliku w Drive (`webViewLink`) |
| G | `time` | timestamp zapisu |
| H | `confidence` | dla wpisów z automatycznego dopasowania AI (n8n) liczba 0–1; dla wpisów z tego skilla (operator jawnie potwierdził dopasowanie w rozmowie) wpisz `1` |

Brak PK — to płaski log, nie relacyjna tabela z generowanymi ID. Nie generuj `document_id` ani żadnego innego sztucznego ID dla wiersza; jedyne ID w grze to już istniejące `surowiec_id`, `id_dostawy`, `id_surowiec_local`.

Brak kolumny na operatora/e-mail wykonującego zapis. Nie dopisuj własnej kolumny do tej tabeli — jeśli operator chce być identyfikowalny, to osobna decyzja projektowa dla właściciela arkusza, nie coś do rozwiązania ad hoc przez ten skill.

## Drive — folder archiwum

Folder: `1rgo4UHMiwhDasq2j7fohcls3qIOw9ipx` (ten sam co używa n8n workflow).

Metadata properties pliku (Drive custom properties), tak jak w n8n: `surowiec_id`, `id_dostawy`, `surowiec_name`.
