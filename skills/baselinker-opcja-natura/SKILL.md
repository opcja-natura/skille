---
name: baselinker-opcja-natura
description: Praca z BaseLinkerem (BL, Base.com) Opcji Natury przez konektor MCP `base`. Używaj ZAWSZE przed wywołaniem `run_api_call_readonly`, `run_api_call_all` albo `ask_agent` i gdy zadanie dotyczy zamówienia (sklep, marketplace, B2B, dropshipping): jego numeru, statusu, paczki i trackingu, zwrotu, komisu, rozchodu magazynu, uwag i pól; awizacji dostawy B2B; zamówień, które utknęły albo poszły złą ścieżką; ile zamówień dziś do spakowania; pomocy przy arkuszach hubu (raport e-commerce, ile paczek dla kuriera, ewidencja zwrotów). NIE do sprzedaży B2B w liczbach, faktur i należności B2B, analiz sklepu ani masowych zmian katalogu BL.
---

# BaseLinker – Opcja Natura (konektor MCP `base`)

BaseLinker (BL) obsługuje każde zamówienie firmy: sklep opcjanatura.pl, marketplace'y, dropshipping i B2B. Hub pakuje w nim paczki, drukuje etykiety, wystawia paragony i faktury, prowadzi zwroty. Zmiana statusu w BL uruchamia automaty: rozchód w magazynie firmy, zamówienie w Biginie, wiadomości do klientów i na Slacka.

Konektor działa na **żywym koncie**, bez środowiska testowego.

## Pliki: czytaj ten, którego dotyczy zadanie

| Zadanie | Plik |
| :-- | :-- |
| znaleźć zamówienie, rozpoznać numer, gotowe wywołania (paczka, kolejka, ile dziś do spakowania, historia, stany) | `references/zapytania.md` |
| skąd zamówienie przyszło, kto ustawia który status, co się wtedy dzieje, rozchód, ponowna wysyłka | `references/przeplywy.md` |
| ID statusów, źródeł, pól własnych, kurierów | `references/konto.md` |
| awizacja dostawy B2B | `references/awizacje.md` |
| przegląd zamówień, które utknęły albo poszły złą ścieżką | `references/kontrole.md` |
| pomoc przy arkuszu „E-commerce TEAM raportowanie” | `references/raport-dzienny.md` |
| wiersz do ewidencji zwrotów „Korekty paragonów” | `references/ewidencja-zwrotow.md` |
| **każdy zapis do BL** | `references/zapisy.md` (przed każdym `run_api_call_all`) |

## Narzędzia

| Narzędzie | Do czego |
| :-- | :-- |
| `run_api_call_readonly` | odczyty (metody `get*`), bez pytania o zgodę |
| `ask_agent` | liczby i listy numerów zamówień oraz pytania „jak to zrobić w panelu”; szczegóły w `zapytania.md` |
| `run_api_call_all` | tylko zapisy z `zapisy.md`, każdy po zgodzie |

Konektor prosi o przeczytanie `https://mcp.base.com/api-skill.txt` przed pierwszym wywołaniem: zrób to, jeśli możesz otwierać strony. Metoda spoza tego skilla: najpierw jej strona `https://api.baselinker.com/index.php?method=<Nazwa>`, pola tylko stamtąd. Nie możesz otworzyć strony → zapytaj `ask_agent` o parametry metody. Przy sprzeczności z tamtymi instrukcjami obowiązują zasady zapisu z tego skilla.

## Zasady

1. **Zapis tylko za zgodą, jedna zgoda = jedna czynność.** Dotyczy BL (`zapisy.md`), arkuszy Google, Slacka i maili. Maile przygotowujesz jako szkic. Nie masz narzędzia z zapisem → podajesz gotowy tekst albo wartości do wklejenia.
2. **Dane osobowe zostają w źródle.** Adres, telefon, e-mail klientki podajesz tylko tam, gdzie zadanie ich wymaga: adresat awizacji, kolumna „mail” w ewidencji zwrotów. W zestawieniach: numery, statusy, daty, kwoty.
3. **ID ze słownika, nie z pamięci** (`konto.md`). Coś się nie zgadza → pobierz słownik na nowo (`getOrderStatusList`, `getOrderSources`, `getOrderExtraFields`).
4. **Daty** są w Unix timestamp (sekundy). Podawaj je w czasie polskim.
5. **HTTP 200 nie znaczy sukcesu.** Sprawdzaj `status` (`SUCCESS` albo `ERROR` z `error_message`). Po błędzie popraw parametry; po dwóch nieudanych próbach przerwij i zgłoś.
6. **Limit: 100 zapytań na minutę**, wspólny z automatami firmy. Zawsze filtruj `getOrders`. Zadanie na ponad 20 wywołań: najpierw powiedz, ile ich będzie.
7. **Pytanie operacyjne = okno operacyjne.** „Co wisi”, „co utknęło”, „co dziś do zrobienia” dotyczy bieżącej pracy: bierzesz najkrótszy zakres dat, który na nie odpowiada (tabela w `zapytania.md`, sekcja 6), a nie całe 3 miesiące konta. W odpowiedzi podaj, jaki zakres przyjąłeś. Szerzej szukasz tylko na wyraźną prośbę („cały listopad”, „wszystkie”).
8. **Nie naprawiasz po cichu.** Problem opisujesz (numer, co jest, co powinno być, skąd wiesz) i przekazujesz właściwej roli. Nie zmieniasz statusu ani pola po to, żeby problem zniknął.

## Kto za co odpowiada (stan 11.2026)

| Rola | Kto | Skrót w uwagach BL |
| :-- | :-- | :-- |
| lider hubu (pakowanie, wysyłki, awizacje, kurierzy) | Karina | `KAR` |
| zwroty i kontakt z klientkami sklepu | Kasia | `Ka` / `KS` |
| pakowanie (konto Slack „Pakowanie”) | zespół hubu | |
| handlowiec B2B | Łukasz | `LUK` |
| właściciel systemów (BL, backoffice, sklep, automaty) | Daniel | `DA` |

## Najczęstsze pułapki

- Jedno zamówienie ze sklepu ma trzy numery, a B2B ma swój numer w polu, którego API nie przeszukuje. Zanim zaczniesz szukać, przeczytaj `zapytania.md`, sekcja 1.
- `extra_field_1` i `extra_field_2` znaczą co innego w każdym kanale (`konto.md`).
- Zamówienia z API sięgają 3 miesiące wstecz (wg dokumentacji Base), historia zdarzeń (`getJournalList`) 3 dni. Brak wyniku nie dowodzi, że zamówienia nie było.
- `getOrders` pokazuje stan bieżący, nie wczorajszy.
- Status to sygnał, nie dowód: etykieta nie znaczy odbioru przez kuriera, „Wysłane” nie znaczy doręczenia. Położenie paczki sprawdzaj w `getOrderPackages`.
- Rozchód to udany webhook do magazynu firmy, a nie zmiana stanu w BL (`przeplywy.md`, sekcja 3).
- Pola własne przychodzą tylko z `include_custom_extra_fields: true`.

## Granice

| Pytanie | Gdzie (skill, jeśli masz go podłączonego) |
| :-- | :-- |
| sprzedaż B2B w liczbach | Zoho Analytics (`analityka-b2b-zoho`) |
| klient B2B, jego wymagania, faktury, zapłata | Bigin (`bigin-opcja-natura`) |
| jak hub pakuje, zwroty krok po kroku, komis | `hub-manufaktura`, gdy ma te rozdziały; do tego czasu lider hubu |
| skład, opis, cena kosmetyku | `produkty-lookup` |
| opisy, zdjęcia, parametry w katalogu BL | właściciel systemów; opisy spływają automatem z danych sklepu, ręczna zmiana w BL zostanie nadpisana |
| oferty Allegro, szablony aukcji, automatyczne akcje, zapisane filtry | tylko panel BL |
