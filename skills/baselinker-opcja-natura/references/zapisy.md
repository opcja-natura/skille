# Zapisy przez `run_api_call_all`

Wolno wykonać **tylko trzy rodzaje zapisu** poniżej. Każdy dotyczy jednego zamówienia i wymaga zgody osoby, która o niego prosi. Wszystko inne robi człowiek w panelu BL albo właściciel systemów.

## Procedura każdego zapisu

1. **Odczytaj stan:** `getOrders` z `order_id` i `include_custom_extra_fields: true`.
2. **Pokaż i czekaj na „tak”:** numer zamówienia, metoda, dokładne `parameters`, wartość przed i po.
3. **Jedna zgoda = jedno wywołanie.** Kilka zamówień to kilka zgód. Ta sama zmiana na więcej niż 5 zamówieniach → przekaż właścicielowi systemów.
4. **Wykonaj i sprawdź:** `status` = `SUCCESS`, potem ponowny odczyt i porównanie.
5. **Błąd:** nie ponawiaj w ciemno, pokaż `error_message` i zapytaj.

## 1. Dopisanie uwagi do zamówienia

`admin_comments` nadpisuje się w całości i mieści **200 znaków**.

1. Weź obecne `admin_comments`.
2. Dopisz na końcu ` | <SKRÓT> <dd.mm>: <treść>`. Skrót = osoba, która prosi (tabela ról w `SKILL.md`).
3. Policz znaki całości. Ponad 200 → nie skracaj cudzych uwag; zaproponuj krótszą treść albo wpis w panelu.

```json
{"method": "setOrderFields", "parameters": {"order_id": 359000001, "admin_comments": "<dotychczasowa treść> | KS 26.11: klientka prosi o dosyłkę w poniedziałek"}}
```

## 2. Pole własne zamówienia

Dozwolone tylko te pola (wartości dokładnie jak w `konto.md`):

| ID | Pole | Przykład |
| :-- | :-- | :-- |
| `77977` | Powód wysyłki za 0pln | `dosylka_do_zamowienia` |
| `77056` | bez paragonu | `nie wystawiaj paragonu` |
| `77366` | FV imienna | `wystaw fv imienną` |
| `78572` | ustaw wysyłkę | `Kurier InPost` |

Wysyłaj tylko jedno zmieniane pole; `""` czyści pole. Pola `77977` i `77056` ustawiasz **przed** spakowaniem: od nich zależy, jak magazyn firmy zapisze rozchód.

```json
{"method": "setOrderFields", "parameters": {"order_id": 359000001, "custom_extra_fields": {"77977": "dosylka_do_zamowienia"}}}
```

**Nigdy:** `77969`, `77970` (ślady webhooków magazynu; ręczne „TAK” ukrywa brak rozchodu), `77836`, `77837`, `78687`, `77620`, `extra_field_1`, `extra_field_2` (przychodzą ze sklepu i arkusza B2B, zasilają Bigin i magazyn), adresy, kwoty, płatności, pozycje.

## 3. Zmiana statusu jednego zamówienia

Zmiana statusu uruchamia automaty BL (rozchód, dokumenty, wiadomości do klientki, Bigin). API nie pokazuje, które. Dlatego dozwolone są **tylko** te przejścia:

| Z | Na | Warunek |
| :-- | :-- | :-- |
| `10454`, `9890`, `341571`, `342066`, `329445`, `356786`, `348458`, `350558`, `343182`, `348497` | `313961` on hold | osoba podała powód; dopisz go w uwagach (zapis 1) |
| `313961` on hold | ta sama kolejka, z której zamówienie przyszło (lista wyżej) | `77969` puste (rozchodu nie było) |

**Zamówień B2B (źródło `39943`) nie przestawiasz wcale:** każda zmiana statusu B2B przestawia zamówienie w Biginie, a przejście `9886` ↔ `313961` po założeniu rekordu kończy się błędem synchronizacji i rozjazdem BL z Biginem (`przeplywy.md`, sekcja 2a). Statusy B2B zmienia handlowiec albo lider hubu w panelu.

Każdy inny status docelowy jest zakazany, w szczególności `10476`, `10475` (Spakowano: uruchamia rozchód), `10455`, `9888`, `294156`, `17910`, `10468` (wiadomości do klientki, Bigin, sklep), `9889` Anulowane, `294244` Rozliczenie komisu oraz wszystkie statusy zwrotów (`284070`, `320111`, `320503`, `320112`, `324032`, `325481`): ani **na** nie, ani **z** nich (także powrót zwrotu do „do wysyłki”). Te przejścia robi człowiek w panelu według procedury hubu.

Przed zapisem powiedz: „Zmiana na <status> może uruchomić automat BL. Czy na pewno?”.

```json
{"method": "setOrderStatus", "parameters": {"order_id": 359000001, "status_id": 313961}}
```

## Czego nie robisz nigdy (także na prośbę)

Faktury, paragony, korekty; paczki i odbiory kurierskie (realne zlecenie i koszt); płatności i oznaczanie zwrotu pieniędzy; nowe zamówienia, kopie, łączenie, dzielenie; pozycje zamówienia; usuwanie czegokolwiek; uruchamianie automatycznych akcji (`run*MacroTrigger`); katalog produktów, stany i ceny; dokumenty magazynowe i inwentaryzacje; ustawienia konta.

Poproś wtedy o zrobienie tego w panelu albo przekaż sprawę właścicielowi systemów.
