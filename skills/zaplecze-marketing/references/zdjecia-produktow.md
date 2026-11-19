# Folder zdjęć kosmetyku

Każdy kosmetyk ma folder w `01_ photo/01_zdjecia produktowe/` (lista z ID: `foldery.md`). Układ w środku jest stały:

```text
NN_nazwa_EAN_--zdjecia produktowe--/
├── 01_packshoty/          sam kosmetyk na tle (białe, gładkie, przezroczyste)
│   ├── 1 : 1/
│   ├── format_0.94/
│   └── archiwum/          (w podfolderach) zastąpione wersje
├── 02_lifestyle/          kosmetyk w scenie, z modelką, swatch, konsystencja
│   ├── 1 : 1/
│   ├── 9 : 16/
│   └── format_0.94/
├── 03_raw/                surowe pliki ze zdjęć (oryginały przed obróbką)
└── _EN_/                  wersje z angielską etykietą
    ├── 1:1/
    └── format_0.94/
```

Uwaga na nazwy: w polskich folderach proporcje są **ze spacjami** (`1 : 1`, `9 : 16`), w `_EN_` **bez** (`1:1`). W kilku kosmetykach zostały stare warianty (`sklep_669x712`, `1:1`, `format 0.94`, `01_packshoty/_en`). Nie zakładaj nowych folderów proporcji: wrzucaj do istniejącego, który pasuje.

## Proporcje i rozmiary

| Folder | Proporcja | Typowe wymiary | Do czego |
| :-- | :-- | :-- | :-- |
| `1 : 1` | kwadrat | 2048×2048, 1500×1500, 1080×1080 | social, B2B, marketplace |
| `9 : 16` | pion | 1080×1920 | stories, reels |
| `format_0.94` | prawie kwadrat (szer./wys. = 0,94) | 1338×1424 (obecny standard), 669×712 (starsze) | **sklep opcjanatura.pl** |

Nazwa folderu mówi o proporcji, nie o pikselach. Plik o innej proporcji niż folder to sygnał błędu: zgłoś go, zanim skopiujesz (np. 1500×1500 do `format_0.94`).

Rozmiar sprawdzaj z metadanych pliku (polecenie systemowe albo krótki skrypt), nie oglądając obrazu.

## Nazwy plików

Wzór z wymiany zdjęć w X 2026 (najnowszy, najbardziej uporządkowany):

```text
<kosmetyk>_<opis>_<szerokość>x<wysokość>.<rozszerzenie>
mazidlo_opatrunkowe_bialeTlo_otwarty_1338x1424.jpg
mazidlo_opatrunkowe_transparentneTlo_1338x1424.png
mazidlo_opatrunkowe_en_gladkieTlo_1338x1424.jpg        ← wersja EN: "_en_" po nazwie
```

- Tylko małe litery bez polskich znaków w nazwie kosmetyku, słowa łączone `_`. Opis może być `camelCase` (`bialeTlo`, `gladkieTlo`).
- Kilka ujęć tego samego rodzaju: `_01`, `_02` przed wymiarami.
- Bez spacji i nawiasów. Nazwy typu `mazidlo_1500x1500 (2).jpg` są starsze; nie poprawiaj ich, tylko nowe pliki nazywaj według wzoru.
- Jeśli osoba ma własną konwencję i ją podaje, stosuj jej. Wtedy w podsumowaniu napisz, że warto dopisać ją do skilla (zgłosić Danielowi).

## Podmiana zdjęcia

Zastępowany plik **przenieś do `archiwum/`** w tym samym podfolderze proporcji (załóż `archiwum`, jeśli go nie ma). Nigdy nie usuwaj ani nie nadpisuj. Tak już wygląda większość folderów kosmetyków.

## Co dzieje się dalej (czego wrzucenie NIE robi)

- **Sklep się nie zmienia.** Zdjęcia na stronie żyją w Contentful i w panelu sklepu, przenosi je tam Daniel. Gdy zdjęcia są na stronę (zwłaszcza `format_0.94`), w podsumowaniu napisz: „jeśli mają trafić do sklepu, wyślij Danielowi link do folderu”.
- Arkusz `BD_zdjecia_produtkowe_2026_linki` wskazuje na foldery kosmetyków, nie na pliki. Wrzucenie pliku go nie zmienia i nie trzeba go aktualizować.
