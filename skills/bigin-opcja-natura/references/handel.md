# Bigin — część handlowa: zamówienia, faktury, klienci, telefony

Czytaj, gdy pytanie dotyczy sprzedaży B2B, należności, portfela handlowca, telefonów albo „co się dzieje u klienta X". Zasady pobierania i pułapki COQL są w `SKILL.md`.

## ⚠️ Zamówienie i faktura to DWA rekordy na tę samą sprzedaż

Każde zamówienie ma bliźniaczy rekord faktury z tą samą kwotą. Liczenie „wszystkich rekordów z kwotą" albo mieszanie etapów zamówień z etapami faktur (np. `Wysłane` + `Faktura oplacona`) **dubluje obrót**.

- **Sprzedaż / „kto zamówił"** → tylko etapy potoku Zamówienia.
- **Należności / „kto nie zapłacił"** → tylko etapy potoku Faktury.
- **Łącznik zamówienie↔faktura:** pole `baselinkerOrderId` (to samo na obu rekordach). Na fakturze numer zamówienia jest też w `Description` („order id: ON-B2B__3525"), ale `Description` **nie da się filtrować**.

Zamówienia i faktury **nie są wpisywane ręcznie** — spływają automatem z BaseLinkera (zamówienia `ON-B2B__…`) i wFirmy (faktury).

## Pola

**Zamówienie** (potok Zamówienia):
`Deal_Name` · `Account_Name` (lookup → klient) · `Stage` · `Amount` (**netto**) · `Kwota_brutto` · `Created_Time` (kiedy wpadło do CRM — nie do okresów) · `Closing_Date` (**dzień finalizacji zamówienia — oś czasu do okresów sprzedaży**) · `baselinkerOrderId` · `strona_zamowienia` (link do zamówienia w BL) · `email_zam_wienia` · `Client_Merchant_Id` (id handlowca klienta, kopiowane na zamówienie) · `Associated_Products` (pozycje: produkt, ilość, cena, rabat — tylko przez `getSpecificRecord`)

**Faktura** (potok Faktury):
`Deal_Name` (nr faktury) · `Account_Name` · `Stage` · `Amount` (netto) · `Closing_Date` = **termin płatności** · `link_do_fv` (wFirma) · `baselinkerOrderId` · `Created_Time` = data wystawienia (w praktyce)

**Klient** (`Accounts`):
| Pole | Znaczenie |
|---|---|
| `Account_Name` | nazwa |
| `Klient_handlowiec` | **opiekun handlowy** (lookup) — filtr portfela |
| `Owner` | kto założył konto — **NIE** oznacza opiekuna |
| `Klient_status` | `aktywny` / `nieaktywny` / `potencjalny` |
| `Segment` | kanał: np. `Drogeryjny (punkty, zrzeszenia, hurtownie)`, apteka, zielarnia, gabinet… (pełne wartości zbierz z danych, do filtra użyj `like`) |
| `rodzaj_sprzeda_y` | multiselect, np. `Internet (sklep, marketplace, sm, kamerki, drop)` |
| `Klient_wartosc` | wartość historyczna — ⚠️ **TEKST** (sortowanie alfabetyczne) |
| `Klient_ostatnie_zam_wienie` | data ostatniego zamówienia |
| `warto_rabatu`, `Spos_b_liczenia_rabatu` | rabat % i „z góry"/retro |
| `Klient_retro_warto`, `Klient_retro_warunki` | warunki retro (patrz `rozliczenia-retro.md`) |
| `Termin_p_atno_ci_dni`, `Spos_b_p_atno_ci` | termin i forma płatności |
| `Wysy_ka_pr_g_darmowej_wysy_ki` | próg darmowej wysyłki (standard 800) |
| `Logistyka_wymagana_awizacja`, `Logistyka_e_mail_awizacji`, `Logistyka_istotne_informacje`, `Logistyka_url_wytycznych` | awizacje i wymagania dostawy |
| `E_mail_dla_fv`, `faktura_wymagany_xml`, `nazwa_faktura`, `Klient_nip` | fakturowanie |
| `formularz_zam_wie` | link do arkusza zamówień klienta |
| `Tag` | m.in. **`dluznik`**, `faktury_do_oplacenia`, `nowy` |

**Rozmowa** (`Calls`): `Subject` · `Call_Start_Time` · `Call_Duration_in_seconds` · `Call_Type` (`Wychodzące`/przychodzące) · `Call_Purpose` · `What_Id` (klient) · `Who_Id` (osoba) · `Owner` (kto dzwonił — **w Calls to jest filtr handlowca**). `Call_Status` istnieje, ale **nie działa w COQL**.

Portfel handlowca = `Klient_handlowiec`, **nie** `Owner` (stare konta zakładał Daniel, a opiekunem jest dziś ktoś inny). Wyjątek: w `Calls` filtruj po `Owner`.

## Zapytania

**Zamówienia od daty (cała firma):**
```sql
select Deal_Name, Account_Name.Account_Name, Amount, Stage, Closing_Date
from Pipelines
where Stage in ('Otrzymano od klienta','Przekazano do realizacji','Spakowano','Wysłane','Zamówiene dostarczone','Dostarczone - komis','Wstrzymane - on hold')
  and Closing_Date >= '2026-09-21'
order by Closing_Date asc limit 200
```
„Co nowego wpadło do CRM od rana" → zamiast `Closing_Date` użyj `Created_Time >= '2026-09-25T00:00:00+02:00'`.

**Portfel handlowca** — trzeci warunek lookupem przez klienta, **nawiasy obowiązkowe** (sprawdzone 10.10.2026):
```sql
... where (Stage in (...) and Closing_Date >= '2026-09-21')
      and Account_Name.Klient_handlowiec = '427926000000706904'
```
(`Client_Merchant_Id = '<id>'` działa na zamówieniach, ale na fakturach bywa puste. Lookup przez `Account_Name` działa dla obu.)

**Niezapłacone faktury / po terminie:**
```sql
select Deal_Name, Account_Name.Account_Name, Amount, Closing_Date, Stage, link_do_fv
from Pipelines
where Stage in ('Wystawiono Fakture','Faktura po terminie platnosci')
  and Closing_Date < '2026-09-25'
order by Closing_Date asc limit 200
```
Stare faktury „po terminie" (termin w 2025, np. Kopalnia Zdrowia, Gemini, Nutridome) bywają nieprzestawione po zapłacie. Przy należnościach starszych niż ~3 miesiące pisz „do sprawdzenia w wFirmie", nie „dług".

**Dłużnicy:** `select Account_Name, Phone from Accounts where Tag = 'dluznik' limit 200`.

**Historia klienta** (najpierw id: `select id, Account_Name from Accounts where Account_Name like '%natura%' limit 5`, potem):
```sql
select Deal_Name, Stage, Amount, Closing_Date, Created_Time
from Pipelines where Account_Name = '<ACCOUNT_ID>'
order by Created_Time desc limit 20
```
Zwraca naraz zamówienia, faktury, akcje, retro i notatki — rozdziel po `Stage`.

**Portfel handlowca, ostatnio zamawiający:**
```sql
select Account_Name, Klient_ostatnie_zam_wienie, Klient_wartosc, Segment, Tag
from Accounts
where Klient_handlowiec = '427926000000706904' and Klient_status = 'aktywny'
order by Klient_ostatnie_zam_wienie desc limit 50
```

**Klienci, którzy zamilkli** (60–180 dni): `where Klient_handlowiec = '<id>' and Klient_ostatnie_zam_wienie between '2026-03-29' and '2026-07-27'`. Tagi `dluznik`/`faktury_do_oplacenia` pokaż osobno.

**Rozmowy handlowca w okresie (tylko odbyte):**
```sql
select Subject, Call_Start_Time, Call_Duration_in_seconds, Call_Type, What_Id
from Calls
where (Owner = '427926000000706904'
  and Call_Start_Time between '2026-09-22T00:00:00+02:00' and '2026-09-26T00:00:00+02:00')
  and Call_Duration_in_seconds is not null
limit 200
```
Bez `is not null` dostaniesz też rozmowy zaplanowane (także na 2027). „Skuteczna" rozmowa = powyżej 10 s. `What_Id` bywa pusty — klienta odczytaj wtedy z `Subject`.

**Zamówienie ↔ faktura:** `select Deal_Name, Stage, Amount from Pipelines where baselinkerOrderId = '347920884'`

## Pułapki tej części

- **Zamówienie przy dostarczeniu dostaje nowy rekord.** Synchronizacja z BaseLinkerem kasuje rekord i zakłada go od nowa: nowe `id`, `Created_Time` i `Closing_Date` = dzień finalizacji, kwota wyrównana do faktury. Stałym kluczem jest numer `ON-B2B__…` albo `baselinkerOrderId`, nie `id`.
- **Okres sprzedaży licz po `Closing_Date`, nigdy po `Created_Time`.** Historię 2023–2024 zaimportowano w 2025, więc według `Created_Time` wszystkie stare zamówienia „powstały" w 2025.
- **`Klient_wartosc` jest tekstem** — do rankingu pobierz i posortuj liczbowo sam.
- Status paczki, palety, WZ, rozliczenie komisu → BaseLinker i hub magazynu, nie Bigin.
