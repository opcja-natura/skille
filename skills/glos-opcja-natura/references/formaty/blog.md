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

Pamiętaj o AI SEO, brief z Notiona zawiera też ten element. Nie ignoruj go.

## Co oddajesz: osobne pliki, nie jeden

Wpis to **kilka osobnych dokumentów**. Nikt nie wycina potem kawałków z jednego pliku.

| Plik | Co w nim jest |
| :-- | :-- |
| **treść wpisu** | H1, akapit wstępu, sekcje H2, "Warto zapamiętać". Bez FAQ i bez bibliografii. |
| **excerpt** (osobny dokument, w nazwie słowo `excerpt`) | sam excerpt, 50-70 słów, nic więcej |
| **FAQ** (`faq_<temat>.json`) | 4-6 pytań w JSON, format ze skilla `faq-json-blog` |
| **bibliografia** (`bibliografia_<temat>.json`) | gdy wpis cytuje badania, format ze skilla `bibliografia-blog` |
| **zdjęcia** (podfolder `foto/`) | okładka z `okladka_` na początku nazwy, reszta to zdjęcia do tekstu; przygotowuje je grafik, nie Ty |

Wszystko w jednym folderze wpisu.

## Budowa treści

**Długość:** 7 000-10 000 znaków ze spacjami.

**Kolejność:**

1. `# H1`, jeden, **bez emotki**.
2. **Akapit wstępu**, czyli zwykły tekst bez nagłówka. Pierwsze H2 pojawia się dopiero **po**
   nim. Wstęp otwiera scenę albo pytanie czytelniczki (ruch 7 w `warsztat-prozy.md`). To nie
   jest excerpt wklejony drugi raz: excerpt żyje w swoim pliku, wstęp pisz jako początek
   rozmowy.
3. `## H2`: 4-6 sekcji zgodnych z briefem. Mogą mieć emotkę, jeśli pasuje, nie każdy musi.
4. `## Warto zapamiętać`: 3-5 punktów z pogrubionym początkiem, przed FAQ.

```
## Warto zapamiętać

* **Słońce rozbija cząsteczki tuszu**, więc SPF 50 każdego dnia, cały rok.
* **Nawilżenie to podstawa**: systematyczna pielęgnacja utrzymuje intensywność koloru.
* **Peeling odsłania pigment**: delikatne złuszczanie przywraca kontrast.
```

## Excerpt

50-70 słów. Streszcza wartość wpisu i zachęca do czytania. Nie zaczyna się od nazwy marki ani
od ogólnika. Osobny dokument (patrz wyżej).

> Świeży tatuaż potrzebuje czasu i właściwej pielęgnacji. Swędzenie, łuszczenie, chwilowe
> blaknięcie kolorów? To normalne etapy. Odnowa skóry trwa od 2 do 3 miesięcy. Sprawdź, czego się
> spodziewać na każdym etapie.

## Formatowanie

- **Bez tabel w treści wpisu.** Blog ich nie wyświetla poprawnie. Porównanie zamień na listę albo
  na krótkie akapity ("Skóra sucha: tak. Skóra tłusta: nie.").
- **Emoji:** maksymalnie 3-4 na cały wpis (H2 + "Warto zapamiętać" razem). H1 nigdy.
- **Pogrubienia:** nazwa kosmetyku przy pierwszym wystąpieniu, kluczowy termin przy
  wprowadzeniu, ważne zalecenie. Reszta bez.
- **Listy:** gdy treść tego wymaga (kroki, kilka równorzędnych porad). Nie zamiast tekstu.
- **Linki:** tylko te, które dostałaś. Przed linkiem zawsze stoi zwykły tekst, nie sam
  pogrubiony nagłówek ("**Polecamy:** [link]" na stronie się skleja; pisz "Polecamy Ci [link]").
- **Bez FAQ w treści.** FAQ żyje w swoim pliku JSON.

## FAQ do wpisu

4-6 pytań, od razu w JSON. Schemat, limity linków i walidacja: skill `faq-json-blog`.
Głos odpowiedzi: jak odpowiedź na wiadomość od klientki, 4-6 zdań, mechanizm zamiast ogólnika,
"kosmetyk", nie "produkt". Pytania o rany i choroby nie wchodzą, uważaj na odpowiedzi pod kątem prawnym (`compliance.md`, wzorzec 1).

## Checklista przed oddaniem

- [ ] Osobne pliki: treść, excerpt, FAQ JSON, (bibliografia), `foto/`
- [ ] H1 bez emotki
- [ ] Akapit wstępu przed pierwszym H2
- [ ] Excerpt 50-70 słów, nie od nazwy marki, nie powtórzony jako wstęp
- [ ] 4-6 sekcji H2 zgodnych z briefem
- [ ] "Warto zapamiętać" (3-5 punktów) na końcu treści
- [ ] Zero tabel, zero myślników, maks. 3-4 emoji
- [ ] Nazwy kosmetyków pogrubione przy pierwszym użyciu i zgodne ze stroną sklepu
- [ ] 7 000-10 000 znaków
- [ ] Audyt AI i szybki test z `SKILL.md`
- [ ] Audyt prawny z `compliance.md` (szczególnie wzorce 1-5)
