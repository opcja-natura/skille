# Konto BL Opcji Natury: słowniki

Stan z odczytu przez MCP 26.11.2026. Gdy coś się nie zgadza, pobierz na nowo metodą podaną przy tabeli.

1. Statusy zamówień
2. Źródła zamówień
3. Pola zamówienia
4. Katalog i magazyn
5. Konta kurierskie

## 1. Statusy zamówień (`getOrderStatusList`)

Grupy są umowne (tak ułożone w panelu): kolejka wejściowa → w trakcie → zakończone → zwroty → problemy.

**Kolejki wejściowe (do zrobienia)**

| ID | Nazwa | Co tu trafia |
| :-- | :-- | :-- |
| `10454` | OpcjaNatura.pl - do wysyłki | sklep www, wysyłka |
| `9890` | OpcjaNatura.pl - odbiór | sklep www, odbiór osobisty |
| `9886` | B2B - wysyłka, odbiór | zamówienia B2B z arkusza handlowca (status główny konta) |
| `341571` | marketingowe - wysyłka, odbiór | wysyłki marketingowe (źródło „marketingowe”) |
| `342066` | Allegro - do wysłania |  |
| `329445` | Amazon - do wysyłki |  |
| `356786` | TikTok Shop |  |
| `348458` | TEMU - do wysłania |  |
| `350558` | InPost Fresh - do wysyłki |  |
| `343182` | drop\_\_wszystkoNaturalne | dropshipping Base Connect |
| `348497` | drop_Aromelia | dropshipping Base Connect (pisownia jak w BL; źródło nazywa się „drop_Aromalia”) |
| `313961` | on hold | wstrzymane, np. nieopłacona fv, ustalenia z klientem |
| `341284` | opcjanatura.pl - duplikaty | potencjalne duplikaty ze sklepu |

**W trakcie**

| ID | Nazwa |
| :-- | :-- |
| `10476` | Spakowano - do wysyłki |
| `10475` | Spakowano - odbiór osobisty |
| `10455` | Wydrukowano etykietę nadawczą |
| `9888` | Wysłane |

**Zakończone**

| ID | Nazwa | Uwagi |
| :-- | :-- | :-- |
| `17910` | Dostarczone |  |
| `10468` | Odebrane/dostarczone |  |
| `294156` | wysłane w komis | towar wysłany do partnera na komis, bez faktury |
| `294244` | Rozliczenie komisu | rozliczenie sprzedanego towaru z komisu, faktura ręczna |
| `338916` | Amazon AFN | realizowane przez magazyn Amazona |

**Zwroty**

| ID | Nazwa | Znaczenie |
| :-- | :-- | :-- |
| `284070` | zwrot - zarej. u kuriera | paczka wraca, jeszcze jej nie ma u nas |
| `320111` | zwrot - wysłany @ | paczka u nas, wysłano mail z propozycją ponownej wysyłki |
| `320503` | zwrot - czekamy na wplatę | klientka zadeklarowała dopłatę |
| `320112` | zwrot - środki do zwrotu | do rozliczenia; nie zawsze jest co oddać (np. nieopłacone pobranie) |
| `324032` | zwrot - wypakowano | wypakowany; sam status nie potwierdza zwrotu pieniędzy |
| `325481` | zwroty - archiwum | zamknięte |

**Problemy i pozostałe**

| ID | Nazwa |
| :-- | :-- |
| `9889` | Anulowane |
| `284310` | reklamowane |
| `355182` | Allegro - nie opłacone |
| `324022` | DlaParagonow (techniczny) |
| `325371` | dla paragonów archive (techniczny) |

Moduł Zwroty BL (`getOrderReturns`) nie jest używany. Zwroty prowadzimy statusami zamówienia z tabeli wyżej.

## 2. Źródła zamówień (`getOrderSources`)

W `getOrders` filtruj parą `filter_order_source` + `filter_order_source_id`.

| Kanał | `filter_order_source` | `filter_order_source_id` |
| :-- | :-- | :-- |
| sklep opcjanatura.pl | `personal` | `39697` |
| B2B | `personal` | `39943` |
| marketingowe | `personal` | `40194` |
| osobiście/telefon | `personal` | `0` |
| Allegro (konto Opcja-Natura) | `allegro` | `40018` |
| Amazon | `amazon` | `2802` |
| TikTok Shop | `tiktokeu` | `46565` |
| Temu PL | `temupl` | `43024` |
| Kaufland | `kauflandpl` | `41597` |
| Ceneo | `ceneo` | `36886` |
| Base Connect „wszystko naturalne” | `blconnect` | `5157` |
| Base Connect drop_Aromalia | `blconnect` | `6677` |

Zamówienia z marketplace'ów filtruj po źródłach integracji z tabeli, nie po podobnie nazwanych źródłach `personal`.

## 3. Pola zamówienia

Pola standardowe (zawsze w odpowiedzi `getOrders`):

| Pole API | W panelu | U nas |
| :-- | :-- | :-- |
| `extra_field_1` | Pole dodatkowe 1 | sklep: „Store, newsletter: true/false, orders: N”; B2B: typ transakcji po ludzku („Drogeria sprzedaż”, „Wysyłka w komis”, „Rozliczenie Komisu”) |
| `extra_field_2` | Pole dodatkowe 2 | sklep: kod kuponu albo „Brak kuponow”; B2B: numer `ON-B2B__1234`, czasem z dopiskiem na fakturę; Amazon FBA: zawiera „AFN fulfillment” |
| `admin_comments` | uwagi sprzedawcy | sklep: bony, pakowanie na prezent; B2B: uwagi handlowca (`LUK`, `KAR`); dalej dopiski zespołu ze skrótem i datą; **maks. 200 znaków** |
| `user_comments` | uwagi kupującego | to, co napisała klientka |
| `user_login` | Klient (login) | sklep: numer zamówienia `ON-123456` (`shop_order_id` jest zawsze 0); B2B: nazwa klienta; marketplace: login kupującego |

Pola własne (`custom_extra_fields`, tylko z `include_custom_extra_fields: true`; słownik `getOrderExtraFields`):

| ID | Nazwa | Typ | Znaczenie |
| :-- | :-- | :-- | :-- |
| `77836` | b2b_client_id | tekst | ID klienta w Biginie |
| `77837` | b2b_transaction_type | tekst | `DIRECT_SALE` (drogeria sprzedaż), `SHIPMENT` (wysyłka w komis), `SALE` (rozliczenie komisu) |
| `78687` | b2b_paymentDue | tekst | termin płatności w dniach |
| `77969` | zrealizowano magazyn spZoo | checkbox `TAK` | ślad udanego rozchodu w magazynie firmy (`przeplywy.md`, sekcja 3) |
| `77970` | przywrócono na stan magazyn spZoo | checkbox `TAK` | ślad udanego przywrócenia stanów po zwrocie |
| `77977` | Powód wysyłki za 0pln | lista | `wysylka_marketingowa`, `wymiana_zniszczonego_produktu`, `dosylka_do_zamowienia` |
| `77056` | bez paragonu | checkbox | „nie wystawiaj paragonu” (np. ponowna wysyłka z produktami za 0 zł) |
| `77366` | FV imienna | checkbox | „wystaw fv imienną” |
| `78572` | ustaw wysyłkę | lista | InPost Paczkomat 24/7, Kurier InPost, Kurier FedEx, DHL paleta, Odbiór osobisty |
| `77620` | transactionId | tekst | sklep: UUID zamówienia w sklepie, ten sam co ID płatności Przelewy24 |
| `78698` | loyaltyMember | checkbox `TAK` | klientka w programie Moja Opcja Natura |

## 4. Katalog i magazyn (`getInventories`)

| ID | Nazwa | Języki |
| :-- | :-- | :-- |
| `28851` | Domyślny (główny, wszystkie kosmetyki) | pl |

Magazyn BL: `bl_37121` „Domyślny” (jedyny). To ewidencja BL, nie magazyn firmy.


## 5. Konta kurierskie (`getCourierAccounts` z `courier_code`)

| `courier_code` | Konto | ID |
| :-- | :-- | :-- |
| `paczkomaty` | InPost Paczkomaty | `57525` |
| `inpostkurier` | Kurier InPost | `27072` |
| `fedexpl` | FedEx | `58026` |
| `dhl` | DHL (palety) | `8386` |
| `dpd` | DPD | `69767` |
| `allegrokurier` | Allegro (wysyłka z Allegro) | `64316` |
| `blpaczka` | BL Paczka | `67565` |
| `ruch` | ORLEN Paczka | sprawdź `getCourierAccounts` |

`getCouriersList` zwraca kilkaset kurierów z całego świata. Nie wołaj go, korzystaj z tej tabeli.
