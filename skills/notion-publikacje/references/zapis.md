# Notion — część techniczna dla agenta

Wszystko, czego potrzebujesz, żeby zapisać i odczytać bez zgadywania. Operatorowi tego nie cytuj — rozmawiasz z nim wg `SKILL.md`. Schemat sprawdzony 10.10.2026; przy błędzie „nie ma takiego pola" zrób `notion-fetch` na data source.

## Bazy

| Baza | data_source_id |
|---|---|
| Publikacje marketingowe | `25cdee07-c0dd-8090-8304-000b514105f9` |
| Tasks Tracker (zadania) | `25adee07-c0dd-80b1-a822-000b6037f86a` |
| Marketing Campaigns | `25bdee07-c0dd-8074-a650-000b4e3d4fd0` |
| Role w produkcji ([widok](https://app.notion.com/p/7b311130746c4dbaab760001da4d4f74?v=4de61d99716a40af9f6fad6b0e127ee8)) | `52fd9c67-81d6-4c15-9cad-bd45146381b2` |
| Przepływy tworzenia treści ([widok](https://app.notion.com/p/7f51aa31bffc4234a81612b6ea5c7a83?v=3acdee07c0dd801da7d3000c931c127a)) | `07019ce5-cb58-4102-b579-47521b4f381e` |

Parent przy zapisie: `{"type":"data_source_id","data_source_id":"…"}`. Zapis: `notion-create-pages` (max 100 naraz). Edycja: `notion-update-page` z `command:"update_properties"`. Odczyt list i przekrojów: `notion-query-data-sources` (SQL). Do znalezienia strony po treści: `notion-search`.

## Ludzie i terminy — czytaj na żywo, nie z pamięci

Role w produkcji (kto, jaka rola, aktywny, user ID):
```sql
SELECT "Osoba", "Role", "Aktywna", "Notion user", "Offset awaryjny"
FROM "collection://52fd9c67-81d6-4c15-9cad-bd45146381b2";
```
- `Notion user` = ID do pola `Responsible Person` / `Assignee` (zdejmij prefiks `user://`).
- `Aktywna = '__NO__'` → nie wpisuj tej osoby.
- `Offset awaryjny` = termin (dni przed publikacją) zadania ogólnego dla osoby bez roli w danym rodzaju.

Kroki i terminy dla rodzaju publikacji:
```sql
SELECT "Krok", "Rola", "Offset dni", "Opis kroku"
FROM "collection://07019ce5-cb58-4102-b579-47521b4f381e"
WHERE "Type" = ? ORDER BY "Krok";
```
Termin zadania = data publikacji − `Offset dni`. Kto dostaje zadanie: osoba z publikacji, której `Role` (z Ról w produkcji) zawiera `Rola` kroku. **Kolumny `Domyślna osoba` w Przepływach nie używaj** — o osobie decyduje obsada publikacji.

Osoby spoza Ról (np. przy zadaniu ręcznym dla kogoś z innego działu): `notion-get-users` z zapytaniem po imieniu lub mailu.

Odczytaj obie bazy raz na rozmowę i trzymaj wynik — nie pytaj o to samo przy każdej publikacji.

## Publikacja — pola

| Na ekranie / operator mówi | Pole API | Format zapisu |
|---|---|---|
| tytuł | `Tytuł` | tekst, bez spacji na końcach |
| data | `date:Date:start` + `date:Date:is_datetime: 0` | `"2026-10-23"` |
| rodzaj | `Type` | jedna z 13 wartości z `SKILL.md`, dokładnie tak zapisana |
| kanał | `Channel` | JSON-string tablicy: `"[\"Instagram\",\"Facebook\"]"`; wartości: Instagram, Facebook, TikTok, YouTube, LinkedIn, Website, Email, Events, Print, Outdoor |
| kto pracuje | `Responsible Person` | JSON-string tablicy gołych UUID: `"[\"36bd872b-…\"]"` |
| kampania | `Campaign` | JSON-string tablicy **URL stron** kampanii |
| status emisji | `Status emisji` | `Zaplanowane` · `Wrzucone` · `Emisja_ok` · `Odpuszczone` |
| koszt · notatki · link do publikacji · link do materiałów | `Cost` · `Notes` · `Link do publikacji` · `Link do materiałów` | liczba · tekst · url · url |
| brief SEO bloga | `WYTYCZNE SEO BLOG` | JSON-string tablicy URL |

**Nie zapisuj nigdy:** `Status` (nie istnieje), `Status emisji` przy zakładaniu (domyślne `Zaplanowane`), `Status produkcji`, `Zadania`, `Responsible Person (automat)`, `Projekt`, `id_strony`, `💬 Slack`, ani pól zleceń: `Status zlecenia`, `Zgłaszający`, `Slack ID zgłaszającego`, `Slack ts karty`, `Termin zgłoszony`, `Pytanie do zgłaszającego`, `Link do akcji Bigin`.

Przykład:
```json
{
  "Tytuł": "Próbowałam trzy miesiące, a zespół zrobił to w 5 minut",
  "date:Date:start": "2026-10-30",
  "date:Date:is_datetime": 0,
  "Type": "video",
  "Channel": "[\"Instagram\",\"Facebook\"]",
  "Responsible Person": "[\"<user ID z Ról>\",\"<user ID z Ról>\"]",
  "Campaign": "[\"https://app.notion.com/p/32fdee07c0dd80e1aab2fa1c583cbb2f\"]"
}
```
Szablon publikacji (opcjonalny): `template_id: 25cdee07-c0dd-80ac-bd60-c64752a79431` — wtedy bez `content`.

**Po zapisie zawsze odczytaj stronę** i sprawdź `Responsible Person` (potrafi się zgubić albo zostać nadpisany autorem). Popraw drugim `update_properties`.

## Zadanie ręczne — pola

```json
{
  "Task name": "Grafiki na stoisko targowe",
  "Assignee": "[\"<user ID>\"]",
  "date:Due date:start": "2026-10-20",
  "date:Due date:is_datetime": 0,
  "Status": "To do",
  "Priority": "High"
}
```
- `Status`: `To do` · `Overdue` · `Done`. `Priority`: `High` · `Medium` (puste = zwykłe).
- Zamknięcie zadania = `"Wykonane": "__YES__"` (samo `Status: Done` nie wystarcza).
- **Nie ustawiaj** przy zadaniu ręcznym: `task_source`, `task_rule`, `Offset dni`, `Krok`, `Type`, `Due date (automat)`. Puste `task_source` chroni zadanie przed systemem.
- Relację `Publikacja` ustawiaj tylko, gdy zadanie naprawdę jest częścią tej publikacji.
- Inne relacje (URL stron): `Marketing Campaigns`, `Projects`, `Meetings`, `Kontakty`, `Analiza`, `Global Tag`, `Team Pages`.
- Szablon zadania: `template_id: 25adee07-c0dd-8021-a1ac-fce53b3924a3`.

Nazwy zadań tworzonych przez system: `[rola · rodzaj] Tytuł` albo `[zadanie · rodzaj] Tytuł` (kropka `·` U+00B7). Nie twórz ręcznie zadań o takich nazwach.

## Gotowe zapytania

Zadania osoby do 7 dni naprzód, niezrobione:
```sql
SELECT "Task name", date("date:Due date:start") AS termin, "Status", url
FROM "collection://25adee07-c0dd-80b1-a822-000b6037f86a"
WHERE "Assignee" LIKE '%<USER_ID>%' AND "Wykonane" = '__NO__'
  AND date("date:Due date:start") <= date('now','+7 days')
ORDER BY 2;
```

Publikacje w okresie:
```sql
SELECT substr("Tytuł",1,50) AS tytul, "Type", "Status emisji", "Status zlecenia", date("date:Date:start") AS data, url
FROM "collection://25cdee07-c0dd-8090-8304-000b514105f9"
WHERE date("date:Date:start") BETWEEN '2026-10-01' AND '2026-10-31' ORDER BY data;
```

Publikacje, którym brakuje daty, rodzaju albo osób:
```sql
SELECT substr("Tytuł",1,50) AS tytul, "Type", date("date:Date:start") AS data, url
FROM "collection://25cdee07-c0dd-8090-8304-000b514105f9"
WHERE "Type" IS NULL OR "Responsible Person" IS NULL OR "date:Date:start" IS NULL;
```

Zadania jednej publikacji („nie widzę zadania"):
```sql
SELECT "Task name", "Assignee", date("date:Due date:start") AS termin, "Wykonane"
FROM "collection://25adee07-c0dd-80b1-a822-000b6037f86a"
WHERE "Publikacja" LIKE '%<ID_STRONY_PUBLIKACJI>%';
```

Zlecenia ze Slacka w toku:
```sql
SELECT substr("Tytuł",1,50) AS tytul, "Status zlecenia", "Zgłaszający", date("date:Termin zgłoszony:start") AS termin, url
FROM "collection://25cdee07-c0dd-8090-8304-000b514105f9"
WHERE "Status zlecenia" IN ('Nowe','Do doprecyzowania','Przyjęte') ORDER BY termin;
```

Kolumny relacji, osób i multi-select to JSON-stringi — filtruj `LIKE`. Checkbox: `'__YES__'` / `'__NO__'`. `Status produkcji` nie jest dostępny w SQL — odczytaj stronę (`notion-fetch`), jeśli potrzebny.

## Typowe błędy zapisu

| Błąd | Skutek |
|---|---|
| `Type` spoza listy (`rolka`, `video short`, `Blog Post`…) | pole zostaje puste, nikt nie dostaje zadań |
| `Campaign` jako nazwa | relacja nie zapisze się |
| osoby jako `"user://…"` albo zwykły string | zły zapis albo przypisanie autora |
| obsada „na wszelki wypadek" | zadania dla ludzi, którzy ich nie robią |
| bulk bez zatwierdzonej tabeli i bez strony testowej | błąd powielony na cały zespół |
