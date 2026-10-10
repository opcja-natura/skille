# Zasoby projektu

## Source of truth

### Rejestr dostaw
- Spreadsheet ID: `1N07AWra-pFjcKPPoirZPVK8O1F-iwuzJYmJq9uYZ088`
- Tab nagłówków zamówień: `dostawy_master`
- Tab pozycji eksploatacyjnych: `dostawy_eksploatacyjne`
- Tab pozycji pozostałych: `dostawy_pozostale`
- Tab pozycji surowców: `dostawy_surowce` (**tylko do odczytu, jeśli w ogóle** — ten skill nie zapisuje tu nic, patrz `SKILL.md`, „Poza zakresem")
- Tab pozycji opakowań: `dostawy_opakowanie` (jw. — tylko odczyt/nigdy)
- Pełna struktura (referencyjna, working doc): `delivery/STRUCTURE.md` w repo `app-sheets`

### Słowniki dropdownów (ten sam spreadsheet, tab `named_ranges_helper`)

| Nazwany zakres | Zakres komórek | Zawartość |
|---|---|---|
| `dostawcy_range` | `D2:D1000` | lista dostawców do pola `dostawy_master.dostawca` — szeroka, wolny wybór (zawiera detalistów typu x-kom, allegro, jysk, komputronik) |
| `rodzaj_range` | `E2:E1000` | dozwolone wartości `dostawa_rodzaj`: `surowce`, `opakowanie`, `eksploatacyjne`, `pozostale` |
| `podmiot_range` | `F2:F3` | dokładnie 2 wartości: `spZoo`, `jdg` (dwa podmioty prawne firmy) |
| `sposobPlatnosci_range` | `G2:G1000` | `przelew`, `blik`, `karta`, `przedpłata` |

Kolumna A (`surowce`), B (`opakowania`), C (`eksploatacyjne`) w tym samym tabie to **osobne, ręcznie utrzymywane listy pomocnicze** — NIE są źródłem prawdy dla FK `eksplo_id`. Źródłem prawdy dla FK jest `BD_materials` (niżej). Nie myl tych dwóch list.

### Słownik materiałów eksploatacyjnych — `BD_materials` (źródło FK dla `eksplo_id`)
- Spreadsheet ID: `1jDPVlulMk5_Y82O5aygNjvcJ6K0lqWflxIgOR58wGrg` (nazwa pliku: `BD_opcja_natura`)
- Tab: `BD_materials`
- Referencja w konfiguracji rejestru dostaw: tab `config` arkusza dostaw, wiersz 10 (kolumna zawierająca URL, kolumna `D`=sheetName, kolumna `F`=spreadsheet_id — ten `config` to lokalny rejestr innych arkuszy, NIE centralny `masterConfig` ERP)
- Kolumny: `_id` (`EXPL_nnn`), `short_name` (**klucz dopasowania** — dokładnie ta wartość musi trafić do `eksplo_nazwa`, żeby ARRAYFORMULA w `dostawy_eksploatacyjne!D` zwróciła poprawny `_id`), `dimmensions/notel`, `url`, `supplier_1`, `supplier_2`, `konto na sklepie`.

### Słownik dostawców strukturalnych — `BD_suppliers` (źródło FK dla `explo_dostawca`)
- Ten sam spreadsheet co `BD_materials` (`1jDPVlulMk5_Y82O5aygNjvcJ6K0lqWflxIgOR58wGrg`), tab `BD_suppliers`
- Referencja: tab `config` arkusza dostaw, wiersz 11
- Kolumny: `_id` (`DST_nnn`), `short_name`, `supplier_type` (`surowce`/`opakowania`/`eksploatacyjne`/`pozostale` — pisownia w danych bywa niespójna, np. `surowcce`, `exploatacyjne`), `biling_name`, `website`, `contact_mail`, `conctact_phone`.
- **Mała, skratowana lista (~33 wiersze)** — detaliści typu x-kom/allegro/jysk zwykle TU nie występują, mimo że są w `dostawcy_range` (wyżej). To normalne — `explo_dostawca` może się nie rozwiązać nawet gdy `dostawca` jest poprawną, znaną wartością z dropdownu. Patrz `references/validation.md`.

## Inne systemy piszące do tych samych tabel

- **AppSheet / arkusz UI** — dziś jedyny istniejący sposób zakładania zamówień (wszystkich 4 rodzajów). Ten skill jest **drugim** punktem zapisu do `dostawy_master`/`dostawy_eksploatacyjne`/`dostawy_pozostale`, ograniczonym do 2 z 4 rodzajów.
- **`pushToInventory`, `cloneDelivery`, `splitDelivery`, `deleteDelivery`** (Apps Script, `delivery/` w repo `app-sheets`) — operują na już istniejących zamówieniach (przyjęcie, klon, split, usunięcie). Ten skill ich nie wywołuje i nie duplikuje ich logiki.

## Granica z innymi skillami tego repo

| | `delivery-order-intake` (ten skill) | `delivery-quality-documents` | `raw-material-documents` |
|---|---|---|---|
| Co robi | Zakłada nowe zamówienie (`dostawy_master` + pozycja) | Podpina dokument jakościowy do istniejącej dostawy surowca | Zarządza stałą dokumentacją surowca |
| Rodzaj dostawy | `eksploatacyjne`, `pozostale` | `surowce` (wyłącznie) | nie dotyczy dostaw |
| Kiedy w rozmowie | „zamówiłem X, dorzuć do dostaw" | „podepnij CoA/MSDS do tej dostawy" | „dodaj SDS dla tego surowca" |

Jeśli operator w trakcie rozmowy z tym skillem prosi o podpięcie dokumentu do dostawy — przekieruj do `delivery-quality-documents`. Jeśli prosi o założenie zamówienia surowca/opakowania — przekieruj do UI/AppSheet (nie ma tu odpowiednika konwersacyjnego, patrz `SKILL.md`).
