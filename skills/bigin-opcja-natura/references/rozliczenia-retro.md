# Bigin — Rozliczenia retro (rabaty przepływowe, retro kwartalne, bonusy, kody partnera)

Czytaj, gdy pytanie dotyczy retro, rabatu przepływowego, bonusu marketingowego dla partnera, „ile oddajemy klientowi X" albo „co jest do opłacenia". Stan sprawdzony na żywych danych 10.10.2026 (48 rekordów, od 07.2025).

## ⚠️ Najważniejsze: kwota bez podstawy

**Rekordy retro mają kwotę, ale nie mają pozycji ani wyliczenia, z którego ta kwota wynika.** Na 48 rekordach:
- `Amount` jest **zawsze pusty** — kwota siedzi w polu **`Warto_c_wpisywana_z_apy`** („wartość wpisywana z łapy”, netto), wpisywanym ręcznie; 5 rekordów nie ma nawet jej;
- `Description`, `Associated_Products`, `Warto_rabatu_netto_licz_od_obrotu`, `Warto_netto`, `Rabat_dla_Klient_od_Opcja_Natura` — **puste na wszystkich**;
- nie ma śladu, od jakiego obrotu, jakich faktur ani jakiego procentu policzono kwotę.

Co z tego wynika dla agenta:
- **Nie traktuj kwoty retro jako zweryfikowanej.** Podając ją, mów „wpisane ręcznie w Biginie”, nie „wyliczone”.
- **Nie odtwarzaj podstawy na zgadywanie.** Jeśli ktoś pyta „z czego wynika ta kwota”: odpowiedź brzmi „w Biginie nie ma wyliczenia”. Możesz zaproponować sprawdzenie: obrót klienta za okres z Zoho Analytics (skill `analityka-b2b-zoho`, po `Closing_Date` zamówień) × warunki z karty klienta, i pokazać różnicę, ale jako szacunek do potwierdzenia, nie jako fakt.
- **Warunki retro są na karcie klienta**, nie na rekordzie rozliczenia: `Accounts.Klient_retro_warto` (%) i `Klient_retro_warunki` (tekst, np. „5% E-commerce i 10% hurt”, „do 24 999-5% powyżej 8%”, „rozliczane co kwartał za sprzedaż, naliczany od cen zakupu”, „na marketing”). U części klientów oba pola są puste (np. DOZ, APTENEO), a retro i tak jest rozliczane.
- Przy sumowaniu retro (koszt partnera, rentowność klienta) zaznacz, ile rekordów nie ma kwoty, i nie zastępuj braków zerem bez słowa.

## Pola, które naprawdę są wypełniane

| Pole | Znaczenie | Uwagi |
|---|---|---|
| `Deal_Name` | okres i rodzaj: „RETRO Q3 2026”, „Rabat przepływowy 08.2026”, „Bonus marketingowy QIV 2025”, „kod MOC 15 od stycznia…” | nazwy dowolne, bez konwencji |
| `Account_Name` | partner | |
| `Stage` | `Do opłacenia` → `Opłacono` | tylko dwa etapy |
| `Warto_c_wpisywana_z_apy` | **kwota retro netto** | ręcznie; czasem pusta |
| `Closing_Date` | koniec rozliczanego okresu | bywa pusty |
| `Forma_rozliczenia` | `Fv od klienta` (partner wystawia nam fakturę) albo `Fv korekta ON` (my wystawiamy korektę) | bywa pusta |
| `fv_url` | link do dokumentu w wFirmie | `…/expenses/…` = faktura kosztowa od klienta, `…/invoices/…` = nasza korekta; pojedyncze linki wskazują kartę kontrahenta albo szkic (`contractors/`, `expense_drafts/`) — błąd wpisu; starsze rekordy bez linku |
| `Data_op_acenia_fv` | kiedy rozliczono | na części „Opłacono” pusta; jeden rekord ma datę sprzed okresu (VICA) — błąd wpisu |
| `Owner` | kto założył (głównie Łukasz) | edytuje też Karina (operacje) |

## Rodzaje rozliczeń (z nazw)

- **Rabat przepływowy** — miesięczny, korektą od nas (PGF, DOZ stacjonarne).
- **Retro kwartalne / półroczne** — fakturą od klienta (NATURA-MED, Melisa, KOALA, ezebra, APTENEO, Polska Grupa Zdrowia…).
- **Bonus marketingowy** — premia na działania marketingowe partnera (Błysk).
- **Rozliczenie kodu rabatowego** partnera (MOC W NATURZE, „kod MOC 15”).

## Zapytania

**Do opłacenia teraz:**
```sql
select Deal_Name, Account_Name.Account_Name, Warto_c_wpisywana_z_apy, Closing_Date, Forma_rozliczenia, fv_url
from Pipelines where Stage in ('Do opłacenia') order by Closing_Date asc limit 50
```

**Historia retro klienta:** jak wyżej z `Stage in ('Do opłacenia','Opłacono')` i `Account_Name = '<id>'` (dwa warunki w nawiasie + trzeci).

**Warunki klienta:**
```sql
select Account_Name, Klient_retro_warto, Klient_retro_warunki, warto_rabatu, Spos_b_liczenia_rabatu
from Accounts where Account_Name = 'PGF' limit 5
```

Zapis (zmiana `Do opłacenia` → `Opłacono`, data rozliczenia) tylko na wyraźną prośbę, po pokazaniu, co się zmieni. Kwot nie poprawiaj sam.
