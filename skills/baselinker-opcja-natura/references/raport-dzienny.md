# Pomoc przy raporcie hubu: arkusz „E-commerce TEAM raportowanie”

Arkusz: https://docs.google.com/spreadsheets/d/1TX0-OlKj0mDLJvcNWs1CRAru0JhOsXqemzl3SsY074s/edit (zakładka na miesiąc `RRRR-MM`, wiersz na dzień roboczy, nagłówki w wierszu 7). Zespół prowadzi go sam, a liczby muszą być dokładne: wpisujesz tylko to, co wynika z danych i co osoba potwierdziła. Agent pomaga, gdy ktoś poprosi: policzy coś z BL, poda wartość zamówienia, ułoży komentarz, wpisze to, co osoba potwierdzi. Nie prowadzi raportu za zespół i nie szuka błędów na własną rękę: duble, błędne paczki i spóźnienia zespół zna z maili i rozmów z klientkami.

## Kolumny i w czym agent może pomóc

| Kol. | Nagłówek | Pomoc agenta |
| :-- | :-- | :-- |
| A–C | data, tydzień, dzień | formuły, nie ruszasz |
| D | raport fiskalny kwota brutto | brak: to raport dobowy z drukarki fiskalnej; z API BL tej sumy nie policzysz |
| E | il. spakowanych paczek baselinker | na prośbę: liczba zamówień, które danego dnia (czas polski) weszły w `10476` Spakowano - do wysyłki, bez `10475` odbiorów osobistych. Najszybciej: `getJournalList` z `logs_types: [18]` (`zapytania.md`, sekcja 7; jedno wywołanie to ok. doba zdarzeń, dalej stronicuj od ostatniego `log_id` + 1), policz zdarzenia z `object_id` 10476 w danym dniu (unikalne `order_id`). Historia sięga 3 dni wstecz; starszy dzień: `ask_agent` „ile zamówień weszło <dnia> w status 10476” |
| F | inwentura: niezgodności | brak: inwentura w aplikacji magazynowej |
| G, H, I | nr id dubel / paczka źle spakowana / niewysłane na czas | osoba podaje zamówienie (często z maila klientki: numer sklepu `ON-…`, e-mail, nazwisko); agent znajduje ID BL (`zapytania.md`, sekcje 1 i 3) i ewentualną dosyłkę |
| J | wartość zam. netto | z pozycji zamówienia: suma `price_brutto × quantity / (1 + tax_rate/100)`, bez dostawy |
| K | komentarz | szkic w formacie zespołu: `<co się stało>; <jak naprawiono> zam. <ID BL dosyłki> z <dd.mm>`, np. `brak 1 szt. Naturalnej Mega Piany; dosyłka zam. 354276251 z 28.10`. Bez danych klientki |
| M–N, wiersze od 34 | narastająco, sumy | formuły, nie ruszasz |

Wpisy w arkuszu: tylko w puste komórki, tylko to, co osoba zatwierdziła, w konkretne komórki (bez dopisywania wierszy, bo arkusz ma formuły tablicowe). Zespół wpisuje jeden błąd na dzień; przy zajętym dniu bierze następny wolny i dopisuje w K `(wpis na dd.mm, bo dd.mm zajęty)`. Brak narzędzia z zapisem do Sheets → podaj wartości z adresami komórek do wklejenia.

## Ile paczek dla kuriera (na przyjazd kuriera)

Zespół przed wydaniem liczy, ile paczek czeka na danego kuriera, żeby porównać z tym, co kurier zabiera. Liczy się **stan w chwili przyjazdu**, więc agent liczy na prośbę, w tym momencie:

1. Zamówienia czekające na odbiór: status `10455` Wydrukowano etykietę (`getOrders` z `status_id`, albo `ask_agent` o listę order_id w tym statusie).
2. Paczki tych zamówień: `getOrderPackages` (`courier_code`, `account_id`, `courier_other_name`; jedno zamówienie może mieć kilka paczek, liczysz paczki). Weź paczki niezwrotne z kodem 0 lub 1 (jeszcze nienadane).
3. Wynik dla pytanego kuriera: liczba paczek i numery zamówień. Kurierzy i konta: `konto.md`.

Po wydaniu, gdy ktoś chce sprawdzić zgodność: `getCourierPackagesStatusHistory` z listą `package_ids` z punktu 2. Paczka zabrana ma w historii kod inny niż 0, 1 i 10, ale przewoźnik aktualizuje go z opóźnieniem, więc „tylko 1” tuż po odbiorze nie jest jeszcze rozbieżnością. Paczka nieobecna w odpowiedzi = usunięta (np. etykieta wygenerowana ponownie; nowa paczka ma nowe `package_id`).

Podziału paczek na kurierów `ask_agent` nie liczy pełnie: licz krokami.
