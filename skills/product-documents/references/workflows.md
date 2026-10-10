# Workflowy

## 0. Cztery obiekty — nie mieszać

```text
A. Surowy plik wejściowy operatora (PDF, DOCX, cokolwiek) — jeszcze nie jest wersją biznesową
B. Dokument logiczny (document_id)                         — co dokument JEST, niezależnie od wersji
C. Archiwalne źródło wersji (source_url, OPCJONALNE)       — niezmieniona kopia oryginału wejściowego,
                                                              tylko gdy wejście NIE było już PDF-em
D. Zamrożony PDF wersji (pdf_url, WYMAGANE)                — stabilny artefakt historyczny
```

**Skill nigdy nie edytuje treści dokumentu** — ani stopki, ani treści merytorycznej, ani nie tworzy w tym celu żadnego natywnego Google Doc. To zasada, nie skrót: obserwowany błąd (2026-09-16) to agent konwertujący gotowy PDF na DOCX, bo błędnie rozumiał `source_url` jako wymagany, edytowalny format. Merytoryczną treść (w tym zmiany z change requestu) operator przygotowuje **poza skillem**, we własnym narzędziu, i przekazuje skillowi już gotowy, finalny plik.

## 0.1. Zasada kopii — obowiązuje w każdym workflow poniżej

Plik, który operator podaje jako wejście, jest **wejściem do skopiowania/przekonwertowania**, nigdy miejscem edycji w miejscu, i nigdy nie jest przez skill ruszany (nie przenoś, nie zmieniaj nazwy, nie edytuj, nie usuwaj — zostaje dokładnie tam, gdzie był).

Obsługa pliku wejściowego jest identyczna w §2 (nowy dokument) i §4 (nowa wersja) — patrz szczegóły przy każdym z nich:

- **Wejście już jest PDF-em**: zrób jego kopię 1:1 do `typ_<TYP>/_pdf/` — to staje się `pdf_url`. `source_url` zostaje pusty (nie ma osobnego "źródła" różnego od samego PDF-a).
- **Wejście NIE jest PDF-em**: (a) zapisz niezmienioną kopię oryginału do `typ_<TYP>/` — to staje się `source_url`, czysto archiwalny zapis "z czego powstał PDF", nigdy więcej nieedytowany po zapisaniu; (b) przekonwertuj kopię na PDF i zapisz do `typ_<TYP>/_pdf/` — to staje się `pdf_url`.

Jeśli plik wejściowy nie jest PDF-em i nie da się go bezpośrednio przekonwertować dostępnym narzędziem — zatrzymaj się i zapytaj operatora, zamiast zgadywać sposób konwersji.

Google Docs revision history nie jest wersjonowaniem biznesowym. Wersją biznesową jest rekord `BD_document_versions` + odpowiadający mu PDF — identyfikowany przez `version_name` (w nazwie pliku), nie przez treść stopki czy inną zmianę wewnątrz dokumentu.

---

## 1. Podgląd dokumentów produktu

1. Znajdź produkt w `DB_products_internal` po nazwie/kontekście (klucz: kolumna `sercet_id` = `product_id`). Przy niejednoznaczności pokaż kandydatów.
2. Pobierz wszystkie relacje z `link_product_document` dla `product_id`.
3. Dla każdego `document_id` pobierz `BD_documents` (także `status=archived`, jeśli operator pyta o historię).
4. Dla każdego dokumentu pobierz wszystkie wersje z `BD_document_versions`; aktualna = `MAX(version_no)`.
5. Pobierz otwarte (`status=open`) change requesty dla każdego `document_id`.
6. Nie ukrywaj archiwalnych dokumentów/wersji, gdy operator pyta o historię.

---

## 2. Nowy dokument — decyzja i zbiórka danych

Ten moduł **nie ma** automatycznego klucza `(product_id, type_id)` rozstrzygającego samodzielnie "nowy dokument czy nowa wersja" (w odróżnieniu od `raw-material-documents`) — jeden produkt może mieć uzasadnione więcej niż jeden aktywny dokument tego samego typu (np. dwie karty technologiczne różnych wariantów opakowania).

### 2.1. Inwentaryzacja (bez zapisu)

1. Zidentyfikuj plik(i) wejściowe i ich prawdopodobny produkt/język/typ.
2. Sprawdź `link_product_document` + `link_document_type` dla tego produktu i typu — czy pasujący aktywny dokument już istnieje.
3. Jeśli pasujący dokument istnieje i wygląda na to samo: zapytaj operatora, czy to podmiana (→ workflow 4, change request + nowa wersja) czy świadomie odrębny, dodatkowy dokument (→ kontynuuj tutaj jako nowy dokument).
4. Przygotuj mapę: `plik → product_id → język → document_id (nowy, proponowany) → version_id/version_name (proponowane)`. Pokaż operatorowi. **Nie zapisuj nic bez akceptacji.**

Nie łącz po nazwach — tylko po stabilnych ID. Nie zgaduj niepewnego mapowania produktu — zaznacz i zapytaj.

### 2.2. Zbierz dane

Wymagane:
- `product_id`,
- czytelna nazwa dokumentu,
- `type_id` (odczytany live z `BD_document_types`, dopasowany do opisu operatora i potwierdzony),
- `language` (`PL`/`EN`),
- plik źródłowy,
- `approved_at`, `approved_by` — **nie wymyślaj**. Jeśli operator przekazuje gotowy, wcześniej zatwierdzony materiał (import baseline'u), musi jawnie potwierdzić datę i osobę. W przeciwnym razie zatrzymaj finalizację i zapytaj.
- operator wykonujący operację → `owner`.

Opcjonalnie: `area_id` (może być kilka), `market`, `notes`, `required` (dla relacji z produktem).

### 2.3. Preflight

Pokaż podsumowanie: produkt, nazwa dokumentu, typ, język, plik, docelowy folder (`typ_<TYP>/`), `owner`. **Poczekaj na jawne potwierdzenie operatora** — obowiązkowo, nawet jeśli polecenie i wszystkie dane były jednoznaczne od początku (SKILL.md, "Twarde zasady" §1). Nie przechodź do §2.4 bez tego potwierdzenia.

### 2.4. Zapis

```text
1. Wygeneruj document_id (kolejny wolny DOC_NN).
2. Wygeneruj link_id dla relacji produkt-dokument.
3. Wygeneruj link_id typu (LDT_<CODE>_NN, licznik per-typ) i ewentualnie obszaru (LDA_NN).
4. Ustal version_no=1, version_name=<document_id>_v01_<data YYYY-MM-DD>.
5. Obsłuż plik wejściowy (patrz §0.1) — plik podany przez operatora zostaje nietknięty,
   dokładnie tam gdzie był (SKILL.md, "Twarde zasady" §2), nie przenoś go i nie edytuj:
   - Jeśli wejście już jest PDF-em: zrób jego kopię 1:1 jako
     typ_<TYP>/_pdf/<version_name>.pdf. source_url zostaje pusty.
   - Jeśli wejście NIE jest PDF-em: zapisz niezmienioną kopię oryginału jako
     typ_<TYP>/<nazwa oryginału> (to source_url), następnie przekonwertuj ją na PDF
     i zapisz jako typ_<TYP>/_pdf/<version_name>.pdf (to pdf_url).
   Nie edytuj treści ani formatowania w żadnym z dwóch przypadków — żadnej stopki,
   żadnego dopisku wersji wewnątrz dokumentu. Wersja jest identyfikowana przez nazwę
   pliku, nie przez treść.
6. Sprawdź, że pdf_url faktycznie istnieje na Drive (i source_url, jeśli został utworzony).
7. Dopisz BD_documents (status=active, owner=<operator>, folder_url=typ_<TYP>/).
8. Dopisz link_product_document — WYŁĄCZNIE kolumny A (link_id), B (product_id),
   D (document_id), F (required). NIGDY kolumna C (product_name — ARRAYFORMULA,
   patrz schema.md) — pomiń ją całkowicie w zapisie, nie wpisuj tam pustego stringa.
9. Dopisz link_document_type / link_document_area — WYŁĄCZNIE kolumny A (link_id),
   B (document_id), D (type_id/area_id). NIGDY kolumny C, E (ARRAYFORMULA) —
   pomiń je całkowicie w zapisie.
10. Dopisz BD_document_versions (version_id, document_id, version_no=1, version_name,
    source_url [puste, jeśli wejście było już PDF-em], pdf_url, approved_at, approved_by).
11. Read-back wszystkich utworzonych rekordów, w tym: odczytaj ponownie kolumnę
    product_name/document_name/type_name/area_name właśnie dopisanego wiersza i
    potwierdź, że pokazuje poprawną wyliczoną wartość (nie pustkę) — to potwierdza,
    że ARRAYFORMULA nadal się rozlewa i zapis w krokach 8–9 jej nie zablokował.
    Jeśli którakolwiek z tych kolumn jest pusta dla nowego wiersza mimo poprawnych
    danych źródłowych — ZATRZYMAJ SIĘ, nie kontynuuj, zgłoś to jako podejrzenie
    zablokowanej ARRAYFORMULA (patrz validation.md) zamiast raportować sukces.
12. Potwierdź document_id i version_id operatorowi.
```

Jeśli którykolwiek krok się nie powiedzie, nie zostawiaj częściowego pakietu — zatrzymaj się, opisz dokładnie co powstało/czego brakuje.

---

## 3. Change request — zgłoszenie potrzeby zmiany

1. Zidentyfikuj `document_id` (po nazwie/kontekście, potwierdź przy niejednoznaczności).
2. Zbierz: `request` (co zmienić), `reason` (dlaczego), opcjonalnie `product_id` (jeśli zmiana dotyczy jednego produktu), `owner` (domyślnie `BD_documents.owner` tego dokumentu, chyba że operator wskaże inaczej), `requested_by` (operator).
3. Pokaż podsumowanie zgłoszenia (dokument, request, reason, owner) i **poczekaj na jawne potwierdzenie** — obowiązkowo, nawet przy prostym, jednoznacznym zgłoszeniu.
4. Wygeneruj `request_id` (`DOCCR_` + 8 losowych znaków hex, sprawdź brak kolizji).
5. Dopisz `BD_document_change_requests`: `status=open`, `implemented_in_version_id` puste.
6. Read-back. Potwierdź `request_id` operatorowi.

Sam CR nie zmienia dokumentu ani wersji.

---

## 4. Wdrożenie change requestu(ów) — nowa wersja

**Skill nie edytuje treści dokumentu** (patrz §0). Zanim ten workflow się zacznie, operator (albo osoba merytorycznie odpowiedzialna) samodzielnie, poza skillem, przygotowuje nowy, finalny plik uwzględniający wyłącznie zmiany z wybranych CR — skill tylko go onboardinguje jako nową wersję, dokładnie jak nowy plik w §2.

1. Zidentyfikuj `document_id` i wszystkie `open` change requesty dla niego.
2. Operator wskazuje, które konkretnie CR wchodzą do tej wersji (może być więcej niż jeden).
3. Odczytaj wszystkie wersje dokumentu; `version_no` nowej = `MAX(version_no)+1`.
4. Poproś operatora o gotowy plik nowej wersji (już z wdrożonymi zmianami z wybranych CR, przygotowany przez niego poza skillem).
5. Pokaż preflight: dokument, lista CR wchodzących do wersji, planowany `version_no`, plik. **Poczekaj na jawne potwierdzenie**, że mają zostać wdrożone — dopiero potem ruszaj do kroku 6.
6. Sprawdź, czy dostarczony plik (po konwersji do PDF, jeśli dotyczy) nie jest identyczny (duplikat) z istniejącą wersją tego samego dokumentu — patrz `validation.md`.
7. Ustal `version_name = <document_id>_v<NN>_<data YYYY-MM-DD>`.
8. Obsłuż plik wejściowy dokładnie jak w §2.4 krok 5 (bez edycji treści/stopki):
   - Jeśli plik już jest PDF-em: kopia 1:1 jako `typ_<TYP>/_pdf/<version_name>.pdf`. `source_url` puste.
   - Jeśli nie jest PDF-em: niezmieniona kopia oryginału jako `typ_<TYP>/<nazwa oryginału>` (`source_url`), plus konwersja do PDF jako `typ_<TYP>/_pdf/<version_name>.pdf` (`pdf_url`).
9. Sprawdź, że `pdf_url` faktycznie istnieje na Drive (i `source_url`, jeśli został utworzony).
10. Dopisz `BD_document_versions` (nowy `version_id`, `document_id`, `version_no`, `version_name`, `source_url`, `pdf_url`, `approved_at`, `approved_by`).
11. Read-back nowej wersji — potwierdź, że `pdf_url` działa (i `source_url`, jeśli dotyczy), nazwa PDF = `version_name` + `.pdf`.
12. **Dopiero teraz** zamknij wybrane CR: `status=implemented`, `implemented_in_version_id=<nowy version_id>`, `closed_at=teraz`.
13. Read-back statusów CR. Podsumuj operatorowi: nowa wersja + lista wdrożonych CR.

Jeżeli którykolwiek z kroków 7–11 się nie powiedzie, **żaden CR nie zmienia statusu** — zostają `open`.

Wzorzec logowania z jedynego dotąd zaobserwowanego pełnego przebiegu (`APP_document_version_workbench` w arkuszu operacyjnym: `work_id`, `status`, `error`) jest dobrym punktem odniesienia, jeśli budujesz własny log tego procesu — nie jest wymagany do wykonania workflow.

---

## 5. Odrzucenie change requestu

1. Zidentyfikuj `request_id`, potwierdź że `status=open`.
2. Pokaż operatorowi, które zgłoszenie ma zostać odrzucone i **uzyskaj jawne potwierdzenie** (nie tylko powód — samą decyzję o odrzuceniu).
3. `status=rejected`, `closed_at=teraz`, `implemented_in_version_id` pozostaje puste.
4. Read-back.

Nie wymaga żadnej zmiany dokumentu/wersji.

---

## 6. Archiwizacja dokumentu

1. Zidentyfikuj dokument, sprawdź `status=active`.
2. Pokaż operatorowi podsumowanie (document_id, name, aktualna wersja) i **uzyskaj jawne potwierdzenie** — obowiązkowo, nawet jeśli operator sam poprosił o archiwizację wprost.
3. `BD_documents.status=archived`.
4. Opcjonalnie (nieobowiązkowe): przenieś źródło aktualnej wersji do `typ_<TYP>/_archive/` — nie jest to wymagane, historia i tak zostaje w bazie.
5. Read-back statusu. Potwierdź, że dokument pozostaje widoczny w historii.

Nie usuwaj dokumentu, wersji, CR ani linków.

---

## 7. Walidacja / diagnostyka

Sprawdź co najmniej:
- unikalność PK wszystkich tabel,
- `UNIQUE(document_id, version_no)`,
- FK: wersja → dokument, CR → dokument, CR → produkt (jeśli wypełnione), linki → dokument/słowniki,
- każdy `implemented` CR ma `implemented_in_version_id` wskazujący wersję **tego samego** `document_id`,
- brak `open`/`rejected` CR z wypełnionym `implemented_in_version_id` (i odwrotnie: brak `implemented` z pustym),
- każda wersja ma działający `pdf_url` (`source_url` wymagany tylko wtedy, gdy wejście nie było już PDF-em — patrz `references/workflows.md` §0),
- nazwa pliku PDF = `version_name` + `.pdf`,
- `status` dokumentu tylko `active`/`archived`,
- `folder_url` dokumentu wskazuje istniejący folder Drive,
- brak zablokowanej `ARRAYFORMULA` w `link_document_type!C,E`, `link_document_area!C,E`, `link_product_document!C` — sprawdź, czy `userEnteredValue` występuje w tych kolumnach wyłącznie w komórce-kotwicy (wiersz 2); jeśli występuje gdziekolwiek indziej, formuła jest zablokowana od tego wiersza w dół (patrz `validation.md`).

Nie naprawiaj automatycznie błędów integralności bez osobnego polecenia operatora — wyjątek: czyszczenie (nie nadpisywanie) pojedynczej komórki blokującej `ARRAYFORMULA`, jeśli operator wyraźnie poprosił o naprawę tego konkretnego problemu.
