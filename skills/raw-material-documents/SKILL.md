---
name: raw-material-documents
description: Zarządzanie dokumentacją surowców Opcja Natura bezpośrednio z rozmowy przez Google Drive i Google Sheets. Używaj, gdy operator chce znaleźć dokumenty surowca, sprawdzić historię i status, dodać dokument (nowy albo kolejną wersję istniejącego), zarchiwizować dokument albo sprawdzić spójność dokumentacji. Skill sam rozstrzyga, czy dodany plik to nowy dokument czy nowa wersja, prowadzi operatora krok po kroku, zapisuje zarządzane PDF-y na Drive i aktualizuje relacyjną bazę po stabilnych ID.
---

# Dokumenty surowców Opcja Natura

## Cel

Obsługuj cały proces `surowiec -> dokument logiczny -> wersje` bez wymagania od operatora ręcznego edytowania tabel. Traktuj bazę dokumentów jako source of truth, a Drive jako magazyn zatwierdzonych PDF-ów.

## Poza zakresem

Ten skill nie obsługuje dokumentu jakościowego surowca (certyfikat jakości / specyfikacja jakościowa dostawy). Ten dokument jest dostarczany przy każdej dostawie i żyje w zupełnie innym systemie: arkusz `dokumentacja_surowce` (spreadsheet `11caP8XxVKVO2tzEH4UFl1VJihX_rcyGYGxiBJev0Ak0`).

Jeśli operator prosi o podpięcie/sprawdzenie dokumentu jakościowego dostawy: **przełącz się na skill `delivery-quality-documents`** — on obsługuje dokładnie tę operację konwersacyjnie (rozpoznaje surowiec, sam znajduje pozycję dostawy, uploaduje plik, dopisuje wiersz). Nie próbuj wykonać tego tutaj i nie proś o ID dostawy w tej rozmowie — to nie jest Twój zakres.

Ten skill nie obsługuje Change Requestów. Zostały usunięte z modelu 2026-08-31 — logika jest teraz prostsza (patrz „Rozróżnienie operacji” niżej).

## Najważniejsza zasada

Nie zgaduj i nie zapisuj częściowej operacji. Najpierw odczytaj stan live, zweryfikuj dane, pokaż operatorowi podsumowanie planowanej zmiany i uzyskaj potwierdzenie. Dopiero potem wykonuj mutacje.

## Zasoby

Przed pierwszą operacją w sesji przeczytaj odpowiednie sekcje:

- `references/project-resources.md` — ID baz, folderów i zasady dostępu.
- `references/schema.md` — tabele, kolumny, klucze i relacje.
- `references/workflows.md` — procedury dla każdej operacji.
- `references/validation.md` — walidacje, bezpieczeństwo, pliki, duplikaty i rollback.
- `references/operator-dialog.md` — jak prowadzić rozmowę i jak potwierdzać wynik.

## Sposób pracy

1. Ustal tożsamość operatora.
   - Jeśli można wiarygodnie pobrać e-mail zalogowanego użytkownika z połączonego konta, użyj go.
   - W przeciwnym razie zapytaj raz o służbowy e-mail i zachowaj go na całą sesję.
   - Nie wpisuj AI jako `owner` ani `approved_by`.

2. Rozpoznaj intencję operatora:
   - podgląd dokumentów / historii,
   - dodanie dokumentu (nowy plik dla surowca — system sam rozstrzyga, czy to nowy dokument czy nowa wersja),
   - archiwizacja,
   - walidacja / diagnostyka.

3. Odczytaj dane z bazy przed każdą mutacją.
   - Dopasowuj po stabilnych ID.
   - Nazw używaj tylko do wyszukiwania i prezentacji.
   - Przy niejednoznacznym dopasowaniu surowca/dokumentu pokaż kandydatów i poproś o wybór.

4. Zastosuj właściwy workflow z `references/workflows.md`.

5. Przed zapisem pokaż krótkie podsumowanie:
   - surowiec,
   - dokument,
   - typ operacji (nowy dokument / nowa wersja),
   - typ(y) dokumentu i obszar(y) — po nazwie ze słownika, z ID w nawiasie; obszar jest obowiązkowy, nawet jeśli operator o nim nie wspomniał,
   - plik,
   - najważniejsze metadane,
   - jeśli dla pary surowiec+typ jest więcej niż jeden aktywny dokument: listę kandydatów z `supplier_name` i pytanie, którego dotyczy zmiana.
   Poproś o potwierdzenie.

6. Wykonuj operację w bezpiecznej kolejności.
   - Operacja na pliku ma się udać przed finalną archiwizacją starego dokumentu/wersji.
   - Po zapisie wykonaj read-back kluczowych rekordów.
   - Jeśli którykolwiek krok krytyczny nie powiedzie się, nie udawaj sukcesu. Zatrzymaj proces i zgłoś konkretny błąd.

7. Po sukcesie podaj wygenerowane ID oraz nowy stan.

## Reguły biznesowe

- Jeden `BD_documents` rekord oznacza jeden dokument logiczny.
- Nowy plik/rewizja istniejącego dokumentu oznacza nowy rekord w `BD_document_versions`, nie nowy `document_id`.
- Nie nadpisuj starych wersji i nie usuwaj historii.
- `is_current` oznacza wersję o najwyższym `version_no` dla danego `document_id`. Kolumna jest zarządzana przez istniejącą `ARRAYFORMULA`: nigdy jej nie zapisuj, nie czyść, nie nadpisuj ani nie rozszerzaj ręcznie. Przy zapisie `BD_document_versions` zapisuj wyłącznie kolumny A:J i po zapisie odczytaj K do walidacji.
- **Każdy dokument logiczny musi mieć co najmniej jeden wiersz w `link_document_type` i co najmniej jeden w `link_document_area`.** Słowniki `BD_document_types` i `BD_document_areas` są jedynym źródłem prawdy o dopuszczalnych typach i obszarach — odczytuj je live przed każdym zapisem, dopasowuj po `type_id` / `area_id`, nigdy nie wpisuj kodów ani nazw do tabel linkujących i nie dodawaj nowych pozycji do słowników samodzielnie. Dokument bez wpisu w którejkolwiek z tych dwóch tabel jest niekompletny: nie raportuj sukcesu, dopóki oba linki nie istnieją (zaobserwowany błąd 2026-09-17: agent zapisywał dokumenty bez `link_document_area`, bo obszar był opisany jako opcjonalny — to była błędna specyfikacja, nie dozwolony skrót).
- `BD_document_types.typ_surowca` mówi, dla jakich surowców dany typ obowiązuje (`all` / `essential_oil` / `n/d`). Przy podglądzie i diagnostyce pokazuj operatorowi, których obowiązujących dokumentów surowiec jeszcze nie ma (`references/schema.md`). Nie blokuj tym zapisu.
- Obszar (`area_id`) nie jest podany przez operatora wprost w większości przypadków — zaproponuj go na podstawie typu i treści dokumentu (np. karta charakterystyki → obszar jakości), pokaż propozycję w preflight i uzyskaj potwierdzenie. Nie zapisuj bez potwierdzonego obszaru.
- Klucz dopasowania „czy to nowy dokument, czy nowa wersja” to wyłącznie `(raw_material_id, type_id)`. `area_id` i `supplier_name` w tym kluczu nie uczestniczą — ale brak `area_id` nadal jest błędem kompletności (patrz wyżej).
- Jeśli dla klucza jest dokładnie 1 aktywny dokument, nowy plik domyślnie zastępuje go jako nową wersję, a stara wersja domyślnie idzie do archiwum (operator potwierdza, domyślna odpowiedź TAK).
- Jeśli dla klucza jest więcej niż 1 aktywny dokument (surowiec ma kilku aktywnych dostawców tego samego typu dokumentu), nie zgaduj którego dotyczy zmiana. Pokaż kandydatów i poproś operatora o wybór; domyślnie nic nie archiwizuj automatycznie.
- Dokument `archived` pozostaje widoczny w historii; nie traktuj archiwizacji jako usunięcia.
- `valid_until` pozostaw jako pole kompatybilności historycznej, ale nie pytaj o nie i przy nowych zapisach pozostaw puste.
- Nowe zatwierdzone pliki zapisuj jako **osobny** PDF w zarządzanym folderze aktywnym `dokumenty/` pod nazwą `<raw_material_id>__<version_name>.pdf`. **Plik podany linkiem z Google Drive → kopia, oryginał zostaje nietknięty na swoim miejscu. Plik załączony w rozmowie → upload oryginału pod nazwą zarządzaną.** Nigdy nie przenoś pliku operatora i nigdy nie wpisuj do `approved_file_url` linku do oryginału zamiast do kopii (`references/workflows.md` §0).
- Przy nowej wersji przenieś poprzedni zarządzany PDF aktualnej wersji do `_archive` dopiero po poprawnym utworzeniu nowej wersji i tylko po potwierdzeniu archiwizacji.
- Przy archiwizacji przenieś aktualny PDF do `_archive`; jeśli przeniesienie się nie uda, nie zmieniaj statusu dokumentu na `archived`.
- Nie twórz kolejnej wersji z tym samym PDF-em dla tego samego dokumentu.

## Rozróżnienie operacji

Przed dodaniem pliku policz dokumenty ze `status=active` pasujące do `(raw_material_id, type_id)` nowego pliku.

**0 aktywnych dokumentów pasujących do klucza — nowy dokument.** Dokument logiczny jeszcze nie istnieje dla tej pary surowiec+typ. Utwórz dokument + relacje + v01.

**Dokładnie 1 aktywny dokument pasujący do klucza — nowa wersja.** Prawie zawsze to podmiana (jeden dostawca danego surowca i typu). Zaproponuj nową wersję istniejącego `document_id` i zapytaj o archiwizację starej — domyślnie TAK.

**Więcej niż 1 aktywny dokument pasujący do klucza — wymagany wybór operatora.** Surowiec ma kilku aktywnych dostawców tego samego typu dokumentu naraz. Pokaż wszystkich kandydatów z `supplier_name` i zapytaj, którego dotyczy nowy plik (albo czy to dodatkowy, niezależny dokument dla nowego dostawcy). Domyślnie nic nie archiwizuj automatycznie.

## Brak możliwości zapisu

Jeśli w bieżącym środowisku nie ma połączonego Google Drive/Sheets z prawem zapisu, nie symuluj operacji. Powiedz, że do wykonania mutacji potrzebne jest połączenie z prawem zapisu i podaj operatorowi dokładnie, jaki krok był planowany.
