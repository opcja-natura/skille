# Workflow

## Nowe zamówienie

Użyj, gdy operator mówi, że coś zamówił/kupił i ma to trafić do rejestru dostaw (np. "zamówiłem klawiaturę w x-kom, dorzuć do dostaw").

### Krok 1 — zbierz, co zamówiono

Dopytaj tylko o to, czego naprawdę potrzebujesz i czego operator jeszcze nie podał:
- nazwa pozycji (co najmniej jedna),
- ilość,
- dostawca,
- cena netto — **opcjonalnie**, często nieznana przed fakturą, nie wymuszaj.

Jeśli operator wymienia kilka rzeczy naraz z tego samego zamówienia u tego samego dostawcy — to może być jedno zamówienie z wieloma pozycjami (patrz krok 6).

`podmiot` **nie jest pytaniem** — zawsze `spZoo`, nie pytaj o to operatora (patrz `references/schema.md`).

### Krok 1b — zapytaj zawsze o odbiór i płatność

Trzy pytania obowiązkowe przy każdym zamówieniu, niezależnie od tego, czy operator je poruszył sam:

1. **„Czy wymagany jest odbiór?"** → `wymagany_odbior` (kol. C): `TRUE` jeśli tak, `FALSE` jeśli nie. Nie zgaduj i nie pomijaj tego pytania.
2. **„Jaki sposób płatności?"** → `sposob_platnosci` (kol. I), jedna z `sposobPlatnosci_range` (`references/project-resources.md`).
3. **„Czy dostawa jest już opłacona?"** → jeśli tak, dopytaj o datę płatności i zapisz ją w `platnosc_data` (kol. P). Jeśli nie — zostaw `P` puste (nie jest to samo co pole formuły, po prostu jeszcze nie ma daty).

### Krok 2 — sklasyfikuj `dostawa_rodzaj`

Nie pytaj o rodzaj wprost jako pierwsze pytanie — spróbuj rozpoznać go z opisu pozycji, zapytaj tylko gdy niejednoznaczne.

**Kryterium `eksploatacyjne`** — zużywalne materiały/wyposażenie do produkcji i magazynu: kartony, taśmy, folie, rękawice, środki czyszczące, rolki/tonery do drukarek etykiet, ubrania robocze, narzędzia produkcyjne. Praktyczny test: czy ta rzecz istnieje jako pozycja w słowniku `BD_materials` (`references/project-resources.md`) — jeśli tak, prawie na pewno to `eksploatacyjne`.

**Kryterium `pozostałe`** — wszystko inne nieprodukcyjne: sprzęt IT/biurowy, opłaty, usługi, jednorazowe zakupy nieujęte w żadnym słowniku. **Przykład z życia: klawiatura z x-kom → `pozostałe`** (sprzęt biurowy, nie materiał produkcyjny).

**Kryterium `surowce`/`opakowanie` — STOP.** Jeśli pozycja to surowiec kosmetyczny (składnik receptury) albo opakowanie produktu (słoiki, butelki, nakrętki, etykiety, kartoniki) — **nie twórz nic w tym skillu**. Powiedz operatorowi, że to zamówienie zakłada się przez istniejący formularz AppSheet/arkusz, i wyjaśnij krótko dlaczego (kolumny sprzężone z recepturami/kosztem partii — patrz `SKILL.md`, „Poza zakresem"). Nie próbuj obejść tego wpisując rodzaj `pozostale` dla surowca czy opakowania — to zafałszuje rejestr.

Jeśli po tym kryterium nadal niejednoznaczne — zapytaj operatora wprost, pokazując oba kryteria w skrócie.

### Krok 3 — dla `eksploatacyjne`: sprawdź `BD_materials`

1. Odczytaj `BD_materials` (`references/project-resources.md`), kolumnę `short_name`.
2. Poszukaj dokładnego lub bardzo bliskiego dopasowania do nazwy podanej przez operatora.
3. **Dopasowanie znalezione** → użyj dokładnej wartości `short_name` ze słownika jako `eksplo_nazwa` (nie parafrazuj — VLOOKUP wymaga dokładnego stringa). Kontynuuj normalnie.
4. **Brak dopasowania** → zgodnie z decyzją operatora (Daniel, 2026-09-02): **zapisz mimo to**, pod nazwą podaną przez operatora, ale w preflight (krok 5) i w potwierdzeniu jawnie zaznacz, że `eksplo_id` się nie rozwiąże automatycznie i wiersz wymaga później ręcznego dopisania materiału do `BD_materials` albo poprawki nazwy. Nie traktuj braku dopasowania jako powodu do zmiany rodzaju na `pozostałe` — o rodzaju decyduje krok 2, nie obecność w słowniku.

Dla `pozostałe` ten krok nie istnieje — brak słownika, brak FK, zapisujesz nazwę wprost.

### Krok 4 — sprawdź dostawcę

Porównaj podaną nazwę dostawcy z `dostawcy_range` (`references/project-resources.md`). Dopasowanie nie musi być idealne (wielkość liter, spacje) — normalizuj rozsądnie. Jeśli nazwa naprawdę nie występuje w słowniku, powiedz to operatorowi wprost i zapytaj, czy zapisać mimo to jako wolny tekst (nie dopisuj sam do słownika bez pytania).

### Krok 5 — preflight

Pokaż podsumowanie (patrz `references/operator-dialog.md`) i poczekaj na potwierdzenie:
- rodzaj (`eksploatacyjne`/`pozostałe`),
- pozycja(-e): nazwa + ilość + cena (jeśli podana),
- dostawca, podmiot (zawsze `spZoo`), sposób płatności,
- czy wymagany odbiór (`TRUE`/`FALSE`),
- czy opłacona i jaka data (jeśli dotyczy),
- ostrzeżenie o niedopasowanym materiale (krok 3), jeśli dotyczy,
- ostrzeżenie o dostawcy spoza słownika (krok 4), jeśli dotyczy.

### Krok 6 — kilka pozycji w jednym zamówieniu

Jeśli operator zamawia kilka rzeczy tego samego rodzaju u tego samego dostawcy naraz — to jedno zamówienie: jeden wiersz `dostawy_master`, po jednym wierszu pozycji na każdą rzecz, wszystkie ze wspólnym `_id_dostawy` i własnym, unikalnym `_id_local`. Jeśli pozycje są różnych rodzajów (jedna `eksploatacyjne`, druga `pozostałe`) — to **dwa osobne zamówienia** (patrz `references/schema.md`, „Model") — powiedz to operatorowi i przeprowadź obie operacje osobno, jedna po drugiej.

### Krok 7 — zapis

Wykonaj dokładnie w kolejności z `references/validation.md`:
1. Wygeneruj `_id_dostawy`.
2. Dopisz wiersz do `dostawy_master`.
3. Po potwierdzonym sukcesie — dopisz wiersz(e) pozycji z nowymi `_id_local`.
4. Read-back wszystkich nowo dopisanych wierszy.

### Krok 8 — potwierdzenie

Podaj operatorowi `_id_dostawy` oraz krótkie podsumowanie zapisanych pozycji. Jeśli w kroku 3 było ostrzeżenie o niedopasowanym materiale, powtórz je tutaj — to jego przypomnienie do uzupełnienia słownika.
