---
name: produkty-lookup
description: Oficjalne dane o kosmetykach i zestawach Opcji Natury (skład INCI i po polsku, działanie, sposób użycia, przeciwwskazania, cena, zdjęcia, link do sklepu, zestawy pod problem skóry, kategorie). Używaj zawsze, gdy w rozmowie lub tekście pojawia się konkretny kosmetyk, jego skład, cena, pojemność albo link, zanim podasz te dane komukolwiek, i gdy ktoś pyta „co polecić na…”, „co jest w zestawie…”, „jaki skład ma…”, „ile kosztuje…”.
---

# Dane o kosmetykach Opcji Natury

Dane o kosmetykach bierzesz **wyłącznie z konektora „Opcja Natura — produkty”**. To oficjalny katalog ze sklepu opcjanatura.pl, odświeżany raz dziennie. Nigdy nie podawaj składu, ceny, pojemności ani działania z pamięci.

## Którego narzędzia użyć

| Pytanie | Narzędzie |
| :-- | :-- |
| „Co mamy na…”, „jakie są balsamy”, lista z cenami | `produkty_szukaj` (fraza, problem, typ skóry, forma) |
| skład, działanie, sposób użycia, FAQ, zdjęcia jednego kosmetyku | `produkty_karta` (nazwa albo EAN; `sekcje` np. `["sklad"]`, żeby dostać tylko to, czego potrzeba) |
| „co polecić na suchą cerę”, zestaw, rutyna | `produkty_rutyna` (problem) |
| struktura sklepu, co jest w kategorii | `produkty_kategorie` |

Wersja angielska: parametr `rynek: "EN"`.

## Zasady

- **Cenę podawaj z datą danych i linkiem**, tak jak zwraca je konektor. Promocje mają termin.
- **Link „brak”** znaczy, że nie znamy jeszcze adresu tej strony. Nie twórz go sam.
- **Konektor zwraca kilka pasujących nazw?** Dopytaj, o który kosmetyk chodzi, zamiast wybierać.
- Dane podajesz tak, jak są w karcie. Jeśli coś w nich wygląda na błąd, powiedz o tym, ale nie poprawiaj sam.
- Tekst na zewnątrz (post, opis, mail) pisz według `glos-opcja-natura`: karta mówi, co kosmetyk ma i do czego służy, a głos marki mówi, czego nie wolno obiecywać.

## Gdy konektora nie ma w rozmowie

Powiedz wprost: „Nie mam dostępu do konektora Opcja Natura — produkty. Włącz go w ustawieniach konektorów (albo przez „+” w oknie rozmowy) i zapytaj jeszcze raz.” Do tego czasu możesz podać tylko link do sklepu https://opcjanatura.pl/sklep/, bez danych o kosmetyku.
