# Awizacje dostaw B2B

Awizacja = wiadomość do klienta B2B (zwykle magazyn sieci, hurtowni, apteki), że dostawa jest w drodze: kiedy, jakim kurierem, z jakim listem przewozowym, ile paczek. Część klientów bez awizacji odmawia przyjęcia dostawy.

## Skąd wiadomo, że jest potrzebna

1. **Kanał Slack `#baselinker-bot`** (`C04FMTRQU7J`, prywatny). Przy każdym nowym zamówieniu B2B, które wymaga działania, Zapier (bot `zapier_b2b`) publikuje wiadomość „_wymagane działanie przy zamówieniu dla klienta_” z oznaczeniem konta „Pakowanie” i lidera hubu (DW). Zawiera:
   - nazwę klienta, link do Bigina (`…/companies/<id Accounts>`) i do zamówienia BL (`…orders.php#order:<order_id>`),
   - **SHORTLISTĘ**: 1. wymagany XML faktury TAK/NIE, 2. wymagana awizacja TAK/NIE, 3. e-mail awizacji, 4. istotne informacje (wymagania klienta, wolny tekst), 5. link do instrukcji klienta (Drive).
2. **Źródło shortlisty to karta klienta w Biginie** (`Accounts`): `Logistyka_wymagana_awizacja`, `Logistyka_e_mail_awizacji`, `Logistyka_istotne_informacje`, `Logistyka_url_wytycznych`, `faktura_wymagany_xml`. Gdy wiadomości na Slacku brak albo nie masz dostępu do kanału, czytaj te pola (skill `bigin-opcja-natura`). Nie masz ani Slacka, ani Bigina → poproś osobę o wymagania klienta. Klienta znajdziesz po polu `77836` zamówienia.
3. **Reakcje pod wiadomością:** ✅ = obsłużone, 👀 = ktoś widział, brak = nikt nie ruszył. Nie widzisz reakcji → pytaj osobę, czy awizacja już poszła.

### Kiedy wysłać

| Shortlista | Działanie |
| :-- | :-- |
| awizacja **TAK** | awizacja mailem na podany adres, w formie z „istotnych informacji” |
| awizacja **NIE**, ale „istotne informacje” proszą o list przewozowy, datę dostawy itp. | to samo: powiadomienie o wysyłce na podany e-mail (np. „nr listu przewozowego, data dostarczenia”) |
| awizacja NIE, informacje dotyczą faktury, kuriera, odbioru (np. „nie chcą FedEx”, „dopisek na fv”, „dowóz własny”) | nie awizacja: to uwaga dla pakowania lub handlowca; nie piszesz maila, ale przypominasz o tym |
| klient wymaga uzgodnienia terminu dostawy **przed** realizacją | to inny proces: termin dostawy uzgadnia się przed pakowaniem. Przygotuj szkic, ale oznacz, że czeka na potwierdzenie klienta, i powiedz o tym liderowi hubu |

Awizację wysyła się **po utworzeniu listu przewozowego** (status `10455`, `9888` albo `17910` / `10468`, paczka w `getOrderPackages`), najlepiej w dniu nadania. Bez numeru listu nie ma czego awizować: zgłoś, że czekasz na etykietę.

## Dane do awizacji (zbierz, nie zgaduj)

| Dana | Skąd |
| :-- | :-- |
| numer zamówienia klienta (jeśli klient go podał) | `admin_comments`, `user_comments`, dopisek w `extra_field_2` po numerze ON-B2B, mail klienta z zamówieniem |
| nasz numer | `extra_field_2` → `ON-B2B__…` |
| kurier i numer listu | `getOrderPackages`: `courier_code`, `courier_package_nr`, `tracking_url` |
| liczba paczek / kartonów / palet | liczba paczek niezwrotnych w `getOrderPackages`; palety = kurier `dhl` „DHL paleta”. Liczby kartonów w jednej paczce API nie zna: zapytaj pakowanie |
| przewidywana data dostawy | **nie wymyślaj.** Podaj datę nadania (pierwszy kod 2 w `getCourierPackagesStatusHistory`, a gdy go brak, pierwszy inny niż 0, 1, 10; przed nadaniem: planowany dzień odbioru od osoby). Termin dostawy: „przewidywany” tylko, gdy osoba go poda albo klient zgodził się na orientacyjny; inaczej „termin podamy po potwierdzeniu przez przewoźnika” |
| wartość dostawy (gdy klient prosi) | suma netto pozycji (`zapytania.md`, sekcja 4) albo kwota faktury z Bigina |
| faktura, WZ/MM (gdy klient prosi o załącznik) | faktura: BL (`getInvoices` po `order_id`, plik `getInvoiceFile`) albo wFirma przez Bigin `link_do_fv`. WZ: tylko z panelu BL (Wydruki i eksporty → Wydanie zewnętrzne). Agent nie dołącza plików sam: wskaż, co trzeba dołączyć |
| adres e-mail | shortlista / Bigin `Logistyka_e_mail_awizacji`; telefoniczna awizacja (np. „awizacja pod numerem telefonu”) → zadanie dla człowieka, nie mail |

## Treść maila

Temat: `Awizacja dostawy Opcja Natura, zamówienie <nr klienta lub ON-B2B__…>` albo w formacie wymaganym przez klienta (podany w jego wymaganiach).

Szkielet (dopasuj do „istotnych informacji” klienta, zachowując wszystkie pola, o które prosi):

```
Dzień dobry,

informujemy o wysyłce zamówienia <nr klienta / ON-B2B__…>.

Dostawca: Opcja Natura sp. z o.o.
Kurier: <nazwa przewoźnika>
Numer listu przewozowego: <nr> (<link śledzenia>)
Liczba paczek: <n>
Data nadania: <dd.mm.rrrr>
Przewidywany termin dostawy: <dd.mm.rrrr / do potwierdzenia>
[Wartość dostawy netto: <kwota> zł]  ← tylko gdy klient prosi
[W załączniku: faktura / WZ]          ← tylko gdy klient prosi i plik jest dołączony

W razie pytań prosimy o kontakt.

Pozdrawiamy
Zespół Opcja Natura
```

Zasady: bez myślników jako ozdobników zdań, bez marketingu, tylko fakty dostawy. Jeśli klient ma okno dostaw (np. „7:00–13:00 pn–pt”) albo nie przyjmuje danego kuriera, sprawdź, czy wybrany kurier i termin są z tym zgodne; niezgodność zgłoś przed wysłaniem.

## Wysłanie i odnotowanie

1. **Szkic, nie wysyłka.** Mail przygotowujesz jako szkic w skrzynce `sklep@opcjanatura.pl` (z niej idą awizacje). Wysyła człowiek po przejrzeniu. Nie masz dostępu do skrzynki → podaj temat, adresata i treść do wklejenia.
2. **Zanim napiszesz:** jeśli masz skrzynkę, sprawdź poprzednią korespondencję z tym adresem. Klient ma ustalony wzór → trzymaj się go.
3. **Po wysłaniu (potwierdzenie od człowieka):**
   - odpowiedź w wątku wiadomości na `#baselinker-bot`: „Awizacja wysłana <dd.mm hh:mm> do <adres>: <kurier> <nr listu>, <n> paczek” i reakcja ✅, po zgodzie; bez narzędzia Slacka podaj tekst do wklejenia;
   - dopisek do uwag zamówienia w BL przez `setOrderFields` wg `zapisy.md`: ` | <SKRÓT> <dd.mm>: awizacja wysłana` (skrót osoby, która wysłała).
4. **Odpowiedź klienta** (przyjęta / odrzucona / zmiana terminu) dopisz w tym samym wątku. Odrzucenie albo zmiana terminu → lider hubu i handlowiec.

## Przegląd zaległych awizacji

Gdy zadanie brzmi „sprawdź awizacje”:

1. Wiadomości z `#baselinker-bot` z ostatnich 14 dni, gdzie „Wymagana awizacja: TAK” albo e-mail awizacji jest wypełniony.
2. Dla każdej: status zamówienia w BL i paczki (`getOrderPackages`).
3. Zaległe = zamówienie z listem przewozowym (status `10455`, `9888`, `17910` albo `10468`) i bez ✅ ani odpowiedzi „awizacja wysłana” w wątku. Najpilniejsze: już `9888` Wysłane.
4. Wynik: lista `ON-B2B__… | klient | status | kurier i list | od kiedy czeka`, bez danych osobowych poza nazwą firmy.
