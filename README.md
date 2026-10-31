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
| `produkty-lookup` | dane o kosmetykach tylko z konektora „Opcja Natura — produkty” (skład, ceny, zdjęcia, zestawy, kategorie) | CC, org | od 15.10 mini-skill; wymaga konektora (Edge Function `produkty-mcp`, on_brain, projekt `n8n/products_and_categories_sync`); dane z dev do przełączenia synca na prod |
| `glos-opcja-natura` | **parasol treści PL**: głos marki, kto mówi, compliance (1223/2009, 655/2013, EmpCo + 6 wzorców z uwag prawnika Trust Luna 09.2026), opis marki, przykłady przed/po, formaty (blog, SEO, newsletter, strona kosmetyku, social, B2B); odsyła do mniejszych skilli | org, CC | 15.10.2026 przebudowany na bazie wersji Agaty (Slack 14.10) + Content Writer (manifest, humanizer PL, FORMAT_*); samowystarczalny, wgrany do org 15.10 (`6392884`); Agata usuwa swoją prywatną kopię; hasło „Natura. To proste.”; 27.10.2026 strona kosmetyku: arkusz zmian opisów + menu „Wygeneruj nowy opis”, podmieniony w org 27.10 (`39d75ef`) |
| `faq-json-blog` | FAQ do wpisu na blogu w JSON (schemat, linki, checklista, przykład) | org (domyślny) | 15.10.2026 przeniesiony z `skille_daniel`; wchłonął `FORMAT_faqJSON.md` z Content Writera, głos odsyła do `glos-opcja-natura`; podmieniony w org 15.10 |
| `bibliografia-blog` | źródła naukowe do wpisu (Consensus → JSON Contentful) | org (domyślny) | 15.10.2026 przeniesiony z `skille_daniel` bez zmian treści; 15.10 podmieniony w org (`533d94b`, bez odesłania do `json_bibliografia.md`) |
| `glos-klienta-opcja-natura` | głos klientki w dwóch warstwach: nasza społeczność (komentarze FB/IG z Supabase socialAutomation `Komentarze`, per kosmetyk) + klientka kategorii (Wizaż: 16 reguł, FAQ i „czego nie obiecywać” dla 19 kategorii) + 5 grup klientek | org, CC | 15.10.2026 nowy; wyciąg z komentarzy social (15.10) i korpusu Wizażu (`~/Claude_praca/n8n/reviews_intelligence/`, 09.2026) + `00_o_marce/wiedza_o_kliencie.md`; podpowiedzi sprzeczne z uwagami prawnika poprawione; wgrany do org 15.10 (`854f874`) |
| `tlumaczenia-opcja-natura` | tłumaczenia EN (UK): glosariusz, compliance MHRA, lekcje z recenzji native | CC, org | 31.10.2026 glosariusz po tłumaczeniu 35 opisów (Meadow Hair Mask, bicarb, dezodoranty bez myślnika), wgrany do org 31.10 (`607e2a1`); 23.10.2026 nazwy chorób (egzema, AZS, łuszczyca) dozwolone przy Atop Stop, Mazidle, teście PTCA i opisie oferty (mamy dokumentację), nigdy jako leczenie; 19.10 lekcje z 2 recenzji Scribbr (⟳2); proces opisów EN (skrypty) tylko w CC |
| `opcja-natura-creative-brand` | wygląd marki: dokumenty biurowe i handlowe (oferty, tabele, PDF) + brandbook 08.2026 dla działu kreatywnego | ChatGPT, CC | 14.10.2026 dodany tryb „dokument” (`references/dokumenty-biurowe.md`); logo PL 09.2026 (Ula) w `assets/logo/`; do wgrania do org i ponownie do ChatGPT |
| `consensus-formulacja` | research naukowy przy recepturach | org | |

### Marketing i social

| Skill | Po co | Gdzie wgrany | Uwagi |
|---|---|---|---|
| `marketing-opcja-natura` | planowanie: plan roczny, kampanie, projekty, historia postów, plan miesiąca; SKILL.md = część dla operatora, `references/zrodla-i-zapis.md` = technika | org, CC | 10.10.2026 przepisany (podział ludzka/techniczna, ludzie z Ról w produkcji); do ponownego wgrania |
| `notion-publikacje` | publikacje i zadania marketingu w Notionie; SKILL.md = część dla operatora (po ludzku), `references/zapis.md` + `inne-bazy.md` = część techniczna dla agenta | org, CC | 10.10.2026 wchłonął `notion-produkcja-tresci`; zweryfikowany na żywym Notionie i n8n; org ma stare wersje obu — wgrać ten; 15.10 podmieniony w org (`05a8e05`, zakładka Home „Moje zlecenia”), tamten zdjąć |
| `tiktok-opcja-natura` | second brain TikToka Agaty | org | master był tylko w paczce |
| `slack-opcja-natura` | Slack dla pracownika: kanały i do czego służą, apki (marketing, kupony, urlopy), wysyłki, boty | org | przepisany 10.10.2026 (bez `employees.json`); 15.10 wgrany do org z zakładką Home „Moje zlecenia” (`05a8e05`) |

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
| `pozyskiwanie-wiedzy-produktowej` | `produkty-lookup` (konektor „Opcja Natura — produkty”) (15.10.2026; nigdzie niewgrany, nic do zdjęcia) |
| `naturalna-pielegnacja` | — **wstrzymany 15.10.2026 do weryfikacji Agaty** (doradztwo, rytuały); folder zostaje w repo, był tylko w CC. Dane o kosmetykach: `produkty-lookup`; jeśli wróci, raczej jako część `produkty-lookup` |

## Poza tym repo (świadomie)

- **Skille robocze Daniela** (tylko Claude Code, nie dla zespołu): lokalne repo `~/Claude_praca/skille_daniel/` — m.in. `radar-aeo`, `metabase-dashboards-opcja-natura`, `backoffice-opcja-natura`, `sklep-ecommerce-database`, `pracownicy-database`, `meetings-opcja-natura`, `influencer-research`, `generowanie-przelewow-pko`. Jeśli taki skill ma trafić do zespołu, przenosimy go tutaj.
- Skille ogólne, niefirmowe (`n8n-*`, `apify-cli`, `google-workspace-cli`, `notion-api`, `kompresja-zdjec*`, `usuwanie-tla-obrazow`), skille Anthropic (docx, pdf, xlsx…) i `humanizer` — tylko w `~/.claude/skills`. Angielski `humanizer` usunięty z biblioteki org 15.10.2026 (polski pas porządkowy jest w `glos-opcja-natura/references/warsztat-prozy.md`).
