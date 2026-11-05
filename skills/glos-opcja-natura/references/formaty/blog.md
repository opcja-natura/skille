# Wpis na blog

Głos opisuje `SKILL.md` i `warsztat-prozy.md`. Tu tylko budowa wpisu i to, co oddajesz.

## Zanim zaczniesz pisać

Nie zaczynaj bez:
- **H1**: tytuł wpisu,
- **H2**: główne sekcje (jeśli ich nie dostałaś, zapytaj; przy wpisach pod SEO są w briefie),
- **tematu**: co czytelnik ma z wpisu wynieść,
- **kosmetyków do wymienienia**: same nazwy; wiedzę o nich bierzesz ze źródeł (strona, inne skille).

Przydatne: sezon albo kampania, w którą wpis się wpisuje. Sprawdź też, czy temat już był na
blogu (nie piszemy drugiego wpisu na to samo).

### Brief

Brief przychodzi od Daniela i ma jeden z dwóch kształtów:

 - JSON na podstawie wytycznych agencji:
```json
{
  "h1": "Tytuł artykułu (fraza kluczowa)",
  "h2": ["Sekcja 1", "Sekcja 2", "Sekcja 3"],
  "url_1": "https://opcjanatura.pl/sklep/...",
  "anchor_1": "tekst linku",
  "url_2": "https://opcjanatura.pl/blog/...",
  "anchor_2": "https://opcjanatura.pl/blog/..."
}
```
 - strona Notion na podstawie Senuto, która jest napisana bardziej dla copywritera, wymaga jego decyzji o kierunku treści, ale zawiera wszelkie elementy tekstu dla SEO.

Minimum: 1 H1, 3 sekcje H2, 2 linki. Gdy anchor jest samym adresem, link wstawiasz jako czysty
adres. Linki osadzasz naturalnie, w zdaniu, które ma sens merytorycznie. Nie dostałaś briefu,
poproś o niego.

Pamiętaj o AI SEO, brief z Notiona zawiera też ten element. Nie ignoruj go. Jak pisać pod Google
i odpowiedzi AI: `references/geo.md`.

## Co oddajesz: osobne pliki, nie jeden

Wpis to **kilka osobnych dokumentów**. Nikt nie wycina potem kawałków z jednego pliku.

| Plik | Co w nim jest |
| :-- | :-- |
| **treść wpisu** | H1, pierwszy akapit z podsumowaniem, sekcje H2. Bez excerptu, bez FAQ i bez bibliografii. |
| **`excerpt`** (zawsze oddzielny plik o tej nazwie: `excerpt.md` albo dokument `excerpt` na Dysku) | sam excerpt, 50-70 słów, nic więcej |
| **FAQ** (`faq_<temat>.json`) | 4-6 pytań w JSON, format ze skilla `faq-json-blog` |
| **bibliografia** (`bibliografia_<temat>.json`) | gdy wpis cytuje badania, format ze skilla `bibliografia-blog` |
| **zdjęcia** (podfolder `foto/`) | okładka z `okladka_` na początku nazwy, reszta to zdjęcia do tekstu; przygotowuje je grafik, nie Ty |

Wszystko w jednym folderze wpisu.

## Budowa treści

**Długość:** 7 000-10 000 znaków ze spacjami.

**Kolejność:**

1. `# H1`, jeden, **bez emotki**.
2. **Pierwszy akapit: podsumowanie wpisu**, zwykły tekst bez nagłówka, 3-5 zdań. Od razu daje
   odpowiedź na pytanie z tytułu i najważniejsze wnioski, po ludzku, głosem marki. Dawną sekcję
   "Warto zapamiętać" przenosimy właśnie tu: na końcu wpisu już jej nie ma.
3. `## H2`: 4-6 sekcji zgodnych z briefem. **Pierwsze H2 pojawia się dopiero po pierwszym
   akapicie.** Scena albo pytanie czytelniczki (ruch 7 w `warsztat-prozy.md`) może otwierać
   pierwszą sekcję. H2 mogą mieć emotkę, jeśli pasuje, nie każdy musi.

```
# Jak zachować kolor tatuażu

Słońce rozbija cząsteczki tuszu, więc najbardziej pomaga SPF 50 każdego dnia, przez cały rok.
Reszta to systematyczne nawilżanie, które utrzymuje intensywność koloru, i delikatne złuszczanie,
które przywraca kontrast.

## Dlaczego tatuaż blednie?
```

## Excerpt

50-70 słów, zawsze w oddzielnym pliku o nazwie `excerpt` (patrz wyżej), nigdy w treści wpisu.
Streszcza wartość wpisu i zachęca do czytania. Nie zaczyna się od nazwy marki ani od ogólnika. To
nie jest pierwszy akapit wpisu wklejony drugi raz: mają inne zadania, więc napisz je osobno.

> Świeży tatuaż potrzebuje czasu i właściwej pielęgnacji. Swędzenie, łuszczenie, chwilowe
> blaknięcie kolorów? To normalne etapy. Odnowa skóry trwa od 2 do 3 miesięcy. Sprawdź, czego się
> spodziewać na każdym etapie.

## Formatowanie

- **Bez tabel w treści wpisu.** Blog ich nie wyświetla poprawnie. Porównanie zamień na listę albo
  na krótkie akapity ("Skóra sucha: tak. Skóra tłusta: nie.").
- **Emoji:** maksymalnie 3-4 na cały wpis. H1 i pierwszy akapit nigdy.
- **Pogrubienia:** nazwa kosmetyku przy pierwszym wystąpieniu, kluczowy termin przy
  wprowadzeniu, ważne zalecenie. Reszta bez.
- **Listy:** gdy treść tego wymaga (kroki, kilka równorzędnych porad). Nie zamiast tekstu.
- **Linki:** tylko te, które dostałaś. Przed linkiem zawsze stoi zwykły tekst, nie sam
  pogrubiony nagłówek ("**Polecamy:** [link]" na stronie się skleja; pisz "Polecamy Ci [link]").
- **Bez FAQ w treści.** FAQ żyje w swoim pliku JSON.

## FAQ do wpisu

4-6 pytań, od razu w JSON. Schemat, limity linków i walidacja: skill `faq-json-blog`.
Głos odpowiedzi: jak odpowiedź na wiadomość od klientki, 4-6 zdań, od razu bezpośrednia odpowiedź ("Tak", "Nie", "Zwykle..."), mechanizm zamiast ogólnika,
"kosmetyk", nie "produkt". Pytania o rany i choroby nie wchodzą, uważaj na odpowiedzi pod kątem prawnym (`compliance.md`, wzorzec 1).

## Checklista przed oddaniem

- [ ] Osobne pliki: treść, `excerpt`, FAQ JSON, (bibliografia), `foto/`
- [ ] H1 bez emotki
- [ ] Pierwszy akapit to podsumowanie, a pierwsze H2 stoi dopiero po nim
- [ ] Na końcu wpisu nie ma już sekcji "Warto zapamiętać"
- [ ] Excerpt w pliku `excerpt`, 50-70 słów, nie od nazwy marki, nie powtarza pierwszego akapitu
- [ ] 4-6 sekcji H2 zgodnych z briefem
- [ ] Zasady z `references/geo.md`, bez kwot i bez wymyślonych liczb
- [ ] Zero tabel, zero myślników, maks. 3-4 emoji
- [ ] Nazwy kosmetyków pogrubione przy pierwszym użyciu i zgodne ze stroną sklepu
- [ ] 7 000-10 000 znaków
- [ ] Audyt AI i szybki test z `SKILL.md`
- [ ] Audyt prawny z `compliance.md` (szczególnie wzorce 1-5)
