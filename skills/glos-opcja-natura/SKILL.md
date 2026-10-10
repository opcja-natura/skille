---
name: glos-opcja-natura
description: Pisanie prozy marki Opcja Natura po polsku głosem człowieka, nie AI. Używaj ZANIM napiszesz jakąkolwiek treść marketingową/redakcyjną w tym repo — odpowiedzi FAQ, opisy produktów, posty, fragmenty bloga/newslettera, treści na stronę. Triggeruj też, gdy tekst „brzmi robotycznie", gdy ktoś prosi „napisz to głosem marki", „przepisz mniej sztucznie", „zhumanizuj", albo gdy zaraz wygenerujesz proze, którą i tak trzeba by potem poprawiać ręcznie. NIE do: doradztwa pielęgnacyjnego (naturalna-pielegnacja), angielskiego (tlumaczenia-opcja-natura), lookupu danych produktu (produkty-lookup), technicznego schematu FAQ JSON (FORMAT_faqJSON.md). Ten skill daje GŁOS; format/pakowanie to osobna sprawa.
type: skill
---

# Głos Opcji Natury — proza marki, po polsku, po ludzku

Ten skill ładuje istniejący system głosu Opcji Natury do Twojego kontekstu **zanim** zaczniesz pisać. Problem, który rozwiązuje: treść pisana „na zimno" (bez tego systemu) brzmi jak AI i wymaga drugiego, marnotrawnego passu humanizacji. Jeśli głos jest w kontekście od pierwszego zdania — pierwsza wersja ma brzmienie, a pas mechaniczny na końcu tylko sprząta typografię.

> **Kluczowa kolejność (nie odwracaj):** GŁOS najpierw (manifest + wiedza o kliencie), MECHANIKA na końcu (`humanizer.md`). Wyczyszczona typograficznie sztampa to dalej sztampa — humanizer nie buduje głosu, robi to manifest i człowiek.

---

## Kanon — wskazuje, nie kopiuje

Nie duplikujemy tych plików do skilla (to psuje kanon). Czytasz je w repo w momencie pisania:

| Plik (ścieżka w repo) | Po co go wczytać |
| :-- | :-- |
| `00_o_marce/brand_dna.md` | fundament: tożsamość, zakazy językowe, mechanizm wyjaśniania składników |
| `projekty_claude/contentWriter/MANIFEST_glosu.md` | **serce głosu** — 8 przykładów „encyklopedia → człowiek" + 3 filtry |
| `00_o_marce/wiedza_o_kliencie.md` | do kogo piszesz: segment, jego lęk, technika komunikacji |
| `projekty_claude/contentWriter/FORMAT_faqJSON.md` | gdy piszesz FAQ (schemat + ton odpowiedzi 4–6 zdań) |
| `projekty_claude/contentWriter/FORMAT_blog.md` / `FORMAT_seo.md` / `FORMAT_newsletter.md` / `FORMAT_stronaProduktu.md` | gdy piszesz odpowiednio bloga / SEO / newsletter / stronę produktu |
| `projekty_claude/contentWriter/humanizer.md` | pas mechaniczny na sam koniec (typografia + polskie AI-frazy) |
| `00_o_marce/produkty.json` | gdy pada konkretny kosmetyk — skład i dane stamtąd, nie z głowy |

Uwaga: `projekty_claude/contentWriter/` to projekt zespołu na claude.ai — **czytaj, nie modyfikuj**. Ten skill jest jego „ zdalną końcówką" w repo: ta sama wiedza, dostępna agentowi pracującemu tutaj.

---

## Rdzeń głosu (destylat — masz go od ręki, bez czytania plików)

To skrót; przy realnym pisaniu i tak wczytaj `MANIFEST_glosu.md` po pełne przykłady.

### Trzy filtry — każde zdanie przez nie przechodzi
1. **Mówię to JA, do Ciebie.** Człowiek podpisany na blogu, nie encyklopedia. Może się czymś jarać, czegoś nie rozumieć, pokazać siebie. Druga osoba: „masz", „zatka Ci", „znasz to uczucie".
2. **Co czytelnik zyska z tego zdania?** Decyzję, spokój, konkret. Jeśli nie wiesz — piszesz encyklopedię na zlecenie.
3. **Czy to mogła napisać konkretnie Opcja Natura?** Jeśli zdanie pasuje też do Avonu i Yves Rocher — nie jest nasze. Przepisz albo usuń.

> Metafora robocza: piszesz tak, jakbyś tłumaczyła to znajomej w kuchni przy herbacie, która właśnie kupiła olej kokosowy i pyta, czy dobrze zrobiła. Powiesz jej prawdę, nawet jeśli źle. I dorzucisz coś od siebie — bo lubisz z nią gadać.

### Osiem ruchów „encyklopedia → człowiek" (skrót z manifestu)
- **Strona bierna → człowiek robiący coś.** „był używany" → kto, kiedy, po co. Wstaw obraz.
- **„Dla skóry X" → „Jeśli masz skórę X".** Mówisz *do niej*, nie *o niej*.
- **Liczba sucho → liczba z intuicją.** „32%" → „3 razy lepiej" — ale **liczbę zostaw** dla wiarygodności, dokładasz przekład, nie zastępujesz.
- **Termin techniczny → most do doświadczenia.** „zmęczenie hygralne" → „znasz to, gdy po trzecim myciu włosy jak słoma?". Ekspert, który mówi zrozumiale.
- **Lista cech → lista decyzji.** Nie „Virgin: tłoczony na zimno, polifenole" → „Virgin — wybierz, gdy chcesz pełni działania". Cecha jako argument, nie wykład.
- **Akapit jednolity → akapit z oddechem.** Krótkie, krótkie, pytanie, odpowiedź, fakt. Monotonny rytm usypia.
- **Wstęp tezowy → wstęp sceną.** „Historia olejku…" → „Na Sri Lance kobiety codziennie…". Hook w pierwszych 3 słowach.
- **Domknięcie podsumowaniem → domknięcie postawą.** Nie „A Ty? 🥥✨", tylko odważne zdanie z charakterem: „Skóra sucha — tak. Skóra tłusta — nie."

### Nasza szczerość = autorytet
Pokazuj ograniczenia. „Dla tej skóry to nie jest dobry wybór" buduje zaufanie mocniej niż dziesięć zachwytów. Marketing zachwala wszystko; rzemiosło mówi „nie dla Ciebie". Mechanizm zamiast ogólnika: „lanolina spowalnia parowanie wody z naskórka" > „intensywnie nawilża".

### Słowa (twarde)
- Zawsze **„kosmetyk"**, nigdy „produkt" (to słowo marki, nie synonim do wymieniania).
- **Zakazane:** premium, innowacyjny, kompleksowy, holistyczny, rewolucyjny, kluczowy, doskonały, wyjątkowy, „skuteczny" bez mechanizmu; czasowniki: zapewnia, zdecydowanie.
- **Bez negatywnego różnicowania** („bez zbędnej chemii", atak na konkurencję).

### Polskie AI-flagi (przepisz na konkret, nie na synonim)
„stanowi", „odgrywa kluczową rolę", „warto pamiętać", „należy podkreślić", „jak widać", „w dzisiejszych czasach"; gerundium-ogon („…nawilżając skórę, wspierając regenerację…"); przeczące paralelizmy („to nie tylko krem, to rytuał"); reguła trójki jako ozdobnik; cykl synonimów (krem→kosmetyk→preparat→specyfik).

> **Rytm ≠ AI-cliché.** Świadome powtórzenie bywa u nas narzędziem („Skóra sucha — tak. Skóra tłusta — nie."; „Proste? Proste, bo Natura to proste!"). Test: przeczytaj na głos. **Wada męczy, rytm niesie.** Tniesz wytarty schemat, zostawiasz mówienie z przekonaniem.

---

## Procedura (proporcjonalnie — nie klon checklisty)

1. **Ustal format i odbiorcę.** Jaki format (FAQ / opis / post / blog / newsletter)? Kto czyta i **czego się boi** (`wiedza_o_kliencie.md`)? Bez odbiorcy piszesz do nikogo.
2. **Wczytaj kanon** z tabeli wyżej: zawsze `brand_dna.md` + `MANIFEST_glosu.md` + `wiedza_o_kliencie.md`; do tego właściwy `FORMAT_*`; `produkty.json` jeśli pada konkretny kosmetyk. Nie polegaj na pamięci — wczytaj.
3. **Materiał wystarczający?** Jak w instrukcjach contentWritera: jesteś pomocą, nie fabryką. Słaby materiał = słaby tekst; lepiej dopytać (maks 2–3 pytania) niż poprawiać na końcu.
4. **Pisz z trzema filtrami.** Mechanizm zamiast ogólnika, liczba zostaje z przekładem, pokazuj ograniczenia, druga osoba, oddech w rytmie.
5. **Audyt AI (obowiązkowy, 3 pytania — szczegóły w `instrukcje.md` Krok 5):** (a) co tu zdradza AI? (b) czy każde zdanie mogła napisać konkretnie Opcja Natura? (c) czy jest choć jedno zdanie z informacją, której nie ma w każdym innym artykule? Nanieś poprawki pozytywnie (wróć do manifestu), nie tylko wycinaj.
6. **Humanizer na końcu.** Dopiero teraz `humanizer.md` — typografia (myślniki < ~10/tekst, cudzysłowy „takie"), artefakty czatu, polskie AI-frazy. To pas porządkowy, nie redakcyjny. **Nie wycina konkretów** (liczby, składniki, nazwy zostają).
7. **Człowiek robi ostateczny szlif.** Nie udawaj, że go zastępujesz — flaguj do człowieka (przy treściach o recepturach: fact-check Agaty).

---

## Granice (żeby się nie nakładać)
- **Doradztwo pielęgnacyjne / dobór rytuału** → `naturalna-pielegnacja`.
- **Angielski** → `tlumaczenia-opcja-natura`.
- **Dane produktu (cena, skład, INCI)** → `produkty-lookup` / `produkty.json`.
- **Techniczny schemat FAQ JSON** (pola, linki, brak markdown) → `FORMAT_faqJSON.md`. Ten skill daje *głos* odpowiedzi; tamten daje *opakowanie*.
- **Briefy SEO dla copywritera** → `wytyczne-seo-blog`. **Draft bloga do Contentful** → `blog-draft-opcja-natura`.

---

*glos-opcja-natura — wersja 1.0 | Opcja Natura 2026 | zdalna końcówka systemu głosu z projektu contentWriter (czytaj, nie modyfikuj kanonu)*
