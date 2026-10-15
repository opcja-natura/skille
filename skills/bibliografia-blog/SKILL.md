---
name: bibliografia-blog
description: Wyszukiwanie, weryfikacja i formatowanie źródeł naukowych do wpisów blogowych Opcji Natury. Używaj zawsze gdy operator prosi o znalezienie badań pod konkretny artykuł, gdy mapujesz tezy z gotowego tekstu do publikacji naukowych, gdy konwertujesz listę źródeł do JSON-a Contentful, lub gdy weryfikujesz wiarygodność cytowanych badań. Zawiera pełny pipeline (research → mapowanie tez → JSON), kryteria jakości źródeł, hierarchię typów badań, limity ilościowe i schemat Contentful. Research wyłącznie przez MCP Consensus — nie używaj web_search ani innych narzędzi do wyszukiwania badań.
---

# SKILL — Bibliografia naukowa do bloga Opcji Natury

Używaj tego skilla zawsze gdy pracujesz ze źródłami naukowymi pod wpisy blogowe — od momentu, w którym dostajesz draft tekstu, aż do gotowego JSON-a do pola `sources` w Contentful.

Skill obsługuje trzy scenariusze:
1. **Pełny pipeline** — dostajesz tekst bez źródeł, masz znaleźć i sformatować.
2. **Sama konwersja** — dostajesz listę źródeł w markdown, masz przerobić na JSON.
3. **Walidacja** — dostajesz istniejące źródła, masz sprawdzić czy realnie wspierają tezy.

Pełna specyfikacja formatu JSON: `json_bibliografia.md` w pamięci projektowej / uploadach.

---

## Narzędzie do researchu: tylko MCP Consensus

**Do wyszukiwania badań naukowych używaj wyłącznie `Consensus:search`.**

- Nie używaj `web_search` do szukania publikacji naukowych.
- Nie używaj `web_fetch` do otwierania abstraktów z Google Scholar, ResearchGate, Sci-Hub ani innych agregatorów.
- Nie korzystaj z innych baz przez interfejs webowy.

Powód: Consensus zwraca ustrukturyzowane wyniki z recenzowanych publikacji (200M+ prac), z metadanymi i scoringiem zgodności. To jedyne narzędzie zapewniające powtarzalną jakość researchu pod kosmetyczny content. Inne narzędzia wprowadzają szum (treści sponsorowane, blogi, fora) i ryzyko źródeł z drapieżnych wydawnictw.

Wyjątek: jeśli operator sam podaje konkretny DOI lub link do publikacji i prosi o weryfikację — wtedy możesz użyć `web_fetch` na ten konkretny URL.

---

## Filozofia: lepiej mniej i mocniej

Bibliografia ma uwiarygadniać tekst, nie udawać pracy magisterskiej. Trzy zasady fundamentalne:

1. **Jakość ponad ilość.** Pięć przeglądów z renomowanych czasopism > dziesięć przypadkowych prac z drapieżnych wydawnictw.
2. **Każde źródło musi coś robić w tekście.** Jeśli nie wspiera konkretnej tezy z artykułu — nie ma go na liście.
3. **Czytelnik nie weryfikuje, ale instytucja partnerska może.** Sieć aptek, sklep ekologiczny, dziennikarz piszący o kosmetyku — wszyscy mogą zajrzeć w bibliografię. Musi się obronić.

---

## Ile źródeł — wytyczna ilościowa

**Standard dla bloga Opcji Natury: 5–8 źródeł na artykuł ~1000 słów.**

| Długość artykułu | Optymalna liczba źródeł |
|---|---|
| 600–900 słów | 4–6 |
| 900–1300 słów | 5–8 |
| 1300–1800 słów | 7–10 |
| 1800+ słów | 8–12 |

**Czerwone flagi:**
- 10+ źródeł przy ~900 słowach → wygląda na nadgorliwość lub brak selekcji (sygnał AI)
- 1–2 źródła przy artykule edukacyjnym o składniku → za mało żeby cokolwiek udowodnić
- Wszystkie źródła z tego samego roku i czasopisma → przypadkowy zrzut z jednej kwerendy

---

## Hierarchia wiarygodności źródeł

**Priorytetyzuj zgodnie z piramidą evidence-based:**

```
1. Meta-analizy i przeglądy systematyczne (Cochrane, PubMed Reviews)
        ↓
2. RCT (Randomized Controlled Trials) — badania kliniczne na ludziach
        ↓
3. Przeglądy narracyjne / mechanism reviews (np. "The Role of X in skin")
        ↓
4. Badania kliniczne nierandomizowane
        ↓
5. Badania in vivo na zwierzętach
        ↓
6. Badania in vitro (komórki, linie komórkowe)
```

**Dla bloga Opcji Natury najczęściej trafia w sedno mix:**
- **1 review/meta-analiza** jako rama mechanizmu (np. "jak działa witamina C na skórę")
- **2–3 badania kliniczne / RCT** jako dowód działania na ludziach
- **1–2 przeglądy specjalistyczne** dla konkretnego składnika (np. olej z rokitnika)
- Reszta: badania uzupełniające mechanizm

**Unikaj jako jedynego źródła:**
- Badań in vitro — pokazują potencjał, nie efekt na skórze
- Badań na zwierzętach przy tezach o skuteczności u ludzi
- Prac z czasopism predatory (sprawdź na Beall's List / DOAJ)

---

## Akceptowane bazy i czasopisma

**Zielona lista — pełne zaufanie:**
- PubMed / PMC (NCBI)
- Cochrane Library
- Nature, Science, NEJM, Lancet
- Czasopisma MDPI w obszarze kosmetologii: *International Journal of Molecular Sciences*, *Antioxidants*, *Nutrients*, *Cosmetics*, *Biomedicines*, *Plants*, *Pharmaceutics*
- Frontiers (*Frontiers in Pharmacology*, *Frontiers in Medicine*)
- *Journal of Cosmetic Dermatology*, *International Journal of Cosmetic Science*, *Clinical, Cosmetic and Investigational Dermatology*
- *American Journal of Clinical Dermatology*
- *Journal of Investigative Dermatology*

**Żółta lista — używaj, ale weryfikuj kontekst:**
- Pojedyncze case studies — OK jako ilustracja, nie jako dowód
- Konferencyjne abstrakty — tylko jeśli nie ma pełnej publikacji

**Czerwona lista — odrzuć:**
- Strony producentów kosmetyków
- Blogi, portale lifestyle, Wikipedia
- Wydawnictwa z Beall's List of Predatory Journals
- Treści sponsorowane bez peer review
- Źródła starsze niż 25 lat (chyba że to klasyk cytowany w nowszych pracach — np. Hoppe 1999 o Q10)

---

## Pełny pipeline — od tekstu do JSON

### Krok 1 — Czytaj tekst i wyodrębnij tezy do udowodnienia

Przejdź artykuł od początku do końca i wynotuj **konkretne stwierdzenia merytoryczne** — te, które mówią "X działa tak, bo Y" albo "składnik A robi B". Pomijaj zdania marketingowe.

**Przykład z artykułu o żelu intymnym z biofermentem:**

> Teza 1: Lactobacillus dominuje w zdrowej mikroflorze pochwy i utrzymuje kwasowe pH.
> Teza 2: Kwas mlekowy ma działanie mikrobójcze i utrzymuje pH chroniące przed patogenami.
> Teza 3: Postbiotyki wspierają zdrowie skóry przez wpływ na mikrobiom.
> Teza 4: Postbiotyki znajdują zastosowanie w preparatach na schorzenia skóry.
> Teza 5: Definicja postbiotyków i ich miejsce w kosmetyce/medycynie.

Każda teza → jedno źródło (lub więcej, jeśli pasują).

### Krok 2 — Szukaj w MCP Consensus

Używaj wyłącznie narzędzia `Consensus:search` — przeszukuje 200M+ recenzowanych prac.

**Zasady zapytań:**
- Po angielsku, terminologia naukowa: nie "witamina C na zmarszczki" tylko "ascorbic acid skin aging topical"
- Łącz mechanizm + efekt: "lactic acid vaginal pH antimicrobial"
- Dodawaj typ badania jeśli szukasz konkretu: "rosehip oil scars clinical trial"
- Jeśli pierwsza kwerenda zwraca słabe wyniki — rozszerz, nie zawężaj
- Jedna kwerenda = jedna teza. Nie łącz wielu tez w jednym zapytaniu.

**Przykładowe queries dla tez powyżej:**
- Teza 1 → `Lactobacillus vaginal microbiome pH`
- Teza 2 → `lactic acid vaginal antimicrobial microbicidal`
- Teza 3 → `postbiotics skin health microbiome`
- Teza 4 → `postbiotics topical skin conditions treatment`
- Teza 5 → `postbiotics definition ISAPP`

### Krok 3 — Selekcja

Dla każdej tezy wybierz **1 źródło** (czasem 2, jeśli mechanizm wymaga dwóch warstw — np. badanie in vitro + RCT potwierdzający).

Kryteria selekcji w kolejności:
1. **Czy abstract realnie popiera tezę?** Sprawdź — nie zakładaj na podstawie tytułu.
2. **Typ badania** — review/meta > RCT > badanie kliniczne > in vitro
3. **Renoma czasopisma** — patrz zielona lista
4. **Świeżość** — preferuj <10 lat, klasyki <25 lat
5. **Cytowania / impact** — Consensus pokazuje ranking

### Krok 4 — Walidacja: czy źródło naprawdę popiera tezę?

To krytyczny krok. **Czytaj abstract, nie tylko tytuł.**

Trzy pytania kontrolne dla każdego źródła:
- Czy autorzy badają to, o czym mówi tekst — czy tylko coś podobnego?
- Czy wnioski badania idą w kierunku tezy, czy są neutralne lub sprzeczne?
- Czy próba badawcza pasuje do kontekstu (ludzie, skóra, kosmetyk topikalny) — czy to in vitro/na myszach, a tekst opisuje efekt u ludzi?

Jeśli źródło nie przechodzi tych pytań → odrzuć, szukaj dalej.

### Krok 5 — Mapowanie i prezentacja operatorowi

Przed konwersją do JSON pokaż tabelę mapowania:

```markdown
| Teza w artykule | Źródło | Co potwierdza |
|---|---|---|
| Lactobacillus dominuje w zdrowej mikroflorze | Amabebe & Anumba (2018) | Fizjologiczna rola Lactobacillus w środowisku pochwy |
| Kwas mlekowy ma działanie mikrobójcze | O'Hanlon et al. (2013) | Mikrobójcze pH przy dominacji Lactobacillus |
```

To pozwala zweryfikować dopasowanie zanim przejdziemy do publikacji.

### Krok 6 — Konwersja do JSON Contentful

Po akceptacji mapowania — przerób na format JSON zgodny ze schematem Contentful.

---

## Schemat JSON (Contentful)

**Format jedyny dopuszczalny:**

```json
[
  {
    "authors": "Mohania D. et al.",
    "year": 2017,
    "title": "Ultraviolet Radiations: Skin Defense-Damage Mechanism",
    "journal": "Advances in Experimental Medicine and Biology"
  }
]
```

### Twarde zasady (zero wyjątków)

1. **Dokładnie te klucze, w tej kolejności:** `authors`, `year`, `title`, `journal`. Każdy obiekt — ten sam kształt (wymóg Gatsby). **Bez klucza `url` — pole nie istnieje w schemacie.**
2. **`year` to liczba** (bez cudzysłowów), pozostałe pola — stringi.
3. **Żadnych linków, DOI ani pola `url`** — nawet jeśli Consensus zwraca pewny DOI/PubMed. Wyniki Consensus mają DOI w metadanych; ignoruj je przy budowie JSON-a. Klucza `url` po prostu nie dodawaj.
4. **`title` bez kropki na końcu**, bez kursywy, bez gwiazdek.
5. **`journal` — sama nazwa czasopisma**: bez kropki, bez `*`, bez roku.
6. **`authors` przepisz 1:1** z listy źródłowej — zostaw "et al.", inicjały, kropki.
7. **Zachowaj kolejność źródeł z artykułu** (kolejność cytowania).
8. **Wynik = sama tablica JSON**, poprawna składniowo, gotowa do wklejenia.

### Mapowanie wpisu markdown → JSON

Wzór wejścia:
```
Mohania D. et al. (2017). Ultraviolet Radiations: Skin Defense-Damage Mechanism. *Advances in Experimental Medicine and Biology.*
```

Rozkład:
- `authors` → `Mohania D. et al.`
- `year` → `2017` (liczba)
- `title` → `Ultraviolet Radiations: Skin Defense-Damage Mechanism` (bez kropki)
- `journal` → `Advances in Experimental Medicine and Biology` (bez kropki, bez *)
- (klucza `url` nie dodajemy — schemat ma 4 pola)

### Jeśli artykuł nie ma sekcji źródeł

Zwróć pustą tablicę `[]` albo pomiń pole — **nie wymyślaj źródeł.**

---

## Najczęstsze błędy

| Błąd | Poprawka |
|---|---|
| Dodany klucz `url` (np. z DOI Consensus) | Schemat ma 4 klucze — `url` nie istnieje, nie dodawaj |
| Research przez web_search zamiast Consensus | Wyłącznie `Consensus:search` |
| Kropka na końcu `title` lub `journal` | Usuń |
| Kursywa/gwiazdki w polach JSON | Czysty tekst |
| `year` jako string `"2017"` | Liczba `2017` |
| Niespójny kształt obiektów | Wszystkie obiekty mają te same 4 klucze: `authors`, `year`, `title`, `journal` |
| 10+ źródeł przy 900 słowach | Selekcja: zachowaj 5–8 najmocniejszych |
| Wszystkie źródła in vitro przy tezach o efekcie na skórze | Dodaj RCT / badania kliniczne |
| Źródło z drapieżnego czasopisma | Sprawdź Beall's List, zamień na publikację z zielonej listy |
| Tytuł abstractu pasuje, ale wnioski nie | Czytaj abstract w całości, nie tylko tytuł |
| Polskie znaki diakrytyczne źle escape'owane | Zostaw natywne `ą ć ę ł ń ó ś ź ż`, nie escape'uj |

---

## Mini-checklist przed oddaniem JSON-a

- [ ] Research zrobiony wyłącznie przez `Consensus:search`
- [ ] Każdy obiekt ma 4 klucze: `authors`, `year`, `title`, `journal`
- [ ] Żaden obiekt nie zawiera klucza `url` (ani innych dodatkowych pól)
- [ ] Kolejność kluczy identyczna we wszystkich obiektach
- [ ] `year` jako liczba, nie string
- [ ] `title` bez kropki, bez kursywy
- [ ] `journal` bez kropki, bez `*`, bez roku
- [ ] `authors` 1:1 z oryginalnej listy
- [ ] Kolejność źródeł zgodna z artykułem
- [ ] JSON się parsuje
- [ ] Liczba źródeł adekwatna do długości artykułu (patrz tabela)
- [ ] Brak źródeł z czerwonej listy / predatory journals
- [ ] Każde źródło realnie wspiera konkretną tezę z tekstu
- [ ] Mix typów badań pasuje do charakteru artykułu (review + RCT + mechanism)

---

## Workflow w jednym diagramie

```
draft artykułu
        ↓
wyodrębnij tezy (Krok 1)
        ↓
Consensus:search per teza (Krok 2)
        ↓
selekcja: 1 źródło / teza (Krok 3)
        ↓
walidacja abstract → teza (Krok 4)
        ↓
tabela mapowania → operator akceptuje (Krok 5)
        ↓
konwersja markdown → JSON Contentful (Krok 6)
        ↓
checklist → oddaj
```

---

## Zasady pracy

- Jeśli artykuł ma tezy bez pokrycia w żadnym badaniu — **zgłoś to operatorowi**, nie udawaj że znalazłeś źródło. Lepiej zaproponować przeformułowanie tezy niż naciągnąć bibliografię.
- Jeśli w tekście pojawia się konkretna liczba/procent bez źródła, której literatura nie potwierdza — **flaguj do weryfikacji**, nie szukaj na siłę uzasadnienia.
- Przy 5+ źródłach pokazuj tabelę mapowania zanim przejdziesz do JSON-a. Przy konwersji 1:1 z gotowej listy markdown — od razu JSON.
- Jeśli operator daje gotową listę markdown do konwersji — pomijasz Kroki 1–5, robisz tylko Krok 6.

---

*SKILL.md — bibliografia-blog | Opcja Natura 2026*
*Format JSON Contentful: zgodny z `json_bibliografia.md`*
