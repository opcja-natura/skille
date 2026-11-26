# Szukanie zamówień i gotowe wywołania

1. Numery zamówień
2. `ask_agent` czy `getOrders`
3. Jedno zamówienie
4. Co czytać w odpowiedzi
5. Paczka i tracking
6. Kolejki i zaległości
7. Historia zamówienia
8. Stany i ceny kosmetyków

Wywołania idą przez `run_api_call_readonly` jako `{"method": "...", "parameters": {...}}`. ID: `konto.md`. Numery w przykładach są fikcyjne.

## 1. Numery zamówień

**Sklep opcjanatura.pl:** jedno zamówienie ma trzy numery.

| Numer | Wygląd | Gdzie w BL |
| :-- | :-- | :-- |
| ID BL | `359000001` | `order_id`; link w panelu `panel-d.baselinker.com/orders.php#order:<ID>` |
| numer sklepu (jest w mailach do klientki) | `ON-123456` | `user_login` („Klient (login)”) |
| UUID sklepu (ten sam co ID płatności Przelewy24) | `a1b2c3d4-…` | pole własne `77620` „transactionId” |

`shop_order_id` i `external_order_id` są w zamówieniach sklepu puste.

**B2B:**

| Numer | Wygląd | Gdzie |
| :-- | :-- | :-- |
| ID BL | `359000002` | `order_id`; w Biginie pole `baselinkerOrderId` na zamówieniu i fakturze |
| numer B2B | `ON-B2B__1234` (w danych dwa podkreślenia) | `extra_field_2`, czasem z dopiskiem na fakturę po spacji; w Biginie początek nazwy zamówienia |
| klient | ID rekordu Bigin | pole własne `77836` |

**Marketplace'y:** numer platformy w `external_order_id`, login kupującego w `user_login`.

## 2. `ask_agent` czy `getOrders`

Jedno zamówienie z `getOrders` to 3 do 15 tys. znaków z adresem i pozycjami. Dziesięć zamówień B2B zapycha rozmowę.

- **Liczba, lista numerów, zestawienie** → `ask_agent`, z prośbą o „same liczby i order_id, bez danych klientów”. Agent Base liczy po swojej stronie, poprawnie dla pytań o jeden status albo jeden dzień. Czasem przegląda tylko pierwsze 100 rekordów i pisze wtedy „to nie jest pełny przegląd”; taki wynik dziel (krótszy okres, jeden status). Zbiorczych podziałów (np. paczki dnia według kurierów) nie liczy pełnie: licz krokami. Przy decyzji zależnej od liczby sprawdź jeden, dwa numery sam.
- **Szczegóły jednego zamówienia** → `getOrders` z `order_id`.
- `ask_agent`: nowy temat = bez `conversation_id`; maks. 2 pytania naraz i 5 na minutę. Nie widzi konfiguracji konta (automatycznych akcji, szablonów, zapisanych filtrów) i na takie pytania odsyła do panelu.

## 3. Jedno zamówienie

| Masz | Wywołanie |
| :-- | :-- |
| ID BL | `{"method": "getOrders", "parameters": {"order_id": 359000001, "include_custom_extra_fields": true}}` |
| numer sklepu `ON-…` | `ask_agent`: „order_id zamówienia ze źródła personal 39697 z user_login ON-123456” (`filter_shop_order_id` nic nie znajdzie) |
| e-mail / telefon klientki | `getOrdersByEmail` (`email`) / `getOrdersByPhone` (`phone`) |
| numer z marketplace'u | `getOrders` z `filter_external_order_id` |
| numer `ON-B2B__…` | Bigin: zamówienie o tej nazwie → `baselinkerOrderId`; bez Bigina: `ask_agent` „order_id zamówienia z polem dodatkowym 2 ON-B2B__1234”; potem `getOrders` z `order_id` |

## 4. Co czytać w odpowiedzi `getOrders`

| Pole | Znaczenie |
| :-- | :-- |
| `order_status_id` | status (`konto.md`) |
| `date_add`, `date_confirmed`, `date_in_status` | złożenie, potwierdzenie, od kiedy w obecnym statusie |
| `order_source`, `order_source_id` | kanał |
| `delivery_method`, `delivery_package_module`, `delivery_package_nr` | sposób wysyłki, kurier, numer ostatniego listu (pusty = brak listu w BL) |
| `payment_done`, `payment_method_cod` | zapłacona kwota, pobranie |
| `admin_comments` | uwagi zespołu i handlowca (skrót osoby na początku), maks. 200 znaków |
| `extra_field_1`, `extra_field_2`, `custom_extra_fields` | zależnie od kanału (`konto.md`) |
| `pick_state`, `pack_state` | skompletowano / spakowano (1 = tak) |
| `products[]` | `name`, `sku`, `ean`, `quantity`, `price_brutto`, `tax_rate`, `product_id` |

Wartość netto pozycji: `price_brutto × quantity / (1 + tax_rate/100)`. W B2B pozycja za 1,23 zł brutto to tester albo gratis.

## 5. Paczka i tracking

`{"method": "getOrderPackages", "parameters": {"order_id": 359000001}}` zwraca aktualne paczki zamówienia: `package_id`, `courier_code`, `account_id`, `courier_package_nr`, `tracking_status`, `tracking_status_date` (data **bieżącego** statusu), `tracking_url`, `is_return`. Paczki usunięte (np. przy ponownym wygenerowaniu etykiety) nie wracają.

Historia ruchów wielu paczek naraz: `getCourierPackagesStatusHistory` z `package_ids` (lista). Datę nadania bierz stąd: pierwsza pozycja z kodem 2 (albo, gdy go brak, pierwsza z kodem innym niż 0, 1, 10).

| Kod | Znaczenie | Kod | Znaczenie |
| :-- | :-- | :-- | :-- |
| 0 | nieznany | 7 | awizo |
| 1 | etykieta utworzona | 8 | czeka w punkcie |
| 2 | nadana | 9 | zagubiona |
| 3 | niedoręczona | 10 | anulowana |
| 4 | w doręczeniu | 11 | w drodze |
| 5 | doręczona | 12 | wyjątek (błąd sortowni, reklamacja) |
| 6 | zwrot | 13 | przekazana za granicę |

Kody nie są uporządkowane. „Kurier zabrał paczkę” = w historii jest jakikolwiek kod poza 0, 1 i 10.

## 6. Kolejki i zaległości

Pytaj `ask_agent` o liczby i numery, np.:
- „Które zamówienia są w statusie 9888 (Wysłane) dłużej niż 2 pełne dni robocze? Same order_id i data wejścia w status.”
- „Ile zamówień czeka w statusach 10454, 342066, 356786, 348458, 329445? Same liczby.”
- „Ile zamówień weszło <dnia> w status 10476? Sama liczba.”

Samodzielnie: `getOrders` z `status_id` i `date_confirmed_from`; maks. 100 na stronę, kolejna od `date_confirmed` ostatniego + 1.

## 7. Historia zamówienia

`{"method": "getJournalList", "parameters": {"order_id": 359000001, "last_log_id": 1}}`: tylko ostatnie 3 dni. Bez `order_id`, z `logs_types` (lista), zwraca zdarzenia całego konta od `last_log_id`; stronicuj od ostatniego `log_id` + 1.

| `log_type` | Zdarzenie | `object_id` |
| :-- | :-- | :-- |
| 1 | utworzenie zamówienia | |
| 3 | płatność | |
| 7 / 8 | faktura / paragon | ID dokumentu |
| 9 / 10 | utworzenie / usunięcie paczki | ID paczki |
| 16 | edycja danych zamówienia (także przez automat) | |
| 18 | zmiana statusu | nowy status |
| 22 | zmiana statusu paczki | ID paczki |

Starsza historia, także automatycznych akcji z komunikatami błędów, jest tylko w panelu.

## 8. Stany i ceny kosmetyków

Produkt po nazwie albo EAN: `getInventoryProductsList` z `inventory_id: 28851` i `filter_name` / `filter_ean`. Stany i ceny: `getInventoryProductsStock` / `getInventoryProductsPrices` z `inventory_id` i `filter_id` (bez filtra zwracają cały katalog). Pełne dane (`getInventoryProductsData`) tylko dla 1 do 3 produktów, gdy ktoś pyta o treść karty w BL.

Stan magazynu BL to osobna ewidencja, nie stan firmy (`przeplywy.md`, sekcja 3). Cenę i opis dla klientki sprawdzaj w danych sklepu (`produkty-lookup`).
