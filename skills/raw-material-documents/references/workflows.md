# Workflowy

## 0. Obsługa pliku wejściowego — kopia albo upload, nigdy przeniesienie i nigdy sam link

Zarządzany plik to zawsze **osobny plik PDF w folderze aktywnym `dokumenty/`**, nazwany `<raw_material_id>__<version_name>.pdf`. `approved_file_url` wskazuje wyłącznie ten plik. Skąd on się bierze, zależy od tego, jak operator przekazał dokument:

| Operator przekazał | Co robisz | Co z oryginałem |
|---|---|---|
| **Link do pliku na Google Drive** (dowolny folder, np. `dokumentacja dostaw/`, folder dostawcy, „Mój dysk” operatora) | **Kopia**: utwórz nowy plik w `dokumenty/` z zawartości oryginału (PDF 1:1 albo eksport do PDF, jeśli oryginał nie jest PDF-em), nadaj nazwę zarządzaną | **Zostaje dokładnie tam, gdzie był**, pod swoją nazwą, nietknięty. Nie przenoś, nie zmieniaj nazwy, nie usuwaj, nie edytuj |
| **Plik załączony w rozmowie** (upload z komputera/telefonu, nie istnieje jeszcze na Drive) | **Upload oryginału** bezpośrednio do `dokumenty/` pod nazwą zarządzaną (po konwersji do PDF, jeśli trzeba). Nie ma czego kopiować — to jest pierwsze i jedyne miejsce tego pliku na Drive | Nie dotyczy |

Zabronione w obu przypadkach:

- **przeniesienie** (`move`) pliku z Drive do `dokumenty/` — oryginał operatora musi zostać na miejscu,
- **zmiana nazwy oryginału** na Drive „żeby pasował do konwencji”,
- **wpisanie do `approved_file_url` linku do oryginału** zamiast do zarządzanej kopii (zaobserwowany błąd 2026-09-17: `DOC_RM_010` linkował surowy plik w `dokumentacja dostaw/karty charakterystki olejki/`). Skutek: archiwizacja przeniosłaby cudzy plik, kontrola duplikatów po file ID traci sens, nazwa nie identyfikuje wersji.

Jedyne pliki, które skill **przenosi**, to jego własne zarządzane PDF-y: z `dokumenty/` do `_archive/` przy nowej wersji (po potwierdzeniu) albo przy archiwizacji dokumentu.

Jeśli nie masz pewności, czy narzędzie, którego używasz, kopiuje czy przenosi — zatrzymaj się i sprawdź, zanim dotkniesz pliku operatora.

## 1. Podgląd dokumentów surowca

1. Znajdź surowiec w `BD_surowce` po `_id` lub nazwie.
2. Pobierz wszystkie relacje z `link_raw_material_document` dla `raw_material_id`.
3. Dołącz `BD_documents`, także `status=archived`.
4. Dla każdego dokumentu pobierz wszystkie wersje i wskaż bieżącą jako najwyższy `version_no`.
5. Nie ukrywaj archiwalnych dokumentów, gdy operator pyta o historię.
6. Pokaż też, **jakich dokumentów brakuje**: odczytaj `BD_document_types` z kolumną `typ_surowca` (`schema.md`), wyznacz typy obowiązujące dla tego surowca (`all`, plus `essential_oil` jeśli surowiec jest olejkiem eterycznym — rozpoznanie po nazwie, potwierdź przy wątpliwości) i wypisz te, dla których nie ma aktywnego dokumentu. Typy `n/d` (`OTHER`) pomiń w tej liście.

## 2. Dodanie pliku dla surowca — rozstrzygnięcie nowy dokument / nowa wersja

Użyj za każdym razem, gdy operator ma nowy plik dla surowca (niezależnie od tego, czy sam wie, czy to "nowy dokument", czy "nowa wersja" — to rozstrzyga system).

1. Zidentyfikuj `raw_material_id` (po nazwie/kontekście, potwierdź przy niejednoznaczności).
2. Zidentyfikuj `type_id` dokumentu (odczytaj `BD_document_types` live; jeśli operator podał typ opisowo, dopasuj do kodu i potwierdź).
3. Pobierz przez `link_raw_material_document` + `link_document_type` wszystkie `document_id` dla tego surowca, których typ = ten `type_id`, i sprawdź ich `BD_documents.status`.
4. Policz, ile z nich ma `status=active`.

### 4a. 0 aktywnych dokumentów pasujących do klucza

Przejdź do workflow „3. Nowy dokument”.

### 4b. Dokładnie 1 aktywny dokument pasujący do klucza

Przejdź do workflow „4. Nowa wersja — podmiana” dla tego `document_id`.

### 4c. Więcej niż 1 aktywny dokument pasujący do klucza

Pokaż operatorowi wszystkie pasujące aktywne dokumenty razem z `supplier_name` i zapytaj:

- którego z nich dotyczy nowy plik → przejdź do workflow „4. Nowa wersja — podmiana” dla wskazanego `document_id`,
- albo czy to dodatkowy, niezależny dokument (np. nowy dostawca) → przejdź do workflow „3. Nowy dokument”.

Nie zgaduj i nie wybieraj kandydata automatycznie.

## 3. Nowy dokument

Użyj, gdy dopasowanie w workflow 2 dało 0 aktywnych dokumentów, albo operator jawnie potwierdził, że to dodatkowy, niezależny dokument mimo istniejących aktywnych dokumentów tego typu.

### Zbierz dane

Wymagane:
- surowiec,
- czytelna nazwa dokumentu,
- typ co najmniej 1 (`type_id` odczytany live z `BD_document_types`),
- **obszar co najmniej 1** (`area_id` odczytany live z `BD_document_areas`) — operator zwykle nie podaje go wprost: zaproponuj obszar na podstawie typu i treści dokumentu (np. karta charakterystyki → `Jakość`), pokaż w preflight i uzyskaj potwierdzenie. Bez potwierdzonego obszaru nie zapisuj,
- język `PL` / `EN` / `N/A`,
- `required` TRUE/FALSE,
- plik źródłowy: link do pliku na Drive **albo** plik załączony w rozmowie — od tego zależy, czy robisz kopię, czy upload (patrz §0),
- `issued_at`,
- operator.

Opcjonalne:
- dodatkowe typy / obszary poza pierwszym,
- supplier_name,
- notes.

Słowniki `BD_document_types` i `BD_document_areas` są SSOT: nie dodawaj do nich pozycji, nie wpisuj kodów/nazw do tabel linkujących, nie konstruuj ID z kodu. Jeśli żadna pozycja słownika nie pasuje — zatrzymaj się i zapytaj operatora, nie zapisuj dokumentu „bez obszaru”.

`issuer` uzupełnij zawsze, gdy można go wiarygodnie ustalić. Najpierw odczytaj wystawcę/autora/producenta wskazanego w dokumencie. Jeśli dokument nie wskazuje wystawcy jednoznacznie, ale znany jest dostawca i prawdopodobnie jest to ta sama firma, zaproponuj `issuer = supplier_name` i poproś operatora o potwierdzenie. Nie zgaduj i nie zostawiaj `issuer` pustego bez świadomego potwierdzenia operatora, że nie da się go ustalić.

Nie pytaj o `valid_until`.
Owner nowego dokumentu = operator wykonujący operację.

### Preflight

1. Rozwiąż `raw_material_id`.
2. Odczytaj live słowniki typów i obszarów; przelicz na ID. Ustal co najmniej jeden `type_id` i co najmniej jeden `area_id` (obszar zaproponuj, jeśli operator go nie podał).
3. Potwierdź wynik dopasowania z workflow 2 (0 aktywnych dokumentów albo świadoma decyzja operatora o dodatkowym dokumencie).
4. Zweryfikuj dostęp do pliku i możliwość utworzenia PDF.
5. Ustal `issuer` i `supplier_name`. Jeśli `issuer` nie jest jednoznaczny, pokaż proponowaną wartość operatorowi i uzyskaj jej potwierdzenie przed zapisem.
6. Pokaż podsumowanie (w tym typ(y) i obszar(y) po nazwie ze słownika + ID) i uzyskaj potwierdzenie.

### Zapis

1. Wygeneruj `document_id`.
2. Wygeneruj `link_id` dla relacji surowiec-dokument.
3. Wygeneruj linki typów i obszarów.
4. Ustal `version_no=1` i `version_name=<document_id>_v01_<issued_at YYYY-MM-DD>`.
5. Utwórz zarządzany PDF w folderze aktywnym `dokumenty/` pod nazwą
   `<raw_material_id>__<version_name>.pdf` — zgodnie z §0: **kopia**, jeśli operator podał link z Drive
   (oryginał zostaje na miejscu); **upload**, jeśli plik przyszedł w rozmowie. Nigdy `move`, nigdy sam link do oryginału.
6. Dopisz `BD_documents` ze `status=active`, `owner=<operator>`.
7. Dopisz `link_raw_material_document`.
8. Dopisz `link_document_type` (min. 1 wiersz) **i** `link_document_area` (min. 1 wiersz) — oba obowiązkowo, po `type_id` / `area_id` ze słowników. Dokument bez któregokolwiek z tych linków jest niekompletny.
9. Dopisz `BD_document_versions` wyłącznie do kolumn A:J:
   - nowy `version_id`,
   - `document_id`,
   - `version_no=1`,
   - `version_name`,
   - `approved_file_url=<zarządzany PDF>`,
   - `issued_at`,
   - `valid_until=''`,
   - `approved_at=teraz`,
   - `approved_by=<operator>`,
   - `notes` (jeśli dotyczą wersji; jeśli operator podał tylko ogólne uwagi, zapisz je w `BD_documents.notes`).
   - **Nie zapisuj kolumny K (`is_current`)**. Jest ona wyliczana przez istniejącą `ARRAYFORMULA`.
   - Dla tej tabeli nie używaj operacji typu `appendCells`/append-row, jeśli mogą wyznaczyć koniec tabeli na podstawie kolumny K. Najpierw znajdź pierwszy wolny fizyczny wiersz po ostatnim niepustym `version_id` w kolumnie A, a następnie zapisz zakres A:J dokładnie w tym wierszu.
10. Read-back wszystkich utworzonych rekordów: `BD_documents`, `link_raw_material_document`, **`link_document_type` i `link_document_area` (potwierdź, że oba wiersze istnieją i wskazują istniejące ID słownikowe)**, oraz `BD_document_versions!K` dla nowej wersji (oczekuj `is_current=TRUE`).
11. Potwierdź `document_id` i `version_id`.

Jeśli zapis pliku lub którykolwiek krytyczny zapis bazy nie powiedzie się, nie pozostawiaj częściowego pakietu. Wycofaj utworzone rekordy/pliki, jeśli narzędzia pozwalają bezpiecznie zrobić rollback; w przeciwnym razie zatrzymaj się i dokładnie wskaż stan wymagający ręcznej naprawy.

## 4. Nowa wersja — podmiana istniejącego dokumentu

Użyj, gdy workflow 2 wskazał dokładnie jeden aktywny dokument pasujący do klucza, albo operator wskazał konkretny `document_id` spośród kilku kandydatów.

1. Zidentyfikuj `document_id` (z workflow 2).
1a. Sprawdź, czy ten dokument ma wpisy w `link_document_type` i `link_document_area`. Jeśli któregoś brakuje (dokument zapisany przed 2026-09-17 mógł nie mieć obszaru), zaproponuj uzupełnienie brakującego linku w tym samym preflight — nowa wersja nie może zostawić dokumentu niekompletnego.
2. Zbierz nowy plik i `issued_at`. Nie pytaj o `valid_until`.
3. Odczytaj wersje dokumentu; wyznacz najwyższy `version_no` i nowy `+1`.
4. Sprawdź, czy nowy PDF nie jest duplikatem istniejącej wersji tego dokumentu.
5. Ustal `version_name=<document_id>_vNN_<issued_at YYYY-MM-DD>`.
6. Zapytaj operatora, czy zarchiwizować poprzednią wersję/plik:
   - jeśli to była podmiana wynikająca z 1 aktywnego dokumentu (workflow 2, przypadek 4b) → domyślna odpowiedź **TAK**,
   - jeśli operator sam wskazał dokument spośród kilku kandydatów (workflow 2, przypadek 4c) → domyślna odpowiedź **NIE**, poczekaj na jawne potwierdzenie.
7. Pokaż preflight (dokument, surowiec, typ, nowa wersja, decyzja o archiwizacji) i uzyskaj potwierdzenie.
8. Utwórz nowy zarządzany PDF w folderze aktywnym `dokumenty/` (kopia z Drive albo upload z rozmowy — §0; oryginał operatora nietknięty).
9. Dopisz nowy rekord `BD_document_versions` do pierwszego wolnego fizycznego wiersza, zapisując wyłącznie kolumny A:J. Nie zapisuj K (`is_current`) i nie używaj append-row, jeśli `ARRAYFORMULA` w K może przesunąć append na koniec arkusza.
10. Read-back nowej wersji, w tym kolumny K, i potwierdź, że jest najwyższą wersją oraz `is_current=TRUE`.
11. Jeśli operator potwierdził archiwizację: przenieś poprzedni zarządzany PDF bieżącej (poprzedniej) wersji do `_archive`. Jeśli operator nie potwierdził — zostaw poprzedni PDF i dokument aktywne bez zmian.
12. Potwierdź `version_id`, `version_name` i lokalizację PDF, oraz czy poprzedni dokument został zarchiwizowany.

## 5. Archiwizacja dokumentu (bez dodawania nowego pliku)

Użyj, gdy surowiec przestaje używać danego dokumentu bez zastępowania go nowym (np. zmiana dostawcy, wycofanie surowca).

1. Zidentyfikuj dokument.
2. Sprawdź, czy `status=active`.
3. Znajdź bieżącą wersję jako najwyższy `version_no` i jej `approved_file_url`.
4. Pokaż operatorowi jednoznaczne potwierdzenie archiwizacji.
5. Najpierw przenieś aktualny zarządzany PDF do `_archive`.
6. Dopiero po sukcesie ustaw `BD_documents.status=archived`.
7. Read-back statusu.
8. Nie usuwaj dokumentu, wersji ani linków.
9. Potwierdź `document_id` i informację, że pozostaje w historii.

## 6. Walidacja / diagnostyka

Sprawdź co najmniej:
- unikalność wszystkich PK,
- unikalność `(document_id, version_no)`,
- FK wersja -> dokument,
- dokładnie jedna current wersja dla dokumentów z wersjami,
- current = najwyższy `version_no`,
- aktywny + required ma zatwierdzony plik,
- każdy `approved_file_url` wskazuje plik w `dokumenty/` (rodzic `1xL1m7jSD-R9ZFrzSDqZqX1hlvwxsJidP`) o nazwie `<raw_material_id>__<version_name>.pdf` — link do pliku poza folderem zarządzanym to błąd (§0),
- **każdy dokument (także `archived`) ma co najmniej jeden wiersz w `link_document_type` i co najmniej jeden w `link_document_area`**, a wskazane `type_id` / `area_id` istnieją w słownikach,
- status dokumentu tylko `active` / `archived`,
- więcej niż 1 aktywny dokument na parę `(raw_material_id, type_id)` bez wyraźnego uzasadnienia liczbą aktywnych dostawców,
- (raport braków, nie błąd) dla każdego surowca z co najmniej jednym dokumentem: typy obowiązujące wg `typ_surowca`, dla których nie ma aktywnego dokumentu; dokument typu `essential_oil` przypięty do surowca, który nie jest olejkiem, zgłoś do weryfikacji.

Nie naprawiaj automatycznie błędów integralności bez osobnego polecenia operatora.
