---
name: delivery-order-intake
description: Zakładanie nowego zamówienia w rejestrze dostaw Opcja Natura bezpośrednio z rozmowy, przez Google Sheets. Używaj, gdy operator mówi, że coś zamówił (np. "zamówiłem klawiaturę w x-kom, dorzuć do dostaw") i chce, żeby to trafiło do rejestru dostaw jako nowe zamówienie oczekujące na przyjęcie. Obsługuje wyłącznie rodzaje `eksploatacyjne` i `pozostałe`. Nie obsługuje surowców ani opakowań — te idą przez istniejący formularz AppSheet, bo mają kolumny sprzężone z recepturami i kosztem partii.
---

# Zakładanie zamówień dostaw Opcja Natura

## Cel

Zapisz nowe zamówienie (jeszcze nie przyjęte) do rejestru dostaw: 1 wiersz w `dostawy_master` + po jednym wierszu na każdą zamówioną pozycję w zakładce pozycji odpowiadającej rodzajowi. Operator nie edytuje arkusza ręcznie ani nie zna żadnych ID — Ty je generujesz i pokazujesz do potwierdzenia.

## Poza zakresem

**Rodzaj `surowce` i `opakowanie` — zablokowane całkowicie.** Te dwie zakładki mają kolumny (`surowiec_id`, `surowiec_dostawca`, `opakowanie_id`, `opakowanie_dostawca` i inne) sprzężone z recepturami produktów i kosztem partii — błąd tam wpływa na produkcję, nie tylko na rejestr zakupów. Jeśli operator prosi o dorzucenie surowca albo opakowania do dostaw, **nie twórz niczego** — powiedz, że to idzie przez istniejący formularz AppSheet/arkusz (tak jak dziś), i że ten skill celowo tego nie obsługuje.

**Przyjęcie dostawy, split, clone, delete — poza zakresem.** Ten skill tylko zakłada zamówienie. Fizyczne przyjęcie towaru (uzupełnienie `data_przyjecia`, ilości realnej, `dostawa_przyjeta=TRUE`), przeniesienie do magazynu (`pushToInventory`), podział (`splitDelivery`), klon (`cloneDelivery`) i usunięcie (`deleteDelivery`) zostają wyłącznie w UI/arkuszu — nie próbuj ich wykonać stąd, nawet jeśli operator o to poprosi. Skieruj go do arkusza.

**Dokumenty jakościowe dostaw** (CoA, MSDS per dostawa surowca) — osobny skill `delivery-quality-documents`. **Stałe dokumenty surowca** (SDS, certyfikat pochodzenia...) — osobny skill `raw-material-documents`. Ten skill nie zajmuje się żadnymi dokumentami.

## Najważniejsza zasada

Nie zgaduj i nie zapisuj częściowej operacji. Rozpoznaj rodzaj zamówienia, sprawdź dostępne słowniki, pokaż operatorowi podsumowanie planowanego zapisu i uzyskaj potwierdzenie. Dopiero potem wykonuj mutacje.

## Zasoby

Przed pierwszą operacją w sesji przeczytaj odpowiednie sekcje:

- `references/project-resources.md` — ID arkuszy, zakładek i słowników.
- `references/schema.md` — tabele, kolumny, które wolno i których nie wolno dotykać.
- `references/workflows.md` — procedura krok po kroku.
- `references/validation.md` — walidacje, ARRAYFORMULA, generowanie ID, kolejność zapisu.
- `references/operator-dialog.md` — jak prowadzić rozmowę i jak potwierdzać wynik.

## Sposób pracy

1. Ustal tożsamość operatora (pole `zamawiajacy`).
   - Jeśli można wiarygodnie pobrać e-mail zalogowanego użytkownika z połączonego konta, użyj go.
   - W przeciwnym razie zapytaj raz o służbowy e-mail i zachowaj go na całą sesję.

2. Zbierz, co operator zamówił: nazwa pozycji, ilość, dostawca, ewentualnie cena — tyle, ile faktycznie wie w tym momencie. Nie wymuszaj pól, których operator jeszcze nie zna (np. ceny przed fakturą) — to normalne, że część danych uzupełni się dopiero przy przyjęciu dostawy. Dodatkowo zapytaj zawsze (niezależnie, czy operator sam to poruszył): czy wymagany jest odbiór, jaki sposób płatności, i czy dostawa jest już opłacona (jeśli tak — jaka data). Podmiotu **nie pytaj** — zawsze `spZoo`.

3. Rozpoznaj `dostawa_rodzaj` (`references/workflows.md`, krok klasyfikacji).
   - Jeśli to jednoznacznie surowiec albo opakowanie — **zatrzymaj się i przekieruj do UI/AppSheet** (patrz „Poza zakresem" wyżej). Nie twórz nic.
   - Jeśli to `eksploatacyjne` albo `pozostałe` — kontynuuj.
   - Jeśli niejednoznaczne — zapytaj operatora, pokazując krótkie kryterium rozróżnienia (patrz `references/workflows.md`).

4. Dla `eksploatacyjne`: sprawdź nazwę pozycji względem słownika `BD_materials` (`references/project-resources.md`). To decyduje, czy kolumna `eksplo_id` (formuła) w ogóle się rozwiąże.
   - Dopasowanie znalezione → użyj dokładnej nazwy ze słownika.
   - Brak dopasowania → **zapisz mimo to** (ta kategoria nie jest krytyczna operacyjnie), ale jawnie uprzedź operatora, że `eksplo_id` nie rozwiąże się automatycznie i wiersz będzie wymagał ręcznego dopisania do słownika materiałów albo poprawki później.

5. Sprawdź `dostawcę` względem listy w `named_ranges_helper` (`references/project-resources.md`). Jeśli nazwa nie występuje w słowniku, powiedz to wprost operatorowi — zapisz jako wolny tekst, nie dopisuj po cichu do słownika.

6. Pokaż podsumowanie przed zapisem (patrz `references/operator-dialog.md`, sekcja „Preflight"):
   - rodzaj, pozycja(-e) z ilością, dostawca, cena (jeśli podana), podmiot, sposób płatności,
   - ostrzeżenie o niedopasowanym materiale (krok 4), jeśli dotyczy.
   Poproś o potwierdzenie.

7. Wykonaj zapis w bezpiecznej kolejności z `references/validation.md`: wygeneruj `_id_dostawy`, dopisz wiersz do `dostawy_master`, dopiero po sukcesie dopisz wiersz(e) pozycji z nowym `_id_local` każda. Nigdy nie pisz do kolumn ARRAYFORMULA. Po zapisie zrób read-back.

8. Po sukcesie podaj operatorowi `_id_dostawy` — to jego jedyny sposób odwołania się do tego zamówienia później (np. przy przyjęciu towaru).

## Reguły biznesowe

- Jedno zamówienie operatora (nawet z kilkoma pozycjami) = jeden wiersz `dostawy_master` + N wierszy pozycji, wszystkie z tym samym `_id_dostawy`.
- Pola dotyczące fizycznego przyjęcia dostawy (`data_przyjecia`, ilość realna, `przyjmujacy`, `komentarz_przyjmujacego`) zostają puste przy tworzeniu — to nie jest Twój krok. `dostawa_przyjeta` (kol. K `dostawy_master`) w ogóle nie jest polem do ustawiania — to ARRAYFORMULA, liczy się sama.
- `podmiot` zawsze `spZoo` — nie pytaj operatora. `wymagany_odbior` i `sposob_platnosci` pytaj zawsze. Płatność: zapytaj czy dostawa jest już opłacona — jeśli tak, zapisz datę w `platnosc_data`.
- Nigdy nie pisz do kolumn oznaczonych jako formuła/ARRAYFORMULA w `references/schema.md` — nadpisanie łamie formułę dla tego wiersza.
- `_id_dostawy` i `_id_local` generuj dokładnie w formacie już używanym przez webhooki tego modułu (`references/validation.md`) — nie wymyślaj nowego formatu, nawet jeśli inne skille w tym repo (dokumentowe) generują ID sekwencyjnie inaczej. Ten arkusz dzieli te same tabele z webhookami Apps Script, które oczekują tego konkretnego formatu.
- Nie usuwaj i nie nadpisuj istniejących wierszy. To wyłącznie operacja dopisania (append).

## Brak możliwości zapisu

Jeśli w bieżącym środowisku nie ma połączonego Google Sheets z prawem zapisu, nie symuluj operacji. Powiedz, że do wykonania zapisu potrzebne jest połączenie z prawem zapisu, i podaj operatorowi dokładnie, jaki wiersz/wiersze zamierzałeś dopisać.
