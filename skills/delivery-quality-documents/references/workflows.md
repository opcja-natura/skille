# Workflowy

## 1. Podpięcie dokumentu jakościowego do dostawy

Użyj, gdy operator ma plik (CoA, MSDS, deklaracja itp.) do podpięcia pod konkretną dostawę surowca.

### Krok 1 — zidentyfikuj surowiec

Rozpoznaj po nazwie z `BD_surowce` (`1jUSESWqYJapu5BrrKMdRk5CMR2cEOXChYKBmtOIsR3A`, tab `BD_surowce`). Uzyskaj `surowiec_id` (`SUR__nnn`). Przy niejednoznaczności pokaż kandydatów i poproś o wybór.

### Krok 2 — znajdź pozycję dostawy (Ty ustalasz ID, nie operator)

1. Przeszukaj `dostawy_surowce` po `surowiec_id` (kol. D), najnowsze najpierw — analogicznie do zakresu "ostatnie dostawy" używanego przez istniejącą automatyzację n8n (praktyczny limit: kilkadziesiąt ostatnich wierszy).
2. Jeśli operator już podał kontekst (data dostawy, dostawca, `id_dostawy`) — użyj go do zawężenia.
3. Jeśli jest dokładnie jedna sensowna kandydatka (np. jedna niedawna dostawa tego surowca) — pokaż ją do potwierdzenia, nie zmuszaj do wyboru z listy jednoelementowej.
4. Jeśli jest kilka kandydatek — pokaż listę (`id_dostawy`, `data_przyjecia` / `data_zamowienia`, `dostawca`) i poproś operatora o wybór.
5. Odczytaj `_id_local` (kol. M) wybranej pozycji. To jest klucz, który zapiszesz w `dokumentacja_surowce.id_surowiec_local` — operator nigdy nie musi go znać ani podawać.

Jeśli nie znaleziono żadnej pasującej pozycji dostawy dla tego surowca — powiedz to wprost operatorowi. Nie zakładaj dostawy, której nie ma w `dostawy_surowce`; to nie jest miejsce do tworzenia nowej dostawy (od tego jest `delivery/` — UI/AppSheet).

### Krok 3 — sprawdź duplikat

Przeszukaj `dokumentacja_surowce` po `id_surowiec_local` = `_id_local` z kroku 2.

- Brak istniejącego wiersza → kontynuuj normalnie.
- Jest już wiersz → **nie blokuj automatycznie**. Pokaż operatorowi istniejący dokument (`dokumentacja_name`, link) i zapytaj, czy to mimo to nowy, dodatkowy dokument dla tej samej dostawy (np. osobno CoA i MSDS) czy pomyłka.

### Krok 4 — zbierz plik

- Plik musi być PDF-em w wyniku; jeśli źródło to Google Doc/Sheet/Slide lub inny format eksportowalny, wyeksportuj do PDF przed zapisem.
- Jeśli nie da się uzyskać poprawnego PDF-u, przerwij operację i powiedz dlaczego.

### Krok 5 — preflight

Pokaż podsumowanie i poproś o potwierdzenie:

- surowiec (nazwa + `surowiec_id`),
- dostawa (`id_dostawy`, data, dostawca),
- plik źródłowy → docelowa nazwa w Drive,
- informacja o duplikacie, jeśli dotyczy (krok 3).

### Krok 6 — zapis

1. Ustal nazwę pliku: `<surowiec_id>__<oryginalna_nazwa_bez_rozszerzenia>__<id_dostawy>` (bez dodatkowego rozszerzenia w samej nazwie logicznej — zachowaj plik jako PDF).
2. Uploaduj plik do folderu archiwum `1rgo4UHMiwhDasq2j7fohcls3qIOw9ipx` z tą nazwą, ustawiając metadata properties: `surowiec_id`, `id_dostawy`, `surowiec_name`.
3. Dopiero po potwierdzonym sukcesie uploadu, dopisz wiersz do `dokumentacja_surowce` (A:H):
   - `surowiec_id`,
   - `surowiec_name`,
   - `id_dostawy`,
   - `id_surowiec_local` = `_id_local` z kroku 2,
   - `dokumentacja_name` = nazwa pliku z kroku 1,
   - `dokumentacja_link` = link do pliku (webViewLink),
   - `time` = teraz,
   - `confidence` = `1` (operator jawnie potwierdził dopasowanie w tej rozmowie).
4. Read-back nowego wiersza.

Jeśli upload pliku się powiedzie, ale zapis wiersza w arkuszu się nie powiedzie — nie zostawiaj tego bez informacji. Zgłoś operatorowi dokładnie: plik jest w Drive pod jaką nazwą/linkiem, a wiersz w `dokumentacja_surowce` NIE został dopisany — wymaga ręcznego uzupełnienia albo ponownej próby zapisu (nie ponownego uploadu pliku).

### Krok 7 — potwierdzenie

Podaj operatorowi: `surowiec_id`, `id_dostawy`, nazwę pliku w Drive i link.

## 2. Podgląd dokumentów jakościowych

Użyj, gdy operator pyta, jakie dokumenty jakościowe ma dana dostawa albo dany surowiec.

1. Zidentyfikuj surowiec i/lub dostawę (jak w workflow 1, krok 1–2, ale bez wymogu wyboru jednej pozycji jeśli operator pyta ogólnie o surowiec).
2. Przeszukaj `dokumentacja_surowce` po `surowiec_id` i/lub `id_dostawy`.
3. Pokaż znalezione wiersze: `id_dostawy`, `dokumentacja_name`, `dokumentacja_link`, `time`.
4. Jeśli brak wyników — powiedz to wprost, nie zgaduj, że dokument istnieje gdzie indziej.
