---
name: opcja-natura-creative-brand
description: "Stosować zawsze, gdy powstaje coś, co ma wyglądać jak Opcja Natura: dokumenty biurowe i handlowe (oferta, cennik, zestawienie, tabela w Sheets/Excelu, one-pager dla partnera, raport, prezentacja, PDF dla klienta, formatowanie w Docs/Word) oraz materiały działu kreatywnego (posty, karuzele, stories, okładki rolek, reklamy, bannery, grafiki newsletterowe, druk, briefy foto/wideo, generowanie obrazów, audyt zgodności z marką). Daje kolory, krój pisma, zasady tabel i wykresów oraz brandbook 08.2026. Przy czystym copy bez decyzji wizualnych nie narzucać tone of voice, bo ten brandbook go nie definiuje."
---

# Opcja Natura Creative Brand

## Zasada nadrzędna

Traktować ten skill jako wizualny system marki Opcja Natura w stanie na **08.2026**.

- Stosować zasady wyłącznie w zakresie wspieranym przez brandbook.
- Nie dopowiadać zasad tone of voice, języka reklamowego, claimów produktowych ani compliance kosmetycznego, jeśli nie wynikają z innego aktywnego źródła.
- Nowsza, jawnie datowana instrukcja marki lub bezpośrednia instrukcja użytkownika ma pierwszeństwo przed snapshotem 08.2026.
- Nie przedstawiać obserwowanych parametrów technicznych PDF jako norm projektowych, jeśli brandbook ich nie ustanawia.

## Workflow

1. Rozpoznać typ zadania: **dokument** (biurowy/handlowy), **create**, **edit**, **review** albo **brief**.
2. Przy **dokumencie** przeczytać `references/dokumenty-biurowe.md` i to zwykle wystarcza. Przy pozostałych zawsze przeczytać `references/brand-guidelines-08-2026.md` przed podjęciem decyzji wizualnych.
3. Gdy potrzebne są dokładne tokeny, kody kolorów, warianty fontów lub strukturalne dane, przeczytać `references/brandbook-agent.json`.
4. Gdy potrzebny jest kontekst wizualny oryginalnych plansz, otworzyć `assets/brandbook-agent.html`. Nie ładować go rutynowo do kontekstu.
5. Wykonać zadanie zgodnie z hierarchią reguł i ograniczeniami poniżej.
6. Przed oddaniem wyniku zrobić krótki QA brandowy.

## Hierarchia decyzji

Stosować kolejno:

1. Bezpośrednia instrukcja użytkownika dla konkretnego materiału.
2. Nowszy oficjalny materiał marki, jeśli użytkownik go dostarczył.
3. Twarde zasady z brandbooka 08.2026.
4. Rekomendacje z sekcji „propozycje zmian” jako kierunek, nie jako bezwzględny obowiązek.
5. Własny osąd projektowy tylko tam, gdzie brandbook pozostawia lukę; nie przedstawiać takiego wyboru jako oficjalnej zasady marki.

## Reguły wykonawcze

### Typografia

- Traktować **New Spirit** jako główny krój display do nagłówków, haseł, CTA i krótkich wyróżnień.
- Traktować **Lato Regular** jako bazę tekstu długiego; używać Italic/Bold/Bold Italic do podkreślenia lub wzmocnienia części tekstu.
- Nie wprowadzać automatycznie Playfair Display jako głównego fontu. W brandbooku występuje niespójna wzmianka o Playfair, ale oficjalna sekcja „I krój pisma” definiuje New Spirit.
- Nie traktować `Editor` / `Edito` jako globalnego fontu marki; to niejednoznaczna wzmianka z kontekstu stories.
- Jeśli narzędzie generatywne nie gwarantuje konkretnego fontu, nie deklarować pełnej zgodności typograficznej. Zachować rolę i charakter typografii, a dokładny skład wykonać w narzędziu projektowym z właściwym fontem.
- Nie kopiować rozmiarów fontów wykrytych technicznie w PDF jako domyślnej skali typograficznej.

### Kolor

- Używać dokładnych kodów z `references/brand-guidelines-08-2026.md` lub JSON.
- Budować materiały przede wszystkim na ciepłej, jasnej bazie i kolorach ziemi/oliwki.
- Unikać przypadkowych, wysoko nasyconych kolorów, jeśli nie wynikają z konkretnego briefu użytkownika.

### Fotografia i grafika

- Preferować fotografie ciepłe, niskonasycone, ziarniste i jakościowe.
- Utrzymywać czystą, jasną bazę projektu.
- Dodawać analogowe elementy z umiarem: papier, tuszowe abstrakcyjno-organiczne malunki, ołówkowe zakreślenia, podkreślenia, strzałki, skany, wycinanki, gazetowość, mazy, plamy i kształty.
- Nie używać wszystkich motywów jednocześnie. Wybrać 1-2 środki pasujące do konkretnego materiału.
- Nie rekonstruować ani nie wymyślać logotypu. Jeśli oficjalny asset logo nie jest dostępny, zostawić miejsce na logo albo przygotować materiał bez niego, zamiast tworzyć pseudo-logo.

### Social media

- Dla okładek rolek brać pod uwagę tytuły w belkach, łączenie krojów i ołówkowe zakreślenia.
- Dla stories budować hierarchię krojów, łączyć Regular i Italic oraz używać kolorów marki.
- Interaktywne naklejki, pytania, linki i emotikony traktować jako narzędzia platformy, nie jako stałe elementy każdego projektu.
- Rekomendacje dotyczące spójnych okładek highlights, twarzy na wyróżnionych postach czy porządkowania relacji oznaczać jako kierunek z sekcji „propozycje zmian”, a nie obowiązkowy przepis.

## Tryby pracy

### Dokument

Najczęstszy przypadek: oferta, cennik, zestawienie, tabela, one-pager, raport, prezentacja. To nie projektowanie, tylko porządne formatowanie w barwach marki:

- jeden krój (Lato), białe tło, bordo jako kolor tekstu i nagłówków,
- tabele i wykresy według `references/dokumenty-biurowe.md`,
- kwoty i daty w polskim zapisie, kwoty z dopiskiem netto/brutto,
- dla klienta PDF, wewnątrz firmy plik edytowalny,
- bez analogowych motywów, ozdobników i wymyślonego logo.

Gdy dokument powstaje narzędziem (skill do docx/xlsx/pptx/pdf, Apps Script, eksport z Sheets), ten skill daje kolory i zasady, a tamto narzędzie mechanikę.

### Create

Tworząc nowy materiał:

- najpierw określić format, kanał i główny komunikat,
- zbudować prostą hierarchię: główny komunikat -> wsparcie -> CTA,
- wybrać paletę z brandbooka,
- wybrać właściwą rolę New Spirit/Lato,
- dobrać maksymalnie kilka analogowych akcentów,
- utrzymać delikatny, naturalny, niekrzykliwy charakter wizualny.

### Edit

Edytując istniejący materiał:

- zachować to, co już jest zgodne,
- zmieniać przede wszystkim elementy naruszające typografię, paletę, hierarchię lub język wizualny,
- nie przeprojektowywać materiału szerzej niż wymaga tego brief, chyba że użytkownik o to prosi.

### Review

W audycie używać trzech kategorii:

- **Zgodne** - znajduje bezpośrednie oparcie w brandbooku.
- **Do korekty** - stoi w sprzeczności z brandbookiem albo osłabia spójność.
- **Brak podstawy w brandbooku** - decyzja, której snapshot 08.2026 nie rozstrzyga.

Oddzielać błędy od preferencji projektowych.

### Brief

W briefie dla grafika, fotografa, montażysty lub generatora obrazu podawać tylko istotne dla zadania elementy systemu marki. Nie wklejać całego brandbooka, jeśli wystarczy zestaw konkretnych ograniczeń.

## QA przed oddaniem

Sprawdzić:

- czy użyta paleta należy do systemu marki,
- czy New Spirit i Lato pełnią właściwe role,
- czy materiał pozostaje jasny, naturalny i niekrzykliwy,
- czy analogowe dodatki są dawkowane z umiarem,
- czy fotografia nie jest nadmiernie nasycona lub „stockowo sterylna”,
- czy nie wprowadzono niepotwierdzonego logo, fontu lub nowej reguły marki,
- czy rekomendacje z brandbooka nie zostały błędnie przedstawione jako twarde zasady,
- czy ewentualne odstępstwo od brandbooka wynika z jawnej instrukcji użytkownika.

## Sposób raportowania

Przy zwykłym tworzeniu materiału nie dokładać długiego raportu zgodności. Jeśli występuje istotne ograniczenie, krótko wskazać je po wyniku, np. brak właściwego fontu lub brak oficjalnego assetu logo.

Przy audycie pokazać konkretne naruszenia i rekomendowane poprawki. Nie tworzyć sztucznych problemów tam, gdzie brandbook nie daje podstawy do oceny.

## Przykładowe zadania

- „Zrób z tej tabeli cennik dla hurtowni w PDF, w naszych kolorach.”
- „Sformatuj ten arkusz ze sprzedażą tak, żeby dało się go wysłać partnerowi.”
- „Przygotuj one-pager z warunkami współpracy dla apteki.”

- „Zrób okładkę rolki Opcja Natura o pielęgnacji skóry po lecie.”
- „Przygotuj karuzelę na Instagram zgodną z naszym brandingiem.”
- „Napisz brief do sesji produktowej w klimacie naszej marki.”
- „Przejrzyj tę reklamę Meta i powiedz, co wizualnie nie pasuje do Opcja Natura.”
- „Wygeneruj background do stories i zachowaj branding.”
- „Zaprojektuj sekcję landing page dla kampanii jesiennej.”
