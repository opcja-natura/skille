# Inne bazy w workspace Notion Opcja Natura + zasady MCP

Rzadziej używane bazy, spięte relacjami z zadaniami, kampaniami i projektami. Kampanie i projekty opisuje skill `marketing-opcja-natura`. Przed zapisem do bazy, której tu nie ma albo która mogła się zmienić, **zawsze** pobierz schemat: `notion-fetch("collection://<data_source_id>")`.

## Mapa

```
Projects ──┬── Marketing Campaigns ──┬── Publikacje marketingowe ── Tasks Tracker (zadania automatu)
           │                         └── Tasks Tracker
           └── Tasks Tracker
Tasks Tracker ↔ Meetings ↔ Kontakty;  Kampanie / Tasks ↔ Analizy marketingowe
```

| Baza | data_source_id |
|---|---|
| Tasks Tracker | `25adee07-c0dd-80b1-a822-000b6037f86a` |
| Publikacje marketingowe | `25cdee07-c0dd-8090-8304-000b514105f9` |
| Marketing Campaigns | `25bdee07-c0dd-8074-a650-000b4e3d4fd0` |
| Projects | `1f4dee07-c0dd-80c8-b00e-000b544e79d2` |
| Kontakty | `25bdee07-c0dd-805c-8196-000b8e9c85b4` |
| Meetings | `25adee07-c0dd-803b-9ea5-000b836c237f` |
| Global Tag | `25edee07-c0dd-80e9-97a0-000ba8525c73` |
| Team Pages | `268dee07-c0dd-8075-9bb2-000bb8968038` |
| Analizy marketingowe | `8c5dacea-8b7c-48bc-aeb2-f8114f23db80` |
| Przepływy tworzenia treści | `07019ce5-cb58-4102-b579-47521b4f381e` |
| Role w produkcji | `52fd9c67-81d6-4c15-9cad-bd45146381b2` |
| Wytyczne SEO blog | `30fc7840-537e-4f9d-a39e-558e0d8487d1` |

## Kontakty

Dostawcy, drukarnie, współpracownicy zewnętrzni, modelki itp. Pola (stan z 04.2026, przed zapisem sprawdź `notion-fetch`): `Nazwa kontaktu` (title) · `Firma` · `Mail` · `Phone` · `Dział` (select: Inne / Właściciel / Biuro / Sprzedaż / Film / maszyny) · `Tag` (multi-select: Ecom, Maszyny, Produkcja, Marketing, Opakowania, Surowce, Dostawca, Współpracownik zewnętrzny, Firma zewnętrzna, Eksport, Grafiki, zdjęcia, Modelka, DRUKARNIA) · `Notatki` · `userDefined:URL` (pole URL wymaga prefiksu `userDefined:`) · relacje `Projekt`, `Meetings`.

Klienci B2B **nie** żyją w Kontaktach — są w CRM Bigin.

## Meetings

Spotkania prowadzone w Notionie (starsze; nagrania i transkrypty rozmów są w Tactiq). Pola (stan z 04.2026): `Meeting Title` · `Date` (datetime) · `Typ` (Zewnętrzne / Wewnętrzne) · `Tag` · `Cel` · `Uczestnicy z ON` (person) · `Uczestnicy z zewnątrz` (→ Kontakty) · `Meeting Tasks` (→ Tasks) · `Project`.

## Zasady MCP (wszystkie bazy)

- **Parent** zawsze `{type:"data_source_id", data_source_id:"…"}`, nie `database_id`.
- **Osoby, relacje, multi-select** = JSON-string tablicy: osoby gołe UUID (`"[\"345d872b-…\"]"`), relacje pełne URL stron, multi-select nazwy opcji. Nie stringi `user://…` i nie nazwy kampanii.
- **Daty** rozbite: `date:<Pole>:start` + `date:<Pole>:is_datetime` (0 = sama data).
- **Checkbox** `__YES__` / `__NO__`.
- **Pola person** potrafią się zgubić przy `notion-create-pages` — po zapisie odczytaj, popraw `notion-update-page` (`update_properties`).
- **Szablony** stosujesz przez jawne `template_id`; wtedy nie podawaj `content`.
- **Nie ustawiaj** formuł, rollupów ani pól automatu. Nie kasuj stron (MCP nie ma kasowania) — neutralizuj.
- **Rename opcji select** kasuje tę wartość w rekordach — zmiany słowników tylko z backupem i za zgodą.
- Wyszukiwanie: `notion-query-data-sources` (SQL, filtry dat wprost) do list i przekrojów; `notion-search` (semantyczny) do znalezienia strony po treści.
- Użytkownicy: `notion-get-users`.
