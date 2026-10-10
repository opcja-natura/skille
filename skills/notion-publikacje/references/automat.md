# Automat produkcji treści — mechanika i diagnostyka

Dla osoby, która diagnozuje albo zmienia automat (zwykle Daniel). Codzienna praca na publikacjach i zadaniach: `SKILL.md`. Stan sprawdzony na żywym Notionie i n8n 10.10.2026.

Publikacja ma datę. Żeby ta data była realna, ktoś musi wcześniej napisać tekst
i zrobić grafikę. Automat zakłada te zadania i pilnuje ich terminów.

**Zasada:** *nie przechowywać terminu — liczyć go.* Zadanie trzyma relację do
publikacji i własny `Offset dni`; rollup ciągnie datę publikacji, formuła
odejmuje offset. Rollup jest żywy, więc przesunięcie publikacji przelicza
`Deadline wyliczony` **natychmiast**, bez udziału automatu. n8n tylko
**przepisuje różnicę** do `Due date`, bo przypomnienia siedzą właśnie tam.

Gdyby n8n padło na tydzień, dane dalej są poprawne — spóźnią się wyłącznie
przypomnienia.

---


## Co system robi po zapisie publikacji

```
Zakładasz publikację (typ + data + osoby)  →  powstają zadania, każde z własnym terminem
Zmieniasz datę publikacji                  →  terminy zadań przesuwają się same
Zmieniasz obsadę                           →  zadania dochodzą / znikają
Kasujesz publikację                        →  jej zadania lądują w koszu
```

**Typ mówi, jakie kroki są możliwe i na kiedy. Obsada mówi, które z nich powstaną.**

Nie ma pojęcia „krok bez obsady" — krok bez osoby to nie luka do uzupełnienia,
tylko stwierdzenie, że tej roboty nie ma. Nie ma też fallbacku: automat nie
produkuje zadań, których nikt nie zamówił.

Odwrotnie też: **osoba w obsadzie, której roli nie ma w przepływie, i tak
dostaje zadanie** — `[zadanie · typ] Tytuł`, z `Offset awaryjny` z rejestru
`Role w produkcji`. Nikt wpisany do publikacji nie zostaje pominięty.

> ⚠ **Skutek dla zespołu:** obsada musi znaczyć „ma zadanie", nie „wie o sprawie".

Automat **nie pamięta, co zrobił** — za każdym razem liczy różnicę zbiorów:
oczekiwane (typ × obsada × przepływy) minus istniejące (klucz: publikacja |
nazwa zadania | assignee). Stąd: ten sam przebieg dwa razy nic nie zmienia,
ręcznie skasowane zadanie zostanie odtworzone, a status zadania **nie wchodzi
do klucza** (odhaczone dopasowuje się normalnie).

---

## Przepływy — co powstaje dla jakiego typu

Łańcuch czytasz od lewej: kto robi krok i ile dni **przed** datą publikacji ma termin.

| `Type` | Kiedy | Łańcuch (rola → dni przed) | Maks. zadań |
|---|---|---|---|
| `stories` | stories — sam tekst, z grafiką Uli jeśli dopiszesz ją do obsady | copy −14 → grafika −14 | 2 |
| `post` | post feedowy IG / FB / LinkedIn | copy −21 → grafika −14 | 2 |
| `video` | każde video poza TikTokiem Agaty | nagranie −21 → montaż −14 → copy −7 → okładka −5 | 4 |
| `video agata` | TikTok Agaty — osobny cykl, krótsze terminy | nagranie −14 → montaż −7 | 2 |
| `newsletter` | wysyłka mailowa | materiały −21 → **weryfikacja tematyki −18** → copy −14 → grafika −7 | 4 |
| `blog creative` | wpis z pomysłu zespołu — temat do sprawdzenia pod SEO | seo −14 → copy −7 → grafika −5 | 3 |
| `blog seo` | wpis z tematu od SEO — kroku `seo` nie ma, temat przyszedł gotowy | copy −7 → grafika −5 | 2 |
| `inne` | konkurs, wyzwanie, jednorazówka | copy / nagranie / montaż równolegle −14 → składanie −7 | 4 |
| `b2b artykuł` | artykuł sponsorowany dla partnera B2B | seo −21 → copy −14 → grafika −7 | 3 |
| `b2b baner` | baner na stronę partnera | copy −7 → grafika −3 | 2 |
| `b2b inne` | inny materiał dla partnera — kopia `inne` | copy / nagranie / montaż −14 → grafika / składanie −7 | 4 |
| `b2b newsletter` | newsletter B2B (od 2026-09-25) — bez weryfikacji Kuby | copy −14 → grafika −7 | 2 |
| `b2b pakiet` | akcja łączona B2B, kilka materiałów (od 2026-09-26) — kopia `b2b inne` | copy / nagranie / montaż −14 → grafika / składanie −7 | 4 |

**„Maks. zadań" to sufit, nie gwarancja.** Publikacja `video` z samym kontem video@
w obsadzie dostanie jedno zadanie (montaż), nie cztery.

Dlaczego akurat tak:
- `video talked` + `video short` **scalone w `video`** — nigdy nie różniły się
  procesem, tylko obsadą, a ta jest już na publikacji.
- `video agata` został osobno, bo **realnie ma inne terminy** (−14/−7 zamiast
  −21/−14). TikTok powstaje szybciej niż produkcja filmowa.
- `blog seo` osobno, bo **realnie nie ma kroku `seo`**.
- `inne` **zakłada zadania** od 01.08 — błędne otypowanie przestało być darmowe.

Źródło prawdy: baza `Przepływy tworzenia treści`,
`collection://07019ce5-cb58-4102-b579-47521b4f381e`, **38 wierszy** (2026-09-26).
Pola: `Przepływ` (title) · `Type` · `Krok` (number) · `Rola` (select) ·
`Offset dni` · `Opis kroku` · `Bumpuj następny krok`.
`Rola`, 10 opcji: `koncept` · `seo` · `copy` · `materiały` · `weryfikacja` ·
`nagranie` · `montaż` · `grafika` · `okładka` · `publikacja`
(`koncept` i `publikacja` bez żywych wierszy — wypadły z blogów 01.08).

> **Żaden przepływ socialowy nie ma kroku `publikacja`** — wrzucenie posta to
> nie zadanie produkcyjne, tylko przestawienie `Status emisji`. W blogu krok
> publikacyjny zostaje, bo tam wrzucenie to realna robota w CMS.

---

## Nazwa zadania

| `task_rule` | Wzór |
|---|---|
| `przeplyw` | `[{Rola} · {Type}] {Tytuł publikacji}` |
| `obsada` | `[zadanie · {Type}] {Tytuł publikacji}` |

Przykład: `[copy · post] Nakarm skórę tak, jak sama byś chciała`.

**Kropka rozdzielająca to `·` (U+00B7)** — nie kropka zwykła, nie myślnik.
Nazwa jest częścią klucza deduplikacji: inny znak = duplikat.

`[zadanie · typ] Tytuł` **nie jest unikalne** — gdy dwie osoby mają rolę spoza
przepływu, powstają dwa zadania o identycznej nazwie, różniące się `Assignee`.
Dedup musi iść po **trójce** (publikacja | nazwa | assignee), nigdy po nazwie.

Nazwę zadania generuje automat. **Tytułów publikacji świadomie NIE generujemy**
— automat składający tytuł walczyłby z człowiekiem, który go edytuje.

⚠ **Zmiana `Type` przepisuje wszystkie zadania publikacji** — typ jest w nazwie,
więc stare stają się nadmiarowe, a nowe brakujące. Poprawne, ale zaskakuje.

---

## Tasks Tracker — pola automatu

`collection://25adee07-c0dd-80b1-a822-000b6037f86a`
(database `25adee07-c0dd-8035-b8ea-e2eeb6859910`)

Baza obsługuje też zadania spoza produkcji treści (spotkania, projekty,
kontakty) — **nie zakładaj, że każdy wiersz dotyczy publikacji.**

| Pole | Typ | Uwagi |
|---|---|---|
| `Task name` | title | generowane przez automat |
| `Assignee` | person | |
| `Due date` | date | przypomnienie **09:00 Europe/Warsaw**, format DD/MM/YYYY |
| `Status` | status | `To do` / `Overdue` / `Done` — `Overdue` chodzi za datą, patrz niżej |
| `Priority` | select | `High` / `Medium` (`Low` skasowane) |
| `Wykonane` | checkbox | `__YES__`/`__NO__` — **to liczy `Status produkcji`** |
| `Publikacja` | relation | dwustronna |
| `Offset dni` | number | dni przed datą publikacji |
| `Krok` | number | kolejność w przepływie (v1 nie używa) |
| `Type` | select | 13 typów, kopiowane z publikacji |
| `Data publikacji` | rollup | `latest_date` przez `Publikacja` |
| `Deadline wyliczony` | formuła | `Data publikacji` − `Offset dni` |
| `Due date (automat)` | date | **pole-cień** — pamięć ostatniego zapisu automatu |
| `task_source` | select | `mcp` / `automation`; **puste = zadanie ręczne, nietykalne dla automatu** |
| `task_rule` | select | `obsada` / `przeplyw` |
| `Marketing Campaigns` | relation | dziedziczone z `Campaign` publikacji |
| `Analiza` | relation | → Analizy marketingowe (skill `analizy-marketingowe`) |
| `Projects` · `Meetings` · `Kontakty` · `Global Tag` · `Team Pages` | relation | kontekst zadań spoza produkcji |

### Po co pole-cień `Due date (automat)`

Różnica `Due date` vs `Deadline wyliczony` ma **dwie przeciwne przyczyny**:
człowiek przypiął datę (nie dotykaj) albo publikacja się przesunęła i automat
nie zdążył (popraw). Rozróżnia je tylko pamięć ostatniego zapisu automatu.

**Ręczna zmiana `Due date` wyłącza automat na tym zadaniu na stałe.**
„Chcę tę datę" to decyzja terminalna.

### `Overdue` chodzi za datą, w obie strony

Automatyzacja Notiona zapala `Overdue`, gdy minie `Due date` — ale **nie cofa
tego**, gdy termin wróci w przyszłość. Przesunięcie publikacji zostawiało zadanie
z dobrą datą i czerwoną flagą. Od 2026-08-04 pilnuje tego n8n:

```
Overdue  AND  nowy termin >= dziś   →  To do
To do    AND  nowy termin <  dziś   →  Overdue
```

Dzień liczony w `Europe/Warsaw`. Robi to `korekta_dat` przy każdym przesunięciu,
a `uzgodnienie` i `zasiew` nadają `Overdue` **już przy zakładaniu**, gdy wyliczony
termin jest za nami (`video` zakładane 2 tygodnie przed emisją ma nagranie −21 dni).

⚠ **Zadanie zamknięte nie bierze w tym udziału** — ochrona `Done`/`Wykonane ✓`
wypada wcześniej. Odhaczone zadanie nigdy nie zapali się na czerwono.

⚠ **Zadania ręczne (`task_source` puste) też nie** — tam `Overdue` zostaje
w rękach automatyzacji Notiona.

---

## Co jest nietykalne

Automat nie archiwizuje zadania, jeśli:

| Co | Dlaczego |
|---|---|
| zadanie **zamknięte** (`Done` / `Wykonane ✓`) | ktoś to zrobił — historia zostaje |
| zadanie **ręczne** (`task_source` puste) | nie automat je zakładał |
| **próg** — >5 naraz (>8 przy kasowaniu publikacji) | rzuca błędem zamiast kasować hurtem |

Korekta dat dodatkowo pomija: zadania ręczne, zamknięte, z przypiętym terminem
oraz publikacje **bez daty** (pusty rollup → pusta formuła → zamrożone).

---

## Gotchy, które wracają

**Węzeł Notion w wersji 3 nie istnieje na tej instancji.** `get_node` poleca
`typeVersion: 3` z zasobem `dataSource` — instancja tego nie ma, węzły wychodzą
jako zepsute ikony. Całe I/O z Notionem idzie `httpRequest` 4.2 z jawnym
`Notion-Version: 2022-06-28`. Nie klikaj autofixa na wersjach.

**Surowe REST API Notiona nie stosuje szablonów bazy.** `POST /v1/pages` tworzy
pustą stronę niezależnie od `default_page_template` — dlatego szkielet treści
zadania jest odtworzony w kodzie n8n. **MCP `notion-create-pages` ma parametr
`template_id` i szablon stosuje** — to różnica między tymi dwiema drogami.

**`relation contains` nie dopasowuje stron w koszu.** Relacja fizycznie zostaje
i widać ją przez `GET`, ale filtr zwraca pustkę. Szukając sierot, pytaj
**skasowaną stronę o jej relację**, nie bazę o wskazujące wiersze.

**RPC logu ma białą listę akcji: `created` · `updated` · `archived` · `skipped`.**
Pozycja z inną akcją jest **po cichu pomijana** — wiersz przebiegu powstaje
z metrykami i payloadem, ale `workflow_log_item` zostaje pusty i widok nic nie
pokazuje. Audyt nazywa więc naprawę `updated`, a niepowodzenie `skipped`
z prefiksem `NAPRAWA NIE POSZLA:` w polu `reason`.

**Powrót do `splitInBatches` musi nieść co najmniej jeden item.** Węzeł, który
dostaje zero itemów, w ogóle się nie wykonuje — więc pętla staje po pierwszej
iteracji, cicho i ze statusem `ok`. Wpada w to każdy sub-workflow kończący się
gałęzią, która akurat nie miała nic do roboty (`uzgodnienie` przy `+2 / -0`
zwraca zero itemów z pustej gałęzi archiwizacji). Wstaw za wywołaniem węzeł
`Code` zwracający jeden sztuczny item i dopiero z niego wracaj do pętli;
`alwaysOutputData` na węźle wywołującym to samo zabezpieczenie z drugiej strony.
Złapane 2026-08-04: 6 do naprawy, naprawiona 1.

**`Execute Workflow` wysyła wszystkie itemy w JEDNYM wywołaniu.** Sub-workflow,
który czyta `$('Wywolanie').first().json` — a tak robi `uzgodnienie` — obsłuży
wtedy wyłącznie pierwszy item i zaloguje `ok`. Reszta znika bez śladu. Podaj
itemy przez `splitInBatches` (`batchSize: 1`), z powrotem do pętli; `mode: "each"`
robi to samo, ale jest deprecated. Złapane 2026-08-04 w audycie: 7 do naprawy,
naprawiona 1.

**Per-item storm.** Węzeł HTTP odpala się raz na item — przy 200 publikacjach to
setki wywołań na przebieg. Zwijaj do jednego itemu przed operacjami zbiorczymi,
respektuj limit 3 req/s.

**Filtr botów odcina pętlę zwrotną.** Utworzenie zadania aktualizuje relację
`Zadania` na publikacji, co samo generuje `page.properties_updated`. Bez filtra
`authors[].type = bot/agent` każde zadanie wywoływałoby kolejne uzgodnienie.

**Układu i widoczności properties nie da się ustawić przez API** — wyłącznie UI
(*Customize layout*). Zadanie z API pokazuje płaską listę 20 pól.

**Rename opcji select kasuje wartości w rekordach** — snapshot przed zmianą.
Snapshoty leżą w `notion_produkcja_tresci/backup/`.

**MCP nie ma narzędzia kasującego stronę** — neutralizuj, nie kasuj.

---

## Workflow n8n (stan 10.10.2026)

| Workflow | ID | Trigger | Rola | Aktywny |
|---|---|---|---|---|
| `notion_webhook_publikacje` | `CscAQuvu1WmHK8Ns` | webhook Notiona | dispatcher: handshake, filtr botów, rozgałęzienie; zdarzenia z innych baz przekazuje do `notion_zdarzenia` | ✅ |
| `produkcja_tresci_uzgodnienie` | `P2qt7ZHKT8zo1kp1` | wywołanie | różnica w obie strony dla jednej publikacji (zakłada / archiwizuje zadania) | ✅ |
| `produkcja_tresci_korekta_dat` | `rk8el0uThdla7rWH` | webhook + wywołanie | przepisuje `Deadline wyliczony` → `Due date`, pilnuje `Overdue` | ✅ |
| `produkcja_tresci_sieroty` | `u5XajQOCg6Z2foq7` | webhook + wywołanie | archiwizuje zadania skasowanej publikacji | ✅ |
| `produkcja_tresci_emisja` | `Y0JqIMiAvwI1JPsz` | 07:00 | `Wrzucone` + data minęła → `Emisja_ok` | ✅ |
| `notion_zdarzenia` | `V0w5sLAHxQ5ynxsi` | wywołanie z dispatchera | router zdarzeń spoza Publikacji (dziś: Tasks Tracker → `zlecenia_gotowe`) | ✅ |
| `zlecenia_gotowe` | `uoVTouO7J8wZjvTK` | wywołanie z routera | ostatnie zadanie zlecenia odhaczone → `Status zlecenia = Gotowe`, `Emisja_ok`, wiadomość w wątku Slacka | ✅ |
| `produkcja_tresci_zasiew` | `GcLJYyK9Ab6lGhlf` | ręcznie | budowniczy zadań dla okna dat (węzeł `Utworz zadanie` bywał wyłączony — sprawdź przed uruchomieniem) | ❌ |
| `produkcja_tresci_audyt` | `j8XDkBhNiy3iSS0i` | (planowo 03:00) | guard: publikacje bez zadań → `uzgodnienie` | ❌ nie ma go wśród workflow instancji |
| `[error] produkcja tresci` | `4UgHQWHfwdpE7PcX` | Error Trigger | Slack + log | ❌ nieaktywny |

**Nocnego audytu nie ma.** Publikacja, której zdarzenie z Notiona zginęło (webhooki Notiona bywają gubione), zostaje bez zadań i nikt tego nie zgłasza. Przy „dlaczego nie ma zadania" sprawdzaj ręcznie (zapytanie w `SKILL.md`), a naprawa = ponowne wywołanie `uzgodnienie` dla tej publikacji albo drobna zmiana na publikacji wykonana przez człowieka (np. zapis obsady), która wygeneruje świeże zdarzenie.

Webhook wysyła **inna integracja niż ta, która pisze**: zapisy robi `n8n_new` (credential `Notion_tworzenie_taskow` `vInUs7r9vqWc3Szg`), subskrypcję ma `webhooks_produkcja_tresci`. Nowa baza, z której mają przychodzić zdarzenia, musi mieć tę integrację w Connections. Filtr botów w dispatcherze sprawia, że zmiany robione przez integracje (n8n, MCP) **nie wyzwalają automatu** — reaguje tylko na ludzi. Zapis publikacji przez agenta (MCP) też jest „botem": jeśli po zapisie przez MCP zadania nie powstały, to może być właśnie to — sprawdź log, a w razie potrzeby wywołaj `uzgodnienie`.

## Log

Supabase `iocuxazmtfstekivrxos`, schemat `marketing`: `workflow_log` · `workflow_log_item` · widok `v_workflow_log` · RPC `log_workflow_run()` (schemat nie jest wystawiony przez PostgREST, zapis przez RPC w `public`).

```sql
select * from marketing.v_workflow_log order by ts desc limit 30;
```

Wiersz, który utknął na `planned`, znaczy: zdecydowaliśmy i nie potwierdziliśmy — sygnał awarii. Przebiegi zerowe też się logują; brak wiersza = coś nie wystartowało. RPC przyjmuje tylko akcje `created` · `updated` · `archived` · `skipped` — inna akcja przepada po cichu.

Dokumentacja projektu: `~/Claude_praca/n8n/notion_produkcja_tresci/` (`AUTOMATYZACJA_N8N.md`, `PRZEPLYWY.md`, `SCHEMATY.md`, `BACKLOG.md`), router: `~/Claude_praca/n8n/notion_zdarzenia/`, zlecenia: `~/Claude_praca/n8n/zlecenia_marketingowe/`.

## Role w produkcji — rejestr

`collection://52fd9c67-81d6-4c15-9cad-bd45146381b2`. Dopasowanie po polu `Notion user` (user ID). Pola: `Osoba` · `Notion user` · `Role` (multi-select, po nim dopasowuje automat) · `Rola główna` · `Offset awaryjny` (działa tylko dla ról spoza przepływu danego typu) · `Aktywna` (odznacz zamiast kasować) · `Uwagi`. Aktualna obsada i role: tabela w `SKILL.md`.
