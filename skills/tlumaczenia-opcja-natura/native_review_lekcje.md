# Lekcje z recenzji native speakera (EN)

Wzorce, które brytyjski redaktor poprawił w naszych tekstach, a których nie łapie ani tłumacz, ani
kontrola pisowni. Czytaj **po napisaniu tekstu EN, przed oddaniem**: przejdź listę i szukaj tych
konstrukcji w swoim tekście. Część łapie automatycznie `check_en.py` (oznaczone 🤖).

Źródło: recenzja Scribbr, 2026-10-13 (Atop Stop, Bye-Bye Pumice). Pełny rejestr decyzji:
`modele-wszystko/opcjanatura_pl/opisy_produktow/en/_review/2026-10-13_decyzje_native_review.md`.
Każda kolejna recenzja dopisuje tu nowe wzorce, nie nowe pliki.

## 1. Kalki z polskiego

| Polski odruch | Kalka (❌) | Po angielsku (✅) |
|---|---|---|
| nawet kilka razy dziennie | even several times a day 🤖 | up to several times a day · as often as you like |
| odnaleźć równowagę | helps it find its balance again 🤖 | helps the skin maintain its natural balance |
| towarzyszy mu mocznik | It’s joined by urea… 🤖 | We combined it with urea… · Alongside it, urea… |
| aż 30% mocznika | a full 30% urea 🤖 | urea at a 30% concentration · contains 30% urea |
| klasyczne kremy | classic creams 🤖 | standard creams · ordinary creams |
| wnika w skórę | sinks into the skin 🤖 | absorbs into the skin |
| nie nadąża (o produkcie) | a lotion can’t keep up with | a lotion can’t provide |
| łagodzi uczucie podrażnienia | soothes the feeling of irritation | soothes skin that feels irritated |
| jedyna wada tego kremu | the only downside of | the only downside to |
| nie lubi się z olejkami | doesn’t get on well with | doesn’t tolerate … well |
| nie pachnie niczym | smells of nothing at all · has a neutral odour 🤖 | is completely unscented · scent-free |

*Odour* w kosmetykach znaczy brzydki zapach. O produkcie: *scent*, *unscented*, *scent-free*.

## 2. Polski rytm, który po angielsku jest balastem

- **Dopowiedzenie na końcu zdania**, które powtarza to, co już padło: *„…as if nothing agrees with it”*, *„…exactly as intended”*, *„…not something missing”*, *„…and helps keep it where it’s needed”*, *„flakes of skin coming away”*. Polski tekst domyka myśl drugi raz dla rytmu; angielski redaktor to tnie. Jeśli koniec zdania da się wyciąć bez utraty informacji, wytnij.
- **Wstęp-deklaracja przed odpowiedzią w FAQ:** *„It’s a deliberate choice.”* przed wyjaśnieniem, dlaczego. Zacznij od wyjaśnienia.
- **Długie zdania sklejone „and … and over time…”** → podziel na dwa. Angielskie zdanie produktowe ma jedną myśl.
- **Urwane zdania bez orzeczenia:** *„Also suitable for…”*, *„Finished with cooling peppermint essential oil.”* Po polsku to styl, po angielsku notatka. Pełne zdanie (formuły MHRA nie ruszasz, tylko obudowujesz: *„It is also suitable for people who may be prone to eczema.”*).

## 3. Logika i precyzja

- **„Instead of adding more fragrance”** sugeruje, że zapach już był. Sprawdzaj *more*, *again*, *even*, czy nie przemycają założenia.
- **Niejasne „it”**: gdy w zdaniu są skóra, mikrobiom i formuła, *it* może znaczyć każde z nich. Nazwij rzeczownik (*the skin*).
- **„very” i inne wzmacniacze** 🤖: zamień na konkret albo wytnij. *very hard heels* → *heels with thick, hard skin*, *very hard skin* → *stubborn hard skin*. **Wyjątek:** *very dry skin* to kategoria typu skóry, zostaje.
- **Kto zrobił badanie:** native od razu pyta, kto przeprowadził test konsumencki. Przy każdym teście podawaj wykonawcę, jeśli go znamy.

## 4. Typografia UK

- Apostrofy i cudzysłowy drukarskie: *it’s*, *“…”* 🤖 (nie `'` ani `"`).
- Spacja między liczbą a jednostką: *200 ml*, *50 ml* 🤖. Bez spacji przed %: *30% urea*.
- **„and” zamiast „&”** wszędzie poza nazwami produktów i podtytułami, także w hasłach na zdjęcia (*Urea and panthenol*) 🤖.
- **Myślniki:** w prozie najwyżej jeden na akapit 🤖. Redaktor zamienił ok. 2/3 naszych myślników na przecinki, kropki i dwukropki. Myślnik jako separator w Benefits (*bold — reszta*) zostaje.
- Liczby do dziesięciu słownie w prozie (*ten years*), mimo że redaktor akademicki zmieni na cyfry.

## 5. Czego NIE przejmować od recenzenta

Recenzenci z serwisów korektorskich (Scribbr) to zwykle redaktorzy akademiccy. Ich odruchy psują tekst sklepowy:

- formalny rejestr: *requires* zamiast *needs*, *daily* zamiast *a day*, *retain* zamiast *keep*, *differentiating it from*;
- zmiany w zablokowanych formułach compliance (glosariusz §6) i w stałych tekstach (`SZABLON_EN.md`);
- zmiany sensu: warunek w ostrzeżeniu, przypisanie działania innemu składnikowi;
- usuwanie słów kluczowych z feedów (*natural*);
- wielkie litery w nazwach pól technicznych (`page_title`).

Zasada: przyjmij **sygnał** (to zdanie brzmi obco), ale poprawkę napisz sam, w naszym rejestrze.
Z recenzji 2026-10-13 tak powstały m.in. *„Less tightness and roughness”* (recenzent: *„Easing of tightness…”*) i *„is completely unscented”* (recenzent: *„has a neutral odour”*).

## 6. Sygnał o marce

Native przeczytał „Option Nature” w tytule jak krzywą frazę (*„Do you mean ‘a natural option’?”*). Nazwa zostaje, ale w tytułach SEO i feedach daj jej kontekst. Glosariusz, decyzja D9.
