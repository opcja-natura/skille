# skille – skille firmowe Opcji Natury

Jedno źródło prawdy dla skilli **organizacji** Opcji Natury: tych, z których korzystają pracownicy (biblioteka organizacji na claude.ai, workspace ChatGPT, projekty zespołu). Narzędzia, z którymi pracuje tylko Daniel w Claude Code, są poza tym repo (lokalne `~/Claude_praca/skille_daniel/`). Repo prywatne `opcja-natura/skille`.

Log wgrań: [`WGRANIA.md`](WGRANIA.md) — po każdym wgraniu dopisz wiersz.

**Zasada:** skill zmieniamy TYLKO tutaj. Po każdej zmianie: commit + push, potem ponowne wgranie paczki tam, gdzie skill jest używany (kolumna „Gdzie wgrany”). Kopie poza tym repo nie istnieją; Claude Code Daniela czyta skille przez symlinki `~/.claude/skills/<nazwa>` → `skills/<nazwa>`.

Wyjątki (skille żyjące przy swojej dokumentacji, bo czytają pliki repo względnymi ścieżkami):
- `opcja-natura-erp` → repo `erp-docs` (`skills/opcja-natura-erp/`)
- `hub-manufaktura`, `ocena-obslugi-klienta` → repo `hub-manufaktura` (`skills/`)

## Struktura

```text
skills/<nazwa>/SKILL.md     skill (+ references/, assets/, skrypty, agents/openai.yaml dla ChatGPT)
wycofane/<nazwa>/           skille zastąpione; zdjąć z claude.ai, nie wgrywać ponownie
scripts/pakuj.sh            buduje paczki do wgrania: dist/<nazwa>.zip
```

Nazwa folderu = pole `name:` we frontmatterze `SKILL.md`. Paczki nie są w repo (`dist/` w `.gitignore`), buduje się je przed wgraniem:

```bash
scripts/pakuj.sh                 # wszystkie
scripts/pakuj.sh przelewy-powracajace product-documents
```

Ta sama paczka nadaje się do claude.ai i do ChatGPT (ChatGPT czyta dodatkowo `agents/openai.yaml`, claude.ai go ignoruje).

## Rejestr (stan 10.10.2026)

Skróty w kolumnie „Gdzie wgrany”: **org** = biblioteka organizacji claude.ai, **claude.ai-D** = skille osobiste Daniela na claude.ai, **ChatGPT** = workspace ChatGPT (Karina), **CC** = Claude Code Daniela.

### Operacje i ERP

| Skill | Po co | Gdzie wgrany | Uwagi |
|---|---|---|---|
| `raw-material-documents` | dokumenty stałe surowców (SDS, certyfikaty, IFRA) w `BD_surowiec_dokumenty` | ChatGPT | zgodny z arkuszem live 10.10 |
| `product-documents` | dokumenty produktów gotowych (PIF, SDS, ROB…) | ChatGPT | zgodny z arkuszem live 10.10; opis we frontmatterze mówi „edytowalne źródło + PDF”, a od 16.09 `source_url` jest opcjonalny (do poprawy) |
| `delivery-quality-documents` | CoA/MSDS do konkretnej dostawy surowca | ChatGPT | zgodny z arkuszem live 10.10 |
| `delivery-order-intake` | zakładanie zamówień eksploatacyjnych/pozostałych w rejestrze dostaw | ChatGPT | zgodny z arkuszem live 10.10 |
| `przelewy-powracajace` | odnotowanie opłaconych płatności powracających | ChatGPT | zgodny z arkuszem live 10.10 |
| `katalog-wersje` | wersje i poprawki katalogu PL/EN | — | niewgrany |

### Marka, produkt, treści

| Skill | Po co | Gdzie wgrany | Uwagi |
|---|---|---|---|
| `naturalna-pielegnacja` | doradztwo pielęgnacyjne, rytuały | CC | 10.10: kopia w CC miała błąd (30% biofermentu w Atop Stop zamiast 10%) i brak sekcji „pachy”; kanon = ta wersja |
| `produkty-lookup` | szybki lookup produktu: opis + link do strony (bez cen i pojemności od 10.10) | CC | nazwy produktów do tatuażu nieaktualne (czeka na decyzję); docelowo lista generowana z `products_catalog` |
| `pozyskiwanie-wiedzy-produktowej` | mapa źródeł wiedzy produktowej | — | |
| `glos-opcja-natura` | pisanie prozy marki PL | CC | odsyła do plików `modele-wszystko/projekty_claude/contentWriter/`; poza CC trzeba je dograć jako wiedzę projektu |
| `tlumaczenia-opcja-natura` | tłumaczenia EN | CC | z glosariuszem `glosariusz_en.md` |
| `opcja-natura-creative-brand` | brandbook 08.2026 dla działu kreatywnego | ChatGPT, CC | |
| `consensus-formulacja` | research naukowy przy recepturach | org | |

### Marketing i social

| Skill | Po co | Gdzie wgrany | Uwagi |
|---|---|---|---|
| `marketing-opcja-natura` | planowanie: plan roczny, kampanie, projekty, historia postów, plan miesiąca; SKILL.md = część dla operatora, `references/zrodla-i-zapis.md` = technika | org, CC | 10.10.2026 przepisany (podział ludzka/techniczna, ludzie z Ról w produkcji); do ponownego wgrania |
| `notion-publikacje` | publikacje i zadania marketingu w Notionie; SKILL.md = część dla operatora (po ludzku), `references/zapis.md` + `inne-bazy.md` = część techniczna dla agenta | org, CC | 10.10.2026 wchłonął `notion-produkcja-tresci`; zweryfikowany na żywym Notionie i n8n; org ma stare wersje obu — wgrać ten, tamten zdjąć |
| `tiktok-opcja-natura` | second brain TikToka Agaty | org | master był tylko w paczce |
| `slack-opcja-natura` | Slack dla pracownika: kanały i do czego służą, apki (marketing, kupony, urlopy), wysyłki, boty | claude.ai-D | przepisany 10.10.2026 (bez `employees.json`); do wgrania do organizacji zamiast wersji z 09.04 |

### B2B, sprzedaż, eksport

| Skill | Po co | Gdzie wgrany | Uwagi |
|---|---|---|---|
| `bigin-opcja-natura` | CRM Bigin na żywo: rdzeń + `references/` (handel, marketing-trade, rozliczenia-retro) | org | przebudowany 10.10.2026 (zweryfikowany na MCP); poprawka zapisu akcji 12.10.2026, wgrany (`c8e81f9`) |
| `analityka-b2b-zoho` | liczenie sprzedaży B2B w Zoho Analytics | org | |
| `sprint-handlowy` | partner Łukasza do szukania sprzedaży | org | |
| `ocena-wydawcy-b2b` | ocena cudzej domeny pod współpracę | org | |


### Wycofane (zdjąć z claude.ai)

| Skill | Zastąpiony przez |
|---|---|
| `bigin-mcp-navigation` | `bigin-opcja-natura` + `analityka-b2b-zoho` (25.09.2026) |
| `notion-produkcja-tresci` | `notion-publikacje` (10.10.2026) |
| `notion-opcja-natura` | `notion-publikacje` + `references/inne-bazy.md` (10.10.2026) |
| `supabase-opcja-natura` | `sklep-ecommerce-database`, `pracownicy-database`, `produkty-lookup`, `meetings-opcja-natura` |

## Poza tym repo (świadomie)

- **Skille robocze Daniela** (tylko Claude Code, nie dla zespołu): lokalne repo `~/Claude_praca/skille_daniel/` — m.in. `radar-aeo`, `metabase-dashboards-opcja-natura`, `backoffice-opcja-natura`, `sklep-ecommerce-database`, `pracownicy-database`, `meetings-opcja-natura`, `influencer-research`, `generowanie-przelewow-pko`. Jeśli taki skill ma trafić do zespołu, przenosimy go tutaj.
- Skille ogólne, niefirmowe (`n8n-*`, `apify-cli`, `google-workspace-cli`, `notion-api`, `kompresja-zdjec*`, `usuwanie-tla-obrazow`), skille Anthropic (docx, pdf, xlsx…) i `humanizer` — tylko w `~/.claude/skills`.
