# Bigin — trade marketing: akcje, propozycje, przepływ do marketingu, standy, kody

Czytaj, gdy pytanie dotyczy akcji promo/trade marketingu u partnerów B2B, propozycji `PRP-…`, materiałów dla partnera, standów albo kodów rabatowych partnera. Zasady pobierania i pułapki COQL są w `SKILL.md`. Stan sprawdzony na żywych danych 10.10.2026.

## Przepływ akcji od propozycji do materiału

```
1. Generator propozycji (arkusz propozycjeB2B, Apps Script)
   handlowiec wybiera klienta i do 5 działań z katalogu → Doc + PDF + N rekordów w Biginie
   → Stage „Warto zaproponować", propo_id = PRP-00xx, Owner = handlowiec, link_propozycji = PDF
   Generator NIC nie wysyła klientowi.
2. Handlowiec wysyła propozycję mailem (ręcznie)          → „Zaproponowano Klientowi"
3. Klient akceptuje działanie                             → „Zaplanowano z klientem"
   (każde działanie osobno: „przyjął 3 z 5" = 3 rekordy dalej, 2 na „Odrzucono")
4. Potrzebny materiał od marketingu (baner, artykuł, plakat, newsletter…):
   handlowiec składa w Slacku skrót ⚡ „Zlecenie B2B" (apka Zlecenia marketing),
   partner wybierany z Bigina, LINK DO AKCJI W BIGINIE OBOWIĄZKOWY
   → karta na #zlecenia-marketing + rekord w Notionie (Publikacje, pole „Link do akcji Bigin")
   → Agata przyjmuje / doprecyzowuje / odrzuca → zadania dla twórców
   → po wykonaniu: „✅ gotowe" + link do materiałów W WĄTKU SLACKA (nie w Biginie)
5. Akcja trwa                                             → „W realizacji"
6. Koniec                                                 → „Zrealizowano"
```

**Bigin nie wie o kroku 4.** Apka zleceń tylko czyta klientów (kopia Bigina w Supabase `b2b.clients_b2b`), nic nie zapisuje do Bigina. Etap akcji przestawia handlowiec ręcznie. Status materiału sprawdzisz w Notionie (Publikacje, `Status zlecenia`) albo w wątku karty na `#zlecenia-marketing`, nie w Biginie.

**Fizyczne paczki dla partnera** (próbki, ulotki, katalogi, standy do wysłania) zleca się na Slacku, kanał `#zlecenia-wysylki` (@Pakowanie), nie w Biginie. Potok **Wysyłki Marketingowe jest martwy**: 2 rekordy, oba z 18.01.2026, bez dalszych zmian.

Etapy `Zaplanowano paczkę marketing` i `Dostarczono paczkę marketing` w potoku Akcji **istnieją w konfiguracji, ale nie są używane** (0 rekordów). Nie interpretuj ich jako kolejki zleceń dla marketingu i nie przesuwaj na nie rekordów. `Dostarczono paczkę marketing` występuje też w potoku Wysyłki Marketingowe.

## Dwa rodzaje rekordów akcji

| | Z generatora | Zakładane ręcznie |
|---|---|---|
| `Deal_Name` | `PRP-0038 · <działanie> · 2026-09` | dowolny: „AKCJA PARASOLOWA Festiwal…", „SAMPLE DO paczek", „Gazetka 10.2026…" |
| `propo_id`, `id_akcji`, `link_propozycji` | wypełnione | puste |
| `Okoliczno` | **forma** z katalogu (lista niżej) | często **okazja** (lista niżej) |
| udział w 30 ostatnio zmienianych akcjach w toku (10.10.2026) | 17 | 13 |

Akcje sprzed generatora (przed 08.2026) nie mają `propo_id` ani `id_akcji`. `Płatne działania marketingowe – <miesiąc>` to zbiorcze budżety, nie pojedyncze działania.

## Pola akcji

- `propo_id` (`PRP-0038`) — wiąże działania jednej propozycji, ta sama wartość w nazwie PDF i w rejestrze `log_propozycji` arkusza generatora.
- `id_akcji` (`EC.02`, `WP.08`, `HD.01`, `PS.52`…) — kod z katalogu działań (`modele-wszystko/b2b/katalog_dzialan/`).
- `typ_akcji` = **cel**: `cena` · `edukacja` · `widocznosc` · `inne`; w starszych/ręcznych rekordach też `promocja na markę`, `promocja na produkty`.
- `Okoliczno` — jedno pole, dwie konwencje:
  - **forma** (generator): `mechanika sprzedazy`, `powierzchnia online`, `content i social`, `komunikacja do bazy`, `ekspozycja w punkcie`, `probki i sampling`, `szkolenie i wiedza`, `event i obecnosc`, `motywacja personelu`;
  - **okazja** (ręczne): `Okazja u klienta`, `Sezonowa`, `Święta`, `Black week`, `Lato / wakacje`, `Inne`.
  Przy przekrojach „wg formy" licz tylko wartości z pierwszej listy i powiedz, ile rekordów ma okazję albo puste pole.
- `Spos_b_rozliczenia` (multiselect) — jak akcja się rozlicza: w praktyce `Fv marketingowa` albo `n/d`.
- `Data_akcji`, `Data_zako_czenia_akcji`, `Warto_akcji_netto`, `Ca_kowity_koszt_akcji`, `Warto_sprzeda_y_netto` (wypełniane rzadko, ~12%).
- `Owner` = handlowiec, który zaproponował (od 06.08.2026; starsze rekordy mają Daniela). `Description` = opis + komentarz handlowca + link do PDF.
- Na etapie propozycji **daty i finanse są celowo puste**; po akceptacji uzupełniane niekonsekwentnie. `Ca_kowity_koszt_akcji = 0` często znaczy „nie wpisano", a nie „za darmo". Pusty budżet na `Warto zaproponować` to nie błąd.
- Akcje w realizacji często nie mają `Data_akcji` — do „co się dzieje teraz" używaj etapu i `Modified_Time`.

## Zapytania

**Akcje w toku (zaakceptowane i realizowane):**
```sql
select Deal_Name, Account_Name.Account_Name, Stage, propo_id, id_akcji, Okoliczno, Data_akcji, Owner
from Pipelines
where Stage in ('Zaplanowano z klientem','W realizacji')
order by Modified_Time desc limit 100
```

**Działania jednej propozycji:**
```sql
select Deal_Name, Stage, id_akcji, typ_akcji, Okoliczno, Data_akcji, Warto_akcji_netto
from Pipelines where propo_id = 'PRP-0038' limit 50
```

**Lejek propozycji** (ile przyjęte vs odrzucone): pobierz `Stage, propo_id` z `propo_id is not null` i policz sam. Koszt i liczbę akcji w czasie licz w Zoho Analytics (skill `analityka-b2b-zoho`).

## Standy i kody rabatowe partnera

- **standy** (osobny potok): `Zaproponowano stand` → `Wstawiono stand` → `Zakończono stand`; pola `Rodzaj_standy`, `Termin_wstawienia`, `Termin_odbioru`. Wysyłka standu = wiadomość na `#zlecenia-wysylki`.
- **Kod rabatowy** (osobny potok): `Kod rabatowy zaproponowany` / `aktywny` / `wygasł`; pola `warto_kodu_lub_kwota`, `data_wyga_ni_cia_kodu`. To kody dla klientów partnera. Kody do sklepu opcjanatura.pl (influ, kampanie) to inna ścieżka: apka „Poproś o kupon” na Slacku.
- Rozliczenie kodu z partnerem (np. „kod MOC 15”) ląduje w potoku **Rozliczenia retro** — patrz `rozliczenia-retro.md`.

## Zapis

Tylko na wyraźną prośbę. Przy tworzeniu akcji `Sub_Pipeline` = `Akcje Promo i Marketing Standardowy` wymaga też `Pipeline: {"id": "427926000000654205"}` (inaczej `MAPPING_MISMATCH`). Wartości techniczne etapów: `Zaproponowano Klientowi`→`Zaproponowano`, `Zaplanowano z klientem`→`Zaplanowano`. Propozycje z PDF-em zakłada generator, nie agent: nie twórz rekordów `PRP-…` ręcznie.
