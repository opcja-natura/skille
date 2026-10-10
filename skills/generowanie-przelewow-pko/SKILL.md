---
name: generowanie-przelewow-pko
description: >
  Składanie pliku z listą przelewów do zaimportowania w iPKO (format Elixir-O, CSV)
  na podstawie tekstu, maila albo PDF-a z pozycjami do zapłaty. Używaj gdy Daniel mówi
  „zrób listę przelewów", „wygeneruj przelewy do banku", „plik do importu w iPKO",
  „przelewy z tego maila/pisma", „opłaty do urzędu", albo wkleja listę „kwota + numer
  konta + tytuł" i chce z tego plik dla banku. Skill zna format PKO, limity pól i
  pułapki (kodowanie, grosze, łamanie tytułu), oraz waliduje sumy kontrolne rachunków.
  NIE używaj do księgowania, analizy kosztów ani do przelewów podatkowych do US/ZUS
  (inny format — patrz „Poza zakresem").
---

# SKILL — Generowanie listy przelewów do iPKO

## Zasada nadrzędna: to są pieniądze

Nigdy nie generuj pliku po cichu i nigdy nie zgaduj brakujących danych.
**Zawsze pokaż Danielowi tabelę pozycji (kwota / odbiorca / rachunek / tytuł) i
poczekaj na potwierdzenie**, zanim zapiszesz CSV. Jeśli w źródle brakuje numeru
konta, kwoty albo tytułu — pytaj, nie uzupełniaj z głowy.

Plik jest tylko wsadem do importu: Daniel i tak zatwierdza przelewy w iPKO.
Twoja odpowiedzialność to **wierność źródłu** i **poprawność techniczna formatu**.

## Przebieg

1. **Weź wejście takie, jakie jest** — wklejony tekst, mail od kancelarii, PDF
   (czytaj przez Read), tabelka. Nie proś Daniela o przepisywanie do struktury.
2. **Wyciągnij pozycje** do pliku JSON (format niżej). Zapisz go obok CSV-ki —
   to ślad, co dokładnie poszło do banku, i pozwala poprawić jedną pozycję
   i wygenerować plik ponownie bez powtarzania całej roboty.
3. **Pokaż tabelę do potwierdzenia.** Wypunktuj też, co dobrałeś sam
   (np. adres odbiorcy, skrócona nazwa) — to najczęstsze miejsce na pomyłkę.
4. **Generuj:** `python3 ~/.claude/skills/generowanie-przelewow-pko/generuj_przelewy.py dane.json`
   Skrypt wypisze tabelę kontrolną z sumą i zapisze plik.
   `--dry-run` sprawdza dane bez zapisu, `--out ŚCIEŻKA` nadpisuje domyślną lokalizację.
5. **Podaj pełną ścieżkę pliku** w odpowiedzi (Daniel importuje go ręcznie w iPKO).

Domyślna lokalizacja wyniku: `~/Downloads/exporty_przelewow/przelewy_<nazwa>_<data>.csv`
— tam leżą wszystkie dotychczasowe eksporty i tam bank je odbiera.

## Format wejścia (JSON)

```json
{
  "data": "2026-08-05",
  "nazwa": "znaki_towarowe",
  "przelewy": [
    { "kwota": 17.00,
      "rachunek": "21 1030 1508 0000 0005 5000 0070",
      "odbiorca": "Urząd Miasta St. Warszawy - COP",
      "adres": "Obozowa 57|01-161 Warszawa",
      "tytul": "opłata skarbowa od pełnomocnictwa udzielonego przez ..." }
  ]
}
```

| Pole | Uwagi |
| :-- | :-- |
| `data` | RRRR-MM-DD, data obciążenia. Domyślnie dziś. |
| `nazwa` | slug do nazwy pliku (bez spacji i polskich znaków) |
| `kwota` | w złotych; `17`, `17.00`, `"1 234,57"` — wszystko działa |
| `rachunek` | ze spacjami lub bez, z „PL" lub bez; skrypt normalizuje |
| `odbiorca` | **max 35 znaków** — skracaj świadomie, bank i tak utnie |
| `adres` | `ulica|kod miasto`, człony max 35 znaków; opcjonalny |
| `tytul` | max 140 znaków; skrypt sam łamie co 35 po spacjach |

Dane nadawcy (rachunek i adres Opcja Natura) są wpisane w skrypcie — nie trzeba ich podawać.

## Co skrypt waliduje (i przerywa, zamiast wygenerować zły przelew)

- **suma kontrolna rachunku (mod 97)** — łapie literówkę w przepisanym numerze;
- kwota dodatnia, przeliczana przez `Decimal` (bez gubienia grosza na floatach);
- nazwa odbiorcy i człony adresu ≤ 35 znaków;
- tytuł mieszczący się w 4 liniach po 35 znaków;
- znaki niedostępne w ISO-8859-2 (przerywa z listą znaków).

## Pułapki formatu (dlaczego plik potrafi się nie zaimportować)

| Pułapka | Jak jest poprawnie |
| :-- | :-- |
| Kodowanie | **ISO-8859-2** (Latin-2), nie UTF-8. UTF-8 = krzaki w nazwach. |
| Końce linii | **CRLF**, z CRLF również po ostatnim wierszu |
| Kwota | w **groszach**, bez kropki: `570 zł` → `57000` |
| Tytuł | 4 linie × 35 znaków, rozdzielone `\|` |
| Łamanie tytułu | **po spacjach, ze spacją na końcu linii** — bank skleja linie bez spacji, więc cięcie w środku słowa daje „słowny Dzi\|ki krem", a wyrzucenie spacji daje „słownyDziki" |
| Cudzysłowy | pole nie ma escape'owania — każdy `"` w treści rozwala CSV; skrypt zamienia je na apostrofy |
| Znak `\|` | to separator linii, nie może trafić do treści z maila |
| Rozliczeniowy banku | cyfry 3–10 numeru rachunku (pole 4 i 11) |
| Typ operacji | `110` … `"51"` = przelew krajowy zwykły |

## Stali odbiorcy (zweryfikowane sumy kontrolne)

| Odbiorca | Rachunek | Po co |
| :-- | :-- | :-- |
| Urząd Miasta St. Warszawy - COP | 21 1030 1508 0000 0005 5000 0070 | opłata skarbowa (m.in. od pełnomocnictwa, 17 zł) |
| Urząd Patentowy RP | 93 1010 1010 0025 8322 3100 0000 | opłaty zgłoszeniowe znaków towarowych (570 zł) |

Adresy dobrane przy pierwszym użyciu: COP — `Obozowa 57|01-161 Warszawa`,
UPRP — `al. Niepodległości 188/192|00-950 Warszawa`. Przy przelewie krajowym adres
nie wpływa na księgowanie.

## Split payment (MPP) — tylko referencja, skrypt tego nie robi

W eksportach z iPKO przelewy MPP mają kod `"53"` zamiast `"51"`, a tytuł ma
sztywną strukturę:

```
/VAT/287,50/IDC/6182187503/INV/6182187503-20260630-9A9BF2400002-6A/TXT/A3/6/2026
```

(kwota VAT / NIP / numer faktury / opis). Jeśli taki przelew będzie potrzebny —
zbuduj wiersz ręcznie na wzór istniejących w `~/Downloads/exporty_przelewow/`
i **zweryfikuj podgląd w iPKO przed zatwierdzeniem**. Ta ścieżka nie była
przepuszczona przez import, więc nie traktuj jej jak sprawdzonej.

## Poza zakresem

- **przelewy podatkowe do US / mikrorachunek, ZUS** — inny typ rekordu i inna
  struktura pól; rób ręcznie w iPKO;
- przelewy zagraniczne / walutowe;
- księgowanie i dekretacja — to nie jest narzędzie księgowe.

Uwaga: opłata skarbowa do urzędu miasta to **zwykły przelew krajowy**, nie przelew
podatkowy — obsługuje ją ten skill.

## Częste błędy

- **Wygenerowanie pliku bez pokazania listy** — zawsze najpierw tabela do potwierdzenia.
- **Kilka identycznych przelewów tego samego dnia** (ta sama kwota, konto i tytuł) —
  bank może ostrzec o duplikatach, a odbiorcy trudniej przypisać wpłatę. Zgłoś to
  Danielowi i zaproponuj rozróżnienie tytułów, ale **nie zmieniaj brzmienia tytułu
  podanego przez kancelarię/urząd bez jego zgody**.
- **Skracanie nazwy odbiorcy po cichu** — powiedz, co skróciłeś.
- **Przepisanie numeru konta „na oko"** z PDF-a — skrypt sprawdza sumę kontrolną,
  ale zgodny cyfrowo numer innego urzędu przejdzie walidację; porównaj ze źródłem.
