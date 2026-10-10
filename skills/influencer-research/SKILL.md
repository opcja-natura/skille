---
name: influencer-research
description: >
  Wyszukiwanie i wstępna kwalifikacja influencerów / kreatorów na Instagramie i TikToku
  pod kampanie Opcji Natury. Używaj tego skilla zawsze gdy ktoś z zespołu pyta o
  znalezienie twarzy/ambasadorów/influ do współpracy, listę kandydatek do kampanii,
  kogo zaprosić do barteru, mapę kreatorów w niszy, lub research konkurencji
  influencerskiej. Triggeruje na: "znajdź influ", "kogo zaprosić do współpracy",
  "kto pisze o X", "lista do kampanii", "potrzebuję twarzy do premiery", "kogo
  warto śledzić w niszy Y", "ambasadorki dla [produkt]". NIE używaj do analizy
  postów konkretnego znanego konta (to inny use case) ani do oceny treści jaką
  konkretna osoba publikuje — to research na poziomie odkrywania nowych kont.
---

# Influencer Research — Opcja Natura

## Cel skilla

Znaleźć **15–30 autentycznych kandydatów** (Instagram, TikTok lub oba) dopasowanych do briefu kampanii i wartości marki Opcji Natury, z gotową strukturą do podjęcia decyzji o kontakcie.

Output to plik markdown z: tabelą kandydatów (tier A/B/C + nisza + komentarz + link), sekcją pominiętych pogrupowaną po powodzie odrzucenia, top 5 do pierwszego kontaktu, wnioskami strategicznymi.

**Mechanika wywołań Apify (CLI vs MCP, wybór actora, kosztorys PPE) żyje w osobnych skillach — `apify-cli` i `apify-ultimate-scraper`.** Ten dokument zawiera tylko domenową wiedzę: które actory pod jaki etap researchu, jakie pola wyciągać, jak czytać wyniki. Jeśli poniżej pojawia się nazwa narzędzia MCP (`get-dataset-items`, `get-actor-output`) — to opis historyczny; obecnie wywołujemy przez `apify-cli` (zobacz gotchę o `--fields`/`--omit` w skillu `apify-cli`).

---

## KROK 1 — Brief od użytkownika (OBOWIĄZKOWY)

**Zanim ruszysz scrapowanie, ZAWSZE przeprowadź dialog briefingowy.** Bez briefu agent nie ma punktu odniesienia żeby filtrować wyniki. Nie zakładaj że użytkownik chce to samo co poprzednio.

Zadaj te pytania (możesz adresować po imieniu jeśli wiesz kto pyta):

```
Cześć! Pomogę Ci znaleźć kreatorów do współpracy. Powiedz mi krótko:

1. KONTEKST — dla jakiego produktu lub kampanii szukamy?
   (np. "premiera dezodorantu w sztyfcie", "linia tatuażu",
    "ogólne budowanie listy ambasadorek", "kampania Dzień Mamy")

2. NISZA — jaki kierunek tematyczny?
   (np. "sport ale nie performance", "ogród + zioła", "młode mamy",
    "tatuaż", "morsowanie", "ja nie wiem, podpowiedz mi opcje")

3. PLATFORMA — gdzie szukamy?
   [ ] Instagram   [ ] TikTok   [ ] Obie

4. SKALA — jaki target followersów?
   [ ] Nano (500–5k, najtaniej, najbardziej autentycznie)
   [ ] Mikro (5k–30k, najlepszy ROI dla nas)
   [ ] Mid (30k–100k, większy budżet)
   [ ] Wszystko, posortuj

5. CO ODSIAĆ — czego NIE chcemy w wynikach?
   (np. "performance fitness", "konta firmowe", "osoby z konkurencyjnymi sponsorami")
```

Jeśli użytkownik nie wie co odpowiedzieć na #2 — zaproponuj 3 nisze z poniższej mapy hashtagów które pasują do produktu z #1 i poproś o wybór.

Jeśli #5 jest puste — to OK, używaj standardowych red flags z sekcji „Filtry odsiewu".

**Po briefie powiedz krótko jaki plan wykonasz** (które hashtagi w którym kroku) i ruszaj.

---

## KROK 2 — Mapa hashtagów PL

To żywa baza. **Status "zweryfikowany"** = sprawdzony empirycznie w prawdziwym scrapie (dane z poniedziałek-niedziela poprzedniego tygodnia). **Status "hipoteza"** = nasza intuicja, **należy zwalidować** przez Hashtag Analytics Scraper przed deep-dive.

### Sport-natura (zweryfikowane)

| Hashtag | Posty | Komentarz |
|---|---|---|
| `#biegaczka` | 441k | **Złoto.** ~100% kobiet, autentyczne biegaczki amatorki |
| `#bieganiejestfajne` | 397k | Ton: radość, nie wyniki |
| `#polskabiega` | 364k | Społeczność biegowa, mieszany gender |
| `#pobiegane` | 327k | Po treningu, casual ton, ~50/50 gender — filtruj |
| `#biegaczkapoczterdziestce` | hipoteza | 40+ kobiety w sportach — sprawdź skalę |
| `#biegamyrazem` | 25k | Bardzo wąskie, autentyczne |
| `#polskawnaturze` | 18k | ⚠️ Top posty = fotografia krajobrazu, głównie mężczyźni-fotografowie (scrape 07.2026) — bez twarzy lifestyle |
| `#joginka` | 93k | Polska joga niche, mid-tier |
| `#jogapolska` | 156k | ⚠️ Top posty = feed szkół i studiów jogi (scrape 07.2026) — konta firmowe, mało osobistych twarzy |

### Ogród i zioła (zweryfikowane jako szum biznesowy)

| Hashtag | Posty | Komentarz |
|---|---|---|
| `#warzywniak` | 43k | ⚠️ 80% sklepów warzywnych — pomijaj |
| `#ogródwarzywny` | 26k | Niche, mieszane |
| `#blizejnatury` | 13k | ⚠️ Parki narodowe, kąpiele leśne, turystyka — pomijaj |
| `#zielarka` | hipoteza | Sprawdź — może działać |
| `#ogródbylinowy` | 1.5k | Bardzo niche, sprawdź jakość |

### Tatuaż (zweryfikowane jako trudna nisza)

⚠️ **Polskie tagi tatuażowe to feed studiów i tatuażystów.** Z 125 video w 5 hashtagach ~70% to konta komercyjne. Hashtag `#starytatuaz` w PL nie istnieje (TikTok zwraca obcojęzyczne „stars tattoo").

Dla linii Naturalny Tatuaż **rekomenduj klientowi Instagram zamiast TikToka** + B2B do polskich tatuażystów-influencerów (@lautiatattoos 49k, @projektink 217k, @dwie_igly 153k).

### Dzika kuchnia i zielarstwo (zweryfikowane 07.2026 — ZŁOTO dla klimatu „jedzenie/natura")

| Hashtag | Posty | Komentarz |
|---|---|---|
| `#dzikakuchnia` | 8.2k | **Złoto.** Mała autentyczna nisza, prawdziwi twórcy, zero szumu marek. Top konta: @max.gotuje.z.natury 17k, @chwasciejemy 5k |
| `#zielarka` | żywy | Osobiste zielarki między kontami firmowymi — filtruj, ale trafia się A-tier (@z.ziolami.jej.do.twarzy 10k, @juliawizowska 9k, @ziolawpelni 18k) |
| `#rokitnik` | żywy | ⚠️ Feed firm: suplementy, lodziarnie, szkółki — pomijaj jako źródło twórców |
| `#domowaspizarnia` | 1.1k | ⚠️ Manufaktury i sklepy; pojedyncze perły domowe (@beata.zam 21k, wysoki ER) |
| `#kuchniaroslinna` | duży | ⚠️ Gastro: bistra i restauracje — szum |

**TikTok (zweryfikowane 07.2026):** `#zielarstwo` = GORĄCA nisza PL (top twórczynie 0,3–2 mln odtworzeń: @slowianskazielarka 476k, @zielarkazkampera 30k, @warmiara 26k); `#dzikakuchnia` działa (@sianko_org, @wild_kitchen21, @maxgotujeznatury); `#naturalnapielegnacja` działa (tu wideo @opcja_natura zrobiło 402k plays). ⚠️ Anty-tag TT: `#ziola` — anglojęzyczny wrestling (zawodnik Ziola).

### Włosy (zweryfikowane 07.2026 — TIKTOK > INSTAGRAM dla tej niszy)

**Polski „hair tok" żyje** — na TT tagi włosowe pełne osobistych twórczyń z widocznymi playCount (konta 10k z wideo 1–2,4 mln odtworzeń); na IG te same tagi = salony/marki/drogerie. Dla kampanii włosowych scrapuj NAJPIERW TikToka.

| Hashtag | Platforma | Komentarz |
|---|---|---|
| `#wlosomaniaczki` | TT+IG | TT: twórczynie osobiste między markami; IG: recenzentki „denek" + szum marek |
| `#kreconewlosy` | TT+IG | TT: **złota nisza curly** (curly.double.twins, mariia_ugc, maja_koscianska); IG: głównie salony |
| `#pielegnacjawlosow` | TT | Działa; filtruj ogólne beauty-makijażowe |
| `#olejowaniewlosow` | IG | Mix marek/salonów z pojedynczymi perłami osobistymi |
| `#trycholog` | IG | Gabinety-oferty; edukacyjnych ekspertów wyławiaj ręcznie |
| `#wlosing` | IG | ⚠️ **SPAM hurtowni przedłużania włosów (Vietnam B2B)** — duży licznik, zero wartości |

**Gotcha niszy:** włosowe mikro-konta żyją ze współprac — przed kontaktem sprawdź ostatnie posty pod Anwen/OnlyBio/Neboa/Sattva (częste konflikty; @lysy_od_wlosow 94k = ambasador OnlyBio).

### Skóra atopowa / wrażliwa / dojrzała + TikTok Shop — TikTok PL (zweryfikowane 08.2026)

Scrape pod afiliację TikTok Shop: 32 tagi × 30 wideo + 71 profili × 10 najnowszych filmów. Raport: `marketing/tikTok/afiliacja_kandydaci_2026-08-07.md`.

| Hashtag | % treści PL | Mikro PL (5–100k) | Komentarz |
|---|---|---|---|
| `#atopowezapalenieskory` | 97% | 13 | **Złoto dla AZS.** Najczystszy tag atopowy w PL |
| `#swiadomapielegnacja` | 90% | **20** | Najwyższy urobek mikro-kont w całym scrapie; kosmetolożki-edukatorki |
| `#zmarszczki` | 100% | 15 | 100% PL; miesza pielęgnację z jogą twarzy |
| `#domowekosmetyki` | 100% | 10 | Czysta nisza DIY/zielarska, zero szumu obcojęzycznego |
| `#ceradojrzala` | 93% | 17 | ⚠️ To głównie **makijaż** dla cery dojrzałej, nie pielęgnacja |
| `#luszczyca` | 90% | 12 | Żywa społeczność pacjencka, osobiste historie |
| `#cerawrazliwa` | 90% | 16 | Szeroki, sporo marek |
| `#polskiekosmetyki` | 87% | 14 | Patriotyzm zakupowy — dobry kontekst dla manufaktury |
| `#kosmetykinaturalne` | 83% | 15 | Rdzeń clean beauty; dużo marek do odsiania |
| `#tiktokshoppolska` | 80% | 8 | **Jedyny działający tag Shopowy w PL**; zdominowany przez gadżeciarzy |
| `#skoraatopowa` | 67% | 14 | Działa, ale ⚠️ ściąga hiszpańskie konta od wyrobów ze **skóry** (plecaki) |

**Anty-tagi TT PL (nie używaj ponownie):** `#inci` 0% PL (Polacy mówią „skład") · `#swiadskory` 0% · `#bezsls` 0% · `#egzema` 0% · **`#azs` 3%** (⚠️ trzyliterowy skrót przegrywa z obcojęzycznym szumem — używaj pełnej nazwy) · `#atopik` 13% (hiszpański `atópica`) · `#alergiaskorna` 13% · `#pozamka` 23% · `#pielegnacjapo40` 30% · `#czytamsklady` 47% (łapie książki i tarot) · `#skladniki` 70% PL ale **0 trafień** (po polsku = przepisy kulinarne, NIE INCI) · `#kobietapo40` 90% PL ale **0 trafień** (taniec i szpilki, tag tożsamościowy) · `#zoltykoszyczek`, `#tiktokshopznalezisko`, `#kosmetykizatiktokshop` = **0 postów**.

**Gotcha 1 — flaga TikTok Shop.** `clockworks/tiktok-profile-scraper` zwraca `authorMeta.ttSeller` i `authorMeta.commerceUserInfo` = twarda flaga „konto ma podpięty Shop". **Scraper hashtagowy tego pola NIE zwraca**, więc listy „kreatorów z Shopem" robione z hashtagów opierają się na deklaracjach z bio, a te kłamią (@alpiland ma „TIK TOK SHOP" w bio i nie ma flagi).

**Gotcha 2 — zasięgi z hashtaga zawyżają rząd wielkości.** Hashtag pokazuje wideo, które zrobiło zasięg, nie normę konta. Zmierzone różnice: @edyta.baranowska 2,1 mln (hashtag) vs 1 249 (mediana 10 ostatnich) = **×1700**. **Zawsze doliczaj profile-scrape z `profileSorting: "latest"`, `resultsPerPage: 10`, `excludePinnedPosts: true`** i raportuj medianę stamtąd. Na TikToku licz ER **do wyświetleń**, nie do followersów (norma 3–8%).

**Stan rynku 08.2026:** afiliacja beauty na TT PL praktycznie nie istnieje — na 71 zweryfikowanych profili tylko 4 KREATORÓW ma Shop (@xnataliexbeautyx, @bywiki, @mgr_farm_ewa_nadziak, @sezam_zdrowia); reszta flag to marki i sklepy. TikTok Shop wszedł do PL latem 2026, kreatorzy dopiero uczą się mechaniki. **Potwierdzone drugim, niezależnym pomiarem** (graf konkurencji, 08.2026): na 56 profili flagę mają 3 (5,4% vs 5,6% w pierwszym biegu). Najmocniejszy znaleziony afiliant: **@patrykwhale** (99,9k obs., mediana 92,5k wyśw., Shop kat. Beauty, oznaczona reklama kosmetyczna z 1,3 mln wyśw.).

**Red flag PL specyficzny — MLM w bio przez link, nie przez nazwę.** Sprawdzaj `bioLink`, nie tylko `signature`: `tiande.eu/r/…`, `*.ringana.com`, `*.raypath.info`, Farmasi. Konto może mieć całkowicie autentyczne treści (@jagoda_kus 69k, świetny content o łuszczycy) i monetyzować się przez MLM.

### Hashtagi MARKOWE (zweryfikowane 08.2026 — zasadniczo NIE DZIAŁAJĄ)

Bieg „graf współpracy konkurencji" (7 polskich marek naturalnych, raport `tikTok_shop/afiliacja/graf_konkurencji_2026-08-07.md`) sprawdził hipotezę „zescrapuj `#nazwamarki`, dostaniesz jej twórców". **Hipoteza upadła.** 8 tagów × 30 wideo = 240 wideo, 172 autorów, z czego użytecznych polskich kreatorów kilkunastu.

| Hashtag | Co NAPRAWDĘ łapie | % PL |
|---|---|---|
| `#sylveco` | **fandom Pokémona Sylveon** (adopty, keychainy) + streamer „Sylvee" | **0%** |
| `#yope` | **aplikację społecznościową Yope** — kilkanaście kont `*.yope` „Sponsored by Yope App" | **0%** |
| `#resibo` | tagalog: **„resibo" = paragon** — filipińskie konta newsowe/polityczne | **0%** |
| `#ministerstwodobregomydla` | **fandom braci Dobre** (Lucas & Marcus) + polskie konta religijne | ~25% |
| `#nacomi` | hiszpańskojęzyczne beauty (marka ma `nacomi_es`, `nacomi_balkan`) | ~10% |
| `#braciamydlarze` | marka + kilku realnych PL twórców + szum | ~40% |
| `#4szpaki`, `#czteryszpaki` | **jedyne dwa działające** — marka, sklepy, kilku twórców | ~70% |

**Reguła:** nazwa marki jako hashtag działa tylko gdy jest **semantycznie unikalna i wielosylabowa po polsku**. Krótkie wymyślone nazwy przegrywają z globalnym szumem, bo są przypadkowo homonimiczne w innych językach i fandomach. To ta sama patologia co `#azs`, tylko silniejsza.

### 🔑 Co ZAMIAST tego: wyszukiwarka TikToka (`searchQueries`)

**Najważniejszy wniosek metodyczny z 08.2026.** `clockworks/tiktok-scraper` z `searchQueries` + `proxyCountryCode: "PL"` na frazach tekstowych (`"bracia mydlarze"`, `"sylveco kosmetyki naturalne"`) dał **niemal 100% trafień na temat** i wyprodukował praktycznie cały graf. Powód: wyszukiwarka czyta **opis wideo i oznaczenie `@marka`**, a twórcy współpracujący z markami **oznaczają markę, nie tagują jej hashtagiem**.

```json
{ "searchQueries": ["nazwa marki", "nazwa marki kosmetyki"],
  "resultsPerPage": 30, "proxyCountryCode": "PL" }
```
⚠️ Gotcha: zwraca **~12 wyników na frazę** niezależnie od `resultsPerPage` (limit TikToka). Rozbudowa = więcej fraz, nie większy `resultsPerPage`.
⚠️ Gotcha: marka może mieć **nick inny niż nazwa** — Sylveco na TT nazywa się „polskie kosmetyki naturalne", więc twórcy oznaczają `@polskie kosmetyki naturalne` i scrape po nazwie marki tego NIE widzi. Sprawdź nick przed scrapem.

### Graf konkurencji na TT — czego się spodziewać (08.2026)

- **Konta marek na TT nikogo nie oznaczają.** 160 wideo z 4 kont markowych → 1 wzmianka, i to o dostawcy opakowań. `mentions`/`detailedMentions` na TikToku to **martwe pole** dla tej metody — inaczej niż na IG.
- **Na IG `paidPartnership` też bywa zerowe.** 152 posty z 5 kont marek → 0 deklaracji płatnej współpracy. `taggedUsers` zdominowane przez **konta-farmy repostujące „aesthetic"** (`aest`, `aest___vibes`, `inspos_we_love`, `cozy.magazine`, `bestinflusite`) — to zasięgowy spam, odsiewaj.
- **Sylveco = Vianek = Aloesove = Biolaven** to jedna firma; wzajemne `coauthorProducers` to cross-posting, nie współprace.
- **Graf konkurencji jest czystszy niż hashtag tematyczny:** 0 kont MLM (vs 5 przy hashtagach). Twórcy pracujący z prawdziwymi markami nie monetyzują się przez piramidy.
- **Oznaczenie reklamy jako filtr jakości:** tylko ~28% wzmianek miało jakiekolwiek oznaczenie (`[reklama]`, `(reklama)`, `[współpraca]`, `[prezent/pr]`, `{prezent}`, `[Wspolpraca Barterowa]`). Kto oznacza — wie, że robi biznes. ⚠️ Wykrywanie po tekście **nie widzi** etykiety „Płatna promocja" z UI TikToka — nie odrzucaj konta wyłącznie na tej podstawie.
- **Graf znajduje INNY typ kandydata niż hashtag:** hashtag daje *ekspertów mówiących o problemie*, graf daje *konsumentów-recenzentów, którzy już kupili polską markę*. Pod afiliację/sprzedaż potrzebujesz drugich; pod wiarygodność — pierwszych. Metody się uzupełniają, nie zastępują.

### Hipotezy do walidacji (jeszcze nie testowane)

| Nisza | Hashtagi do sprawdzenia | Potencjał |
|---|---|---|
| **Morsowanie** | `#morsowanie`, `#morsujemy`, `#zimnakapielmoja`, `#morsownik` | Wysoki — silna społeczność PL, sezon X–III, idealne dla Mazidła i Atop Stopa |
| **Macierzyństwo amatorskie** | `#mamabiegaczka`, `#matkawbiegu`, `#ogródzdzieckiem`, `#mamawogrodzie` | Średni — sprawdź czy nie zdominowane przez wielkie konta |
| **Dezodorant / pot zdrowy** | `#zdrowypot`, `#naturalnydezodorant`, `#beztoksyn` | Niski-średni — nisza może być za mała |
| **Beauty naturalne** | `#cleanbeauty­polska`, `#naturalkosmetyki` | Średni — dużo konkurencji marek; `#naturalnapielegnacja` ZWERYFIKOWANY 07.2026 jako szum: marki, salony, ambasadorki Weledy — pomijaj |
| **Cross — slow life** | `#slowliving­polska`, `#prostożycie`, `#żyjpoprostu` | ⚠️ Większość polskich „slow life" frazr to wymysł — waliduj |
| **40+ aktywne kobiety** | `#kobietapoczterdziestce`, `#zdrowiepoczterdziestce`, `#aktywnamama` | Wysoki potencjał, segment underrepresented |

### Anty-hashtagi (NIE używaj — sprawdzone że 0 postów)

`#ruchwnaturze`, `#slowlivingpolska` (sic), `#kobietywgorach`, `#mamawbiegu`, `#dziewczynywnaturze`, `#blizejnatury­polska`, `#zyciezamiastem`, `#sezonowakuchnia`, `#jemsezonowo` (0 postów, 07.2026).

**Wzorzec:** złożone „lifestyle" frazy które brzmią ładnie po polsku ale nikt ich nie używa. Polskie tagowanie preferuje krótkie, identity-based, czasownikowe.

### Półka makro 100k–500k (zweryfikowane 07.2026)

**Hashtagi i user-search NIE znajdują kont 100k+.** Top posty polskich tagów niszowych to mikro-konta i firmy; user-search dopasowuje NAZWY kont (zwraca nano). Dla półki makro działa tylko metoda seedów: typuj znane nazwiska pasujące do klimatu → weryfikuj `instagram-search-scraper` (searchType user, searchLimit 2–3, zwraca followers+bio) → do listy trafiają wyłącznie konta potwierdzone scrapem. Wniosek strategiczny: „natura/slow" 100k+ w PL to osobowości medialno-książkowe (autorki, edukatorki), nie influencerki; aktywne kobiety 100k+ to niemal wyłącznie performance fitness. Zweryfikowane przykłady: @agnieszkamaciag 187k (slow/dobrostan), @kasiagandor 237k (science+bieganie), @katarzynabosacka 231k (świadoma konsumpcja, TV), @monikakingamrozowska 177k (eko-mama, TV), @jadlonomia 327k (przerwa w bio 07.2026), @whatannawears 566k (well-being, Bali).

---

## KROK 2b — Mapa hashtagów RO (Rumunia, walidacja 31.07.2026)

Kontekst: wejście marki na rynek rumuński. Zwalidowano 25 tagów (2 rundy Analytics) + deep-dive 5 tagów × 15 postów + 9 profili. Pełny raport: `marketing/influencer_research/rynek-rumunski_wejscie_instagram.md`.

### 🚩 Wniosek nadrzędny: IG RO nie ma warstwy twórczyń

Deep-dive nie dał **ani jednej kandydatki A-tier**. `#ingrijirenaturala` = 15/15 postów to marki i dystrybutorzy, lajki 0–3. `#cosmeticenaturale` = 15/15 marek. Rumuńskie „naturalne" na IG to marki postujące do siebie nawzajem. Zanim zaproponujesz komuś research influ w RO na Instagramie — pokaż mu to.

**MLM to główny red flag RO.** W 75 postach wpadło sześć systemów: Life Care, Atomy, SNEP, LR Health & Beauty, Finclub, InCruises. Rumuńska „influencerka od naturalnej pielęgnacji" bardzo często = dystrybutorka MLM. Sprawdzaj przed każdym kontaktem.

**Jedyna żywa nisza: włosy kręcone `#parcret`** (31–278 lajków, reszta tagów 0–3) — i ma jednego gatekeepera: Dana `@parcretsibuclerasfatate` (2,9k) = founder `@naturalhysteria` (sklep 12,4k) + społeczność FB 123k + curlyhair.ro. Wejście w curly RO to **rozmowa dystrybucyjna, nie barter**.

### ⚠️ Gotcha licznika (dotyczy też PL!)

`postsCount` z `instagram-hashtag-analytics-scraper` przy wartościach **≥1 mln jest niewiarygodny**. Twardy dowód: `#ingrijireapielii` zwrócił `postsCount: 4 387 000`, a w polu `relatedRare` innego tagu ten sam hashtag ma `43.87 k` — te same cyfry, czynnik ×100. Tagi małe (<10k) zwracają liczby dokładne i spójne.

**Zasada:** przy wartościach milionowych ufaj **rankingowi, nie wartości bezwzględnej**; realną skalę potwierdza dopiero deep-dive (liczby lajków w top postach). Nie przepisuj tych liczb do raportu jako faktów.

### Reguły języka RO (zweryfikowane empirycznie)

| Reguła | Dowód | Konsekwencja |
|---|---|---|
| **Rumuni tagują BEZ diakrytyków** | `ingrijirenaturala` 7 629 vs `îngrijirenaturală` 2 849 (2,7:1); `ingrijireaparului` ~19k vs `îngrijireapărului` 2 909 (~6,5:1) | Scrapuj wersję bez diakrytyków. Wersja z diakrytykami to osobny, marginalny zbiór — opcjonalny dodatek |
| **„skincare" się zadomowiło, „beauty" nie** | `skincareromania` żywy vs `beautyromania` 9 327 (prawie martwy) | Angielskie zapożyczenia testuj pojedynczo, nie hurtem — RO ma własne `#frumusete` (210k) |
| **Kontaminacja romańska jest realna** | patrz anty-tagi niżej | Każdy tag RO waliduj po `relatedFrequent` — jeśli sąsiedzi są francuscy/włoscy/hiszpańscy, tag nie jest rumuński |

### Zweryfikowane — czyste, niszowe (deep-dive TU)

| Hashtag | Posty | Komentarz |
|---|---|---|
| `#ingrijirenaturala` | 7 629 | **Rdzeń niszy.** Bez diakrytyków, czysto rumuński |
| `#parnatural` | 8 189 | Włosy naturalne — żywy |
| `#parcret` | 7 079 | Włosy kręcone — żywy (odpowiednik PL `#kreconewlosy`) |
| `#zerowasteromania` | 6 097 | Eko-świadomość, mała ale autentyczna |
| `#cosmeticeromanesti` | 4 823 | ⚠️ Prawdopodobnie feed rumuńskich MAREK — użyj jako **źródła listy konkurencji**, nie twórczyń |
| `#pielesensibila` | 3 611 | Cera wrażliwa — bardzo wąskie, sprawdź jakość |
| `#cosmeticehandmade` | 2 032 | ⚠️ Manufaktury i sprzedawcy — raczej anty |

### Zweryfikowane — duże, z rumuńskim rdzeniem (deep-dive z filtrem)

| Hashtag | Komentarz |
|---|---|
| `#cosmeticenaturale` | Jedyny duży tag z realnymi markerami RO w `related` (`#romania`, `#brasov`, `#madeinromania`). Zatłoczony, ale to główna arteria niszy |
| `#skincareromania` | Żywy, kraj w nazwie = automatyczny filtr geo |
| `#ingrijireatenului` / `#ingrijireapielii` | Generyczny angielski skincare + szum; jedyne trafienie RO to `#frumusete` |

### Markery RO odkryte przez `related` (używaj jako filtra i seedów)

`#frumusete` 210k (uroda) · `#sanatate` 550k (zdrowie) · `#madeinromania` 528k · `#madeinro` 202k · `#bucuresti` 4,1M · `#brasov` 2,3M (tagi miast = skuteczny filtr geo) · `#copii` 368k · `#bebelusi` 93k · `#sapun` 62k · `#stildeviata` 55k · `#tratamentefaciale` 74k (gabinety)

### Anty-hashtagi RO (0 postów lub kontaminacja)

| Hashtag | Powód odrzucenia |
|---|---|
| `#mamicideromania` | **0 postów** |
| `#leacuribabesti` | **0 postów** — hipoteza „ludowe leki" martwa |
| `#plantemedicinale` | Klaster **francuski**: `#bienetre`, `#naturopathie`, `#herboristerie`, `#printemps`. Tag pan-romański, nie RO |
| `#deodorantnatural` | Klaster **arabski/Zatoka**: `#uae`, `#jordan`, `#الإمارات`. Bolesne — dezodorant to nasz produkt wejściowy, ale tag nieużywalny |
| `#viatasanatoasa` | Klaster **brazylijskich memów** (`#memesbrasil`, `#memesbr`) + `#kangenwater` (MLM woda jonizowana) |
| `#beautyromania` | 9 327 — praktycznie martwy, RO używa `#frumusete` |

### Red flagi specyficzne dla RO

- **Salony i gabinety zabiegowe dominują „beauty"** — `#frumusetenaturala` ciągnie `#dermapen`, `#bbglow`, `#tratamentefaciale`, `#cosmetica`. Dokładnie ten sam wzorzec co polskie `#jogapolska`
- **Dietetycy i trenerzy w „zdrowiu"** — `#traiestesanatos` ciągnie `#nutritionist`, `#fitness`, `#detox` = performance, odsiać
- **MLM** — `#kangenwater` w sąsiedztwie tagów zdrowotnych; w RO scena MLM jest silna, sprawdzaj bio
- **Słownik red flags RO (bio):** `magazin`, `farmacie`, `cabinet`, `salon`, `clinica`, `cod reducere`, `comenzi`, `livrare`, `colaborare`, `distribuitor`

### Konkurencja RO (zebrana z deep-dive'u — używaj do filtra konfliktów)

**Marki rumuńskie:** Simte Natura · TECHIR · Terra Issa · Ariuna Cosmetice · One Drop Cosmetics · Atelierul de Săpun · Cubul de Aloe · Herb & Hearth · Blans
**Zagraniczne obecne w RO:** MaterNatura 🇮🇹 (najbliższy nam profil, mocno w curly) · STYX 🇦🇹 · Herbella 🇹🇷 · Marnys 🇪🇸 · ARDES 🇮🇹 · Bernard Cassière 🇫🇷 · Garmastan
**MLM (osobna kategoria red flag):** Life Care · Atomy · LR Health & Beauty · Finclub · SNEP · InCruises
**Sklepy eko (partnerzy B2B, nie konkurencja):** Ecotheum · ZeroZen · Eco Curier · FoodPlop · Transylvanian Food Market

### Otwarte

- **TikTok RO — następny krok, nie sprawdzony.** W PL TT wygrał z IG dokładnie dla włosów; rumuński IG pokazał identyczny objaw. Tagi do scrapu: `parcret`, `parcretromania`, `curlyhairromania`, `ingrijirenaturala`, `cosmeticenaturale`
- `#cosmeticeromanesti` (4 823) — osobny mały scrape pod rozbudowę listy konkurencji; jedyny tag, w którym rumuńskie marki tagują się świadomie jako rumuńskie
- Dezodorant (nasz produkt wejściowy) nie ma niszy na IG RO — `#deodorantnatural` jest arabski. Potrzebny inny mechanizm wejścia niż hashtagi

---

## KROK 3 — Workflow scrapingu

### ⚠️ Zacznij TU: hashtagi to słabe narzędzie odkrywania

**Instagram od lat nie promuje treści przez hashtagi** — twórcy rosną na Reels/FYP i w większości przestali tagować. Kto dalej wrzuca 15 tagów pod post? Sklepy, marki i dystrybutorzy MLM, bo to dla nich darmowa dystrybucja.

Skutek: **„Top posts" hashtaga nie jest rankingiem najlepszych twórców w niszy — jest rankingiem tych, którym jeszcze zależy na tagach.** Scraper hashtagowy jest strukturalnie zoptymalizowany pod znajdowanie dokładnie tego, co chcemy odrzucić.

Konsekwencja dla starszych wniosków w tym skillu: część notatek typu „ten tag to feed sklepów / salonów" (`#warzywniak`, `#jogapolska`, `#rokitnik`, cała nisza tatuażowa) to prawdopodobnie **artefakt narzędzia, nie prawda o rynku**. Traktuj je jako „hashtag tego nie pokazuje", nie „tego nie ma".

### A0. Graf współpracy konkurencji (DOMYŚLNA metoda odkrywania)

Odwróć kierunek: zamiast szukać twórczyń, **zapytaj marki konkurencyjne, kogo oznaczają**. Marka oznacza tego, z kim realnie pracuje.

```
apify/instagram-post-scraper
{ "username": [8 marek konkurencyjnych], "resultsLimit": 30,
  "onlyPostsNewerThan": "1 year", "dataDetailLevel": "detailedData" }
```
Potem pobierz dataset (`apify datasets get-items <id> --format json > plik.json`) i z `jq` wyciągnij pola `ownerUsername,paidPartnership,mentions,likesCount,commentsCount`:
- `mentions` — kogo marka wspomina w treści
- `taggedUsers` / `coauthorProducers` — oznaczeni i współautorzy postów
- **`paidPartnership: true`** — zadeklarowana współpraca płatna, najmocniejszy sygnał
- **obce `ownerUsername`** w wynikach = posty współautorskie; ich właściciel to partner marki

Następnie profile-scrape wyłowionych kont (patrz sekcja D niżej po ile naraz i dlaczego).

**Dowód skuteczności (RO, 31.07.2026, ta sama nisza i budżet tego samego dnia):**

| | Hashtagi (~$0,40) | Graf konkurencji (~$0,60) |
|---|---|---|
| Kandydatki A-tier | **0** | **3** |
| Największe znalezione konto | 12k (sklep) | **60k (twórczyni)** |

Metoda grafowa znajduje też **leady, które nie są influencerami**, a bywają cenniejsze — media niszowe i festiwale rzemieślnicze (w RO: `@vizitadelucru` reportaże o ludziach pracujących z pasją, `@rocreator` festiwal artyzanów w Cluj). Nie wyrzucaj ich z wyników.

**Bonus diagnostyczny:** policz, ile w ogóle jest `paidPartnership: true`. Jeśli w 200+ postach konkurencji jest ich zero lub jeden — na tym rynku nikt nie robi influencer marketingu, więc pula twórczyń jest wolna, ale nie ma lokalnego wzorca do skopiowania.

### A1. Zacznij od tego, co firma już wie o rynku

Zanim odpalisz jakikolwiek scraper na nowym rynku: **przeszukaj repo**. Dla Rumunii istniał gotowy `export/RAPORT_TIER_A_dla_dyrektora_eksportu.md` z dystrybutorami (Secom Healthcare, Sano Vita), e-commerce'ami (Vegis.ro, Republica BIO, BioPortal.ro), oznaczonym konkurentem (Plafar) i wskazanym produktem wejściowym (**Atop Stop + Rescue Balm**) — a research poszedł od zera pod dezodorant i część budżetu przepadła.

Zawsze sprawdź: `export/`, `b2b/`, `spotkania/`, `MAPA.md`. Brief influencerski na nowy rynek ma wynikać ze strategii wejścia, nie odwrotnie.

### A. Walidacja hashtagów (uzupełniająca, nie pierwsza)

Cel: odsiać martwe i niskiej jakości hashtagi przed kosztownym deep-dive.

**Instagram:** `apify/instagram-hashtag-analytics-scraper`
```json
{
  "hashtags": ["biegaczka", "pobiegane", "kandydat1", "kandydat2", "kandydat3"],
  "includeLatestPosts": false,
  "includeTopPosts": false
}
```
- Maks 8 hashtagów na raz (kontrola kosztu)
- Wyciągasz: liczbę postów, top related hashtags (znajdziesz tam tagi których nie wymyśliłeś)
- **Pomijaj hashtagi <5k postów** (chyba że nisza jest skrajnie wąska)
- **Pomijaj hashtagi >2M postów** dla mikro-influ (zatłoczone, trudne do filtrowania)

### B. Deep-dive Top Posts (dla 4–5 najmocniejszych z A)

**Instagram:** `apify/instagram-hashtag-scraper`
```json
{
  "hashtags": ["topowy1", "topowy2", "topowy3", "topowy4", "topowy5"],
  "resultsLimit": 15,
  "resultsType": "posts"
}
```

**TikTok:** `clockworks/tiktok-hashtag-scraper`
```json
{
  "hashtags": ["topowy1", "topowy2", "topowy3", "topowy4", "topowy5"],
  "resultsPerPage": 25
}
```

- Cel: znaleźć konta które dzisiaj postują w niszy
- Wyciągasz tylko: username, fans (followers), bio/signature, text postu, diggCount/likes, link
- Pobierz dataset przez CLI (`apify datasets get-items <id> --format json > plik.json`) i filtruj przez `jq` do tych pól przed pokazaniem czegokolwiek w czacie — avatary/thumbnaile w pełnym payloadzie to głównie przepalony kontekst, nie techniczny limit (CLI go nie ma)

### C. User Search (opcjonalny, do uzupełnienia)

**Instagram:** `apify/instagram-search-scraper` z `searchType: "user"`
```json
{
  "search": "naturalna pielegnacja, skora atopowa, zero waste kosmetyki",
  "searchLimit": 10,
  "searchType": "user"
}
```
- Używaj jeśli deep-dive dał za mało kandydatów lub żeby pokryć nisze identity-based (np. „matka biegaczka")
- Wyniki search są mniej trafne niż hashtag deep-dive — traktuj jako uzupełnienie

### D. Profile Scraper (OPCJONALNY, dla shortlisty top 5–8)

Dla policzenia Engagement Rate dla finalnej shortlisty.

⚠️ **UWAGA: `apify/instagram-profile-scraper` zwraca `latestPosts` — ciężkie pole (media, captions) przy 30+ kontach.** Przez CLI nie ma tu twardego limitu 1MB (to było ograniczenie MCP), ale pełny payload to i tak niepotrzebnie dużo tokenów w moim kontekście. Rozwiązania:
1. Pobierz przez `apify datasets get-items <id> --format json > plik.json`, potem `jq` do pól: `username,followersCount,biography,businessCategoryName,externalUrl,verified` — odetnij `latestPosts.caption`, `latestPosts.images`, `latestPosts.displayUrl`, `latestPosts.videoUrl`, `latestPosts.taggedUsers`, `profilePicUrl`, `profilePicUrlHD`, `externalUrls`
2. Jeśli dataset jest duży i chcesz ograniczyć payload już przy pobieraniu (nie tylko po fakcie): `apify api GET "datasets/<id>/items" -p '{"fields":"username,followersCount,biography","omit":"latestPosts"}'` (gotcha opisana w skillu `apify-cli`)
3. Nadal rozsądnie ograniczaj liczbę kont na jeden run (koszt actora, nie limit narzędzia) — kilka–kilkanaście naraz, nie setki
4. Alternatywa: powiedz użytkownikowi że ER liczymy ręcznie dla top 5 (otworzyć profil, średnia like'ów z 5 ostatnich postów / followers × 100)

Wzór ER: `(średnia likes + comments z 12 ostatnich postów) / followers × 100`
- **>5%** — świetny dla mikro
- **3–5%** — bardzo dobry
- **1–3%** — standard
- **<1%** — słaby, pasywni followersi

---

## KROK 4 — Filtry odsiewu

### 🔴 Red flags (odrzuć od razu)

W bio lub nazwie konta:
- `studio tatuażu`, `klub biegowy`, `gospodarstwo`, `sklep`, `hurtownia`, `warzywniak`, `manufaktura X`, `firma`, `sp. z o.o.`
- `ambasadorka [marka]`, `[marka] team`, `sponsored by`, `współpraca: [link]`
- Kody rabatowe: `kod: XYZ -10%`, `code: XYZ`
- `coach`, `trener`, `kursy`, `akademia` (gdy edu/sprzedaż jest głównym tematem)
- `MLM`, `kolagen`, `suplementy` (sprzedawcy)
- Konta organizatorów: `[miasto] półmaraton`, `[nazwa] run club`, `[park narodowy]`

### 🟡 Yellow flags (sprawdź dokładniej, czasem OK)

- Sponsorzy w bio ale nie konkurencyjni z Opcją Natury (np. buty biegowe = OK dla dezodorantu, krem od konkurenta = nie)
- Linki do bloga / strony własnej (autentyczny twórca z marką osobistą — OK)
- Verified ale małe konto (sprawdź czy nie jest to konto firmy lub agencji)
- Konto głównie wideo bez bio (otwórz post, sprawdź ton)

### 🟢 Green flags (kandydaci A-tier)

- Bio z osobistą narracją („mama dwojga, biegam dla siebie")
- Kontakt mail w bio (sygnał otwartości na współpracę)
- Lifestyle ton w postach, nie sprzedażowy
- Wąska niche (zielarka, morsowanie, etnobotanika) z autentycznym contentem
- Linki do innych osobistych platform (YouTube, blog, podcast)

### Specyficzne dla Opcji Natury

- **Konflikty kontraktowe:** Suunto, Salomon, Garmin, Orlen, Sportano (mają lub miały kody rabatowe / ambasadorów w niszy sport)
- **Konkurencja kosmetyczna:** Nacomi, Yope, Sylveco, Weleda, Make Me Bio, La Rive — jeśli ambasadorka jednej z tych marek, oznacz jako C-tier z ostrzeżeniem
- **Mężczyźni** — domyślnie pomijaj dla kampanii konsumenckich (target Opcji to kobiety), chyba że nisza wymaga (np. tatuaż, sport mixed)

---

## KROK 5 — Output (zawsze tym samym formatem)

Stwórz plik markdown w `/mnt/user-data/outputs/` o nazwie `[nisza]_[platforma].md` (np. `dezodorant_instagram.md`, `morsowanie_obie.md`).

### Struktura pliku:

```markdown
# [Tytuł kampanii] — [Platforma]

**Data scrapingu:** [data]
**Cel kampanii:** [z briefu]
**Brief:** nisza = [X], platforma = [Y], skala = [Z], odsiać = [W]
**Źródła scrapingu:** [lista actorów + ile hashtagów × ile postów]

---

## Tier legenda

- **A-tier** — top kandydatki, autentyczny ton, zgodne z DNA marki
- **B-tier** — drugi rzut, dobre ale wymagają weryfikacji
- **C-tier** — uwagi (konflikty kontraktowe / konta firmowe / inne ryzyko)

---

## Kandydatki ([N] profili)

| Tier | Profil | Imię | Followers | Nisza | Bio (skrót) | Link | Komentarz |
|---|---|---|---|---|---|---|---|
| A | @xyz | Imię | 5 000 | sport-natura | „..." | [link](https://...) | Dlaczego A — konkretny powód |
...

---

## Wcześniej odrzucone profile

Pogrupowane po powodzie odrzucenia:

### Sklepy / firmy / instytucje
| Profil | Powód |
...

### Konta z konfliktem sponsorów
...

### Performance / fitness (nie pasuje do tonu marki)
...

### Mężczyźni (poza targetem kampanii)
...

### Pozostałe
...

---

## Wnioski strategiczne

- **Co działa w hashtagach niszy:** [...]
- **Co odsiać programowo następnym razem:** [...]
- **Czego brakuje na liście (kierunki do dalszego researchu):** [...]
- **Czy platforma pasuje do niszy:** [TAK / NIE z uzasadnieniem]

---

## Top 5 do pierwszego kontaktu

1. **@xyz** — [dlaczego top 1, konkretne uzasadnienie]
2. **@xyz** — [...]
...
```

Po zapisaniu pliku **wywołaj `present_files`** żeby użytkownik mógł go pobrać.

---

## KROK 5b — Zapis do bazy Analiz (OSTATNI KROK, nie pomijaj)

Research bez tego kroku zostaje plikiem, którego marketing nie znajdzie — czyli dokładnie
problemem, dla którego ta baza powstała.

Użyj skilla **`analizy-marketingowe`**: strona w bazie „Analizy marketingowe" w Notionie
(`Typ = influencer research`, `Tematy` z `influencerzy` + ewentualnie `konkurencja`/`kampania`,
`Kanał` = platformy z briefu, `Źródło = skill: influencer-research`, **adresat: Zuza**), plus plik
w `raporty_ai/influencerzy_raporty/` na Drive i `Link` do niego.

Tamten skill trzyma cały kontrakt zapisu — schematu, słowników ani ID nie odtwarzaj z pamięci.

Mapowanie sekcji researchu na szkielet bazy: brief i „dlaczego te nisze" → **1. Co się stało**;
kandydatki + odsiew → **2. Ustalenia**; wnioski strategiczne → **3. Sygnały wymagające decyzji**;
Top 5 do kontaktu → **4. Rekomendacje**; źródła scrapingu + data → **5. Metodologia**.
W metodologii **zawsze** dopisz datę scrape'u i ostrzeżenie, że zasięgi się starzeją.

---

## KROK 6 — Heurystyki uczciwości

Te zasady są ważniejsze niż dostarczenie długiej listy. Lepiej krótka uczciwa lista niż długa wymęczona.

### Kiedy powiedzieć „ta platforma nie pasuje do niszy"

Jeśli po deep-dive z 3+ hashtagów:
- Ponad 70% wyników to konta komercyjne lub spam → powiedz to wprost
- Konta autentyczne są wszystkie poniżej 500 followersów → niska użyteczność biznesowa
- Większość trafień to konta zagraniczne (algorytm zmiksował) → platforma słabo działa dla tej niszy w PL

**Przykład:** „TikTok PL pod tagi tatuażowe to feed studiów i tatuażystów. ~70% wyników to konta komercyjne. Dla linii Naturalny Tatuaż rekomenduję Instagram + B2B do polskich tatuażystów-influencerów."

### Kiedy powiedzieć „nie mam wystarczająco danych"

- Hashtagi z briefu są wszystkie martwe → poproś o nowe lub zaproponuj alternatywy z mapy
- Wyniki scrapingu pokazują 0 polskich kont → zaproponuj sąsiednie hashtagi lub inną platformę
- Brief jest zbyt szeroki („znajdź influ dla kosmetyków") → wróć z 3 pytaniami doprecyzowującymi

### Kiedy lista będzie krótka ale jakościowa

Lepiej oddać 8 kandydatek A/B-tier niż 25 z czego 20 to C-tier. **Nie wymuszaj listy 30 osób** jeśli nisza nie generuje takiej liczby trafień.

### Czego nigdy nie rób

- Nie wymyślaj kont których nie znalazłeś w scrapach
- Nie zgaduj liczby followersów — jeśli scraper nie zwrócił, napisz „nieznane" lub zrób osobny Profile Scraper
- Nie kopiuj profili z poprzednich scrape'ów do nowego — zawsze świeży scraping per brief
- Nie zostawiaj sekcji „Top 5" pustej — jeśli masz mniej niż 5 dobrych kandydatów, podaj top 3 i wyjaśnij dlaczego

---

## Constraints techniczne

### Duże payloady (dawniej: „limit 1MB tool output")
To była twarda ściana narzędzia MCP (`get-actor-output`/`get-dataset-items` >1MB → błąd), przez CLI (`apify datasets get-items`) już nie istnieje jako techniczny limit. Nadal warto filtrować — inaczej przepalasz mój kontekst na thumbnaile/avatary/listy postów z mediami, nie dlatego że coś się wywali:

**Po pobraniu, `jq` do pól:**
```
username,followersCount,biography,businessCategoryName,externalUrl,verified
```

**Albo odetnij (`jq 'del(...)'` lub `--omit` w `apify api` — patrz skill `apify-cli`):**
```
latestPosts.caption,latestPosts.images,latestPosts.displayUrl,profilePicUrl,profilePicUrlHD
```

### Apify Search Scraper hashtag = losowe wyniki
`apify/instagram-search-scraper` z `searchType: "hashtag"` zwraca semantycznie podobne (czasem zagraniczne) konta, nie konkretny hashtag. Dla hashtagów używaj **Hashtag Analytics** (walidacja) + **Hashtag Posts Scraper** (deep-dive).

### TikTok actor `clockworks/tiktok-hashtag-scraper`
- Limit ~800 video na hashtag (hard limit TikToka)
- Cena ~$0.001–0.005 per video w zależności od tieru
- Output zawiera dużo metadanych muzyki/wideo — używaj `fields` żeby ograniczyć

### Budżet orientacyjny per scraping
- Walidacja 8 hashtagów IG: ~$0.10–0.50
- Deep-dive 5 hashtagów × 15 postów IG: ~$0.50–1.50
- 25 video × 5 hashtagów TT: ~$0.50–1.50
- Profile Scraper 10 kont IG: ~$0.20

Całkowicie typowy research: **~$2–5 za pełną listę 20–30 kandydatów**.

---

## Przykład pełnego flow (skrócony)

```
USER: "Daniel pyta — znajdź mi influ pod morsowanie dla Mazidła"

AGENT: [przeprowadza dialog briefingowy]
  - kontekst: kampania na zimę, Mazidło + Atop Stop
  - nisza: morsowanie
  - platforma: Instagram (Daniel wybrał)
  - skala: mikro (5k–30k)
  - odsiąć: kluby morsujące jako organizacje, sklepy ze sprzętem

AGENT: "OK, plan: 
  1) waliduję 5 hashtagów morsowych
  2) deep-dive 3–4 najmocniejsze
  3) generuję plik morsowanie_instagram.md
  Ruszam."

[Hashtag Analytics: morsowanie, morsujemy, zimnakapielmoja, morsownik, morsowanie­polska]
[3 z 5 hashtagów działają, 2 to anty-hashtagi → zapisz do mapy jako "hipoteza odrzucona"]

[Deep-dive: 3 hashtagi × 15 postów = 45 kont do przeglądu]
[Filtrowanie: red flags → 18 odrzuconych, yellow → 6 do weryfikacji, green → 21 kandydatek]

[Generowanie pliku → present_files]

AGENT: "Gotowe. 21 kandydatek (12 A-tier, 7 B-tier, 2 C-tier). Top 1: @xyz —
        morsuje od 5 lat, bio z mailem, ER 6.2%, fokus na regenerację skóry.
        Plik: morsowanie_instagram.md"
```

---

## Aktualizacja mapy hashtagów

**Po każdym scrapingu nowej niszy zaktualizuj sekcję „Mapa hashtagów PL"** w tym pliku:
- Hashtagi „hipoteza" które się potwierdziły → przenieś do „zweryfikowane" z liczbą postów
- Hashtagi „hipoteza" które okazały się martwe → przenieś do „Anty-hashtagi"
- Nowe related hashtagi znalezione w Analytics → dopisz jako „zweryfikowane"

To utrzyma skill aktualny dla kolejnych użyć.
