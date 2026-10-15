# Artykuł SEO

Tekst pisany jednocześnie dla Google i dla czytelnika. Odpowiada na realne pytanie ("jak
zachować kolor tatuażu") i przy okazji pozycjonuje stronę na konkretne frazy. Rozwiązuje
problem, nie sprzedaje.

Głos jak wszędzie (`SKILL.md`), z jedną różnicą: **rejestr bardziej formalny niż blog.**
Mniej "Patrzysz na swój tatuaż i...", więcej "Skóra z tatuażem potrzebuje...". Dalej po
ludzku i konkretnie, tylko bez blogowej poufałości.

Artykuły SEO często pisze agencja albo copywriter. Wtedy Twoja rola to **audyt przed
publikacją**: `compliance.md`, sekcja 6. Wszystkie siedem uwag prawnika z września 2026 dotyczyło
właśnie artykułów SEO.

## Brief: bez niego nie zaczynasz

Brief przychodzi od Daniela (narzędzia SEO) w takim kształcie:

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

Minimum: 1 H1, 3 sekcje H2, 2 linki. Gdy anchor jest samym adresem, link wstawiasz jako czysty
adres. Linki osadzasz naturalnie, w zdaniu, które ma sens merytorycznie. Nie dostałaś briefu,
poproś o niego.

## Budowa

**Długość:** 10 000-15 000 znaków ze spacjami.

1. `# H1` zgodny z briefem, bez emotki.
2. **Wstęp bez nagłówka**, 150-250 słów. Pierwsze H2 dopiero po nim. Hook w pierwszym zdaniu,
   główna fraza w pierwszym akapicie.
3. `## H2` z briefu (6-10 sekcji). Frazy w nagłówkach brzmią naturalnie, bez upychania.
4. **Podsumowanie**: krótkie, z praktycznym wnioskiem. Bez "Jak widać, pielęgnacja jest ważna".
5. **FAQ w treści artykułu**, 6-10 pytań (tu FAQ jest w markdownie, inaczej niż na blogu):

```
## Najczęściej zadawane pytania o [temat]

### Pytanie tak, jak wpisuje je człowiek w Google?

Odpowiedź w 3-5 zdaniach, konkretna, z mechanizmem. **Pogrubienie** kluczowego terminu.
```

## Formatowanie

- **Emoji:** zero, najwyżej 1-2 w całym tekście, gdy sekcja to uzasadnia.
- **Listy punktowane:** tak, pomagają Google i czytelnikowi skanować tekst.
- **Pogrubienia:** kluczowe terminy, nazwy kosmetyków, ważne fakty.
- **Frazy kluczowe:** główna w pierwszym akapicie, dalej warianty i synonimy ("pielęgnacja
  tatuażu", "dbanie o tatuaż"). Bez upychania.

## Nagłówki i lead to najczęstsze miejsca problemów prawnych

"Bez chemii", "bez podrażnień", nazwa choroby albo obietnica efektu w H1/H2 waży więcej niż w
treści. Przykłady zakwestionowane przez prawnika: "Naturalny dezodorant: skuteczna ochrona bez
aluminium i podrażnień", "Anty tarka: nowoczesna kuracja na pięty bez agresywnego tarcia",
"składniki, których warto unikać".

## Checklista przed oddaniem

- [ ] H1 zgodny z briefem, bez emotki
- [ ] Wstęp bez nagłówka przed pierwszym H2, fraza w pierwszym akapicie
- [ ] H2 zgodne z briefem
- [ ] Linki z briefu wstawione naturalnie, żadnych wymyślonych
- [ ] FAQ 6-10 pytań w treści
- [ ] 10 000-15 000 znaków, zero myślników, emoji minimum
- [ ] "Kosmetyk", nie "produkt"; brak zakazanych słów
- [ ] Audyt prawny z `compliance.md` (sekcja 6), także nagłówki
- [ ] Każde zdanie o kosmetyku zgodne z jego stroną w sklepie
