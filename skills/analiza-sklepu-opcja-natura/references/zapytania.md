# Sprawdzone zapytania

> Dla agenta. Każde zgodne ze słownikiem (`slownik-metryk.md`) i sprawdzone niezależnie 25.11.2026 (wyniki zgodne z dashboardami Metabase). Podmień daty `:od` / `:do` (doba polska, włącznie).

## Przychód, zamówienia, AOV w okresie

```sql
SELECT count(*) AS zamowienia,
       round(sum((grand_total - tax_total) - coalesce(shipment_total,0)/1.23)) AS przychod_netto,
       round(avg((grand_total - tax_total) - coalesce(shipment_total,0)/1.23), 2) AS aov_netto
FROM prod."order"
WHERE status IN ('PAID','DELIVERED')
  AND (date_created at time zone 'UTC' at time zone 'Europe/Warsaw')::date BETWEEN :od AND :do;
```

## Nowe i powracające klientki w okresie

```sql
WITH pierwsze AS (
  SELECT lower(email) AS em, min(date_created) AS f
  FROM prod."order" WHERE status IN ('PAID','DELIVERED') AND email IS NOT NULL GROUP BY 1)
SELECT (o.date_created = p.f) AS nowa, count(*) AS zamowienia,
       round(avg((o.grand_total - o.tax_total) - coalesce(o.shipment_total,0)/1.23)) AS koszyk_netto
FROM prod."order" o JOIN pierwsze p ON p.em = lower(o.email)
WHERE o.status IN ('PAID','DELIVERED')
  AND (o.date_created at time zone 'UTC' at time zone 'Europe/Warsaw')::date BETWEEN :od AND :do
GROUP BY 1;
```

## Powrót w 180 dni (kohorty pierwszego zakupu; szybka wersja)

```sql
WITH o AS (SELECT lower(email) AS em, date_created AS d,
                  row_number() OVER (PARTITION BY lower(email) ORDER BY date_created) AS rn
           FROM prod."order" WHERE status IN ('PAID','DELIVERED')),
p AS (SELECT em, max(d) FILTER (WHERE rn = 1) AS d1, max(d) FILTER (WHERE rn = 2) AS d2 FROM o WHERE rn <= 2 GROUP BY em)
SELECT date_trunc('month', (d1 at time zone 'UTC' at time zone 'Europe/Warsaw'))::date AS kohorta,
       round(100.0 * avg(((d2 IS NOT NULL) AND d2 <= d1 + interval '180 days')::int), 1) AS powrot_pct, count(*) AS klientki
FROM p WHERE d1 < date_trunc('month', now() - interval '180 days') GROUP BY 1 ORDER BY 1;
```

## Program lojalnościowy: powroty z zarobionymi punktami (główny wskaźnik)

```sql
WITH powrot AS (
  SELECT o.order_id FROM prod."order" o
  WHERE o.loyalty_points_used > 0 AND o.status IN ('PAID','DELIVERED') AND o.account_id IS NOT NULL
    AND EXISTS (SELECT 1 FROM prod.loyalty_points_item l JOIN prod."order" o2 ON o2.order_id = l.order_id
                WHERE l.item_type = 'ORDER' AND l.status IN ('CONFIRMED','DELETED') AND o2.status IN ('PAID','DELIVERED')
                  AND o2.account_id = o.account_id AND o2.date_created < o.date_created))
SELECT date_trunc('month', (o.date_created at time zone 'UTC' at time zone 'Europe/Warsaw'))::date AS miesiac,
       count(*) AS powroty,
       round(sum((o.grand_total - o.tax_total) - coalesce(o.shipment_total,0)/1.23)) AS przychod_netto
FROM prod."order" o WHERE o.order_id IN (SELECT order_id FROM powrot) GROUP BY 1 ORDER BY 1;
```
Kontrola: XI 2026 = 149 powrotów z 365 zakupów z punktami.

## Program: koszt, zobowiązanie, wygasanie

```sql
-- koszt (wartość wykorzystanych punktów) w okresie
SELECT round(sum(loyalty_points_used) * 0.05) AS koszt_zl FROM prod."order"
WHERE status IN ('PAID','DELIVERED') AND (date_created at time zone 'UTC' at time zone 'Europe/Warsaw')::date BETWEEN :od AND :do;

-- zobowiązanie
SELECT round(sum(loyalty_points) * 0.05) AS zobowiazanie_zl FROM prod.account WHERE is_loyalty_member;

-- wygaśnie w 30 dni (pełne doby PL od dziś)
WITH last_ord AS (SELECT account_id, max(date_created) AS d FROM prod."order" WHERE status IN ('PAID','DELIVERED') AND account_id IS NOT NULL GROUP BY 1),
last_ev AS (SELECT account_id, max(date_updated) AS d FROM prod.loyalty_points_item WHERE status = 'CONFIRMED' GROUP BY 1),
m AS (SELECT a.loyalty_points, greatest(coalesce(o.d,'1900-01-01'), coalesce(e.d,'1900-01-01')) + interval '12 months' AS wygasa
      FROM prod.account a LEFT JOIN last_ord o ON o.account_id = a.id LEFT JOIN last_ev e ON e.account_id = a.id
      WHERE a.is_loyalty_member AND a.loyalty_points > 0)
SELECT count(*) AS osoby, round(sum(loyalty_points) * 0.05, 2) AS zl FROM m
WHERE (wygasa at time zone 'UTC' at time zone 'Europe/Warsaw')::date
      BETWEEN (now() at time zone 'Europe/Warsaw')::date AND (now() at time zone 'Europe/Warsaw')::date + 30;
```

## Kody rabatowe: wynik per kod (influ i pozostałe)

```sql
SELECT c.kod, c.rodzaj, c.influencer_id, count(DISTINCT o.order_id) AS zamowienia,
       round(sum((o.grand_total - o.tax_total) - coalesce(o.shipment_total,0)/1.23)) AS przychod_netto
FROM prod.coupon_redemption cr
JOIN marketing.kody_mapa c ON c.kod = upper(trim(cr.code)) AND cr.date_created >= c.edycja_od AND cr.date_created < c.edycja_do
JOIN prod."order" o ON o.order_id = cr.order_id AND o.status IN ('PAID','DELIVERED')
WHERE c.rodzaj <> 'wewnetrzny'
  AND (o.date_created at time zone 'UTC' at time zone 'Europe/Warsaw')::date BETWEEN :od AND :do
GROUP BY 1, 2, 3 ORDER BY zamowienia DESC;
```
„Kody influ” = `c.rodzaj IN ('influencer','wspolpraca_reklamowa')`. Nazwa influencerki: `marketing.influencers` (`id`, `username`, `profile_name`).

## Newsletter: kampanie wysłane

```sql
WITH wys AS (
  SELECT campaign_id, min(d) AS wyslano FROM (
    SELECT campaign_id, (date_updated at time zone 'UTC' at time zone 'Europe/Warsaw')::date AS d, count(DISTINCT email) AS n
    FROM prod.email_campaign_tracking_event WHERE event_type = 'OPEN' GROUP BY 1, 2) t
  WHERE n >= 20 GROUP BY 1)
SELECT k.name, w.wyslano,
       count(DISTINCT t.email) FILTER (WHERE t.event_type = 'OPEN') AS otwarcia,
       count(DISTINCT t.email) FILTER (WHERE t.event_type = 'CLICK' AND t.link NOT ILIKE '%/unsubscribe%') AS klikniecia,
       count(DISTINCT t.email) FILTER (WHERE t.event_type = 'CLICK' AND t.link ILIKE '%/unsubscribe%') AS wypisy
FROM (SELECT DISTINCT ON (campaign_id) campaign_id, name FROM prod.email_campaign
      WHERE event_type = 'B2C' AND NOT "isTestCampaign" ORDER BY campaign_id, date_updated DESC) k
JOIN wys w USING (campaign_id)
JOIN prod.email_campaign_tracking_event t USING (campaign_id)
GROUP BY 1, 2 ORDER BY 2 DESC;
```

## Rozkład koszyków wobec progu darmowej dostawy (150 zł brutto)

```sql
SELECT (floor((grand_total - coalesce(shipment_total,0)) / 10) * 10)::int AS koszyk_od,
       count(*) AS zamowienia, round(100.0 * count(*) / sum(count(*)) OVER (), 1) AS pct
FROM prod."order"
WHERE status IN ('PAID','DELIVERED')
  AND (date_created at time zone 'UTC' at time zone 'Europe/Warsaw')::date BETWEEN :od AND :do
  AND grand_total - coalesce(shipment_total,0) < 300
GROUP BY 1 ORDER BY 1;
```
„Górka” tuż nad 150 zł (150–159 zł ok. 3× więcej zamówień niż 140–149 zł) = klientki dobijające do progu.
