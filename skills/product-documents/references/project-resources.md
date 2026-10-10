# Zasoby projektu

## Source of truth

### Baza dokumentów
- Nazwa: `BD_documents`
- Spreadsheet ID: `1oDY9v1Whi86hYYkqnuo4VsOJQbvJbmAnHh8UZO-4OJA`
- URL: `https://docs.google.com/spreadsheets/d/1oDY9v1Whi86hYYkqnuo4VsOJQbvJbmAnHh8UZO-4OJA/edit`

Zakładki:
- `BD_documents`
- `BD_document_versions`
- `BD_document_change_requests`
- `BD_document_types`
- `BD_document_areas`
- `link_document_type`
- `link_document_area`

### Baza produktów
- Nazwa: `BD_produkty`
- Spreadsheet ID: `1r22doIQDQDhYaZh1f3eWr8b1gj3gGBlbcjq41hf-ino`
- URL: `https://docs.google.com/spreadsheets/d/1r22doIQDQDhYaZh1f3eWr8b1gj3gGBlbcjq41hf-ino/edit`

Zakładki istotne dla tego skilla:
- `DB_products_internal` — klucz produktu: kolumna A, nagłówek `sercet_id` (literówka; semantycznie `product_id`)
- `link_product_document`

`BD_produkty` ma dziesiątki innych zakładek (per-produktowe robocze, koszty, B2B/Baselinker, `spis_tresci`, lokalny `config`) niezwiązanych z tym skillem — nie czytaj/nie zapisuj ich przy tej operacji.

**Uwaga**: `BD_produkty` ma własną zakładkę `config` (kolumny `id/name/url/sheetName/dataRange/spreadsheet_id/comment`) — to lokalny rejestr źródeł dla automatyzacji B2B/Baselinker tego workbooka, **nie** centralny `masterConfig` ERP i **nie** config arkusza operacyjnego (patrz niżej). Nie mylić tych trzech.

## Google README (opis modelu, nie dane)

Google Doc „System dokumentów produktowych — instrukcja i plan wdrożenia”:
`https://docs.google.com/document/d/1j9ojaNjrabDgEXfNVmFS0UcJiqN91Mt0EoaatIPAsJI/edit`

Traktuj jako materiał pomocniczy do zrozumienia intencji, nie jako źródło prawdy o schemacie — w co najmniej jednym miejscu jest nieaktualny względem żywego arkusza (nazwa pola `implemented_in_version_id`, patrz `schema.md`). W razie sprzeczności ufaj żywemu nagłówkowi arkusza.

## Drive — struktura docelowa (per typ dokumentu, od 2026-09-15)

Root:

```text
0000 DOKUMENTACJA PODLACZONA DO PRODUKTU
1Vy9Tgu9F4GTXdxghtH0oFf0uUPcB6Cjt
```

Mapa folderów per typ (nazwa folderu = dokładnie `BD_document_types.name`):

| Typ (`BD_document_types.name`) | folder `typ_<TYP>` | `_pdf/` | `_archive/` |
|---|---|---|---|
| PIF | `18Zo5b04pCDZNgjCzLshvgVZB3BJbs52U` | `1tmT-WOAtPl3LF4fVHpkX4pkf8OQv4p0S` | `1XAwaRk9ntTkEuT_JMy3MUvrUZEOl4hvh` |
| Karta charakterystyki (SDS) | `1I0SuCePd2tUKdYm79rvi7e9wvnrjTqjJ` | `1GB5xSK0YcWCFPrCuIg0Vs3nCxpwoWiHa` | `10tqVxR0hXIJ77uJf8bKIzJXo0GJjocRb` |
| ROB | `1jDrG2-z4xsQam98If7qchnmZjy4M7CTQ` | `1No8bwEidXxHLEq6szP4svsQMDI2lsC1J` | `1sVjhhAotV4RWwCP116I6VWPdPqEQWIOI` |
| Karta opisowa marketingowa | `19HXteW4aPKxM7eKWYQ9esAucmEr_-y00` | `11qZ1MGItwLYgbSXo8Mx6FabQMDmiXvQT` | `14WYr4Al2YwSxb5Z1wI905O4WsIOioPQC` |
| Specyfikacja jakościowa | `1Ez7A0fq4N2csv327HBbg0YpPZnypjCbC` | `1ba4M_KlZ5q0SkZpJ4RpLIkQwN9jNlcIG` | `1vNh4VCI4nmpQ9VxSXcodEeoxa7Mho29g` |
| Karta technologiczna | `1yUF76944BqJu_8e0rQZ9hbckNXuPegx4` | `1BnY4l-MoJEXb3JTE705wniX-a5js0I2i` | `1kpaWpg5iK2OhLN2ZQwyKKVCWyaixNV2G` |
| Instrukcja | `1bkBATNOqp77IrT24TF2HmscOJqKn50Mb` | `1cu8RzL-aTyGRDvz3A8U_63AdSe_fAMrL` | `1zr5mQOmL_M3eV5hKYOc8PLGMLT1BzYqo` |
| Dokument regulacyjny | `1V8wAhZ_d5svNpXj4Dhoxoq_9PvR_aPgi` | `1fVFaypMrS8hsOTvL35ujopcoHAi5Yrap` | `1IQqHt1nLMr9J-cQP_16uaMlGlPENGEma` |
| Inny dokument | `1q9UOoSAl-luPTJJ3NCpM8EA7lGOltQrw` | `1KuDa8uW29JdUMmt2BckZgXPR57mXkNjI` | `1FArxS4ApzuM6uKJKpJtkxwiaE-u51RQm` |
| Badanie dermatologiczne | `1mKaEQSVSb1GSAuVE1nsVUxujavfaa8vH` | `1SFHCvoiLx7q14ZDF0vLrdfx3dRuK29Cb` | `1u-LN2I29Ka9H2RW_yZ_EigrgSLNK8Z5m` |
| Badanie aparaturowe | `1fGfG5BQJEjU2zjps3KfzuRQaZGpppDqF` | `1czZNvSMuuCByDxGeAneqcTFAzGis9dVm` | `10Hd5W0f_nLv8Jm0gA7aLwDJSr_swb_Qt` |
| Badanie konsumenckie | `1pkP-geJTCHaBHIWLNwlcovGphwy7hvb7` | `1o2wgpZkGWkAlKVbRrL-uvlJ-P2G-9xVt` | `1VtJB9bIB9c_pxFCbJHSUDNmtDhmNjRDE` |
| Indeks pochodzenia naturalnego | `1TGs0GYSz3DBLjIcx8iKGq28YIJIQFcVW` | `195venv7cxRUQQpqgZwgU0hJhFayxphfH` | `1OckYOPX2PyS4LozJO7hpwsdT9TXp7DCG` |

Wszystkie foldery i podfoldery istnieją (pierwsze 9 typów od 2026-09-15 rano, ostatnie 4 typy — testy dermatologiczne/aparaturowe/konsumenckie + indeks pochodzenia naturalnego — dołożone tego samego dnia), wszystkie są puste. Nie twórz podfolderów per produkt ani per język wewnątrz `typ_<TYP>/`.

Jeśli w `BD_document_types` pojawi się nowy typ (kolejny wiersz w słowniku), a nie ma dla niego jeszcze folderu `typ_<TYP>/`, nie zgaduj lokalizacji — zatrzymaj się i zapytaj operatora, gdzie ma powstać (albo utwórz go analogicznie do istniejących, jeśli operator wyraźnie o to poprosi).

## Drive — struktura historyczna (tylko PIF, do migracji, NIE ruszać samodzielnie)

```text
_EN_  1aI1ZZhi0N7fPdzb2G8h9mvapyHJ2TVr1   (35 dokumentów PIF, język EN)
_PL_  11nIMRKI5rsoanVJdQhcH_Z17NzpYaKw_   (11 dokumentów PIF, język PL + zaległe .docx nieonboardowane)
```

oba pod wspólnym rodzicem `1Oyqcc53XSH4SxeZh-fIjrNOyA9mjFSpi`, każdy z podfolderami `_pdf/` i `_archive/`.

**Nowe wersje istniejących dokumentów PIF nadal trafiają tutaj** (do folderu wskazanego przez `BD_documents.folder_url` tego konkretnego dokumentu), nie do `typ_PIF/`, dopóki migracja nie zostanie wykonana jako osobne zadanie. Nie przenoś istniejących dokumentów PIF do `typ_PIF/` samodzielnie, nawet jeśli operator o to zapyta mimochodem — potwierdź, że to świadoma decyzja o uruchomieniu migracji, nie rutynowa operacja tego skilla.

## Warstwa operacyjna (podgląd, nie source of truth)

- Arkusz: `Dokumenty tabela operacyjna`
- Spreadsheet ID: `1Su71RzbUReFy9ikpJaQt7bHEiuVHGaA_zk2jgL3OoWA`
- **Widoczne zakładki (stan od 2026-09-16): `dokumenty` (pierwsza, jedyny widok operacyjny), `koszyk_eksportu`.** Wszystkie pozostałe (`per_dzial`, `per_product`, `per_typ`, `tabela`, `config`, `helper_*`, `APP_document_version_workbench`, `log_eksportow`) są **ukryte** — zostają jako techniczne źródło danych, nie do klikania przez operatora.
- `dokumenty` — jeden widok z 6 filtrami łączonymi na zasadzie AND (Produkt/Typ/Obszar/Właściciel/Status/Stan), jedna formuła `FILTER()` czytająca `tabela`. Zbudowany na wzór analogicznego widoku w `raw-material-documents` (`arkusz_operacyjny_surowiec_dokumenty`, zakładka `dokumenty`). Kolumna PDF (Q) jest formułą OSOBNĄ od głównego `FILTER`/`HSTACK` — `HSTACK()` w Google Sheets kasuje metadane hyperlinku, więc link musiał zostać wydzielony (`XLOOKUP`+`HYPERLINK` keyed po ID w tej samej kolumnie), inaczej PDF wygląda klikalnie ale nie jest.
- `koszyk_eksportu` — jedyne miejsce z trwałym stanem selekcji dokumentów do eksportu (patrz `scripts/20_basket.gs`). `dokumenty` sam w sobie NIE trzyma żadnego checkboxa/stanu — wiersz pod daną pozycją zmienia się przy każdej zmianie filtra, więc trwały stan tam by się rozjeżdżał między sesjami (kruczek hybrydy skryptowo-formułowej, zgłoszony przez Daniela 2026-09-16). Dodawanie do koszyka czyta natywne zaznaczenie wierszy w Sheets (`getActiveRangeList`) w momencie kliknięcia menu — nigdy stan zapisany wcześniej.
- `helper_filters_v2` (ukryta) — źródła dropdownów filtrów + kolumna `stan` (OK/ZMIANA W TOKU/ARCHIWUM/BRAK PDF; bez `valid_until`/`WYGASA` — te pola nie istnieją w tym schemacie) + `pdf_link` (niewykorzystywana finalnie w `dokumenty`, patrz wyżej).
- Techniczne: `tabela` (zdenormalizowany widok per dokument, source dla `dokumenty` i `koszyk_eksportu`), `config` (lokalny, 3 kolumny: źródło/url/zakładka — trzeci, inny „config" w tym systemie, patrz uwaga wyżej), `helper_*`.
- `log_eksportow` (ukryta) — jeden wiersz per uruchomienie eksportu (`scripts/40_log.gs`).
- Log/kolejka jobów „nowa wersja”: `APP_document_version_workbench` (ukryta) — nie jest wymagana do działania tego skilla, ale jest jedynym realnym śladem, jak wyglądał dotąd cały przebieg wdrożenia change requestu; przydatna jako wzorzec logowania.

Skill nie powinien wymagać od operatora ręcznego klikania w tym arkuszu. AI ma wykonywać operacje bezpośrednio na źródłowych tabelach i Drive. Arkusz operacyjny może służyć do diagnostyki/podglądu, ale nie jest source of truth.

## Eksport do klienta zewnętrznego (`scripts/`)

Pierwszy Apps Script tego modułu (2026-09-16), związany (bound) z arkuszem operacyjnym powyżej, menu **OPCJA NATURA**:

- `Dodaj zaznaczone wiersze do koszyka` / `Wyczyść koszyk` — patrz `scripts/20_basket.gs`.
- `Eksportuj koszyk do Dysku klienta…` — kopiuje aktualne PDF-y dokumentów z koszyka do nowego podfolderu `docsExport_<data>_<logId>_<nazwa>/` na Dysku współdzielonym **„Udostepnianie zewnetrzne"** (`0ADEjsNIiVeqgUk9PVA` — to Dysk współdzielony, NIE zwykły folder; ID czytane z zakładki `config`, rekord „Dysk eksportu klienta"), w podfolderze `dokumenty/`, plus osobny arkusz „Tabela dokumentów" z linkami **do kopii** (nigdy do oryginałów wewnętrznych). `logId` w nazwie folderu jednoznacznie łączy folder na Drive z jego wierszem w `log_eksportow`. Nadaje folderowi eksportu „anyone with the link", pokazuje wynik w oknie z klikalnym przyciskiem „Otwórz folder z linkiem" (zwykły `ui.alert` nie robi linków klikalnych). Limit **`PD_CONFIG.MAX_EXPORT_DOCUMENTS = 100`** dokumentów na jeden eksport (Daniel, 2026-09-16 — powyżej tego Apps Script i tak nie zdąży w limicie czasu wykonania). Patrz `scripts/30_export.gs`.
- Po każdym „Dodaj zaznaczone wiersze do koszyka" operator jest automatycznie przełączany na zakładkę `koszyk_eksportu`, żeby od razu widział co się dodało.
- Nie zweryfikowane na produkcji: czy polityka admina Workspace na tym konkretnym Dysku współdzielonym pozwala na „anyone with the link" — sprawdzić na pierwszym realnym eksporcie, nie zakładać z góry.
- Deploy: ręczne wklejenie plików `scripts/*.gs` do edytora Apps Script związanego z arkuszem operacyjnym (brak clasp w tym repo, patrz `CLAUDE.md`).

## Poza zakresem

- Dokumentacja surowców: zupełnie inny system (`BD_surowiec_dokumenty`, `1jPGq47sgSVsBRpcB_WGzIIKO2gC9dGdWjBd13BoRIaQ`). Obsługuje go skill **`raw-material-documents`** — przełącz się, nie próbuj tutaj.
- Dokumenty jakościowe dostawy: obsługuje skill **`delivery-quality-documents`** — przełącz się, nie próbuj tutaj.
