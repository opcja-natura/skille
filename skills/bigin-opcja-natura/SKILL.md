---
name: bigin-opcja-natura
description: Mapa CRM Bigin (Zoho) Opcji Natury dla agenta z MCP Bigin — 10 potoków w jednym module Pipelines (zamówienia B2B, faktury, akcje trade marketingowe i propozycje PRP-…, rozliczenia retro, standy, kody rabatowe, pozyskiwanie…), prawdziwe nazwy API pól, łączenie zamówienie↔faktura↔klient, sprawdzone zapytania COQL i pułapki, które po cichu zwracają zero albo dublują kwoty. Używaj ZAWSZE przed zapytaniem do Bigin — gdy ktoś pyta o klientów B2B, zamówienia hurtowe, faktury i należności, dłużników, akcje promo/trade marketing, propozycje, materiały dla partnera, retro i rabaty przepływowe, telefony handlowca, portfel handlowca, awizacje, komis, standy albo "co się dzieje u klienta X". Sumy, obroty za okres i rankingi liczy się w Zoho Analytics — od tego skill analityka-b2b-zoho. NIE do sprzedaży sklepu www (to Supabase, skill sklep-ecommerce-database).
---

# Bigin – Opcja Natura

Bigin to CRM działu B2B: klienci hurtowi (drogerie, apteki, zielarnie, gabinety), ich zamówienia, faktury, akcje trade marketingowe, rozliczenia retro i telefony handlowców. Zamówienia i faktury spływają automatem (BaseLinker, wFirma). Ręcznie handlowiec zakłada klientów, loguje rozmowy, prowadzi akcje i rozliczenia retro.

Ten plik to rdzeń: jak pobierać dane, mapa potoków, ludzie, pułapki COQL. **Szczegóły czytaj z `references/` dopiero, gdy pytanie ich dotyczy:**

| Pytanie o… | Plik |
|---|---|
| zamówienia, faktury, należności, dłużników, portfel, klientów, telefony | `references/handel.md` |
| akcje trade marketingowe, propozycje `PRP-…`, generator propozycji, materiały od marketingu dla partnera, standy, kody rabatowe partnera | `references/marketing-trade.md` |
| retro, rabat przepływowy, bonus marketingowy, „co do opłacenia partnerowi” | `references/rozliczenia-retro.md` |

Wszystko sprawdzono na żywych danych 25.09.2026, a ludzi, akcje i retro ponownie 10.10.2026. Jeśli zapytanie zwraca błąd `column given seems to be invalid`, pole zmieniło nazwę — dopiero wtedy sięgnij po metadane.

## Pobieranie danych — jak nie przepalać kontekstu

Każdy zwrócony rekord ląduje w rozmowie. Orientacyjnie: wiersz COQL z 5 polami ≈ 60 tokenów (200 wierszy ≈ 12 tys.), pełny rekord z `Bigin_getSpecificRecord` ≈ 2–3 tys., `Bigin_getModules` ≈ 5 tys., `Bigin_getLayoutsMetadata` dla Pipelines ≈ 390 tys. znaków (nie mieści się w limicie narzędzia). Idź po drabinie od góry:

1. **Czy odpowiedź jest już w polach klienta?** `Accounts` trzyma gotowe podsumowania: `Klient_ostatnie_zam_wienie`, `Klient_wartosc`, `Tag` (dłużnik), rabat, retro, termin płatności, wymagania logistyczne. „Kiedy X ostatnio zamawiał", „czy X jest dłużnikiem", „kto zamilkł" → jedno zapytanie do `Accounts`, **bez skanowania zamówień**.
2. **COQL z minimalną listą pól.** Nazwę klienta bierz lookupem `Account_Name.Account_Name`, nie drugim zapytaniem.
3. **Zawężaj w `WHERE`, zanim podniesiesz `limit`**: data, portfel handlowca, etapy. Zacznij od `limit 50`; `more_records: true` = jest więcej (`limit 200 offset 200` dla kolejnej strony).
4. **Nie wołaj metadanych** (`getModules`, `getLayoutsMetadata`, `getFields`) — struktura jest w tym skillu. Listę wartości sprawdzisz tanio przez `group by` (niżej).
5. **`Bigin_getSpecificRecord` tylko wtedy, gdy potrzebujesz czegoś, czego COQL nie da** — w praktyce pozycji zamówienia (`Associated_Products`).
6. **Nie pobieraj drugi raz tego, co już jest w rozmowie.**

**Duże przekroje** (więcej niż ~200 rekordów):
- **Masz narzędzie do subagentów** (np. `Agent` w Claude Code): zleć pobranie i przeliczenie subagentowi z tym skillem i poleceniem „zwróć tylko tabelę wynikową, maks. 20 wierszy".
- **Wynik narzędzia trafia do pliku** albo masz wykonywanie kodu: przelicz plik skryptem (`jq`/Python), nie czytaj go.
- **Nie masz żadnego z nich** (zwykły czat claude.ai): stronicuj z minimalną listą pól, licz na bieżąco. Jeśli masz Zoho Analytics — **każdą sumę, ranking i przekrój w czasie licz tam** (skill `analityka-b2b-zoho`).

## Moduły

| API name | Co to | Uwagi |
|---|---|---|
| `Accounts` | **Klienci** | jedno konto = jedna firma/punkt |
| `Pipelines` | **wszystko, co ma etap** | 10 potoków w jednym module — patrz niżej |
| `Contacts` | osoby | z kontem = kontakt u klienta; bez konta = lead |
| `Calls` | rozmowy telefoniczne | także **zaplanowane** (przyszła data, brak czasu trwania) |
| `Tasks`, `Events`, `Products`, `Notes` | zadania, spotkania, produkty, notatki | `Associated_Products` = pozycje zamówienia (subform) |

## Potoki w `Pipelines` — rozpoznawaj po etapie (`Stage`)

⚠️ **Nie da się filtrować po potoku.** `Sub_Pipeline` w `WHERE` → błąd „invalid column". `Pipeline = '<id>'` → **pusty wynik bez błędu**. Potok wybieraj przez listę `Stage`.

| Potok (`Pipeline.id`) | Otwarte | Zamknięte ✓ | Odpadło ✗ | Więcej |
|---|---|---|---|---|
| **Zamówienia** (`…032043`) | `Otrzymano od klienta` · `Przekazano do realizacji` · `Spakowano` · `Wysłane` · `Dostarczone - komis` · `Wstrzymane - on hold` | `Zamówiene dostarczone` | `Zamknięty, utracony` | `handel.md` |
| **Faktury** (`…1199353`) | `Wystawiono Fakture` · `Faktura po terminie platnosci` | `Faktura oplacona` · `Faktura anulowana` | — | `handel.md` |
| **Akcje Promo i Marketing** (`…654205`) | `Warto zaproponować` · `Zaproponowano Klientowi` · `Zaplanowano z klientem` · `W realizacji` (+ nieużywany `Zaplanowano paczkę marketing`) | `Zrealizowano` (+ nieużywany `Dostarczono paczkę marketing`) | `Odrzucono` | `marketing-trade.md` |
| **Rozliczenia retro** (`…950289`) | `Do opłacenia` | `Opłacono` | — | `rozliczenia-retro.md` ⚠️ kwota nie w `Amount` |
| **standy** (`…1514096`) | `Zaproponowano stand` | `Wstawiono stand` | `Zakończono stand` | `marketing-trade.md` |
| **Kod rabatowy** (`…1135540`) | `Kod rabatowy zaproponowany` | `Kod rabatowy aktywny` | `Kod rabatowy wygasł` | `marketing-trade.md` |
| **Wysyłki Marketingowe** (`…1481416`) | `Zaplanowwano wysyłke marketingową` | `Dostarczono paczkę marketing` | — | **martwy** (2 rekordy z 01.2026); paczki idą przez Slack `#zlecenia-wysylki` |
| **Pozyskiwanie klientów** (`…706257`) | `Zimny Kontakt` · `Zimny Kontakt - priorytet` · `Wysłano mail - oferta 1` · `Wykonano telefon zainteresowani` · `wysłano paczkę marketingową` · `Otrzymano zapytanie` · `Klient utworzony - brak zamówienia` | `Klient pozyskany - złożono zam.` | `Klient utracony` | nazwisko / nazwa leada |
| **Notatnik** (`…749485`) | `Notatki handlowca` · `Notatki administracyjne` | — | — | notatka jako rekord |
| **Komentarze o produkcie** (`…705104`) | `Opinia neutralna` · `Pomysł` | `Opinia pozytywna` | `Opinia negatywna` | `www/<tytuł>` — opinie ze sklepu B2C, **nie B2B**; wykluczaj z „co nowego w CRM" |

Pełne id potoku = `427926000000` + końcówka (np. Akcje = `427926000000654205`) — potrzebne tylko przy **zapisie**.

- Literówki (`Zamówiene`, `Fakture`, `oplacona`, `Zaplanowwano`) wpisuj 1:1, inaczej wynik jest pusty.
- **COQL filtruje po nazwie wyświetlanej.** Przy **zapisie** część etapów ma inną wartość techniczną: `Zaproponowano Klientowi`→`Zaproponowano`, `Spakowano`→`Proposal/Price Quote`, `Wysłane`→`Negotiation/Review`, `Zamówiene dostarczone`→`Closed Won`, `Zamknięty, utracony`→`Closed Lost`, `Zimny Kontakt`→`Potencjalny Klient`, `Wykonano telefon zainteresowani`→`Wykonano telefon`, `Klient pozyskany - złożono zam.`→`Klient pozyskany`. Wyjątek: `Zaplanowano z klientem` zapisuj pełną nazwą (`Zaplanowano` → `MAPPING_MISMATCH`, sprawdzone 12.10.2026).

## Ludzie (id użytkowników Bigina, stan 10.10.2026)

| Osoba | id | Rola w danych |
|---|---|---|
| Łukasz Jakubiec | `427926000000706904` | handlowiec: portfel, akcje, prawie wszystkie rozliczenia retro |
| Konrad Orzechowski | `427926000001433004` | handlowiec (portfel, m.in. tatuaż) |
| Daniel Suliga | `427926000000297001` | portfel części klientów; Owner starych rekordów |
| Karina Orwat | `427926000001864306` | operacje: edytuje rozliczenia retro |
| Grzegorz Gęsiarek | `427926000001727366` | były lider handlu (odszedł 10.2026); rekordy z 09.2026. Stare id `…000000720544` nieużywane |
| Monika Kwiecień-Gonda, Krystian Konieczny | `…1535630`, `…640006` | historyczni, brak aktywności od 06.2026 |

Aktywne portfele (`Klient_handlowiec` na kontach aktywnych): tylko Łukasz, Konrad i Daniel. Portfel = `Klient_handlowiec`, **nie** `Owner`; wyjątek: w `Calls` filtruj po `Owner`.

## Sumy, okresy, rankingi → skill `analityka-b2b-zoho`

Bigin nie liczy (brak `SUM/COUNT`). Obroty za okres, porównania, rankingi, koszt akcji w czasie licz w **Zoho Analytics**. Z Bigina dobieraj to, czego Analytics nie ma: rekordy z dzisiaj, szczegóły jednego rekordu, kontakty, rozmowy, zapis.

## Pułapki COQL (każda sprawdzona)

1. **Więcej niż 2 warunki w `WHERE` → nawiasy.** `a and b and c` = `SYNTAX_ERROR near where` (sprawdzone ponownie 10.10.2026); `(a and b) and c` działa.
2. **`in` tylko małymi literami.** `Stage IN (...)` → „invalid operator".
3. **Filtr po potoku nie działa** — `Sub_Pipeline` = błąd, `Pipeline = '<id>'` = cisza.
4. **Brak `COUNT/SUM/AVG`** (`group by` z agregatem → błąd). Ale `group by` **bez agregatu działa jak DISTINCT**: `select Stage from Pipelines where id is not null group by Stage limit 200` — tak sprawdzisz listę wartości zamiast metadanych.
5. **`Description` i inne długie pola tekstowe nie wchodzą do `WHERE`.**
6. **Daty z pełną strefą:** `'2026-09-21T00:00:00+02:00'` (od końca X do końca III `+01:00`). Brak funkcji dat — podstaw konkretną datę.
7. **Zero wyników wygląda jak sukces bez danych:** `{"data":{"message":"…executed successfully!"}}` bez `data.data` = 0 rekordów, nie błąd. Zanim powiesz „nic nie ma", sprawdź literówkę w etapie i czy nie filtrujesz po `Pipeline`.
8. **Puste pole kwoty to nie zawsze zero.** `Amount` jest wypełniany tylko w zamówieniach i fakturach. W retro kwota jest w `Warto_c_wpisywana_z_apy`, w akcjach w `Warto_akcji_netto` / `Ca_kowity_koszt_akcji` (często niewpisane).
9. **Lookup w zapisie** to obiekt `{"id": "..."}`, nie string. Przy tworzeniu rekordu `Sub_Pipeline` wymaga też `Pipeline`. `updateRecords` przyjmie sam `id` + zmieniane pole.
10. **Pól ani wartości picklist nie da się zakładać przez API** — robi to admin w UI.

## Tryb pracy

- Domyślnie **tylko odczyt**. Zapis (zmiana etapu, notatka, tag) — tylko na wyraźną prośbę, z potwierdzeniem, co dokładnie się zmieni. **Nie usuwaj** rekordów.
- Agent handlowca widzi tylko swój portfel (filtr `Klient_handlowiec`) — instrukcje projektu konkretnego handlowca mają pierwszeństwo.
- Status paczki, palety, WZ, rozliczenie komisu → BaseLinker i hub magazynu. Materiały od marketingu → Notion/Slack (`marketing-trade.md`).
