---
name: ocena-wydawcy-b2b
description: Pełna ocena, czy i jak podjąć współpracę marketingową (artykuł, banner, poradnik itp.) z właścicielem cudzej domeny — dla działu handlowego Opcji Natury, powiązana z systemem propozycjeB2B. Umieszcza domenę na drabinie realnych klientów Opcji Natury (DOZ, Gemini, Nutridome, Kopalnia Zdrowia, opcjanatura.pl) wg siły SEO (Senuto MCP), liczy relację ceny do wartości ruchu, proponuje profil/temat artykułu i sugeruje kategorię działania (banner/artykuł/pakiet) do dalszego dobrania w propozycjeB2B. Używaj gdy ktoś pyta "czy warto opublikować u [domena]", "oceń tego wydawcę", "sprawdź domenę pod publikację", "czy ta cena za artykuł ma sens", "jaki temat zaproponować [domena]", "jaką współpracę zaproponować [domena]", "wycena współpracy blogowej [domena], cena X zł". NIE używaj do analizy WŁASNEJ domeny opcjanatura.pl (od tego są skille `monitoring-senuto` / `radar-aeo`) ani do researchu influencerów (`influencer-research`) — to wyłącznie pre-screening cudzych stron pod płatną współpracę marketingową.
---

# SKILL — Ocena wydawcy pod publikację B2B

Odpowiadasz na cztery pytania handlowca: **jak silna jest ta strona na tle naszych realnych
klientów, czy cena ma sens, o czym warto tam napisać, i jaki typ współpracy w ogóle
zaproponować.** To pre-screening SEO/ruchu + kierunek dla propozycjeB2B, NIE pełny audyt — na
końcu zawsze dokładasz listę rzeczy do sprawdzenia ręcznie, których dane Senuto nie widzą.

> **Wymaga:** connectora MCP **Senuto** podłączonego na koncie użytkownika (Ustawienia →
> Connectors → Senuto, logowanie w przeglądarce, bez klucza API). Jeśli narzędzia Senuto nie są
> dostępne, poproś użytkownika o podłączenie connectora zanim zaczniesz — nie zgaduj liczb.

Nie oszczędzaj na liczbie wywołań Senuto w tym skillu — pełny obraz (benchmark + profil
tematyczny) jest ważniejszy niż minimalizowanie zapytań. Dzienny limit kont to standardowo 200
zapytań widoczności — jeden pełny check zużywa ~7, więc jest zapas na wiele sprawdzeń dziennie.

---

## 1. Czego potrzebujesz od użytkownika

Zapytaj wprost, jeśli brakuje:
1. **Domena wydawcy** (wystarczy wklejony URL, np. `https://www.koalacosmetics.pl/artykul` —
   ty wyciągasz z niego samą domenę, patrz §2).
2. **Cena za artykuł** (zł, jednorazowa opłata). Jeśli użytkownik jej jeszcze nie zna (dopiero
   pyta "czy w ogóle warto rozmawiać") — zrób ocenę **bez ceny** (sama siła domeny + profil
   tematyczny), zaznacz wprost że to ocena częściowa, i dopytaj o cenę gdy się pojawi.

Nie proś o nic więcej — typ linku, dokładna tematyka i jakość strony "na oko" to punkty do
checklisty ręcznej (§7), nie dane wejściowe do liczenia.

---

## 2. Normalizacja domeny

Z wklejonego URL zostaw samą domenę: bez `https://`, bez `www.`, bez ścieżki i query stringa.
`https://www.koalacosmetics.pl/blog/artykul?utm=x` → `koalacosmetics.pl`.

Jeśli artykuł ma iść na wyraźną, samodzielną subdomenę (np. `blog.firma.pl`, nie
`firma.pl/blog`) — użyj tej subdomeny jako `domain` z `fetch_mode: "subdomain"`. W 95%
przypadków wystarczy `fetch_mode: "topLevelDomain"` na domenie głównej.

---

## 3. Dane z Senuto — pełny zestaw

Wszystko z `country_id: "200"` (PL Base 2.0), `fetch_mode: "topLevelDomain"`.

**A. `get_domain_statistics` na domenie wydawcy** — sedno sprawy (ranga, widoczność,
ads_equivalent, trend).

**B. `get_domain_statistics` na 5 domenach referencyjnych** — to nasza drabina benchmarku,
realni klienci Opcji Natury o bardzo różnej skali:

| Domena | Rola w drabinie |
|---|---|
| `doz.pl` | gigant ogólnopolski (apteka) |
| `gemini.pl` | gigant ogólnopolski (apteka) |
| `nutridome.pl` | średni portal zdrowotny |
| `kopalnia-zdrowia.pl` | średni portal zdrowotny |
| `opcjanatura.pl` | MY — punkt odniesienia |

**Cachuj zestaw referencyjny (B) na całą rozmowę.** Jeśli użytkownik sprawdza kilka domen pod
rząd, pobierz te 5 tylko raz — to te same, niezmienne dane, nie ma sensu ich powtarzać (nie
chodzi o oszczędzanie limitu, po prostu to nadmiarowe zapytanie o to samo).

**C. `get_urls` na domenie wydawcy** (`limit: 30`, `detail_level: "standard"`) — do profilu
tematycznego, patrz §6. Jeśli domena ma <5 URL-i w wyniku albo wynik jest pusty, potraktuj to
jako dodatkowy sygnał słabej/śladowej widoczności, nie błąd.

**Świadomie NIE wywołuj** (to inne zadania, nie kwestia oszczędzania):
- `get_competitors`, `backlinks_queries` — chyba że użytkownik wprost poprosi o głębszą analizę
  konkurencji tej konkretnej domeny.
- `rt_*` (Rank Tracker), `serp_*` — to narzędzia do naszych śledzonych fraz i ad-hoc SERP, nie
  do oceny cudzej domeny.

**Jeśli `get_domain_statistics` zwróci błąd/pustkę dla domeny wydawcy:** to NIE znaczy
automatycznie "zła strona" — może być za mała/nowa, żeby Senuto ją mierzyło. Umieść ją w tierze
"śladowa widoczność / brak danych" (§5) i zaproponuj sprawdzenie ręczne (Google, Similarweb).

---

## 4. Liczenie wskaźników

Z `full_statistics` weź `ads_equivalent.recent_value` (szacowany miesięczny koszt wykupienia
takiego ruchu w Google Ads — najbardziej zrozumiała liczba bez tła SEO) i
`domain_rank.recent_value` (niższa liczba = mocniejsza domena — to pozycja w rankingu
wszystkich zindeksowanych domen w Polsce; Senuto nie ma osobnego "rankingu domen",
`domain_rank` JEST tym rankingiem).

```
ratio_sily = ads_equivalent(wydawca) / ads_equivalent(opcjanatura.pl)

# tylko jeśli podano cenę:
ratio_ceny = cena_za_artykul / ads_equivalent(wydawca)
             # cena to jednorazowa opłata, ads_equivalent to wartość MIESIĘCZNA —
             # ratio_ceny mówi "ile miesięcy ruchu tej domeny kosztuje ten jeden artykuł"
```

Sprawdź też deltę `changes.visibility` z `summary` domeny wydawcy — spadek >20% w ostatnim
okresie to sygnał możliwej kary Google, nie tylko szumu.

---

## 5. Tabela benchmarku + tier

Zbuduj tabelę wszystkich 6 domen (5 referencyjnych + wydawca), **posortowaną po randze rosnąco**
(najmocniejsza na górze), z kolumną tieru:

| Ranga domeny | Tier |
|---|---|
| ≤ 300 | Gigant ogólnopolski |
| 300 – 3 000 | Duży portal branżowy |
| 3 000 – 15 000 | Średni portal zdrowotny/tematyczny |
| 15 000 – 100 000 | Mały/niszowy sklep |
| > 100 000 lub brak danych w Senuto | Śladowa widoczność / brak danych |

Przykład (dane referencyjne z 02.09.2026 — pobieraj świeże, te mogą się zmieniać):

| Domena | Ranga | Ads equivalent (zł/mies.) | Tier |
|---|---|---|---|
| doz.pl | 16 | 23 496 845 | Gigant ogólnopolski |
| gemini.pl | 115 | 3 449 296 | Gigant ogólnopolski |
| nutridome.pl | 5 213 | 137 010 | Średni portal zdrowotny |
| kopalnia-zdrowia.pl | 9 550 | 81 093 | Średni portal zdrowotny |
| **opcjanatura.pl (Ty)** | 55 121 | 22 789 | Mały/niszowy sklep |
| **[sprawdzana domena]** | … | … | … |

Werdykt bazuje na **pozycji tieru wydawcy względem tieru opcjanatura.pl**, nie na sztywnym
progu liczbowym:

- 🟢 **warto rozważyć** — tier wydawcy równy lub wyższy niż opcjanatura.pl, I (`ratio_ceny` ≤
  1.0 lub cena nieznana), I brak sygnału spadku widoczności.
- 🟡 **do przemyślenia / dopytaj** — tier o jeden stopień niżej niż opcjanatura.pl, albo cena
  tuż nad progiem 1.0, albo wyraźny spadek widoczności ostatnio.
- 🔴 **raczej nie** — tier "śladowa widoczność/brak danych", albo `ratio_ceny` wyraźnie > 2,
  albo silny świeży spadek widoczności sugerujący karę.

Ta drabina jest zakotwiczona w realnych, znanych kontach — nie jest zgadywaniem. Rozszerzaj
listę referencyjną w §3.B, gdy Daniel wskaże kolejnych dużych klientów do dopisania.

---

## 6. Profil tematyczny (z `get_urls`)

Z listy `urls` (posortowanej po `keywords_count`/widoczności) wyciągnij:

1. **Czy w TOP URL-ach widać sekcję poradnikową/blogową?** Szukaj segmentów ścieżki typu
   `/blog/`, `/poradnik/`, `/artykul/`, `/aktualnosci/`, `/magazyn/`, `/wiedza/`. Jeśli TOP
   URL-e to niemal same strony produktowe/kategorie (`/p/`, `/c/`, `/producer/`) — **zaznacz to
   wprost**: siła SEO tej domeny pochodzi z e-commerce, nie z contentu, więc realna wartość
   NOWEGO artykułu może być niższa niż sugeruje ogólny `ads_equivalent` całej domeny.
2. **Jakie kategorie/tematy dominują?** Wypisz 3-5 rozpoznawalnych kategorii produktowych lub
   tematycznych z URL-i (np. "kosmetyki dziecięce, zabawki, pielęgnacja włosów").
3. **Zaproponuj kąt artykułu** — znajdź część wspólną między tym profilem a ofertą Opcji
   Natury. Nie zgaduj składu/działania produktów z pamięci — sprawdź `produkty-lookup` (i
   `naturalna-pielegnacja`, jeśli chodzi o dobór pod konkretny problem skórny) po konkretny
   produkt/kategorię do wskazania. Podaj 1 propozycję tematu, nie listę.

---

## 7. Kolejne kroki — jaki typ współpracy zaproponować

Opcja Natura ma już system na to (**propozycjeB2B** — arkusz + katalog ~139 działań, segment ×
kanał klienta, część płatna — MY płacimy partnerowi — część darmowa jako wartość dodana). Ten
skill nie ma do niego żywego dostępu (inne konto, inny system) i **nie wskazuje konkretnego ID
z katalogu** — te zmieniają się często i wskazanie nieaktualnego ID myliłoby bardziej niż
pomagało. Zamiast tego: rekomenduje **kategorię** działania na bazie tieru + profilu
tematycznego z §5/§6, a dokładną pozycję i cenę handlowiec dobiera sam w KROKU 2
propozycjeB2B, gdzie katalog jest zawsze aktualny.

**Ogólne kategorie (orientacyjne — realny katalog bywa szerszy i się zmienia):**

| Kategoria | Forma / koszt | Kiedy pasuje |
|---|---|---|
| Banner / slider (strona główna, nawigacja) | powierzchnia online, płatne, zwykle niski jednorazowy koszt | Brak sekcji poradnikowej, ale realny ruch e-commerce (dużo stron produktowych/kategorii w TOP) |
| Rich content / ranking / porównanie na kartach produktowych | content i social, zwykle płatne | Rozbudowany katalog produktowy, ruch skupiony na kartach produktów |
| Pakiet multi-placement (kilka powierzchni naraz) | powierzchnia online, płatne, wyższy koszt | Tier "Duży portal" lub wyżej — koszt uzasadniony skalą ruchu |
| Artykuł ekspercki / poradnik tematyczny | content i social, zwykle **bezpłatne** dla partnera (wartość dodana, kosztuje Wasz czas) | Domena **ma** wykrytą sekcję poradnikową/blog w profilu tematycznym (§6) — bez niej nie ma gdzie tego osadzić |
| Wywiad/Q&A, webinar edukacyjny | content i social, bezpłatne | Domena z zaangażowaną publicznością/redakcją, niezależnie od tieru |

**Heurystyka doboru:**
- Brak sekcji poradnikowej (§6.1) → kieruj w stronę banneru/slidera/rich contentu, nie artykułu.
- Jest sekcja poradnikowa → artykuł/poradnik ma sens niezależnie od tieru, bo to zwykle
  darmowa forma — jedynym kosztem jest czas, nie złotówki.
- Tier "Gigant"/"Duży portal" (§5) → płatny pakiet multi-placement ma ekonomiczny sens.
- Tier "Śladowa widoczność" → odradzaj większą płatną inwestycję; ewentualnie tylko forma
  darmowa, jeśli relacja z partnerem i tak istnieje.

Zamknij tę sekcję jednym zdaniem: proponowana kategoria + odesłanie do propozycjeB2B po
konkretną pozycję i wycenę.

---

## 8. Zawsze dołącz — czego dane NIE oceniają

Niezależnie od werdyktu, dodaj tę checklistę:

1. **Dokładna tematyka strony** — profil z §6 to sygnał z URL-i, nie potwierdzenie; sprawdź
   naocznie czy to spójna strona w naszej niszy, nie przypadkowy "content-hub".
2. **Typ linku** — dofollow czy nofollow/sponsored (inna wartość SEO; dopytaj wydawcę wprost).
3. **Oznaczenie treści sponsorowanej** — czy wydawca rzetelnie to robi (wymóg prawny; jeśli
   nie oznacza, to ryzyko niezależnie od liczb).
4. **Wrażenie "na oko"** — zalew reklam, brak realnego czytelnictwa/komentarzy, byle jaka szata
   graficzna → czerwona flaga mimo dobrych liczb SEO.

---

## 9. Format odpowiedzi

Tabele, nie ściana tekstu. Struktura:

1. Tabela benchmarku (§5) z wydawcą podświetlonym.
2. Krótka tabela oceny:

| Kryterium | Wynik |
|---|---|
| Tier wydawcy vs Ty | … |
| Siła domeny (ratio_sily) | … % |
| Cena vs skala (ratio_ceny) | … (jeśli podano cenę) |
| Trend widoczności | stabilny / spadek |
| Profil tematyczny | 3-5 kategorii + info o (braku) sekcji poradnikowej |
| **Werdykt** | 🟢/🟡/🔴 + jedno zdanie dlaczego |

3. Propozycja tematu artykułu (§6.3) — jedno zdanie.
4. Sugerowana kategoria współpracy (§7) — jedno zdanie + odesłanie do propozycjeB2B.
5. Checklista ręczna (§8) — lista punktowana.

---

## 10. Rozszerzenia (nie teraz)

- Sprawdzanie kilku domen naraz (batch) — logika per-domena już to wspiera, brakuje pętli.
- Źródło kandydatów z Bigin (klienci handlowca) — **wstrzymane**: w module Accounts Bigin nie
  ma obecnie pola z URL-em strony klienta (sprawdzone w metadanych modułu). Do podjęcia gdy
  Daniel ustali, gdzie ten URL ma żyć (nowe pole w Bigin / inne źródło).
- Żywy odczyt katalogu propozycjeB2B (zakładka `helper_katalog`) zamiast ogólnych kategorii z
  §7 — do rozważenia, jeśli handlowiec dostanie connector Google Sheets w claude.ai.
- Lista już zaakceptowanych/odrzuconych publikacji jako druga oś kalibracji tierów z §5.
