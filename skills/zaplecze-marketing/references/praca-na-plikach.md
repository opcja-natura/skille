# Jak pracujesz z plikami (Mac, Dysk Google na komputer, Cowork)

## Środowisko osoby

- **Dysk Google na komputer** (Google Drive for desktop) pokazuje dysk w Finderze jak zwykły folder. Co zapiszesz w środku, program sam wysyła do chmury w tle.
  - Ścieżka na Macu: `~/Library/CloudStorage/GoogleDrive-<adres e-mail>/`, a w niej `Dyski współdzielone` (albo `Shared drives`, zależnie od języka systemu) → `[04] OpcjaNatura - marketing`.
  - Dyski współdzielone są **strumieniowane**: pliki ściągają się dopiero przy otwarciu. Listowanie folderów i zapisywanie nowych plików działa normalnie.
- **Folder roboczy** osoby, zwykle `~/OpcjaNatura/`:
  - `do_wgrania/`: tu osoba wrzuca materiały (zdjęcia z sesji, eksporty z programu graficznego, pliki od Darii);
  - `wgrane/RRRR-MM-DD/`: tu odkładasz pliki po skopiowaniu na dysk (ślad, co poszło).
  Źródłem może być też inny folder, który osoba wskaże (np. Pobrane).
- **Cowork** widzi tylko foldery, do których osoba dała mu dostęp. Ścieżki wewnątrz Coworku mogą wyglądać inaczej niż w Finderze: szukaj folderu po nazwie w udostępnionych miejscach, nie zakładaj ścieżki.

Jeśli folderu z Dyskiem Google nie widzisz, powiedz osobie wprost: „Nie mam dostępu do folderu Dysku Google. Dodaj go w Coworku (folder `[04] OpcjaNatura - marketing` albo konkretny podfolder)”. Jeśli Cowork nie pozwala go dodać, przejdź na **plan B** (niżej).

## Od ID albo linku do folderu na dysku

Osoba często podaje link `https://drive.google.com/drive/folders/<ID>` albo samo ID. Kolejność:

1. Szukaj ID w `foldery.md`, tam jest ścieżka.
2. Nie ma w tabeli, a masz konektor Google Drive: pobierz **tylko metadane** folderu (nazwa, rodzic) i przejdź w górę po rodzicach, aż dojdziesz do `[04] OpcjaNatura - marketing`. To da ścieżkę.
3. Nie masz konektora: zapytaj o nazwę folderu i znajdź go w Finderze po nazwie.

Gdy osoba opisuje cel słowami („packshoty mazidła, format 0.94”), zbuduj ścieżkę z `foldery.md` + `zdjecia-produktow.md`.

## Kopiowanie

- **Kopiuj** pliki poleceniem systemowym (jak w Finderze). Nie otwieraj ich, nie czytaj zawartości do rozmowy i **nie wgrywaj przez konektor Drive**: zapychasz rozmowę i przy kilkunastu plikach przerwiesz pracę.
- Zmiana nazwy przy kopiowaniu: nowa nazwa trafia do pliku na dysku Google, oryginał w `do_wgrania/` zostaje z nazwą pierwotną, dopóki go nie przeniesiesz do `wgrane/`.
- Plik o tej samej nazwie już jest w folderze docelowym: **nie nadpisuj**. Zapytaj: stary do `archiwum/` czy nowy z dopiskiem `_02`?
- Nie usuwaj niczego na dysku Google. Nie zmieniaj nazw ani układu istniejących folderów.

## Sprawdzenie i ślad

1. Po skopiowaniu porównaj liczbę i rozmiary plików w folderze docelowym z tym, co miało pójść.
2. Przenieś oryginały z `do_wgrania/` do `wgrane/RRRR-MM-DD/` (dzisiejsza data).
3. Wysyłka do chmury trwa chwilę. Ikona Dysku Google na górnym pasku pokazuje postęp. Jeśli osoba chce pewności: konektor Drive, wyszukanie **jednego** pliku po nazwie w folderze docelowym.

## Plan B: Cowork nie może pisać do Dysku Google

Przygotuj wszystko lokalnie w `do_wgrania/gotowe/<folder docelowy>/` (nazwy, podział na proporcje). Napisz osobie, który podfolder przeciągnąć do którego folderu na dysku (ścieżka i link). Ona robi to w Finderze jednym ruchem.

## Zmiana rozmiaru (tylko na prośbę)

Zwykle osoba eksportuje pliki w gotowym rozmiarze z programu graficznego. Jeśli prosi o zmniejszenie, a masz możliwość uruchomienia kodu:
- sklep (`format_0.94`): 1338×1424, JPG jakość 85; PNG z przezroczystością zostaje PNG;
- social `1 : 1`: dłuższy bok 2048 albo 1080 (zapytaj); `9 : 16`: 1080×1920;
- nie powiększaj mniejszych plików, nie zmieniaj proporcji przez rozciąganie (najpierw kadr, o kadrze decyduje osoba).
Jeśli nie możesz uruchomić kodu, powiedz to i poproś o eksport w programie graficznym.
