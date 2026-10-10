---
name: notion-opcja-natura
description: Kompleksowy przewodnik po workspace Notion dla Opcja Natura — struktura baz danych, relacje między nimi, schematy właściwości, mechanika tworzenia stron i zadań przez MCP, znani użytkownicy z ID, common pitfalls. Używaj gdy Daniel chce tworzyć lub edytować zadania, kampanie, publikacje, projekty, kontakty lub spotkania w Notion, albo gdy pyta o strukturę workspace'u, relacje między bazami, dostępne pola i ich wartości, lub napotyka błędy przy operacjach Notion MCP.
---

# Notion Opcja Natura — Nawigacja i Best Practices

## Kiedy używać tego skilla

Używaj gdy Daniel:
- Chce tworzyć/edytować zadania, kampanie, publikacje, projekty, spotkania lub kontakty
- Pyta o strukturę baz danych i relacje między nimi
- Potrzebuje znać dostępne wartości pól (Status, Type, Channel itd.)
- Napotyka błędy przy operacjach Notion MCP
- Pyta o ID użytkowników do przypisania (`Assignee`, `Person Responsible`)

---

## UŻYTKOWNICY (Notion User IDs)

| Osoba | Email | Notion User ID |
|---|---|---|
| Daniel Suliga | daniel@opcjanatura.pl | `user://1f4d872b-594c-81f9-b5cf-00025e45b0dd` |
| Agata | agata@opcjanatura.pl / kontakt@opcjanatura.pl | `user://25ad872b-594c-8176-86eb-0002d9a624e7` |
| Jakub Biernacki | jakub@opcjanatura.pl | `user://329d872b-594c-810b-b1ed-000228735433` |

**WAŻNE — pole `Assignee` / `Person Responsible`:**
- Format wartości: string `"user://UUID"` (NIE tablica, NIE lista)
- Przykład: `"Assignee": "user://1f4d872b-594c-81f9-b5cf-00025e45b0dd"`
- Notion MCP ignoruje tablice dla pól `person` — zawsze przekazuj string

---

## BAZY DANYCH — MAPA

```
Projects (Projekty strategiczne)
    └── Marketing Campaigns (Kampanie taktyczne)
            ├── Publikacje marketingowe (Posty, maile, treści)
            │       └── Tasks Tracker (zadania wykonawcze)
            └── Tasks Tracker (zadania wykonawcze)

Tasks Tracker ←→ Meetings (spotkania)
Tasks Tracker ←→ Kontakty
Meetings ←→ Kontakty
```

---

## 1. TASKS TRACKER (Zadania)

**Data Source ID:** `25adee07-c0dd-80b1-a822-000b6037f86a`
**URL bazy:** `https://www.notion.so/25adee07c0dd8035b8eae2eeb6859910`
**Template domyślny:** `25adee07-c0dd-8021-a1ac-fce53b3924a3` (nazwa: "New task")

### Schemat właściwości

| Pole | Typ | Wartości / Format |
|---|---|---|
| `Task name` | title | string — tytuł zadania |
| `Status` | status | `"To do"` / `"Overdue"` / `"Done"` |
| `Assignee` | person | string `"user://UUID"` |
| `date:Due date:start` | date | ISO-8601, np. `"2026-04-22"` |
| `date:Due date:is_datetime` | integer | `0` = data, `1` = datetime |
| `Priority` | select | `"High"` / `"Medium"` / `"Low"` |
| `Marketing Campaigns` | relation | URL strony z kolekcji `25bdee07-c0dd-8074-a650-000b4e3d4fd0` |
| `Projects` | relation | URL strony z kolekcji `1f4dee07-c0dd-80c8-b00e-000b544e79d2` |
| `Meetings` | relation | URL strony z kolekcji `25adee07-c0dd-803b-9ea5-000b836c237f` |
| `Kontakty` | relation | URL strony z kolekcji `25bdee07-c0dd-805c-8196-000b8e9c85b4` |
| `Wykonane` | checkbox | `"__YES__"` / `"__NO__"` |
| `Global Tag` | relation | URL strony z kolekcji `25edee07-c0dd-80e9-97a0-000ba8525c73` |

### Tworzenie zadania — przykład

```json
{
  "parent": { "data_source_id": "25adee07-c0dd-80b1-a822-000b6037f86a", "type": "data_source_id" },
  "pages": [{
    "properties": {
      "Task name": "Nazwa zadania",
      "Status": "To do",
      "Assignee": "user://1f4d872b-594c-81f9-b5cf-00025e45b0dd",
      "date:Due date:start": "2026-04-22",
      "date:Due date:is_datetime": 0,
      "Priority": "High",
      "Marketing Campaigns": "https://www.notion.so/2e7dee07c0dd80f9bae7c75860d9c2d9"
    }
  }]
}
```

### Widoki dostępne

| Widok | Typ | Filtr |
|---|---|---|
| All Tasks | table | brak |
| By Status | board | grupowane po Status |
| My Tasks | table | Assignee = me |
| Timeline | timeline | po Due date |
| Dzisiejsze | list | Due date = today AND Assignee = me |
| Jutro | list | Due date = tomorrow AND Assignee = me |
| Ten tydzień | list | Assignee = me |
| Zaległe | list | Status = Overdue AND Assignee = me |
| Wg projektu | list | grupowane po Projects |

---

## 2. MARKETING CAMPAIGNS (Kampanie)

**Data Source ID:** `25bdee07-c0dd-8074-a650-000b4e3d4fd0`
**URL bazy:** `https://www.notion.so/25bdee07c0dd80f284fbc424fcb425ad`

### Schemat właściwości

| Pole | Typ | Wartości / Format |
|---|---|---|
| `Campaign Name` | title | string |
| `Cel kampani` | text | string — opis celu |
| `Person Responsible` | person | string `"user://UUID"` |
| `date:Start Date:start` | date | ISO-8601 |
| `date:End Date:start` | date | ISO-8601 |
| `Planowany budżet` | number | float, format: złoty |
| `Zrealizowana` | checkbox | `"__YES__"` / `"__NO__"` |
| `Target Channel` | multi_select | `"B2B"` / `"B2C"` / `"Enterprise"` / `"Government"` |
| `Powiązany projekt` | relation | URL strony z Projects |
| `Publikacje Marketingowe` | relation | URL strony z Publikacje |
| `Zadania` | relation | URL strony z Tasks Tracker |
| `Progress` | rollup | auto — % zrealizowanych publikacji (checkbox) |
| `Łączny koszt publikacji` | rollup | auto — suma Cost z Publikacji |
| `Status` | formula | auto — obliczana |

### Przykład kampanii — URL do podlinkowania

Kampania Moja Opcja Natura:
`https://www.notion.so/2e7dee07c0dd80f9bae7c75860d9c2d9`

---

## 3. PUBLIKACJE MARKETINGOWE

**Data Source ID:** `25cdee07-c0dd-8090-8304-000b514105f9`
**URL bazy:** `https://www.notion.so/25cdee07c0dd80b3bbc5f4eaac3c63c6`

### Schemat właściwości

| Pole | Typ | Wartości / Format |
|---|---|---|
| `Tytuł` | title | string |
| `Type` | select | `"Social Media Post"` / `"Blog Post"` / `"Współpraca B2B"` / `"Kampania Email"` / `"Video"` / `"Podcast / Live"` / `"Prasa drukowana"` / `"Influencer"` / `"Banner"` / `"boxy"` / `"relacja"` / `"newsletter"` / `"wydarzenie"` / `"rolka"` |
| `Channel` | multi_select | `"Instagram"` / `"Facebook"` / `"TikTok"` / `"Email"` / `"Website"` / `"LinkedIn"` / `"YouTube"` / `"Events"` / `"Print"` / `"Outdoor"` / `"blog"` |
| `Status 1` | status | `"Not started"` / `"In progress"` / `"Done"` |
| `date:Date:start` | date | ISO-8601 — data publikacji |
| `Responsible Person` | person | string `"user://UUID"` |
| `Cost` | number | float, format: złoty |
| `Zrealizowane` | checkbox | `"__YES__"` / `"__NO__"` |
| `Campaign` | relation | URL strony z Marketing Campaigns |
| `Link do publikacji` | url | string |
| `Notes` | text | string |
| `Projekt` | rollup | auto — przez Campaign → Projects |
| `Status` | formula | auto |

---

## 4. PROJECTS (Projekty)

**Data Source ID:** `1f4dee07-c0dd-80c8-b00e-000b544e79d2`
**URL bazy:** `https://www.notion.so/1f4dee07c0dd80b29dc3e258e9b5d7a2`

### Schemat właściwości

| Pole | Typ | Wartości / Format |
|---|---|---|
| `Project name` | title | string |
| `Status` | status | `"Not started"` / `"In progress"` / `"Done"` |
| `Assignee` | person | string `"user://UUID"` |
| `Priority` | select | `"High"` / `"Medium"` / `"Low"` |
| `Typ` | select | `"Modyfikacja Produktu"` / `"Wprowadzenie Produktu"` |
| `date:Start date:start` | date | ISO-8601 |
| `date:End date:start` | date | ISO-8601 |
| `Marketing Campaigns` | relation | URL z Marketing Campaigns |
| `Tasks Tracker` | relation | URL z Tasks Tracker |
| `Kontakty` | relation | URL z Kontakty |
| `Documents` | relation | URL z Documents |
| `Progress` | rollup | auto — % zadań Done |
| `Ilość zadań` | rollup | auto — count Tasks |

---

## 5. KONTAKTY

**Data Source ID:** `25bdee07-c0dd-805c-8196-000b8e9c85b4`
**URL bazy:** `https://www.notion.so/25bdee07c0dd80d1ad59e992f2684add`

### Schemat właściwości

| Pole | Typ | Wartości / Format |
|---|---|---|
| `Nazwa kontaktu` | title | string |
| `Firma` | text | string |
| `Mail` | email | string |
| `Phone` | phone_number | string |
| `Dział` | select | `"Inne"` / `"Właściciel"` / `"Biuro"` / `"Sprzedaż"` / `"Film"` / `"maszyny"` |
| `Tag` | multi_select | `"Ecom"` / `"Maszyny"` / `"Produkcja"` / `"Marketing"` / `"Opakowania"` / `"Surowce"` / `"Dostawca"` / `"Współpracownik zewnętrzny"` / `"Firma zewnętrzna"` / `"Eksport"` / `"Grafiki"` / `"zdjęcia"` / `"Modelka"` / `"DRUKARNIA"` |
| `Notatki` | text | string |
| `userDefined:URL` | url | string — UWAGA: pole URL wymaga prefiksu `userDefined:` |
| `Projekt` | relation | URL z Projects |
| `Meetings` | relation | URL z Meetings |

---

## 6. MEETINGS (Spotkania)

**Data Source ID:** `25adee07-c0dd-803b-9ea5-000b836c237f`
**URL bazy:** `https://www.notion.so/25adee07c0dd8069a852c928398530df`

### Schemat właściwości

| Pole | Typ | Wartości / Format |
|---|---|---|
| `Meeting Title` | title | string |
| `date:Date:start` | date | ISO-8601 datetime |
| `date:Date:is_datetime` | integer | `1` (zawsze datetime) |
| `Typ` | select | `"Zewnętrzne"` / `"Wewnętrzne"` |
| `Tag` | multi_select | `"Tygodniówka"` / `"Marketing"` / `"Produkcja"` / `"Projekt"` / `"B2C"` / `"B2b"` / `"działania naprawcze"` |
| `Cel` | text | string — agenda/cel spotkania |
| `Uczestnicy z ON` | person | string `"user://UUID"` |
| `Uczestnicy z zewnątrz` | relation | URL z Kontakty |
| `Meeting Tasks` | relation | URL z Tasks Tracker |
| `Project` | relation | URL z Projects |

---

## MECHANIKA NOTION MCP — KLUCZOWE ZASADY

### 1. Tworzenie stron (notion-create-pages)

**Parent** — zawsze `data_source_id`, nie `database_id`:
```json
"parent": { "data_source_id": "25adee07-c0dd-80b1-a822-000b6037f86a", "type": "data_source_id" }
```

**Relacje** — format: pełny URL strony jako string:
```json
"Marketing Campaigns": "https://www.notion.so/2e7dee07c0dd80f9bae7c75860d9c2d9"
```

**Pola person** — string z `user://UUID`:
```json
"Assignee": "user://1f4d872b-594c-81f9-b5cf-00025e45b0dd"
```

**Daty** — zawsze podawaj parę `start` + `is_datetime`:
```json
"date:Due date:start": "2026-04-22",
"date:Due date:is_datetime": 0
```

**Checkboxy:**
```json
"Wykonane": "__NO__"
```

**URL (specjalne pole w Kontaktach):**
```json
"userDefined:URL": "https://..."
```

### 2. Znane pułapki

| Problem | Przyczyna | Rozwiązanie |
|---|---|---|
| Pole `Assignee` przypisuje zawsze autora | Błędny format — tablica zamiast stringa | Użyj stringa: `"user://UUID"` nie `["user://UUID"]` |
| Status odrzucony | Zła nazwa opcji | Sprawdź tabelę powyżej — dla Tasks Tracker: `"To do"` / `"Overdue"` / `"Done"` |
| Relacja nie zapisuje się | Podano ID bazy zamiast URL strony | Podaj pełny URL konkretnej strony, nie ID bazy |
| Pole URL odrzucone | Brak prefiksu | W Kontaktach użyj `"userDefined:URL"` |
| Formula / Rollup — próba zapisu | Pola read-only | Nie próbuj ustawiać `Status` (formula), `Progress` (rollup), `Łączny koszt` (rollup) |

### 3. Pobieranie schematu przed operacją

Przed tworzeniem stron w nieznajomej bazie zawsze pobierz schemat:
```
notion-fetch("collection://DATA_SOURCE_ID")
```
Zwróci dokładne nazwy pól, dostępne wartości selectów i typ każdej właściwości.

### 4. Wyszukiwanie użytkowników

```
notion-search(query="daniel@opcjanatura.pl", query_type="user")
```
Zwraca `id` w formacie `{{user://UUID}}` — używaj tego UUID w polach person.

---

## HIERARCHIA MARKETINGOWA

```
Project (długoterminowy — np. "Wprowadzenie Naturalny Tatuaż")
    └── Marketing Campaign (taktyczna — np. "Moja Opcja Natura", "GWIAZDKA 2025")
            ├── Publikacja (konkretny post/mail/rolka)
            └── Task (zadanie wykonawcze przypisane osobie)
```

Kampania agreguje:
- `Progress` = % zrealizowanych Publikacji (rollup z checkbox `Zrealizowane`)
- `Łączny koszt publikacji` = suma `Cost` z Publikacji (rollup)
- `Zadania` = powiązane Tasks Tracker

---

## DATA SOURCE IDs — ŚCIĄGAWKA

| Baza | Data Source ID |
|---|---|
| Tasks Tracker | `25adee07-c0dd-80b1-a822-000b6037f86a` |
| Marketing Campaigns | `25bdee07-c0dd-8074-a650-000b4e3d4fd0` |
| Publikacje marketingowe | `25cdee07-c0dd-8090-8304-000b514105f9` |
| Projects | `1f4dee07-c0dd-80c8-b00e-000b544e79d2` |
| Kontakty | `25bdee07-c0dd-805c-8196-000b8e9c85b4` |
| Meetings | `25adee07-c0dd-803b-9ea5-000b836c237f` |
| Global Tag | `25edee07-c0dd-80e9-97a0-000ba8525c73` |
| Team Pages | `268dee07-c0dd-8075-9bb2-000bb8968038` |
