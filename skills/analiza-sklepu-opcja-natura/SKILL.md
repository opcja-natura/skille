---
name: analiza-sklepu-opcja-natura
description: Jak analizować dane sklepu internetowego opcjanatura.pl (zamówienia, przychód, klientki nowe i powracające, program lojalnościowy Moja Opcja Natura, kody rabatowe i influencerskie, newsletter, próg darmowej dostawy) oraz jak odpowiadać na pytania o stan magazynu i planowanie produkcji (na ile wystarczy, ile doprodukować, kto z B2B już zamówił). Daje jedyne obowiązujące definicje metryk (słownik), mapę bazy z pułapkami, sprawdzone zapytania i metodę pracy: od pytania o decyzję, przez liczenie i sprawdzenie drugim sposobem, do wniosku po ludzku. Używaj ZAWSZE, gdy ktoś pyta o liczby sklepu www albo chce analizy („ile sprzedaliśmy”, „czy program lojalnościowy się opłaca”, „który kod działa”, „ile nowych klientek”, „jak poszedł newsletter”, „czy obniżyć próg dostawy”, „ile doprodukować”, „na ile wystarczy zapasu”), a także gdy liczby z różnych miejsc się nie zgadzają. NIE do sprzedaży B2B (skill analityka-b2b-zoho) ani do pojedynczych zamówień klientek w obsłudze.
---

# Analiza sklepu opcjanatura.pl

Na tych liczbach zarząd podejmuje decyzje. Dlatego liczysz **zawsze według słownika metryk** (`references/slownik-metryk.md`) i **sprawdzasz wynik drugim sposobem**, zanim go podasz. Liczba policzona „po swojemu”, choćby rozsądna, jest błędem, bo nie zgodzi się z dashboardami i z poprzednimi analizami.

## Zasady

1. **Definicje tylko ze słownika.** Przychód = netto **bez wysyłki**; zamówienie = opłacone lub doręczone (nigdy anulowane); doba i miesiąc = czas polski; klientka = e-mail. Gdy słownik czegoś nie rozstrzyga, powiedz to wprost, przyjmij najdosłowniejsze rozumienie i zapisz pytanie do Daniela.
2. **Dane z żywej bazy, tylko odczyt.** Baza sklepu jest produkcyjna: wyłącznie zapytania SELECT. Gdy nie masz dostępu do bazy, powiedz to i nie zgaduj liczb.
3. **Najpierw pytanie o decyzję.** Zanim policzysz, ustal, jaką decyzję ma wesprzeć analiza („czy przedłużyć współpracę z X”, „czy obniżyć próg”). Od tego zależy okres, porównanie i to, co pominąć.
4. **Porównuj uczciwie.** Ten sam okres tej samej długości albo te same dni tygodnia rok wcześniej; nigdy niepełny miesiąc z pełnym. Uwzględnij przełomy w danych (`references/baza-sklepu.md`, sekcja „Przełomy”).
5. **Sprawdź drugim sposobem.** Kluczową liczbę policz inną drogą (inne zapytanie, suma części = całość, porównanie z dashboardem Metabase). Jeśli się nie zgadza, nie podawaj jej, dopóki nie wiesz dlaczego.
6. **Związek to nie skutek.** Np. członkinie programu wracają częściej, ale część zapisuje się, bo już wraca. Mów „wiąże się z”, a nie „powoduje”, chyba że był test.
7. **Dwie różne zgody.** Zapis do programu lojalnościowego = zgoda na komunikację programu (np. przypomnienie o punktach). Newsletter = osobna zgoda (`email_optin`). Nie mieszaj ich.
8. **Bez danych osobowych w wynikach.** Agreguj. Listy e-maili tylko wtedy, gdy ktoś wprost prosi o listę do działania (np. przypomnienie o punktach), i tylko do tej osoby.

## Jak pracować

1. **Pytanie i decyzja.** Zapisz jednym zdaniem, co trzeba rozstrzygnąć. Postaw 2–3 hipotezy („skok kodów to jedna influencerka”, „to Black Week”).
2. **Definicje.** Znajdź w słowniku każdą metrykę, której użyjesz. Nowe pojęcie (np. „koszyk blisko progu”) zdefiniuj wprost w odpowiedzi.
3. **Liczenie.** Zacznij od gotowych zapytań (`references/zapytania.md`). Agreguj w SQL, nie ściągaj tysięcy wierszy.
4. **Kontrola.** Suma części = całość; porównanie z sąsiednimi okresami; drugi sposób dla kluczowej liczby; czy okno nie przechodzi przez przełom.
5. **Wniosek.** Najpierw odpowiedź na pytanie (2–3 zdania), potem liczby, potem zastrzeżenia, na końcu „co bym zrobiła / co sprawdzić”.

## Magazyn i planowanie produkcji

Pytania „ile mamy”, „na ile wystarczy”, „ile doprodukować” liczysz przez konektor **analityk**, według `references/magazyn-i-produkcja.md`. Trzy rzeczy, które najczęściej psują wynik:

- **Sklep pokazuje dzień zamówienia, magazyn dzień pakowania.** To te same sztuki; nie sumuj ich i nie porównuj dzień do dnia. Tempo i kształt sezonu bierz ze sklepu.
- **Tempo z promocji nie jest tempem bazowym.** Najpierw sprawdź, czy promocja trwa i do kiedy.
- **Zacznij odpowiedź od danych produktu** (pełna nazwa, SKU, EAN), policz w trzech wariantach, a pytania o plany (promocje, akcje B2B) zadaj na końcu, jeśli pytający ich nie podał.

## Jak podawać wynik

- Po ludzku: „co druga klientka”, „o jedną trzecią więcej”. Kwoty jako „47 871 zł”, procenty „8,1 %”.
- Zawsze okres i porównanie („18–24.11 wobec 11–17.11”).
- Zastrzeżenia krótko, przy liczbie, której dotyczą (np. „członkostwo to stan dzisiejszy”).
- Nie używaj nazw tabel ani kolumn w odpowiedzi dla osoby nietechnicznej; zostaw je w części „dla analityka”, jeśli ktoś o nią prosi.

## Kiedy się zatrzymać i zapytać

- Słownik nie definiuje potrzebnej metryki albo dwie definicje dają różne liczby.
- Wynik różni się od dashboardu Metabase o więcej niż 0,5 % i nie umiesz wskazać przyczyny.
- Pytanie dotyczy kosztów, których nie ma w bazie (realny koszt kuriera, opłaty dla influencerek, koszt pracy) — powiedz, czego brakuje, i policz scenariusze zamiast zgadywać.

## Materiały

- `references/slownik-metryk.md` — **jedyne definicje** (przychód, klientki, program, kody, okresy, newsletter, formaty).
- `references/baza-sklepu.md` — tabele, klucze, pułapki, przełomy w danych.
- `references/magazyn-i-produkcja.md` — konektor „analityk”: źródła, pułapki, tok liczenia doprodukcji, przykład.
- `references/zapytania.md` — sprawdzone zapytania (przychód w okresie, nowe/powracające, powroty z punktami, kody influ, newsletter, wygasanie punktów, rozkład koszyków).
