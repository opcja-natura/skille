---
name: product-documents
description: Dokumenty PRODUKTÓW GOTOWYCH Opcja Natura (PIF, SDS, ROB, karta technologiczna, karta opisowa marketingowa, specyfikacja jakościowa, instrukcja, dokument regulacyjny i inne). Używaj, gdy ktoś chce: pokazać/znaleźć dokumenty danego produktu, sprawdzić aktualną wersję lub historię wersji dokumentu, dodać nowy dokument dla produktu, zgłosić potrzebę zmiany dokumentu (change request), wdrożyć zmianę jako nową wersję, odrzucić zgłoszenie zmiany, zarchiwizować dokument, albo sprawdzić spójność bazy dokumentów produktowych. Działa bezpośrednio na Google Drive/Sheets: prowadzi krok po kroku, zapisuje edytowalne źródło + PDF, aktualizuje bazę po stabilnych ID. NIE używaj do dokumentacji SUROWCÓW (SDS/certyfikaty surowca — to skill raw-material-documents) ani do dokumentów jakościowych POJEDYNCZEJ DOSTAWY (CoA/MSDS dostawy — to skill delivery-quality-documents).
---

# Dokumenty produktowe Opcja Natura

## Cel

Obsługuj cały proces `produkt -> dokument logiczny -> wersje` oraz `change request -> nowa wersja` bez wymagania od operatora ręcznego edytowania tabel. Traktuj bazę dokumentów jako source of truth, a Drive jako magazyn edytowalnych źródeł i zatwierdzonych PDF-ów.

## Poza zakresem

Ten skill nie obsługuje dokumentacji **surowców** (SDS/certyfikat pochodzenia/deklaracja alergenów surowca). To zupełnie inny system, inna baza, inne Drive. Jeśli operator pyta o dokumenty surowca — **przełącz się na skill `raw-material-documents`**, nie próbuj tego zrobić tutaj.

Ten skill nie obsługuje dokumentów jakościowych dostawy (CoA, MSDS przypisane do konkretnej dostawy). Jeśli operator o to prosi — **przełącz się na skill `delivery-quality-documents`**.

Ten skill nie wykonuje migracji istniejących dokumentów PIF ze starej struktury folderów (`_PL_`/`_EN_`) do nowej (`typ_PIF/`). To osobne, zaplanowane zadanie — nie próbuj go wykonać przy okazji zwykłej operacji na dokumencie.

## Twarde zasady — zero wyjątków

Te cztery zasady obowiązują zawsze, niezależnie od tego, jak prosta, oczywista albo pilna wydaje się operacja. Złamanie którejkolwiek to błąd skilla, nie "skrót", nawet jeśli końcowy zapis okazał się poprawny.

### 1. Zawsze pytaj o potwierdzenie przed KAŻDYM zapisem/mutacją

Nie ma operacji na tyle prostej, żeby pominąć preflight + potwierdzenie (`references/operator-dialog.md`). Nie wykonuj zapisu "od razu", nawet jeśli polecenie operatora brzmiało jednoznacznie i konkretnie (np. "dodaj kartę technologiczną dla X, plik tutaj: [link]") — jednoznaczność polecenia nie zwalnia z pokazania podsumowania i uzyskania jawnego "tak" przed zapisem do bazy/Drive. Wyjątek: sam odczyt/podgląd (workflow 1) nigdy nie wymaga potwierdzenia, bo nic nie zmienia.

### 2. Nigdy nie modyfikuj ani nie przenoś pliku źródłowego wskazanego przez operatora

Jeśli operator podaje link do istniejącego pliku (PDF, DOCX, Google Doc, cokolwiek) — ten plik jest **wejściem**, nie miejscem pracy. Zawsze:

- jeśli plik już jest PDF-em: zrób jego kopię 1:1 w `typ_<TYP>/_pdf/` — to `pdf_url`, koniec (`source_url` zostaje pusty),
- jeśli plik NIE jest PDF-em: zapisz niezmienioną kopię oryginału w `typ_<TYP>/` (to `source_url`, czysto archiwalne), a osobno przekonwertuj go na PDF do `typ_<TYP>/_pdf/` (to `pdf_url`),
- **nigdy nie edytuj treści ani formatowania** pliku — ani oryginału, ani kopii, ani PDF-a — żadnej stopki, żadnego dopisku wersji wewnątrz dokumentu; wersję identyfikuje nazwa pliku, nie jego treść,
- oryginalny plik podany przez operatora zostaje dokładnie tam, gdzie był, w niezmienionej postaci — nie przenoś go, nie zmieniaj jego nazwy, nie edytuj go w miejscu, nie usuwaj.

Dotyczy to zarówno nowego dokumentu (workflow 2), jak i nowej wersji (workflow 4) — przy wdrażaniu change requestu treść zmiany przygotowuje operator **poza skillem**, we własnym narzędziu; skill dostaje gotowy plik i tylko go onboardinguje (kopia/konwersja), nigdy nie edytuje treści sam. Szczegóły: `references/workflows.md`, `references/validation.md`.

### 3. Nigdy nie zgaduj — potrzebujesz pewności, nie prawdopodobieństwa

Jeśli identyfikacja produktu, dokumentu, typu, wersji, pliku albo rozstrzygnięcie "nowy dokument czy nowa wersja" nie jest jednoznaczne wprost z danych (dokładnie jedno pasujące ID, jawne potwierdzenie operatora) — **zatrzymaj się i zapytaj**, zamiast przyjąć najbardziej prawdopodobną opcję. "Najpewniej chodzi o..." nie jest podstawą do zapisu. Dotyczy to też sytuacji, gdy tylko jedno dopasowanie *wygląda* oczywiste — jeśli nie zostało jawnie zweryfikowane/potwierdzone, i tak pokaż je operatorowi w preflight zamiast przyjmować milcząco.

### 4. Nigdy nie zapisuj do kolumn zarządzanych `ARRAYFORMULA` — nawet pustego stringa

`link_document_type!C,E`, `link_document_area!C,E`, `link_product_document!C` (pełna lista i formuły: `references/schema.md`) są wypełniane jedną, rozlaną `ARRAYFORMULA` na całą kolumnę. Zapisanie tam czegokolwiek — łącznie z `""` — trwale blokuje dalsze rozlewanie się formuły dla wszystkich kolejnych wierszy, bez widocznego błędu w danym momencie (ujawnia się dopiero jako brak nazwy dla kolejnych, nowszych wierszy). To realny, zaobserwowany sposób psucia się tego systemu, nie teoretyczne ryzyko.

Przy dopisywaniu wiersza do tych tabel zakres zapisu **pomija te kolumny całkowicie** (nie ustawia ich na pusto — w ogóle ich nie dotyka). Po zapisie zawsze wykonaj health-check: odczytaj ponownie kolumnę formułową dla nowego wiersza i potwierdź, że pokazuje wyliczoną wartość, a nie pustkę. Jeśli jest pusta mimo poprawnych danych źródłowych — zatrzymaj się, nie raportuj sukcesu, zgłoś podejrzenie zablokowanej formuły. Szczegóły i dokładne bezpieczne zakresy zapisu: `references/schema.md`, `references/validation.md`, `references/workflows.md`.

Poza tymi czterema: nie zapisuj częściowej operacji. Najpierw odczytaj stan live, zweryfikuj dane, pokaż operatorowi podsumowanie planowanej zmiany. Dopiero po potwierdzeniu wykonuj mutacje. Nie zamykaj change requestu jako `implemented`, dopóki nowa wersja nie ma w pełni zweryfikowanego `pdf_url` (i `source_url`, jeśli dotyczy — patrz zasada 2).

## Zasoby

Przed pierwszą operacją w sesji przeczytaj odpowiednie sekcje:

- `references/project-resources.md` — ID baz, folderów Drive (w tym pełna mapa `typ_<TYP>/`) i zasady dostępu.
- `references/schema.md` — tabele, kolumny, klucze i relacje.
- `references/workflows.md` — procedury dla każdej operacji.
- `references/validation.md` — walidacje, bezpieczeństwo, pliki, duplikaty i rollback.
- `references/operator-dialog.md` — jak prowadzić rozmowę i jak potwierdzać wynik.

## Sposób pracy

1. Ustal tożsamość operatora.
   - Jeśli można wiarygodnie pobrać e-mail zalogowanego użytkownika z połączonego konta, użyj go.
   - W przeciwnym razie zapytaj raz o służbowy e-mail i zachowaj go na całą sesję.
   - Nie wpisuj AI jako `owner`, `approved_by` ani `requested_by`.

2. Rozpoznaj intencję operatora:
   - podgląd dokumentów produktu / historii wersji,
   - dodanie zupełnie nowego dokumentu (dla produktu i typu, dla których jeszcze nic nie ma),
   - zgłoszenie change requestu (potrzeba zmiany istniejącego dokumentu),
   - wdrożenie change requestu(ów) jako nowej wersji,
   - odrzucenie change requestu,
   - archiwizacja dokumentu,
   - walidacja / diagnostyka.

3. Odczytaj dane z bazy przed każdą mutacją.
   - Dopasowuj po stabilnych ID (`product_id`, `document_id`, `version_id`, `request_id`, `type_id`, `area_id`).
   - Nazw (`product_name`, `document_name`, `type_name`, `area_name`) używaj tylko do wyszukiwania i prezentacji — część z nich to w bazie same formuły `XLOOKUP`, nie wpisuj tam wartości ręcznie.
   - Przy niejednoznacznym dopasowaniu produktu/dokumentu pokaż kandydatów i poproś o wybór.
   - Ten moduł **nie ma** automatycznego klucza `(product_id, type_id)` rozstrzygającego samodzielnie "nowy dokument czy nowa wersja" (w odróżnieniu od `raw-material-documents`) — rozstrzygnięcie zawsze potwierdza operator, patrz `references/workflows.md` §1.

4. Zastosuj właściwy workflow z `references/workflows.md`.

5. Przed zapisem pokaż krótkie podsumowanie (produkt, dokument, typ operacji, plik, kluczowe metadane, przy wdrożeniu CR — pełną listę wdrażanych zgłoszeń) i **poczekaj na jawne potwierdzenie operatora**. To krok obowiązkowy zawsze, nawet gdy polecenie było w 100% jednoznaczne i wszystkie dane pochodzą wprost z tego, co powiedział operator — patrz "Twarde zasady" §1. Nie interpretuj braku sprzeciwu jako potwierdzenia; potrzebujesz jawnego "tak"/odpowiednika.

6. Wykonuj operację w bezpiecznej kolejności (kopia pliku → baza po plikach/PDF, patrz `references/workflows.md`). Pracuj wyłącznie na kopiach — patrz "Twarde zasady" §2.
   - Po zapisie wykonaj read-back kluczowych rekordów.
   - Jeśli którykolwiek krok krytyczny nie powiedzie się, nie udawaj sukcesu. Zatrzymaj proces i zgłoś konkretny błąd — nie zamykaj change requestu przy niepełnym pakiecie.

7. Po sukcesie podaj wygenerowane ID oraz nowy stan.

## Reguły biznesowe

- Jeden rekord `BD_documents` = jeden dokument logiczny, niezależny od liczby wersji.
- Nowa treść dokumentu = nowy rekord w `BD_document_versions` (kolejny `version_no`), nigdy nowy `document_id` i nigdy nadpisanie istniejącej wersji.
- Aktualna wersja to zawsze `MAX(version_no)` dla danego `document_id` — nie ma osobnej kolumny do tego; nie próbuj jej ustawiać ani szukać `is_current`.
- Każda zatwierdzona wersja musi mieć `pdf_url` (zamrożony PDF) — wersja bez `pdf_url` nie jest zamknięta, nie raportuj jej jako gotowej. `source_url` jest **opcjonalny i wyłącznie informacyjny** — niezmieniona kopia oryginalnego pliku wejściowego, ustawiana tylko wtedy, gdy to wejście NIE było już PDF-em; jeśli wejściem był bezpośrednio PDF, `source_url` zostaje pusty. Skill nigdy nie tworzy natywnego Google Doc jako "źródła" ani nie konwertuje PDF-a na format edytowalny — patrz "Twarde zasady" §2.
- Zmianę treści dokumentu prowadzi change request (`open` → `implemented`/`rejected`), nie bezpośrednia edycja wersji "od ręki".
- `implemented` change request musi mieć `implemented_in_version_id` wskazujący wersję należącą do **tego samego** `document_id`. Pole to w żywej bazie nazywa się `implemented_in_version_id` — jeśli natrafisz na dokumentację (np. Google Doc README) nazywającą je `target_version_id`, to nieaktualna nazwa; trzymaj się nagłówka żywego arkusza.
- Kilka change requestów może zostać wdrożonych razem w jednej wersji — wszystkie dostają ten sam `implemented_in_version_id`.
- Relacja produkt↔dokument (`link_product_document`) wskazuje zawsze `document_id`, nigdy `version_id`.
- Nowe zatwierdzone pliki zapisuj jako PDF w `typ_<TYP>/_pdf/` (folder właściwy dla typu dokumentu — pełna mapa w `references/project-resources.md`), z nazwą dokładnie równą `version_name` + `.pdf`.
- Nowe dokumenty (jakiegokolwiek typu poza PIF) zapisuj do folderu `typ_<TYP>/` — bez podziału na język wewnątrz folderu; język to wyłącznie pole `BD_documents.language`.
- **PIF pozostaje wyjątkiem**: istniejące dokumenty PIF nadal używają starych folderów `_PL_`/`_EN_` (patrz `BD_documents.folder_url` konkretnego dokumentu) do czasu osobnej migracji. Nie przenoś ich samodzielnie do `typ_PIF/`.
- Nie usuwamy dokumentów, wersji, change requestów ani linków — archiwizacja (`BD_documents.status=archived`) to jedyny sposób wycofania dokumentu, i nie usuwa historii.
- Nie twórz kolejnej wersji z identycznym PDF-em jak istniejąca wersja tego samego dokumentu.
- Plik/dokument podany przez operatora jako wejście nigdy nie jest edytowany ani przenoszony w miejscu, i skill nigdy nie edytuje treści dokumentu (żadnej wersji) — zawsze kopia 1:1 (jeśli wejście już jest PDF-em) albo kopia + konwersja do PDF (jeśli nie jest). Patrz "Twarde zasady" §2.
- Kolumny `link_document_type!C,E`, `link_document_area!C,E`, `link_product_document!C` są zarządzane `ARRAYFORMULA` — nigdy nie zapisuj do nich niczego, nawet pustego stringa. Patrz "Twarde zasady" §4.

## Rozróżnienie operacji

**Podgląd** — zawsze bezpieczny odczyt, bez potwierdzenia.

**Nowy dokument** — gdy dla produktu i typu dokumentu nie ma jeszcze żadnego pasującego aktywnego dokumentu (operator potwierdza to świadomie, nie ma tu automatycznego zliczania jak w `raw-material-documents`). Patrz `references/workflows.md` §2.

**Change request** — zawsze gdy zgłaszana jest potrzeba zmiany istniejącego dokumentu. Sam w sobie nie zmienia żadnej wersji.

**Wdrożenie (nowa wersja)** — gdy co najmniej jeden `open` change request dla danego `document_id` jest gotowy do realizacji. Patrz `references/workflows.md` §4.

**Odrzucenie CR** — zamyka zgłoszenie bez tworzenia wersji.

**Archiwizacja** — gdy dokument przestaje być używany bez zastępowania nową wersją.

## Brak możliwości zapisu

Jeśli w bieżącym środowisku nie ma połączonego Google Drive/Sheets z prawem zapisu, nie symuluj operacji. Powiedz, że do wykonania mutacji potrzebne jest połączenie z prawem zapisu i podaj operatorowi dokładnie, jaki krok był planowany.
