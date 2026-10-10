#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generator pliku importu przelewów do iPKO (format Elixir-O, przelew krajowy zwykły).

Użycie:
    python3 generuj_przelewy.py dane.json [--out /sciezka/plik.csv] [--dry-run]

Wejście: JSON opisany w SKILL.md. Wyjście: CSV w ISO-8859-2 z CRLF.
Skrypt WALIDUJE i przerywa przy błędzie — lepiej nie wygenerować pliku
niż wygenerować przelew z literówką w numerze konta.
"""
import json
import re
import sys
from decimal import Decimal, ROUND_HALF_UP

# --- stałe nadawcy (Opcja Natura Sp. z o.o.) ---------------------------------
NADAWCA_RACH = "91102022670000490202243202"
NADAWCA_DANE = "Opcja Natura Sp. z o.o.||Kościuszki 8c/7|63-700 Krotoszyn"

LINIA = 35          # maks. długość jednej linii pola tekstowego w Elixirze
MAKS_LINII_TYTUL = 4  # tytuł: 4 x 35 = 140 znaków

# Znaki, które regularnie wpadają z maili i PDF-ów, a psują plik:
# - typograficzne cudzysłowy/myślniki nie istnieją w ISO-8859-2,
# - PROSTY cudzysłów " rozwala cytowanie pola CSV (format nie ma escape'owania),
#   więc wszystkie cudzysłowy lądują jako apostrof,
# - "|" to w Elixirze znak łamania linii, w treści nie może wystąpić.
PODMIANY = {
    "\u201e": "'", "\u201d": "'", "\u201c": "'", "\u201f": "'", "\u2033": "'",
    '"': "'", "\u201a": "'", "\u2019": "'", "\u2018": "'", "\u2032": "'",
    "\u2013": "-", "\u2014": "-", "\u2212": "-", "\u2011": "-",
    "\u2026": "...", "\u00a0": " ", "\u202f": " ", "\u2009": " ",
    "\u20ac": "EUR", "|": " ",
}


class BladDanych(Exception):
    pass


def oczysc(txt):
    """Zamienia typograficzne cudzysłowy/myślniki na odpowiedniki z ISO-8859-2."""
    for zly, dobry in PODMIANY.items():
        txt = txt.replace(zly, dobry)
    txt = re.sub(r"\s+", " ", txt).strip()
    niekodowalne = sorted({z for z in txt if not _koduje(z)})
    if niekodowalne:
        raise BladDanych(
            "znaki niedopuszczalne w ISO-8859-2: %s (w tekście: %r)"
            % (" ".join(niekodowalne), txt))
    return txt


def _koduje(znak):
    try:
        znak.encode("iso-8859-2")
        return True
    except UnicodeEncodeError:
        return False


def nrb(numer, opis):
    """Normalizuje numer rachunku i sprawdza sumę kontrolną (mod 97)."""
    czysty = re.sub(r"[\s-]", "", str(numer)).upper()
    if czysty.startswith("PL"):
        czysty = czysty[2:]
    if len(czysty) != 26 or not czysty.isdigit():
        raise BladDanych("%s: rachunek ma %d znaków (oczekiwane 26 cyfr): %s"
                         % (opis, len(czysty), czysty))
    if int(czysty[2:] + "2521" + czysty[:2]) % 97 != 1:
        raise BladDanych(
            "%s: BŁĘDNA SUMA KONTROLNA rachunku %s — sprawdź, czy numer jest "
            "przepisany poprawnie" % (opis, czysty))
    return czysty


def grosze(kwota, opis):
    """Kwota -> grosze. Decimal, żeby nie zgubić grosza na floatach."""
    d = Decimal(str(kwota).replace(",", ".").replace(" ", ""))
    if d <= 0:
        raise BladDanych("%s: kwota musi być dodatnia (jest %s)" % (opis, d))
    return int(d.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) * 100)


def lam(txt, maks_linii, opis):
    """Łamie tekst na linie <= 35 znaków PO SPACJACH, spacja zostaje na końcu
    linii — dzięki temu po sklejeniu przez bank wyrazy się nie zlepiają."""
    linie, biezaca = [], ""
    for slowo in txt.split(" "):
        if len(biezaca + slowo) <= LINIA:
            biezaca += slowo + " "
        else:
            if biezaca:
                linie.append(biezaca)
            biezaca = slowo + " "
        while len(biezaca) > LINIA:      # słowo dłuższe niż linia
            linie.append(biezaca[:LINIA])
            biezaca = biezaca[LINIA:]
    if biezaca:
        linie.append(biezaca)
    linie[-1] = linie[-1].rstrip()
    if len(linie) > maks_linii:
        raise BladDanych(
            "%s: tekst za długi — %d znaków wymaga %d linii, limit to %d "
            "(%d znaków). Skróć: %r"
            % (opis, len(txt), len(linie), maks_linii, maks_linii * LINIA, txt))
    return "|".join(linie)


def dane_odbiorcy(p, nr):
    """'nazwa||ulica|kod miasto' — każdy człon max 35 znaków."""
    nazwa = oczysc(p["odbiorca"])
    if len(nazwa) > LINIA:
        raise BladDanych(
            "przelew %d: nazwa odbiorcy ma %d znaków, limit %d. Skróć ją "
            "świadomie (bank i tak utnie): %r" % (nr, len(nazwa), LINIA, nazwa))
    # adres rozbijamy PRZED czyszczeniem — tam "|" to celowy separator linii
    czlony = [oczysc(c) for c in p.get("adres", "").split("|")]
    czlony = [c for c in czlony if c]
    for c in czlony:
        if len(c) > LINIA:
            raise BladDanych("przelew %d: człon adresu > %d znaków: %r"
                             % (nr, LINIA, c))
    return "|".join([nazwa, ""] + czlony)


def zbuduj(dane):
    data = str(dane["data"]).replace("-", "")
    if not re.fullmatch(r"20\d{6}", data):
        raise BladDanych("data ma być w formacie RRRR-MM-DD, jest: %r"
                         % dane["data"])
    nad_rach = nrb(dane.get("nadawca_rachunek", NADAWCA_RACH), "nadawca")
    nad_dane = dane.get("nadawca_dane", NADAWCA_DANE)

    wiersze, kontrola = [], []
    for nr, p in enumerate(dane["przelewy"], 1):
        odb_rach = nrb(p["rachunek"], "przelew %d (%s)" % (nr, p["odbiorca"]))
        kw = grosze(p["kwota"], "przelew %d" % nr)
        tytul = lam(oczysc(p["tytul"]), MAKS_LINII_TYTUL, "przelew %d: tytuł" % nr)
        wiersze.append(",".join([
            "110", data, str(kw), nad_rach[2:10], "0",
            '"%s"' % nad_rach, '"%s"' % odb_rach,
            '"%s"' % nad_dane, '"%s"' % dane_odbiorcy(p, nr),
            "0", odb_rach[2:10], '"%s"' % tytul, '""', '""', '"51"',
        ]))
        kontrola.append((nr, kw, oczysc(p["odbiorca"]), odb_rach,
                         oczysc(p["tytul"])))
    return wiersze, kontrola


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    dane = json.load(open(sys.argv[1], encoding="utf-8"))
    suchy = "--dry-run" in sys.argv

    try:
        wiersze, kontrola = zbuduj(dane)
    except (BladDanych, KeyError) as e:
        print("BŁĄD: %s" % e)
        return 1

    print("Data obciążenia: %s" % dane["data"])
    print("-" * 78)
    for nr, kw, odb, rach, tyt in kontrola:
        print("%2d. %10s zł  %-33s %s" % (nr, "%.2f" % (kw / 100), odb[:33],
                                          rach))
        print("    tytuł: %s" % (tyt if len(tyt) <= 66 else tyt[:63] + "..."))
    print("-" * 78)
    print("RAZEM: %d przelewów, %.2f zł"
          % (len(kontrola), sum(k[1] for k in kontrola) / 100))

    if suchy:
        print("\n(--dry-run: plik nie zapisany)")
        return 0

    if "--out" in sys.argv:
        sciezka = sys.argv[sys.argv.index("--out") + 1]
    else:
        sciezka = "/home/daniel/Downloads/exporty_przelewow/przelewy_%s_%s.csv" % (
            dane.get("nazwa", "lista"), dane["data"])
    with open(sciezka, "wb") as f:
        f.write(("\r\n".join(wiersze) + "\r\n").encode("iso-8859-2"))
    print("\nZapisano: %s" % sciezka)
    return 0


if __name__ == "__main__":
    sys.exit(main())
