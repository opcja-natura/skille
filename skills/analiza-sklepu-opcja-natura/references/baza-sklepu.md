# Baza sklepu opcjanatura.pl — mapa, pułapki, przełomy

> Dla agenta, nie cytuj osobie nietechnicznej. Stan 25.11.2026.

## Dostęp

- Supabase, projekt **`nmgxsrkxbbkutqucedmm`** (sklep, produkcja), schemat **`prod`** (+ `marketing` = dane influencerów i mapa kodów, `ads` = wydatki reklamowe). Schemat `public` jest pusty — to nie błąd dostępu.
- **Tylko SELECT.** Żadnych zmian w bazie.
- `order` to słowo kluczowe SQL → zawsze `prod."order"`.

## Tabele

| Tabela | Co to | Klucze i uwagi |
|---|---|---|
| `prod."order"` | zamówienia sklepu www (od 09.2022, ok. 110 tys.) | klucz w relacjach to **`order_id`** (nie `id`); `email` zawsze jest, `account_id` tylko przy zakupie z konta (ok. 1/3); kwoty: `grand_total` (brutto z dostawą), `tax_total`, `shipment_total` (brutto dostawy), `discount_total`, `loyalty_points_used`; `status` (enum) |
| `prod.order_item` | pozycje zamówień | `order_order_id` → `order.order_id`; `product_id`, `name`, `quantity`, `price_total` |
| `prod.product` | słownik produktów sklepu (ceny netto, koszt) | `product_id`; `cost_price_net` (do COGS), `price_net` |
| `prod.account` | konta klientek | `id`, `email` (unikalny); `is_loyalty_member`, `loyalty_points` (saldo), `loyalty_membership_status` (BRONZE/SILVER/GOLD — prawie wszyscy BRONZE), `email_optin` (zgoda na newsletter); ok. 5,7 tys. kont ma fałszywą datę założenia 1970-01-01 |
| `prod.loyalty_points_item` | historia punktów (od 03.06.2025) | `account_id`; `item_type` (ORDER, ENROLLMENT = zapis, RECOMMENDATION, REVIEW), `status` (CONFIRMED, BLOCKED = czeka na doręczenie, DELETED = **wygasłe**), `order_id` (przy ORDER), `date_updated` |
| `prod.coupon` / `prod.coupon_redemption` | kupony i ich użycia (od 03.2024) | `coupon_redemption.order_id` → `order.order_id`; `code` porównuj po `upper(trim())`; `coupon.description` z apki Slack „Kupony” zaczyna się od `[Rodzaj] @nick` |
| `prod.discount_item` | rabaty rozbite per zamówienie | `order_order_id`; `source_type` (COUPON, PROMOTION, LOYALTY_POINTS, GIFT_CARD), `source_name`, `amount` |
| `marketing.kody_mapa` (widok) | **kod → rodzaj i influencerka**, z edycjami kodu | `kod`, `edycja_od`, `edycja_do`, `influencer_id`, `rodzaj` (influencer, wspolpraca_reklamowa, kampania_wlasna, obsluga_klienta, lojalnosc, b2b, wewnetrzny, inne, nieprzypisany) |
| `marketing.influencers`, `marketing.coupons`, `marketing.shipments`, `marketing.shipment_items`, `marketing.publications`, `marketing.monthly_plan` | kopia arkusza INFLU app (codziennie rano) | wszystkie kolumny tekstowe; `shipments.packed_at` bywa pusty (wtedy data zlecenia pakowania lub „kiedy wysłać”) |
| `prod.email_campaign` | kampanie mailowe | `campaign_id`, `name`, `event_type` (B2C/B2B), `"isTestCampaign"`; **brak daty i statusu wysyłki** (patrz słownik §6) |
| `prod.email_campaign_tracking_event` | otwarcia i kliknięcia (od 02.2026) | `campaign_id`, `email`, `event_type` (OPEN/CLICK), `link` (wypis = link `/unsubscribe`), `date_updated` |
| `ads.spend_daily` | wydatek reklamowy dziennie (od 08.2024) | `dzien`, `platforma` (Meta, Google), `koszt` (netto), `roas_platformy`; Google spływa z opóźnieniem 1–2 dni |
| `prod.cart` / `cart_item` | koszyki (od 28.01.2026) | nie mierz po nich „prób użycia kodu” |
| `prod.baselinker_order*` | **B2B** | nie wchodzi do sklepu www |

## Pułapki

| Pułapka | Co robić |
|---|---|
| dwie ery statusów zamówień (do 03.2024 DELIVERED, potem PAID/CANCELLED) | zawsze `status IN ('PAID','DELIVERED')` |
| znaczniki czasu w UTC | do doby/miesiąca polskiego: `(kolumna at time zone 'UTC' at time zone 'Europe/Warsaw')` |
| `coupon_redemption.value_redeemed` = 0 dla kuponów procentowych na produkt | kwotę rabatu bierz z `discount_item` (`source_type='COUPON'`) |
| kod nadany dwóm osobom albo dwa wiersze kodu w arkuszu | zawsze przez `marketing.kody_mapa` z warunkiem edycji; nigdy bezpośrednio `marketing.coupons` |
| próg darmowej dostawy (150 zł brutto) liczy się od kwoty **przed** rabatem | koszyk z kodem może mieć darmową dostawę poniżej 150 zł |
| członkostwo w programie bez historii | „członkini” = stan dzisiejszy; dla dawnych okresów zawyża udział programu |
| zapisy do programu z wygasłymi punktami mają status DELETED z datą wygaśnięcia | data zapisu = `date_updated − 1 rok` (dla DELETED od 06.2026) |
| ok. 100 członkiń bez wpisu ENROLLMENT | opisz osobno, nie wliczaj do „zapisów w miesiącu” |
| wysyłki testowe newslettera (pojedyncze otwarcia przed wysyłką) | data wysyłki = pierwszy dzień z ≥ 20 otwarciami |
| baza newslettera w bazie sklepu jest niepełna | `email_optin` to tylko zapisani **z kontem**; ok. połowa otwierających nie ma konta (lista poza bazą sklepu) → zasięg % jest zawyżony |
| zapytania z `lower(email)` w podzapytaniu skorelowanym są bardzo wolne | licz pierwsze zamówienie raz (CTE z `min(date_created)` albo `row_number()`), potem łącz |

## Przełomy w danych (nie porównuj przez nie bez komentarza)

- **29.03.2024** — migracja platformy sklepu (zmiana statusów, start kuponów w bazie).
- **03.06.2025** — start programu lojalnościowego.
- **06.2026** — początek fali wygasania punktów (rok po starcie programu).
- **02.11.2026** — nowa strona sklepu: punkty dużo widoczniejsze (zakupy z punktami ×2–3), inna kasa; od tego dnia inna skala wartości w Google Ads.
- **04.11.2026** — kody rabatowe zakładane przez apkę Slack „Kupony” (opis kuponu ma rodzaj i @nick).
- **Black Week** (ok. 22–30.11) i **Walentynki** (kod WALENTYNKI) — porównuj z tymi samymi dniami tygodnia rok wcześniej, nie z poprzednim tygodniem.

## Czego w bazie nie ma

Realnego kosztu kuriera (jest tylko cennik), opłat dla influencerek, kosztów pracy, liczby odbiorców wysyłki newslettera, historii członkostwa i zgód. Przy takich pytaniach licz scenariusze i powiedz, czego brakuje.
