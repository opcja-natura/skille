# Algorytm TikToka — wersja operacyjna (do diagnoz, nie do wykładów)

Destylat z raportu "Algorytm TikToka: research pogłębiony" (07/2026; źródła: oficjalne
materiały TikToka, wyciek "TikTok Algo 101"/NYT, śledztwo WSJ, audyty akademickie
2022–2025). Poziomy pewności: [W] potwierdzone oficjalnie/badawczo, [Ś] prawdopodobne,
[N] hipoteza branżowa. W rozmowie z Agatą nie cytuj poziomów — używaj ich do ważenia
własnych rekomendacji.

## Co naprawdę decyduje o dystrybucji

- [W] Trzy grupy sygnałów: zachowania widzów (oglądanie, pominięcia, lajki, komentarze,
  udostępnienia, zapisy, follow, "nie interesuje mnie"), informacje o filmie (opis,
  dźwięk, hashtagi, tekst), ustawienia konta/urządzenia (język, kraj — niska waga).
- [W] Obejrzenie do końca = jeden z najsilniejszych sygnałów. [Ś] Czas przy filmie
  (lingering, rewatch, pauza) to praktycznie waluta platformy (WSJ; replikacja audytu
  2025: akcja oglądania daje najsilniejszą personalizację).
- [W] Liczba obserwujących i historia konta NIE są bezpośrednimi czynnikami rankingu
  filmu. Konto działa pośrednio (returning viewers, spójność tematyczna) — podnosi
  podłogę wyników, nie sufit. Dowód wewnętrzny: 402k na koncie z 2,3k obserwujących.
- [W] System celowo dywersyfikuje feed (nie dwa filmy z rzędu z tym samym dźwiękiem/
  twórcą; wtrącanie treści spoza zainteresowań) — dlatego trendujący dźwięk nie
  gwarantuje niczego.
- [Ś] Nadrzędna optymalizacja platformy: retencja użytkownika + czas spędzony
  (wyciek "TikTok Algo 101"). Scoring ≈ ważona suma przewidywanych interakcji.

## Pierwsza pula i "batch testing"

- [N] Model "200–500 wyświetleń testowych i progi" to folklor branżowy — liczb nikt
  nie potwierdził. [Ś] Kierunkowo prawdziwe jest, że pierwsza, mała dystrybucja
  dostarcza dane do decyzji o dalszej — dlatego hook i pierwsze sekundy mają
  nieproporcjonalne znaczenie.
- Film "stojący" na 35–500 odtworzeniach = normalny wynik nieprzekroczenia benchmarku
  retencji w pierwszej puli, nie kara ani awaria.
- [Ś] "Drugie życie" filmu po dniach/tygodniach istnieje (search, udostępnienia,
  ponowny sampling) — nie kasować słabych filmów; ewentualnie prywatyzować.

## Interpretacja metryk (tryb "czemu nie działa")

Kolejność diagnozy:
1. **Retencja po 3 s** < ~70% → problem hooka/pierwszej klatki. Napraw pierwsze zdanie.
2. **Krzywa retencji** — znajdź sekundę odpływu i przeczytaj, co tam pada w filmie
   (dygresja? zmiana tematu? spadek tempa?). To jedyna metryka, którą warto pokazać
   Agacie wprost, bo mapuje się na treść.
3. **Completion** — porównuj tylko w obrębie podobnej długości. 46 s z 40% completion
   bije 15 s z 55%.
4. **Zapisy i udostępnienia /1000** — miara użyteczności; niskie przy dobrej retencji =
   brakuje konkretu wartego zachowania.
5. **Follow /1000** — miara relacji; niskie = film dobry, ale bez obietnicy serii.
6. **Źródła ruchu** — rosnący udział wyszukiwania w starszych filmach = SEO działa.
7. **0 komentarzy** = brak pytania na końcu albo pytanie retoryczne.

Kalibracja: cold start 4–8 tygodni; sukces tygodnia = mediana odtworzeń rośnie
i kolejne filmy przebijają ~500 odtworzeń częściej niż poprzednie.

## Mity — szybkie odpowiedzi (gdy Agata o nie pyta lub się nimi martwi)

- "Shadowban" → nie istnieje jako kara za słabe wyniki; istnieje stan "nieuprawnione
  do rekomendacji" za konkretne naruszenia (drastyczność, spam, engagement bait,
  watermarki, duplikaty) — widoczny w analityce filmu, z możliwością odwołania.
  99% słabych wyników to po prostu retencja poniżej benchmarku.
- "Liczy się pierwsza godzina" → nie; ocena jest ciągła, drugie życie udokumentowane.
- "Trzeba codziennie" → każdy film oceniany osobno; kadencja pomaga uczyć się szybciej,
  ale 3–5 dobrych/tydzień > 7 wymuszonych. (U Agaty kadencja dzienna działa — utrzymać,
  dopóki nie ciąży.)
- "Konto firmowe ma gorsze zasięgi" → brak dowodów na karę; realna różnica to uboższa
  biblioteka muzyki komercyjnej. Rozwiązanie: oryginalne audio z mówioną frazą.
- "Hashtagi robią zasięg" → klasyfikują temat i wspierają wyszukiwanie; nie ratują
  słabego hooka.

## TikTok jako wyszukiwarka (SEO)

- [Ś] Duża część odbiorców (zwłaszcza młodszych) szuka bezpośrednio w TikToku;
  w beauty discovery przez social jest szczególnie silne. Filmy "jak / czy / co to"
  mają drugą ścieżkę dystrybucji, niezależną od feedu.
- Warstwy indeksacji: mowa (transkrypcja auto-napisów) ≥ tekst na ekranie > opis >
  hashtagi > komentarze. Stąd żelazna zasada: fraza kluczowa wypowiedziana na głos
  w pierwszych 2 s + w tekście na ekranie + w opisie.
- Frazy brać z realnych zapytań: Creator Search Insights (w aplikacji) + podpowiedzi
  paska wyszukiwania; uzupełniająco Answer the Public / Google Trends (workflow Daniela).
- Treści evergreen (składniki, "jak czytać INCI") pracują tygodniami przez search —
  oceniać je po 30 dniach, nie po 48 h.

## Eligibility — czego pilnować, żeby film w ogóle wszedł do rekomendacji

- Zakazane/ograniczane: watermarki innych platform, re-uploady 1:1, engagement bait
  ("skomentuj X a..."), clickbait wprowadzający w błąd, sztuczne interakcje, spam
  publikacyjny, treści drastyczne.
- Kosmetyki: obietnice terapeutyczne mogą podpaść pod polityki dezinformacji medycznej
  TikToka i prawo o oświadczeniach (szczegóły i bezpieczne sformułowania:
  `checklisty.md`). Przy tematach typu łuszczyca/AZS: opisujemy skórę i mechanizm,
  nie chorobę i wyleczenie.

## Katalog formatów (skrót; pełna wersja: raport, sekcja M)

Najwyższa oczekiwana wartość dla manufaktury: (a) proces produkcji jako mikrohistoria
z napięciem ("ta partia prawie poszła do kosza"), (b) jeden składnik / jeden film pod
search, (c) Q&A ze screenshota pytania klientki, (d) mit vs fakt okiem biologa,
(e) seria "od receptury do słoika" (returning viewers), (f) "nie kupuj tego u nas,
jeśli..." (odwrócona sprzedaż), (g) test na żywo / przetestujmy razem, (h) duet/stitch
z zielarkami z listy kampanii. Produktowe wideo działa, gdy zaczyna od problemu widza
i tłumaczy mechanizm (wzorzec własnego hitu 402k).
