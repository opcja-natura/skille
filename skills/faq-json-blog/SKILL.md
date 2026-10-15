---
name: faq-json-blog
description: FAQ do wpisu na blogu Opcji Natury w formacie JSON dla Contentful. Używaj, gdy piszesz albo sprawdzasz FAQ do wpisu blogowego, gdy ktoś pyta o schemat pliku FAQ, linki, anchory albo pola dozwolone w odpowiedziach, albo gdy trzeba zamienić FAQ z tekstu na JSON. Daje schemat, twarde zasady techniczne, limity linków, typowe błędy, checklistę i wzorcowy przykład. Głos odpowiedzi i to, co wolno napisać o kosmetyku, daje skill glos-opcja-natura. NIE do FAQ w artykule SEO ani w newsletterze (tam FAQ jest zwykłym tekstem).
---

# FAQ JSON do wpisu na blogu

FAQ do wpisu na blogu powstaje **od razu w JSON**, jako osobny plik obok treści wpisu
(`faq_<temat>.json`). Na stronie wyświetla się pod sekcją "Warto zapamiętać". Nie piszemy
najpierw FAQ w tekście wpisu, żeby potem je przenosić.

Jak mają brzmieć odpowiedzi i czego nie wolno w nich obiecać: skill **`glos-opcja-natura`**
(głos, `references/compliance.md`). Ten skill pilnuje formatu.

## Schemat (jedyny dopuszczalny)

```json
{
  "faq": [
    {
      "question": "Pytanie?",
      "answer": "Czysty tekst bez markdown.",
      "links": [
        { "anchor": "nazwa kosmetyku", "url": "https://opcjanatura.pl/sklep/..." }
      ]
    },
    {
      "question": "Pytanie bez linków?",
      "answer": "Tu pole links pomijasz całkowicie."
    }
  ]
}
```

**Dozwolone pola:** `faq`, `question`, `answer`, `links`, `anchor`, `url`. Nic więcej (żadnych
`source_url`, `id`, `tags`, `category`).

## Twarde zasady

1. **Brak markdown w `answer`**: żadnego pogrubienia, `[link](url)`, list, nagłówków.
2. **Linki tylko w tablicy `links`**, nigdy w treści odpowiedzi.
3. **`url` zawsze pełny**, z `https://`. Tylko adresy, które dostałaś; nie zgaduj.
4. **Pusta tablica `links` znika**: nie zostawiaj `"links": []`.
5. **Maksymalnie 2 linki na pytanie**, najczęściej 0 albo 1.
6. **Każdy kosmetyk linkowany raz na cały plik.** Dalej sama nazwa.
7. **Cudzysłowy proste** (`"`), polskie znaki bez escape'owania.
8. **`anchor` = nazwa kosmetyku, która pada w odpowiedzi**, w tej samej formie. Bez "nasz",
   "polecam".
9. Każde pytanie kończy się `?`.

## Treść odpowiedzi (format)

- **4-6 pytań** na wpis, w ramach tematu wpisu. Nowych tematów nie dokładasz.
- **4-6 zdań** na odpowiedź. Krótsza brzmi sucho, dłuższa jak akapit bloga.
- Układ, gdy pasuje: krótka odpowiedź (1-2 zdania), mechanizm albo kontekst (2-3 zdania),
  kosmetyk, jeśli naturalnie pasuje (1 zdanie).
- Pisz jak do osoby, która zadała to pytanie w wiadomości.
- Bez pytań o rany, choroby i leczenie (`glos-opcja-natura`, compliance, wzorzec 1).

## Kiedy linkować

- **Tak:** kosmetyk pada w odpowiedzi z nazwy, odpowiedź realnie dotyczy jego działania i nie
  był jeszcze linkowany w tym pliku.
- **Nie:** pytanie czysto edukacyjne; padają tylko składniki, nie nazwa kosmetyku; kosmetyk
  wspomniany przelotnie.

## Typowe błędy

| Błąd | Poprawka |
|------|----------|
| link w treści `answer` | tekst bez linka + tablica `links` |
| `"links": []` | pomiń pole |
| pogrubienie w odpowiedzi | czysty tekst |
| ten sam kosmetyk linkowany 2 razy | link raz, dalej sama nazwa |
| anchor "Mazidło", a w odpowiedzi "krem regenerujący" | dopisz nazwę do odpowiedzi albo nie linkuj |
| pole `source_url` lub inne | usuń |
| odpowiedź pasująca do każdej marki | konkret, mechanizm, nasz kosmetyk |
| "Bariera lipidowa stanowi kluczowy element fizjologii skóry." | "Bariera lipidowa to warstwa, która trzyma wodę w skórze. Zimą słabnie szybciej, niż się odbudowuje." |

## Kolejność pracy

1. Wpis jest napisany (`glos-opcja-natura`, `references/formaty/blog.md`).
2. Piszesz FAQ od razu w JSON.
3. Przegląd na gotowym JSON-ie: fakty, głos, prawo, literówki.
4. Checklista niżej.
5. Agata sprawdza fakty przed wrzuceniem na blog.

## Checklista

- [ ] JSON się parsuje
- [ ] Tylko dozwolone pola
- [ ] Brak markdown w `answer`
- [ ] Każde pytanie kończy się `?`
- [ ] `url` pełny, z `https://`, żaden nie jest zgadnięty
- [ ] Każdy kosmetyk linkowany najwyżej raz, najwyżej 2 linki na pytanie
- [ ] Brak `"links": []`
- [ ] Anchor = nazwa padająca w odpowiedzi
- [ ] 4-6 pytań, odpowiedzi 4-6 zdań
- [ ] Głos i compliance według `glos-opcja-natura` (kosmetyk, nie produkt; zero myślników)

## Przykład wzorcowy

```json
{
  "faq": [
    {
      "question": "Jak nawilżyć skórę twarzy zimą?",
      "answer": "Zimą skóra traci wodę szybciej niż w innych porach roku. Na zewnątrz mróz i wiatr, w środku suche powietrze z ogrzewania. Bariera lipidowa, która normalnie zatrzymuje wilgoć, ma podwójną robotę. Dlatego zimą warto przejść na bogatszy krem niż latem i nie pomijać hydrolatu po myciu. Hydrolat delikatnie nawilża skórę, zanim nałożysz krem, dzięki czemu krem lepiej się rozprowadza. Serum Owoce Nocy stosowane wieczorem dostarcza witaminę C i bioflawonoidy, które wspierają naturalną odnowę skóry w nocy.",
      "links": [
        { "anchor": "Serum Owoce Nocy", "url": "https://opcjanatura.pl/sklep/serum-owoce-nocy" }
      ]
    },
    {
      "question": "Dlaczego skóra twarzy jest sucha i napięta zimą?",
      "answer": "Zimą skóra dostaje z dwóch stron. Na zewnątrz mróz i wiatr wysuszają naskórek. W domu ogrzewanie obniża wilgotność powietrza do poziomu, który skórze nie służy. Do tego bariera lipidowa w chłodzie słabiej zatrzymuje wodę. Efekt to skóra sucha, szorstka, czasem reaktywna, choć latem nie sprawiała kłopotu. To nie wina kremu, tylko zmiana warunków, na którą pielęgnacja musi odpowiedzieć."
    }
  ]
}
```

Pytanie 1 ma jeden link, bo kosmetyk pada z nazwy i odpowiedź do niego nawiązuje. Pytanie 2 nie
ma pola `links`, bo jest czysto edukacyjne.
