# Schemat zapisu

## Model

```text
dostawy_master (1 wiersz = 1 zamówienie, nowy _id_dostawy)
    |
    +--> dostawy_eksploatacyjne (0..N wierszy, ten sam _id_dostawy, własny _id_local)
    +--> dostawy_pozostale      (0..N wierszy, ten sam _id_dostawy, własny _id_local)
```

Jedno zamówienie może mieć pozycje wyłącznie jednego rodzaju na raz (jeśli operator zamawia jednocześnie coś z `eksploatacyjne` i coś z `pozostale`, to są **dwa osobne zamówienia** — dwa różne `_id_dostawy`, bo `dostawa_rodzaj` żyje na poziomie `dostawy_master`, nie pozycji). Zapytaj operatora, żeby to rozdzielić, jeśli poda mieszankę.

## `dostawy_master` — kolumny A:T

| Kol | Pole | Zapisuj przy tworzeniu? | Wartość |
|---|---|---|---|
| A | `_id_dostawy` | tak | nowo wygenerowane, patrz `references/validation.md` |
| B | `data_zamowienia` | tak | dziś, chyba że operator poda inną datę |
| C | `wymagany_odbior` | tak | **zapytaj zawsze** operatora wprost („czy wymagany jest odbiór?"); `TRUE` jeśli tak, `FALSE` jeśli nie — nie zgaduj i nie pomijaj pytania |
| D | `podmiot` | tak | zawsze `spZoo` — **nie pytaj o to operatora**, firma ma też `jdg` w słowniku, ale ten skill zapisuje wyłącznie `spZoo` |
| E | `dostawa_rodzaj` | tak | wyłącznie `eksploatacyjne` lub `pozostale` (patrz `SKILL.md`) |
| F | `dostawca` | tak | tekst; sprawdź względem `dostawcy_range`, patrz `references/validation.md` |
| G | `zamawiajacy` | tak | e-mail operatora |
| H | *(puste)* | **nie** | zawsze pusta w danych źródłowych — nie pisz tu nic |
| I | `sposob_platnosci` | tak | **zapytaj zawsze** operatora, jedna z `sposobPlatnosci_range` |
| J | *(puste)* | **nie** | jw. |
| K | `dostawa_przyjeta` | **NIGDY** | **ARRAYFORMULA** — potwierdzona odczytem formuł z XLSX (2026-09-02): `VLOOKUP` po `_id_dostawy` względem `BD_fakturyKosztowe!Invoices` (import przez `config` wiersz 56). Liczy się automatycznie, gdy tylko wiersz ma wypełnioną kolumnę A — **nie wpisuj tu nic, nawet `FALSE`.** |
| L | *(puste)* | **nie** | jw. |
| M | `komentarz_zamawiajacego` | opcjonalnie | wolny tekst z rozmowy, jeśli coś istotnego padło |
| N | *(puste)* | **nie** | jw. |
| O | `fv_nazwa_pliku` | **nie** | uzupełnia się przy fakturze, poza tym skillem |
| P | `platnosc_data` | **warunkowo** | **zapytaj zawsze** „czy dostawa jest już opłacona?"; jeśli tak — zapytaj o datę i zapisz ją tutaj; jeśli nie — zostaw puste. Zwykła wartość (data), **nie** formuła — bezpieczna do zapisu (potwierdzone: literały dat w danych źródłowych). |
| Q | `inovice_url` | **NIGDY** | **ARRAYFORMULA** — potwierdzona odczytem formuł z XLSX (2026-09-02, ta sama rodzina co K/T, import z `BD_fakturyKosztowe`). Nieudokumentowana wcześniej. (literówka `inovice` jest celowa — istnieje w danych/formule) |
| R | `data_transferu` | **nie** | ustawia wyłącznie `pushToInventory` przy przyjęciu |
| S | `wartość dostawy` | **nie** | formuła |
| T | `invoice_net_value` | **NIGDY** | **ARRAYFORMULA** — potwierdzona odczytem formuł z XLSX (2026-09-02), ta sama rodzina co K/Q. Nieudokumentowana wcześniej. |

## `dostawy_eksploatacyjne` — kolumny A:J

Spreadsheet dostaw, ten sam co `dostawy_master`.

| Kol | Pole | Zapisuj? | Uwaga |
|---|---|---|---|
| A | `_id_dostawy` | tak | = ID z `dostawy_master` tego zamówienia |
| B | `data_przyjecia` | **nie** | puste = jeszcze nie przyjęta |
| C | `eksplo_nazwa` | tak | patrz krok dopasowania do `BD_materials` w `references/workflows.md` |
| D | `eksplo_id` | **NIGDY** | **ARRAYFORMULA** — `VLOOKUP` po `eksplo_nazwa` względem `BD_materials.short_name` (import przez `config` wiersz 10). Zapis tu łamie formułę dla tego wiersza. |
| E | `explo_dostawca` | **NIGDY** | **ARRAYFORMULA** — pochodna, prawdopodobnie po dostawcy z tego zamówienia względem `BD_suppliers` (import przez `config` wiersz 11). Zapis tu łamie formułę dla tego wiersza. |
| F | `eksplo_ilosc_szt` | tak | ilość zamówiona |
| G | `eksplo_cena_netto` | jeśli znana | inaczej puste — uzupełni się z faktury |
| H | `komentarz_przyjmujacego` | **nie** | wypełnia się przy fizycznym przyjęciu |
| I | `przyjmujacy` | **nie** | jw. |
| J | `_id_local` | tak | nowo wygenerowane, unikalne per pozycja |

**Kolumny D i E są potwierdzone jako ARRAYFORMULA przez odczyt formuł z eksportu XLSX (2026-09-02)** — `delivery/STRUCTURE.md` w repo tego wcześniej nie dokumentował dla `dostawy_eksploatacyjne` (dokumentował tylko dla `surowce`/`opakowanie`). Traktuj to jako obowiązującą, zweryfikowaną wiedzę, nie hipotezę.

## `dostawy_pozostale` — kolumny A:H

| Kol | Pole | Zapisuj? | Uwaga |
|---|---|---|---|
| A | `_id_dostawy` | tak | = ID z `dostawy_master` |
| B | `data_przyjecia` | **nie** | puste = jeszcze nie przyjęta |
| C | `pozostale_nazwa` | tak | wolny tekst, bez słownika/FK |
| D | `ilosc` | tak | ilość zamówiona |
| E | `cena_netto` | jeśli znana | inaczej puste |
| F | `komentarz_przyjmujacego` | **nie** | wypełnia się przy przyjęciu |
| G | `przyjmujacy` | **nie** | jw. |
| H | `_id_local` | tak | nowo wygenerowane |

Brak kolumn formułowych w tej zakładce — potwierdzone odczytem XLSX (2026-09-02), same literały w istniejących danych.

## Zakres do zapisu — podsumowanie

- `dostawy_master`: pisz **A, B, C, D, E, F, G, I, (M), (P)**. Nigdy H, J, **K**, L, N, O, **Q**, R, S, **T** (K/Q/T — ARRAYFORMULA, patrz wyżej).
- `dostawy_eksploatacyjne`: pisz **A, C, F, (G), J**. Nigdy B, D, E, H, I.
- `dostawy_pozostale`: pisz **A, C, D, (E), H**. Nigdy B, F, G.

(Pola w nawiasach — warunkowo: `M` jeśli operator coś istotnego powiedział, `P` jeśli dostawa jest już opłacona.)

## `dostawy_master` — zapis to append z pominięciem kolumn (nie ciągły zakres)

Tak samo jak `dostawy_eksploatacyjne`: arkusz `dostawy_master` ma formuły wpisane z góry aż do dużego numeru wiersza (obserwowane: do wiersza ~2044), więc appendowanie nowego wiersza w kolumnie A automatycznie "budzi" formuły K/Q/T dla tego wiersza — nie trzeba (i nie wolno) nic tam wpisywać. Zapisuj segmentami z pominięciem kolumn `[7, 9, 10, 11, 13, 14, 16, 17, 18, 19]` (0-based: H, J, K, L, N, O, Q, R, S, T), analogicznie do `setRowsSkippingCols` używanego przez webhooki tego modułu — nie jednym ciągłym zakresem A:T.
