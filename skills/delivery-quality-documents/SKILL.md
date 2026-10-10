---
name: delivery-quality-documents
description: Podpinanie dokumentów jakościowych (Certyfikat Analizy/CoA, karty MSDS, deklaracje dostawcy itp.) do konkretnej dostawy surowca Opcja Natura, bezpośrednio z rozmowy przez Google Drive i Google Sheets. Używaj, gdy operator chce podpiąć dokument jakościowy do dostawy, sprawdzić jakie dokumenty ma dana dostawa albo dany surowiec, albo znaleźć dostawę do podpięcia dokumentu. To NIE jest ten sam system co stałe dokumenty surowca (SDS, certyfikat pochodzenia, deklaracja alergenów itd. — od tego jest skill `raw-material-documents`) — tu dokument jest przypisany do konkretnej pozycji konkretnej dostawy, nie do surowca jako stałego atrybutu.
---

# Dokumenty jakościowe dostaw surowców Opcja Natura

## Cel

Obsłuż proces `dostawa (pozycja surowca) -> dokument jakościowy tej dostawy` bez wymagania od operatora ręcznego edytowania tabel ani znajomości ID. Traktuj arkusz `dokumentacja_surowce` jako source of truth, a Drive (folder archiwum) jako magazyn plików.

## Granica z `raw-material-documents`

Dwa oddzielne systemy, oddzielne arkusze:

| | `raw-material-documents` | `delivery-quality-documents` (ten skill) |
|---|---|---|
| Co opisuje | stały dokument surowca (SDS, certyfikat pochodzenia, deklaracja alergenów, IFRA...) | dokument jakościowy jednej konkretnej dostawy |
| Grain | 1 dokument logiczny na (surowiec, typ) z wersjami | 1 wiersz na (dostawa, surowiec, dokument) |
| Arkusz | `BD_surowiec_dokumenty` (`1jPGq47sgSVsBRpcB_WGzIIKO2gC9dGdWjBd13BoRIaQ`) | `dokumentacja_surowce` (`11caP8XxVKVO2tzEH4UFl1VJihX_rcyGYGxiBJev0Ak0`) |
| Wersjonowanie / archiwizacja | tak, `is_current` + `_archive` | nie — każda dostawa to nowy, niezależny wiersz |

Jeśli operator w trakcie rozmowy z tym skillem prosi o SDS/certyfikat pochodzenia/inny stały dokument surowca (nie przypisany do konkretnej dostawy) — powiedz, że to obsługuje skill `raw-material-documents`, i tam się przełącz. Analogicznie, `raw-material-documents` przy prośbie o dokument jakościowy dostawy powinien kierować tutaj.

## Inne wejścia do tej samej tabeli

`dokumentacja_surowce` jest też zapisywana przez dwa inne kanały poza tym skillem:

- n8n workflow `rlQMTUIDAtHlwiAn` — mail z PDF-em na `dostawy.opcjanatura@gmail.com`, AI dopasowuje dostawę, human-in-the-loop przez mail, potem upload + append,
- AppSheet webhook `wJxjzMrb1IU0gSJu` — bezpośredni upload z formularza.

Ten skill jest **trzecim, konwersacyjnym wejściem** do tej samej tabeli. Zapisuj w dokładnie tym samym formacie (kolumny, konwencja nazwy pliku, metadata) co tamte dwa kanały — patrz `references/schema.md` i `references/project-resources.md`. Nie zakładaj, że jesteś jedynym źródłem zapisu; zawsze odczytuj stan live przed sprawdzeniem duplikatów.

## Najważniejsza zasada

Nie zgaduj i nie zapisuj częściowej operacji. Najpierw odczytaj stan live, zidentyfikuj dokładnie surowiec i pozycję dostawy (operator nie musi znać `id_dostawy` ani `_id_local` — Ty je ustalasz), pokaż podsumowanie i uzyskaj potwierdzenie. Dopiero potem wykonuj mutacje.

## Zasoby

Przed pierwszą operacją w sesji przeczytaj odpowiednie sekcje:

- `references/project-resources.md` — ID baz, folderów, granica z n8n/AppSheet.
- `references/schema.md` — tabele, kolumny, klucze dopasowania.
- `references/workflows.md` — procedury dla każdej operacji.
- `references/validation.md` — walidacje, pliki, duplikaty.
- `references/operator-dialog.md` — jak prowadzić rozmowę i jak potwierdzać wynik.

## Sposób pracy

1. Ustal tożsamość operatora, jeśli potrzebna do komunikatów/logu (ten arkusz nie ma pola "kto wykonał operację" — patrz `references/schema.md`, nie dopisuj własnej kolumny).
2. Rozpoznaj intencję operatora:
   - podpięcie dokumentu jakościowego do dostawy,
   - podgląd dokumentów jakościowych surowca / dostawy.
3. Zidentyfikuj surowiec (nazwa → `surowiec_id`, format `SUR__nnn` — ta sama pula ID co w `raw-material-documents`).
4. Znajdź konkretną pozycję dostawy (`id_dostawy` + `_id_local`) dla tego surowca. To Ty to ustalasz, nie operator — patrz `references/workflows.md`, workflow 1, krok 2. Przy więcej niż jednej sensownej kandydatce pokaż listę i poproś o wybór.
5. Sprawdź, czy dla tej pozycji nie ma już dokumentacji (możliwy duplikat) — ostrzeż, nie blokuj automatycznie.
6. Pokaż podsumowanie przed zapisem: surowiec, dostawa (ID, data przyjęcia, dostawca), plik, docelowa nazwa. Poproś o potwierdzenie.
7. Wykonaj w bezpiecznej kolejności: najpierw upload pliku do Drive, dopiero po sukcesie dopisz wiersz do `dokumentacja_surowce`. Po zapisie zrób read-back.
8. Po sukcesie podaj lokalizację pliku i potwierdzenie zapisanego wiersza.

## Reguły biznesowe

- Klucz dopasowania pozycji dostawy to `_id_local` (kol. M w `dostawy_surowce`) = `id_surowiec_local` (kol. D w `dokumentacja_surowce`). Globalnie unikalny, jednoznacznie wskazuje pozycję nawet gdy ten sam surowiec jest w dostawie wielokrotnie.
- Nie ma tu wersjonowania ani archiwizacji — każda dostawa to niezależny wiersz. Nie próbuj "zastępować" starego dokumentu przy nowej dostawie tego samego surowca.
- Duplikat = już istniejący wiersz z tym samym `id_surowiec_local`. To sygnał do ostrzeżenia operatora, nie twardy blok — dostawca może przesłać uzupełniający dokument (np. CoA + osobno MSDS) do tej samej pozycji.
- Plik zatwierdzony jest PDF-em (jak w `raw-material-documents`); jeśli źródło jest innym formatem możliwym do eksportu, eksportuj do PDF.
- Konwencja nazwy pliku w Drive: `<surowiec_id>__<oryginalna_nazwa_bez_rozszerzenia>__<id_dostawy>` (dokładnie jak w n8n workflow — nie zmieniaj formatu).
- Nie usuwaj wierszy z `dokumentacja_surowce` ani plików z folderu archiwum.
- `id_dostawy` w tej tabeli bywa przepinane przez `delivery/splitDelivery` przy splicie dostawy — to nie jest Twoja odpowiedzialność, nie koryguj go ręcznie.

## Brak możliwości zapisu

Jeśli w bieżącym środowisku nie ma połączonego Google Drive/Sheets z prawem zapisu, nie symuluj operacji. Powiedz, że do wykonania mutacji potrzebne jest połączenie z prawem zapisu i podaj operatorowi dokładnie, jaki krok był planowany.
