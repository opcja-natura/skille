# Walidacja i bezpieczeństwo

## Przed każdą mutacją

- Odczytaj stan live słowników (`BD_materials`, `dostawcy_range`) — nie polegaj na wcześniejszym wyniku w tej samej rozmowie, jeśli minęło dużo czasu; inne kanały (AppSheet/UI) piszą do tych samych tabel równolegle.
- Sprawdź, że masz komplet danych wymaganych do zapisu (patrz `references/schema.md`, kolumny „tak").
- Nigdy nie zapisuj częściowego zamówienia (np. samego `dostawy_master` bez pozycji, albo pozycji bez mastera) bez poinformowania operatora, że coś się nie udało.

## ARRAYFORMULA — zasada bezwzględna

Dwie zakładki mają kolumny sterowane nagłówkową ARRAYFORMULA rozlaną w dół arkusza (ten sam wzorzec co `surowiec_id`/`opakowanie_id` w `dostawy_surowce`/`dostawy_opakowanie`, udokumentowany w `delivery/STRUCTURE.md`). **Nigdy nie zapisuj do tych kolumn** — ani wartości, ani pustego stringa. Zapis (nawet `""`) w wierszu z ARRAYFORMULA nadpisuje formułę dla tego konkretnego wiersza i ją trwale usuwa (nie da się tego cofnąć samym ponownym odczytem).

**`dostawy_eksploatacyjne`** — D (`eksplo_id`), E (`explo_dostawca`). Zapisując wiersz pozycji, zapisz osobno segmenty **A, C** i **F:G** i **J** (pomijając B, D, E, H, I) — nie zapisuj jednego ciągłego zakresu A:J.

**`dostawy_master`** — K (`dostawa_przyjeta`), Q (`inovice_url`), T (`invoice_net_value`) — potwierdzone odczytem formuł z XLSX (2026-09-02), wcześniej nieudokumentowane. Zapisując wiersz zamówienia, zapisz osobno segmenty **A:G**, **I**, **(M)**, **(P)** (pomijając H, J, K, L, N, O, Q, R, S, T) — patrz `references/schema.md`, sekcja o append z pominięciem kolumn.

`dostawy_pozostale` nie ma kolumn formułowych (potwierdzone odczytem XLSX 2026-09-02) — tam można zapisać ciągły zakres A, C:E, H (z pominięciem tylko B, F, G, które zostają puste do przyjęcia).

## Generowanie ID — dokładnie ten format, nie inny

Ten arkusz dzieli tabele z webhookami Apps Script (`pushToInventory`, `cloneDelivery`, `splitDelivery`, `deleteDelivery`), które oczekują konkretnego formatu ID. Nie używaj schematu sekwencyjnego (`PREFIX_nnn`) znanego z innych skilli tego repo (`raw-material-documents`) — tu obowiązuje inny, już ustalony format.

**`_id_dostawy`** (nowe zamówienie):
```text
<YYYYMMDDHHMMSS><4 losowe wielkie litery A-Z>
```
Przykład: `20260902143512_QXTM`. Timestamp = aktualny czas UTC, tylko cyfry (bez separatorów), 14 znaków. Brak sekwencyjnego skanowania — timestamp + losowość wystarczają do unikalności.

**`_id_local`** (każda pozycja):
```text
<_id_dostawy>_<YYYYMMDDHHMMSS><6 losowych znaków base36 wielkimi literami>[_<index>]
```
Przykład (pierwsza pozycja w zamówieniu): `20260902143512_QXTM_20260902143513_7F2KQ1_0`. `index` = numer pozycji w tym zamówieniu (0, 1, 2...), dodawaj go zawsze gdy zamówienie ma więcej niż jedną pozycję — zapobiega kolizji, gdyby timestamp i losowy fragment wypadły identycznie dla dwóch pozycji zapisywanych w tej samej chwili.

## Kolejność zapisu

Dozwolona:

```text
walidacja -> preflight + potwierdzenie -> generuj _id_dostawy -> append dostawy_master
  -> potwierdzenie sukcesu -> generuj _id_local per pozycja -> append pozycji (z pominięciem kolumn formułowych)
  -> read-back wszystkich nowych wierszy
```

Niedozwolona:

```text
append pozycji przed zapisaniem mastera (osierocona pozycja bez _id_dostawy w rejestrze)
```

Jeśli zapis mastera się powiedzie, ale zapis którejkolwiek pozycji się nie powiedzie: **nie zostawiaj tego bez informacji**. Powiedz operatorowi dokładnie: `_id_dostawy` już istnieje w `dostawy_master`, ale która pozycja nie została dopisana i dlaczego — wymaga ponownej próby zapisu samej pozycji, nie ponownego zakładania zamówienia (unikaj duplikatu mastera).

## Append — gdzie w arkuszu

Docelowy wiersz zapisu to pierwszy pusty wiersz **po ostatnim niepustym wierszu w kolumnie A** danej zakładki — nie polegaj na "ostatnim wierszu arkusza" z UI ani na żadnej metodzie liczącej po kolumnach z ARRAYFORMULA (te zawyżają realny zakres danych, bo formuła bywa rozlana dużo dalej niż faktyczne dane). Kolumna A jest zawsze plain-text ID, nigdy formuła — licz po niej.

## Duplikat zamówienia

Jeśli w tej samej rozmowie operator już założył zamówienie o identycznej treści (ta sama nazwa pozycji + dostawca + dzień) — zapytaj, czy to naprawdę drugie, niezależne zamówienie, zanim zapiszesz drugi raz. To ostrzeżenie, nie blokada — czasem operator faktycznie zamawia to samo dwa razy tego samego dnia.

## No delete, no overwrite

Ten skill ma jedną operację: dopisanie nowego zamówienia. Nie usuwaj i nie nadpisuj istniejących wierszy `dostawy_master` ani żadnej zakładki pozycji. Jeśli operator chce poprawić albo usunąć zamówienie, które już istnieje — powiedz, że to wymaga ręcznej interwencji w arkuszu (poza zakresem tego skilla).
