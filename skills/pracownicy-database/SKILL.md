---
name: pracownicy-database
description: Praca z bazą pracowników Opcja Natura w Supabase (tabela public.pracownicy). Użyj, gdy pytanie dotyczy pracowników, zespołu, kontaktów służbowych, działów, ról, typów umów, mapowania osoba↔Slack/Bigin/Notion, albo gdy trzeba sprawdzić kto jest aktywny / kto za co odpowiada. Zawiera schemat tabeli, gotowe zapytania SQL, zasady joinów z innymi tabelami i krytyczne gotchas (upsert po worker_id — nie edytuj ręcznie).
---

# Pracownicy Database — Opcja Natura

Tabela `public.pracownicy` w Supabase to aktualna, AI-friendly baza zespołu Opcja Natura.
Zasilana codziennie z Google Sheets przez workflow n8n `pracownicy_sync`.

| | |
|---|---|
| Projekt Supabase | `iocuxazmtfstekivrxos` |
| Tabela | `public.pracownicy` |
| Źródło | Google Sheet `1CvkCx_ArpbwQEYdhUbhbl73gXC7HcLoEgns1kbpxj58` (gid `1454522352`) |
| Workflow | `pracownicy_sync` (n8n ID `ATS1ye5R69ORq99V`) — codziennie 03:00 + Manual Sync |
| Strategia | **FULL REFRESH** (delete-all + insert) co bieg |

---

## ⚠️ Krytyczne zasady

1. **NIE pisz ręcznie do `public.pracownicy`.** Od 2026-10-07 sync (03:00 lub Manual) robi **upsert po
   `worker_id`**: nadpisuje wiersze z arkusza, nie kasuje tych, których w arkuszu już nie ma.
   Ręczne zmiany kolumn z arkusza zostaną nadpisane. `worker_id` jest UNIQUE NOT NULL i ma
   FK z `kadry.urlopy` — nigdy go nie zmieniaj (odejście = `active = FALSE`).
   Chcesz zmienić dane? → **edytuj Google Sheet**, potem uruchom Manual Sync.
2. **Zmiana schematu (DDL) wymaga wyraźnej zgody Daniela.** Dotyczy `ALTER TABLE`,
   nowych kolumn, nowych tabel. Nie rób DDL „przy okazji".
3. **Brak PII.** Tabela celowo NIE zawiera: nr konta bankowego, prywatnego telefonu/e-maila,
   bitwarden, loginów do menedżerów haseł, loginów BL / old workspace. Te dane są tylko
   w arkuszu źródłowym. Jeśli ktoś ich potrzebuje — kieruj do arkusza, nie dodawaj do bazy.
4. **`active` to filtr domyślny.** Prawie zawsze chcesz `where active = true`
   (wyjątek: pytania o byłych/nieaktywnych pracowników).

---

## Schemat

| kolumna | typ | opis |
|---------|-----|------|
| `id` | bigint (identity) | PK techniczny (od 2026-10-07 stabilny, ale kluczem biznesowym jest `worker_id`) |
| `worker_id` | text | **klucz biznesowy** (UNIQUE NOT NULL, FK z `kadry.urlopy`), np. `worker_001`. Format niespójny (`worker_001`…`009` vs `worker_10`…`18`) |
| `user_name` | text | imię i nazwisko (małe litery) |
| `active` | boolean | TRUE = aktywny, FALSE = były/nieaktywny |
| `dzial` | text | `zarząd`, `e-commerce`, `produkcja`, `handel b2b`, `marketing`, `backoffice`, `export` |
| `role` | text | stanowisko, np. `e-commerce manager` |
| `agreement_type` | text | `UOP`, `B2B`, `Umowa cywilna` |
| `work_phone` | text | telefon służbowy (może być null) |
| `work_zogo_email` | text | mail służbowy (np. `sklep@opcjanatura.pl`) |
| `opcjanatura_workspace_login` | text | login do workspace (np. `krystian@opcjanatura.pl`) |
| `bigin_crm_id` | text | ID w Zoho Bigin CRM (do joinu z CRM) |
| `slack_user_id` | text | Slack user ID (np. `U08QRU291V2`) — klucz do integracji Slack |
| `notion_user_email` | text | e-mail użytkownika Notion |
| `zoho_view_url` | text | link do widoku Zoho Analytics |
| `synced_at` | timestamptz | znacznik ostatniej synchronizacji |

**Stabilne klucze biznesowe:** `worker_id` (główny), `slack_user_id`, `bigin_crm_id`, `work_zogo_email`.

---

## Narzędzie

Zapytania przez Supabase MCP: **`execute_sql`** (read-only zapytania) na projekcie
`iocuxazmtfstekivrxos`. Do DDL (tylko za zgodą) — `apply_migration`.

```
execute_sql({ project_id: "iocuxazmtfstekivrxos", query: "select ... from public.pracownicy ..." })
```

---

## Gotowe zapytania

**Kto pracuje w dziale / pełni rolę**
```sql
select user_name, role, work_zogo_email, slack_user_id
from public.pracownicy
where active and dzial = 'marketing'
order by user_name;
```

**Znajdź osobę po nazwisku (fuzzy)**
```sql
select * from public.pracownicy
where user_name ilike '%konieczny%';
```

**Mapowanie Slack ID → osoba** (np. gdy agent dostaje wiadomość ze Slacka)
```sql
select user_name, dzial, role, work_zogo_email
from public.pracownicy
where slack_user_id = 'U08QRU291V2';
```

**Mapowanie osoba → Slack** (np. komu wysłać DM)
```sql
select user_name, slack_user_id
from public.pracownicy
where active and slack_user_id is not null
  and user_name ilike '%łukasz%';
```

**Zespół wg działu (zliczanie)**
```sql
select dzial, count(*) filter (where active) as aktywni
from public.pracownicy
group by dzial order by aktywni desc;
```

**Osoby z dostępem do CRM (Bigin)**
```sql
select user_name, role, bigin_crm_id
from public.pracownicy
where active and bigin_crm_id is not null;
```

**Kontakty służbowe (książka adresowa)**
```sql
select user_name, dzial, role, work_zogo_email, work_phone
from public.pracownicy
where active and work_zogo_email is not null
order by dzial, user_name;
```

---

## Joiny z innymi tabelami

Tej samej bazy Supabase. Najpewniejsze klucze złączeń:

| Cel | Klucz | Przykład |
|-----|-------|----------|
| Slack cache | `slack_user_id` ↔ `slack_users_cache.slack_user_id` | wzbogacenie danych Slack |
| Uczestnicy spotkań | `work_zogo_email`/`opcjanatura_workspace_login` ↔ `meeting_attendees.email` | kto był na spotkaniach |
| Zadania ze spotkań | `user_name` ↔ `meeting_tasks.assignee` (luźny, tekstowy — uważaj) | zadania osoby |
| Zoho Bigin CRM | `bigin_crm_id` → API Bigin (nie tabela) | rekord CRM |

```sql
-- Pracownik + jego dane ze Slack cache
select p.user_name, p.dzial, p.role, s.user_name as slack_name
from public.pracownicy p
left join public.slack_users_cache s on s.slack_user_id = p.slack_user_id
where p.active;
```

```sql
-- Na ilu spotkaniach był pracownik (po mailu służbowym)
select p.user_name, count(a.id) as spotkania
from public.pracownicy p
left join public.meeting_attendees a
  on lower(a.email) = lower(p.work_zogo_email)
where p.active
group by p.user_name order by spotkania desc;
```

> Maile/assignee bywają niespójne (różne adresy, literówki). Przy joinach po tekście
> używaj `lower(...)` i traktuj wyniki jako orientacyjne.

---

## Znane problemy w danych źródłowych

Wynikają z arkusza — naprawia się je **w arkuszu**, nie w bazie:

- `worker_11` — pusty `user_name` (monika gonda, export, `active=false`).
- Niespójny format ID: `worker_001`…`worker_009` vs `worker_10`…`worker_18`.
- Literówka w `notion_user_email` worker_002: `agta@opcjanatura.pl`.

---

## Wymuszenie odświeżenia

Dane w arkuszu się zmieniły i trzeba je mieć od razu (bez czekania do 03:00):
otwórz workflow `pracownicy_sync` w n8n → **Execute Workflow** (trigger „Manual Sync").
Triggerów Manual/Schedule nie da się odpalić przez API n8n.

Sprawdzenie świeżości danych:
```sql
select max(synced_at) as ostatni_sync from public.pracownicy;
```
