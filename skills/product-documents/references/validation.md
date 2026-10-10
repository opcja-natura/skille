# Walidacja i bezpieczeństwo

## Potwierdzenie operatora — bez wyjątków

Żadna mutacja (nowy dokument, change request, nowa wersja, odrzucenie CR, archiwizacja) nie następuje bez jawnego potwierdzenia operatora po preflight — niezależnie od tego, jak jednoznaczne było polecenie. "Operator poprosił wprost o X, więc wykonuję X" **nie jest** wystarczające — nadal pokaż preflight i poczekaj na potwierdzenie. Jedyny wyjątek: sam odczyt/podgląd (workflow 1) i diagnostyka (workflow 7), które niczego nie zmieniają.

Jeśli w trakcie testu/rozmowy okaże się, że operacja została wykonana bez tego kroku — to błąd do natychmiastowego zatrzymania i zgłoszenia, nie coś do "naprawienia przy okazji".

## Plik źródłowy operatora — nigdy nie edytuj, nie przenoś, nie zmieniaj treści

Plik, który operator wskazuje jako wejście (dowolny format: PDF, DOCX, Google Doc), jest zawsze **punktem startowym do skopiowania/przekonwertowania**, nigdy miejscem pracy, i **skill nigdy nie edytuje jego treści**:

- jeśli wejście już jest PDF-em: kopia 1:1 do `typ_<TYP>/_pdf/` → `pdf_url`. `source_url` zostaje pusty — nie twórz dla niego żadnego dodatkowego "źródła".
- jeśli wejście NIE jest PDF-em: niezmieniona kopia oryginału do `typ_<TYP>/` → `source_url` (czysto archiwalne, informacyjne "z czego powstał PDF", nigdy więcej nieedytowane po zapisaniu), plus konwersja do PDF → `pdf_url`.
- żadnej stopki, żadnego dopisku wersji wewnątrz dokumentu — wersję identyfikuje `version_name` w nazwie pliku, nie treść. Zaobserwowany błąd (2026-09-16): agent konwertował gotowy PDF na DOCX, bo błędnie rozumiał `source_url` jako wymagany, edytowalny Google Doc — nie powtarzaj tego.
- oryginał podany przez operatora zostaje dokładnie tam, gdzie był, bez zmiany treści, nazwy ani lokalizacji.
- przy wdrażaniu change requestu treść zmiany przygotowuje operator **poza skillem** (własne narzędzie); skill dostaje gotowy plik nowej wersji i stosuje do niego dokładnie tę samą zasadę kopii/konwersji co do nowego dokumentu — nigdy sam nie edytuje treści.

Jeśli nie masz pewności, czy dane narzędzie faktycznie tworzy kopię, a nie modyfikuje plik w miejscu, albo czy wejście da się bezpiecznie przekonwertować do PDF — zatrzymaj się i zapytaj, zanim czegokolwiek dotkniesz. Pełne umiejscowienie tej zasady w każdym workflow: `workflows.md` §0.1.

## Kolumny chronione `ARRAYFORMULA` — nigdy nie zapisuj, nawet pustego stringa

`link_document_type!C,E`, `link_document_area!C,E`, `link_product_document!C` (pełen opis i formuły: `schema.md`) są wypełniane jedną, rozlaną `ARRAYFORMULA` zakotwiczoną w wierszu 2. Zapisanie do dowolnej z nich CZEGOKOLWIEK — łącznie z pustym stringiem `""` — blokuje dalsze rozlewanie się formuły dla wszystkich kolejnych wierszy, trwale (dopóki ktoś ręcznie nie wyczyści zablokowanej komórki). Skutek jest niewidoczny w samej wyświetlanej wartości (pusta komórka wygląda tak samo, zablokowana czy zdrowa) — ujawnia się dopiero jako brak wyliczonej nazwy dla kolejnych, nowszych wierszy.

Zasady:

- Przy każdym dopisywaniu wiersza do tych trzech tabel, zakres zapisu **fizycznie nie obejmuje** kolumny formułowej — nie ustawiaj jej na `""`, nie zostawiaj "pustej wartości dla porządku", tylko pomiń ją całkowicie w wywołaniu zapisu (zapisuj rozłączne zakresy kolumn, np. `A:B` + `D`, a nie ciągły `A:E` wypełniony częściowo pustkami).
- Jeśli narzędzie zapisu, którego używasz, nie pozwala pominąć pojedynczej kolumny w środku zakresu (wymusza zapis ciągłego bloku) — zapisz kolumny osobnymi wywołaniami (np. osobno A:B, osobno D), zamiast zapisywać cały wiersz jednym wywołaniem obejmującym kolumnę formułową.
- **Obowiązkowy health-check po każdym takim zapisie**: odczytaj ponownie wartość kolumny formułowej dla właśnie dopisanego wiersza. Powinna pokazywać poprawnie wyliczoną nazwę (nie pustkę), jeśli dane źródłowe (np. `product_id`/`type_id`/`area_id`) są poprawne. Jeśli jest pusta mimo poprawnych danych źródłowych — **nie kontynuuj, nie raportuj sukcesu**. To sygnał, że formuła została właśnie zablokowana (przez Twój zapis albo przez coś wcześniejszego) — zatrzymaj się i zgłoś to operatorowi wprost, z dokładnym wskazaniem wiersza/kolumny.
- Nie polegaj na samej wyświetlanej (`formattedValue`) pustej komórce jako dowodzie zdrowia formuły — jeśli masz wątpliwości i narzędzie na to pozwala, sprawdź `userEnteredValue`: w zdrowej kolumnie formułowej występuje wyłącznie w komórce-kotwicy (wiersz 2), nigdzie indziej.
- Jeśli podejrzewasz, że formuła jest już zablokowana od wcześniej (nie z Twojego bieżącego zapisu) — nie próbuj tego naprawiać samodzielnie w ramach zwykłej operacji dodawania dokumentu. Zgłoś to jako osobny problem do naprawy (wyczyszczenie zablokowanej komórki), a bieżącą operację albo wstrzymaj, albo kontynuuj świadomie informując operatora, że nazwa dla tego wiersza nie wyliczy się automatycznie, dopóki ktoś nie odblokuje formuły.

## Zero zgadywania — wymagana pewność, nie prawdopodobieństwo

"Prawdopodobnie chodzi o ten produkt/dokument/typ" nie jest podstawą do zapisu. Pewność oznacza jedno z:

- dokładnie jedno jednoznaczne dopasowanie po stabilnym ID, zweryfikowane odczytem live,
- albo jawne potwierdzenie operatora, gdy dopasowań jest więcej niż jedno lub dane są niekompletne.

Jeśli żaden z tych warunków nie jest spełniony — zatrzymaj się i zapytaj, nawet jeśli oznacza to przerwanie w połowie zbierania danych. Nie kontynuuj "na razie z najbardziej prawdopodobną opcją, skoryguję później" — korekta po zapisie jest znacznie kosztowniejsza niż jedno dodatkowe pytanie.

## Przed każdą mutacją

- Odczytaj stan live z source of truth, nie polegaj wyłącznie na wcześniejszym wyniku w tej rozmowie.
- Sprawdź istnienie wszystkich FK (`product_id`, `document_id`, `type_id`, `area_id`, `version_id`).
- Sprawdź status obiektów (`BD_documents.status`, `BD_document_change_requests.status`).
- Sprawdź duplikaty (patrz "Duplikat pliku" niżej).
- Sprawdź dostęp do pliku źródłowego.
- Sprawdź, czy wymagane dane są kompletne (patrz `workflows.md` po listę wymaganych pól per operacja).
- Pokaż preflight i uzyskaj jawne potwierdzenie operatora (patrz wyżej) — dopiero potem zapisuj.

## `version_no` — wartość statyczna, nie formuła

W tym module `BD_document_versions.version_no` jest zapisywany jako zwykła wartość liczbowa w momencie tworzenia rekordu — nie ma tu mechanizmu `ARRAYFORMULA` jak przy `is_current` w `raw-material-documents`. Oznacza to:

- musisz sam wyliczyć `MAX(version_no)+1` przed zapisem — nic nie przeliczy się automatycznie,
- błędny zapis `version_no` (np. duplikat) nie zostanie wykryty przez arkusz — musisz to sam zweryfikować przy read-back (`UNIQUE(document_id, version_no)`).

## Klucz "nowy dokument vs nowa wersja" — brak automatu, decyzja operatora

W odróżnieniu od `raw-material-documents` ten moduł nie liczy automatycznie aktywnych dokumentów pasujących do `(product_id, type_id)` i nie decyduje sam. Zawsze:

1. Pokaż operatorowi, czy istnieje pasujący aktywny dokument.
2. Zapytaj wprost, czy to podmiana (→ nowa wersja, `workflows.md` §3–4) czy nowy, odrębny dokument (→ `workflows.md` §2).
3. Nie zgaduj na podstawie samej zgodności `(product_id, type_id)` — kontekst biznesowy (np. inny wariant opakowania) może uzasadniać kilka równoległych aktywnych dokumentów tego samego typu dla tego samego produktu.

## Duplikat pliku

Dla tego samego `document_id` nie twórz nowej wersji, jeśli nowy plik jest tym samym PDF-em/źródłem co istniejąca wersja.

Preferowane sprawdzenia w kolejności możliwości narzędzia:

1. ten sam Drive file ID,
2. identyczny hash zawartości PDF, jeśli narzędzie pozwala pobrać bytes,
3. jeśli nie można wiarygodnie porównać zawartości, przynajmniej zablokuj identyczny source file ID i poinformuj operatora o ograniczeniu.

Nie używaj samej nazwy pliku jako dowodu identyczności.

## `pdf_url` wymagany zawsze, `source_url` tylko gdy dotyczy

Zatwierdzona wersja ma mieć **zawsze** działający `pdf_url`. `source_url` jest wymagany tylko wtedy, gdy plik wejściowy nie był już PDF-em (patrz `workflows.md` §0) — jeśli wejściem był bezpośrednio PDF, brak `source_url` jest poprawnym, oczekiwanym stanem, nie błędem. Nie zapisuj rekordu `BD_document_versions` jako finalny, jeśli:

- `pdf_url` nie działa,
- `source_url` powinien istnieć (wejście nie było PDF-em) i nie działa,
- nazwa PDF nie zgadza się dokładnie z `version_name`.

Nie sprawdzaj i nie wymagaj treści stopki dokumentu — skill nigdy jej nie ustawia (patrz `workflows.md` §0).

## Change request — kolejność zamykania

Dozwolona:

```text
walidacja -> nowy PDF+źródło -> nowy rekord wersji -> read-back -> (dopiero teraz) CR = implemented
```

Niedozwolona:

```text
CR = implemented -> próba dokończenia wersji
```

Jeśli którykolwiek krok tworzenia wersji się nie powiedzie, CR **pozostaje `open`** — nie ustawiaj `implemented` "na wyrost".

`implemented_in_version_id` musi wskazywać `version_id` należący do **tego samego** `document_id`, co CR. Przed zapisem zweryfikuj to explicite (nie zakładaj).

## Foldery Drive — nie mylić starej i nowej struktury

- Nowy dokument dowolnego typu poza PIF → `typ_<TYP>/` (mapa: `project-resources.md`).
- Nowa wersja **istniejącego** dokumentu PIF → folder wskazany przez `BD_documents.folder_url` tego konkretnego dokumentu (obecnie `_PL_` lub `_EN_`), **nie** `typ_PIF/`, dopóki migracja nie zostanie przeprowadzona jako osobne zadanie.
- Jeśli operator prosi o "przeniesienie" dokumentów PIF do nowej struktury — to nie jest zwykła operacja tego skilla. Potwierdź, że to świadoma decyzja o migracji, i jeśli tak, potraktuj to jako osobne zadanie, nie jako efekt uboczny dodania/aktualizacji jednego dokumentu.

## No delete

Nie usuwaj:
- dokumentów logicznych,
- wersji,
- change requestów,
- linków (typ/obszar/produkt),
- plików (źródeł ani PDF).

Archiwizuj zamiast usuwać.

## Owner i pola osobowe

- nowy dokument: `owner = operator`,
- nowa wersja: `approved_by = operator`,
- change request: `requested_by = operator zgłaszający` (może różnić się od `owner` dokumentu),
- nigdy nie wpisuj AI jako osoby w żadnym z tych pól,
- `approved_at`/`approved_by` nowej wersji nie są wymyślane — jeśli operator nie potwierdza jawnie daty/osoby zatwierdzenia (np. przy imporcie gotowego materiału), zatrzymaj finalizację i zapytaj.
