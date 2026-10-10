# Dialog z operatorem

## Styl

Prowadź rozmowę krótko i operacyjnie. Nie wymagaj od operatora znajomości ID, jeśli można je znaleźć po nazwie i kontekście. Jednocześnie nie zgaduj przy wielu dopasowaniach.

## Preflight i potwierdzenie — zawsze, nawet przy jasnym poleceniu

Nawet gdy operator poda wszystko od razu, jednym zdaniem ("dodaj kartę technologiczną dla X, plik: [link]") — nie wykonuj zapisu od razu. Zawsze najpierw pokaż preflight (patrz sekcje niżej) i poczekaj na osobne, jawne potwierdzenie ("tak", "rób", "potwierdzam" itp.), zanim cokolwiek zapiszesz do bazy lub Drive. Samo podanie kompletnych danych przez operatora nie jest równoznaczne z potwierdzeniem zapisu — to dwa osobne kroki rozmowy, nawet jeśli w praktyce mogą wypaść blisko siebie.

Analogicznie: jeśli którykolwiek element (produkt, dokument, typ, plik) nie jest zweryfikowany z pewnością — zapytaj wprost, zamiast założyć najbardziej prawdopodobną odpowiedź i iść dalej.

## Tożsamość operatora

Jeśli e-mail nie jest dostępny z konta:

> Podaj proszę służbowy e-mail, który mam zapisywać jako osobę wykonującą operacje w tej sesji.

Zapytaj tylko raz na sesję.

## Niejednoznaczny produkt/dokument

> Znalazłem kilka dopasowań. Które wybierasz?
> 1. PIF — Bio tox (EN) [DOC_04]
> 2. PIF — Bio tox (PL) [DOC_15]

## Podejrzenie, że to podmiana istniejącego dokumentu, a nie nowy

> Dla [produkt] / [typ] mam już aktywny dokument [document_id — nazwa]. Czy nowy plik ma zastąpić go jako kolejną wersję, czy to świadomie odrębny, dodatkowy dokument (np. inny wariant)?

Nie proponuj domyślnej odpowiedzi — to moduł bez automatycznego rozstrzygania, poczekaj na jawną decyzję operatora.

## Preflight — nowy dokument

> Zamierzam utworzyć nowy dokument:
> - Produkt: Elixir of Youth [product_id: 6214ac72...]
> - Dokument: Karta technologiczna — Elixir of Youth
> - Typ: Karta technologiczna
> - Język: PL
> - Wymagany: TAK
> - Właściciel: operator@opcjanatura.pl
> - Plik: <nazwa pliku> → kopia 1:1 do typ_Karta technologiczna/_pdf/ (plik już jest PDF-em)
> - Pierwsza wersja: v01
> Potwierdzasz zapis?

Jeśli plik wejściowy NIE jest PDF-em, ostatnia linijka preflightu wygląda tak:

> - Plik: <nazwa pliku> → kopia oryginału do typ_Karta technologiczna/ (source_url) + konwersja do PDF w typ_Karta technologiczna/_pdf/ (pdf_url)

## Zgłoszenie change requestu — potwierdzenie

> Zapisuję zgłoszenie zmiany:
> - Dokument: SDS — Bio-tox [DOC_04]
> - Co zmienić: aktualizacja listy składników
> - Powód: zmiana składu
> - Zgłasza: operator@opcjanatura.pl, właściciel: agata@opcjanatura.pl
> Potwierdzasz?

## Preflight — wdrożenie nowej wersji

> Wdrażam do DOC_04 następujące otwarte zgłoszenia: CR DOCCR_a1b2c3d4 ("aktualizacja listy składników").
> - Nowa wersja: v03
> - Plik: <plik z wdrożoną zmianą, przygotowany przez Ciebie> → kopia 1:1 do typ_Karta charakterystyki (SDS)/_pdf/
> - Po zapisie oznaczę wybrane zgłoszenie jako wdrożone w tej wersji
> Potwierdzasz, że treść jest zatwierdzona biznesowo i mogę zapisać?

(Skill nie edytuje treści dokumentu — plik z wdrożoną zmianą operator przygotowuje sam, poza rozmową z agentem.)

## Kilka change requestów w jednej wersji

> Dla DOC_04 masz teraz 2 otwarte zgłoszenia: CR_a1b2 i CR_c3d4. Czy oba wchodzą do tej samej nowej wersji, czy tylko jedno z nich?

## Odrzucenie change requestu

> Potwierdzasz odrzucenie zgłoszenia CR_a1b2c3d4 ("aktualizacja listy składników") bez wdrażania? Dokument i wersje zostają bez zmian.

## Archiwizacja

> Zamierzam zarchiwizować dokument DOC_31 (Karta technologiczna — Detox Body Scrub). Pozostanie widoczny w historii, ale przestanie być traktowany jako obowiązujący. Potwierdzasz?

## Sukces

Nowy dokument:

> Utworzono dokument DOC_47, wersja VER_000048 / DOC_47_v01_2026-09-15. PDF zapisano w typ_Karta technologiczna/_pdf/.

Wdrożona zmiana:

> Utworzono wersję VER_000049 / DOC_04_v03_2026-09-15. Zgłoszenie CR_a1b2c3d4 oznaczone jako wdrożone w tej wersji.

Odrzucona zmiana:

> Zgłoszenie CR_a1b2c3d4 odrzucone. Dokument i wersje bez zmian.

Archiwizacja:

> Zarchiwizowano dokument DOC_31. Pozostaje widoczny w historii.

## Błąd

Podaj operatorowi konkretny etap i brak zmian końcowych, np.:

> Nie wykonałem operacji. Nie udało się wygenerować poprawnego PDF z zatwierdzonego źródła. Baza nie została zmieniona, zgłoszenie zmiany pozostaje otwarte.

Jeśli nie można zagwarantować rollbacku, opisz dokładnie, co zostało zapisane i czego nie udało się cofnąć. Nigdy nie używaj samego „wystąpił błąd”.

## Prośba o coś poza zakresem tego skilla

Dokumenty surowca:

> To dotyczy dokumentacji surowca, nie produktu — przełączam się na odpowiedni skill (`raw-material-documents`).

Dokumenty jakościowe dostawy:

> To dotyczy dokumentu jakościowego konkretnej dostawy — przełączam się na `delivery-quality-documents`.

Migracja PIF do nowej struktury folderów:

> Migracja istniejących dokumentów PIF do `typ_PIF/` to osobne, zaplanowane zadanie, nie rutynowa operacja tego skilla. Czy na pewno chcesz to zrobić teraz, jako świadomą decyzję o migracji?
