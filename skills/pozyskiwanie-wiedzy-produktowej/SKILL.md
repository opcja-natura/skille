---
name: pozyskiwanie-wiedzy-produktowej
description: Skąd i jak pozyskiwać wiedzę o produktach i pielęgnacji Opcji Natury (rytuały, mechanizmy, składy) — mapa źródeł, kolejność sięgania, playbook NotebookLM. Używaj ZANIM zaczniesz pisać treści produktowe/pielęgnacyjne (FAQ, blog, opisy, posty), żeby gruntować w wiedzy marki, a nie zgadywać.
type: skill
---

# SKILL — Pozyskiwanie wiedzy produktowej Opcja Natura

Zasada nadrzędna: **nie zgaduj składów, działań ani mechanizmów.** Wiedza marki żyje w plikach i w NotebookLM. Najpierw ją zbierz, potem pisz. Lepszy materiał wejściowy = lepszy tekst.

---

## 1. Mapa źródeł — co gdzie leży

| Źródło | Co zawiera | Kiedy używać |
| :-- | :-- | :-- |
| `00_o_marce/produkty.json` | **TWARDE DANE**: INCI, ceny, pojemności, wyróżnione składniki, działania, linki do sklepu (35 produktów; `_meta.pola` opisuje każde pole). To **źródło prawdy o składzie**. | Zawsze, gdy potrzebujesz nazw / składów / cen / linków. Nigdy nie wymyślaj — sprawdź tu. (Kopie produktu.json mogą leżeć też w innych folderach projektów — bierz `00_o_marce/`.) |
| `wiedza_produktowa/` (folder z mapą w `README.md`) | Eksperckie artykuły = **szkolenia Agaty w formie tekstu**. Uporządkowane: `rytualy/` (jak pielęgnować wg problemu), `produkty/` (opis kosmetyku), `dezodoranty/` (cała linia), `referencje/` (PTCA, strategia, CSV), `opracowania/` (treści pochodne, np. FAQ). | Pierwszy sięg po mechanizm i rytuał — szybsze i tańsze niż NotebookLM. Zacznij od `README.md`. |
| skill `naturalna-pielegnacja` | Mapa rytuału per typ cery (oczyszczanie → hydrolat → serum → krem), produkt-na-krok, sekcje „Uważaj" z pułapkami. | Najlepszy **pojedynczy punkt startu** dla doradztwa i rytuałów. |
| skill `produkty-lookup` | Szybki lookup produktów po kategorii (nazwa, cena, skład, działanie). | Gdy potrzeba tylko danych, nie doradztwa. |
| NotebookLM, notebook `przewodnik-po-naturalnej-piel-` | Realne **nagrania szkoleń Agaty** (`Recording_1.m4a`), „ABC Sprzedawcy", „Kompendium dezodorantów". Synteza Gemini z jej źródeł. | Do pogłębienia / weryfikacji i tematów słabo pokrytych w repo. Daje **głos Agaty**. |
| `wiedza_produktowa/b2b_opisy/` | Opisy B2B per produkt (np. deklaracje wegańskości, twarde claimy). | Twarde deklaracje — autorytatywniejsze niż synteza NotebookLM. |
| Contentful (MCP) | Gotowe wpisy blog (narracja, cytaty marki). | Gdy szukasz istniejącej narracji z bloga (rezerwa — w sesji FAQ nietknięte). |

**Kluczowy insight:** pliki `wiedza_produktowa/*.md` to w dużej mierze **ta sama wiedza co w NotebookLM**, tylko w tekście. Dla większości tematów NotebookLM nie jest konieczny — czytaj repo najpierw, a NotebookLM trzymaj na luki i weryfikację.

---

## 2. Kolejność sięgania (od taniego do drogiego)

1. skill `naturalna-pielegnacja` + właściwy plik z `wiedza_produktowa/rytualy/` lub `produkty/` → rytuał + mechanizm.
2. `00_o_marce/produkty.json` → weryfikacja twardych danych (skład, stężenia, nazwy, linki).
3. NotebookLM → **tylko** luki, weryfikacja głosem Agaty, tematy słabo opisane w repo.
4. Contentful blog → istniejąca narracja, jeśli potrzebna.

---

## 3. NotebookLM — playbook operacyjny

- `get_health` → jeśli `authenticated:false`, uruchom `setup_auth` (`show_browser:true`). Loguje się Daniel/Agata (konto opcja_natura), ~1 min. **To akcja użytkownika — uprzedź, nie odpalaj „w tle".**
- `ask_question` ZAWSZE z `show_browser:true`. W trybie headless Google serwuje okrojoną stronę bez pola czatu → błąd „could not find chat input".
- **Follow-upy w tej samej sesji (`session_id`) potrafią się wieszać** — tooltip cytatu przykrywa pole input i `ask_question` zwraca timeout „textarea intercepts pointer events". **Obejście: każde pytanie jako ŚWIEŻA sesja** (pomiń `session_id`). Koszt: brak kontekstu rozmowy → formułuj każde pytanie kompletnie i samodzielnie.
- **Batchuj** 3–4 podtematy w jedno pytanie — mniej wywołań, mniej okazji do zawieszenia.
- `source_format:"footnotes"` pokazuje, z którego źródła pochodzi fragment (np. `Recording_1.m4a` = głos Agaty) — dowód, że odpowiedź jest gruntowana w jej szkoleniu, nie w ogólnej wiedzy Gemini.
- Odpowiedź jest AI (Gemini 2.5 z user-uploaded sources) — **przy rozbieżności twarde dane bierz z `produkty.json` / `b2b_opisy`, nie z syntezy.**

---

## 4. Jak pisać z tej wiedzy

Sourcing to połowa roboty — styl i format są w `projekty_claude/contentWriter/` (pliki `FORMAT_*`), a kanon marki (`brand_dna.md`, `wiedza_o_kliencie.md`) w `00_o_marce/`. Zasada: „edukacja, nie reklama". Domyślnie dla treści edukacyjnych klienta: **rytuał + mechanizm, prosty język**, a nazwy produktów/linki tylko jeśli tak ustalono z Agatą/Danielem.

Zob. [[reference_wiedza_produktowa]], [[reference_notebooklm_mcp]].

---

*Źródło: wnioski z sesji budowy FAQ na strony zestawów (czerwiec 2026) | Opcja Natura*
