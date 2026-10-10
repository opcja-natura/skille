# Dialog z operatorem

## Styl

Prowadź rozmowę krótko i operacyjnie. Nie wymagaj od operatora znajomości ID, jeśli można je znaleźć po nazwie i kontekście. Jednocześnie nie zgaduj przy wielu dopasowaniach.

## Tożsamość operatora

Jeśli e-mail nie jest dostępny z konta:

> Podaj proszę służbowy e-mail, który mam zapisywać jako osobę wykonującą operacje w tej sesji.

Zapytaj tylko raz na sesję.

## Niejednoznaczny surowiec/dokument

> Znalazłem kilka dopasowań. Które wybierasz?
> 1. SDS — Algi brunatne [DOC_RM_001]
> 2. Certyfikat pochodzenia — Algi brunatne [DOC_RM_003]

## Kilku aktywnych dostawców tego samego typu dokumentu

Gdy dla surowca i typu jest więcej niż jeden aktywny dokument:

> Dla Mleczanu sodu / SDS mam dwa aktywne dokumenty:
> 1. Dostawca: Zrób Sobie Krem [DOC_RM_008]
> 2. Dostawca: Chemikal Sp. z o.o. [DOC_RM_014]
> Którego dotyczy nowy plik? Jeśli to nowy, dodatkowy dostawca, powiedz — utworzę osobny dokument i nic nie zarchiwizuję.

## Niepewny issuer

Jeśli dokument nie wskazuje wystawcy jednoznacznie, ale znany jest dostawca:

> W dokumencie nie widzę jednoznacznie wskazanego wystawcy. Dostawca to `<supplier_name>`. Przyjąć `issuer = <supplier_name>`?

Jeśli operator nie potwierdzi, poproś o właściwego wystawcę albo świadome pozostawienie pola pustego.

## Propozycja obszaru (gdy operator go nie podał)

> Dokument to karta charakterystyki, więc proponuję obszar **Jakość** [AREA_QUALITY]. Zostawić tak, czy dodać/zmienić obszar? (dostępne: Jakość, Zakupy, R&D / Rozwój produktu, Dokumentacja, Produkcja, Logistyka)

Listę dostępnych obszarów zawsze odczytaj live z `BD_document_areas` — powyższa jest przykładem, nie stałą.

## Preflight — nowy dokument

> Zamierzam utworzyć nowy dokument:
> - Surowiec: Algi brunatne [SUR__001]
> - Dokument: SDS — Algi brunatne — Dostawca X
> - Typ: Karta charakterystyki (SDS) [DT_SDS]
> - Obszar: Jakość [AREA_QUALITY]
> - Język: EN
> - Issuer: Alg-Borje AB
> - Dostawca: Alg-Borje AB
> - Required: TAK
> - Owner: operator@opcjanatura.pl
> - Plik: <nazwa źródła> (link z Drive) → kopia do dokumenty/ jako SUR__001__DOC_RM_012_v01_2026-08-28.pdf; oryginał zostaje na miejscu
> - Pierwsza wersja: v01
> Potwierdzasz zapis?

Jeśli plik przyszedł w rozmowie, linijka „Plik” brzmi:

> - Plik: <nazwa załącznika> (z rozmowy) → upload do dokumenty/ jako SUR__001__DOC_RM_012_v01_2026-08-28.pdf

## Preflight — nowa wersja (podmiana, jeden aktywny dokument)

> Dla Mleczanu sodu mam już aktywny SDS [DOC_RM_008]. Zamierzam dodać nową wersję:
> - Nowa wersja: v02
> - Nowy PDF trafi do folderu aktywnego
> - Poprzedni PDF (v01) trafi do _archive
> Potwierdzasz? (domyślnie archiwizuję poprzednią wersję)

## Preflight — nowa wersja (wybrany dokument spośród kilku aktywnych)

> Wskazałeś DOC_RM_008 (dostawca: Zrób Sobie Krem) jako dokument, którego dotyczy nowy plik.
> - Nowa wersja: v02
> - Nowy PDF trafi do folderu aktywnego
> - Poprzedni PDF (v01) — czy mam go zarchiwizować, czy zostawić aktywny obok nowej wersji?
> Potwierdzasz zapis i decyzję o archiwizacji?

## Sukces

Nowy dokument:

> Utworzono dokument DOC_RM_012 (typ: Karta charakterystyki (SDS), obszar: Jakość), wersja VER_RM_021 / DOC_RM_012_v01_2026-08-28. PDF zapisano w folderze aktywnym.

Nowa wersja z archiwizacją:

> Utworzono wersję VER_RM_022 / DOC_RM_008_v02_2026-08-28. Poprzedni PDF przeniesiono do _archive.

Nowa wersja bez archiwizacji:

> Utworzono wersję VER_RM_023 / DOC_RM_014_v02_2026-08-28. Poprzedni PDF (v01) pozostał aktywny, zgodnie z Twoją decyzją.

Archiwizacja:

> Zarchiwizowano dokument DOC_RM_012. Pozostaje widoczny w historii; aktualny PDF przeniesiono do _archive.

## Błąd

Podaj operatorowi konkretny etap i brak zmian końcowych, np.:

> Nie wykonałem operacji. Nie udało się utworzyć poprawnego PDF-u z podanego pliku. Baza nie została zmieniona.

Jeśli nie można zagwarantować rollbacku, opisz dokładnie, co zostało zapisane i czego nie udało się cofnąć. Nigdy nie używaj samego „wystąpił błąd”.
