# TODO — skille Notion i Slack na claude.ai (audyt 2026-09-30)

Stan: **spostrzeżenia zebrane, nic nie zmienione.** Rekomendacja czeka na akceptację Daniela.
Kontekst: pracownicy korzystają ze skilli w claude.ai (przeglądarka). Zmiany w projekcie
zlecenia marketingowe (`~/Claude_praca/n8n/zlecenia_marketingowe/`, v0.13.x) dotykają obu skilli.

## Co jest dziś wgrane na claude.ai (org)

Źródło: `~/.claude/skills/synced/<org>/manifest.json` (lokalna kopia skilli organizacji).

| Skill | Wgrany | Master w repo |
|---|---|---|
| `notion-opcja-natura` | 2026-04-15 | tylko paczka `pakiety/notion-opcja-natura.skill` (czerwiec) — nowsza niż claude.ai, też nieaktualna |
| `slack-opcja-natura` (+ `employees.json`) | 2026-04-09 | **brak** — nie ma go w repo |

`notion-publikacje`, `notion-produkcja-tresci`, `marketing-opcja-natura` (sierpień) są tylko w Claude Code —
na claude.ai nigdy nie trafiły. Statystyk użycia skilli na claude.ai nie widać.

## notion-opcja-natura — błędy

1. **Format pola person:** każe `"user://UUID"` jako string → od czerwca przypisuje autora. Poprawny: JSON-array z gołym UUID
   (paczka z czerwca ma to dobrze). Plus pułapka: `create-pages` gubi person — ustawiać drugim wywołaniem `update-page`.
2. **Publikacje wg stanu sprzed pół roku:** nieistniejące `Status 1`, `Zrealizowane`, formuła `Status`; stare `Type`.
   Dziś (fetch 2026-09-30) `Type` = stories, post, video, video agata, newsletter, blog creative, blog seo, inne,
   b2b artykuł, b2b baner, b2b inne, b2b newsletter, b2b pakiet. Brak `Status emisji`, `Status produkcji` (rollup),
   `Responsible Person (automat)`, `Link do materiałów`, `Link do akcji Bigin`, `WYTYCZNE SEO BLOG`.
   Brak informacji, że Date + Type + obsada = automat zakłada zadania.
3. **Nic o zleceniach:** pola `Status zlecenia` (Nowe / Do doprecyzowania / Przyjęte / Odrzucone / Gotowe),
   `Zgłaszający`, `Slack ID zgłaszającego`, `Slack ts karty`, `Termin zgłoszony`, `Pytanie do zgłaszającego`
   — ustawia je workflow, AI ma ich nie ruszać. Zlecenie składa się przez Slacka, nie przez stronę w Notionie.
   Na stronie zlecenia źródło dla wykonawcy = sekcja **„📋 Wytyczne dla marketingu”** (Claude przy Przyjmij),
   nie surowy brief ani zwinięty zapis rozmowy.
4. **Użytkownicy:** tylko 3 osoby. Brakuje m.in. Antoniny (copy@), Uli (studio@), Darii Szczygieł (foto@),
   Julii Zawadzkiej (video@), Łukasza (lukasz@), Konrada. Mapowanie mail→Notion jest w `public.pracownicy.notion_user_email`.

## slack-opcja-natura — błędy

1. Mapa kanałów bez `#zlecenia-marketing` (`C0C4E1CGFDJ`) i `#bot_errors` (`C0BMBRTLE5C`).
2. Nic o apce „Zlecenia marketing”: skróty ⚡ „Zgłoś do marketingu” / „Zlecenie B2B” / z wiadomości;
   statusy karty 🟡 Nowe · 🟠 Do doprecyzowania · 🔵 Przyjęte · 🟢 Gotowe · 🔴 Odrzucone;
   ustalenia w wątku pod kartą **przed** przyjęciem (po przyjęciu wytyczne są zamknięte); decyzje tylko Agata/Daniel.
   Strona procesu dla działów (Notion): https://app.notion.com/p/3e9dee07c0dd8140bfd8d7bc7cdb36e4
3. `employees.json` rozjechany z `public.pracownicy` (on_brain `iocuxazmtfstekivrxos`, stan 2026-09-30):
   brakuje Antoniny Zaleskiej, Darii Szczygieł, Julii Zawadzkiej, Urszuli Mierzwy-Pakuły, Kariny Orwat, Tomasza Wirbala;
   jest Monika Kwiecień-Gonda — nie ma jej wśród aktywnych w bazie (sprawdzić, czy odeszła).
4. Opis skilla: „gdy Daniel pyta” — a używają pracownicy.

## Rekomendacja (do akceptacji)

1. Notion: przepisać `notion-opcja-natura` na dziś (format + pułapki z czerwcowej paczki, schemat Publikacji z żywej bazy,
   sekcja „Zlecenia ze Slacka”). Master `.md` do repo.
2. Slack: `slack-opcja-natura.md` do repo; kanały, sekcja o zleceniach, pracownicy; `employees.json` generować z `pracownicy`.
3. Obie paczki `.skill` w `pakiety/`, commit; upload na claude.ai robi Daniel ręcznie.
4. Otwarta decyzja: czy wgrać na claude.ai także `notion-publikacje` + `notion-produkcja-tresci`.
   Rekomendacja: **nie** — jeden `notion-opcja-natura` z tym, co potrzebne do poprawnego zapisu, + link do strony procesu.
