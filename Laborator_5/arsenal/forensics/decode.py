
import argparse
import base64
import binascii
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote_to_bytes

RADACINA = Path(__file__).resolve().parents[2]
PROBE = RADACINA / "probe"
FISA = Path(__file__).resolve().parent / "fisa.json"


# A1 - Text si octeti
def exercitiul_a1():
    s = "Salut"
    b = s.encode("utf-8")

    print("Text:", s)
    print("Octeti:", b)
    print("Primul octet:", b[0])
    print("Hex:", b.hex())
    print("Inapoi din hex:", bytes.fromhex(b.hex()))


# A2 - Recunoasterea codarii
def ghici_strat(s):
    """Recunoaste codarea URL, hex sau Base64."""
    s = s.strip()

    if re.search(r"%[0-9A-Fa-f]{2}", s):
        return "url"

    if s and len(s) % 2 == 0:
        if re.fullmatch(r"[0-9A-Fa-f]+", s):
            return "hex"

    if len(s) >= 4 and len(s) % 4 == 0:
        if re.fullmatch(r"[A-Za-z0-9+/]+={0,2}", s):
            try:
                base64.b64decode(s, validate=True)
                return "base64"
            except (binascii.Error, ValueError):
                pass

    return "necunoscut"


# A3 - Decodarea unui strat
def desfa(s):
    """Decodeaza un strat si returneaza octetii."""
    strat = ghici_strat(s)

    if strat == "url":
        return strat, unquote_to_bytes(s)

    if strat == "hex":
        return strat, bytes.fromhex(s)

    if strat == "base64":
        return strat, base64.b64decode(s, validate=True)

    return strat, s.encode("utf-8")


# A4 - Decodarea mai multor straturi
def citibil(b):
    """Verifica daca octetii sunt imprimabili."""
    return all(32 <= c < 127 for c in b)


def decodeaza_straturi(val, maxim=8):
    """Desface succesiv straturile recunoscute."""
    pasi = []

    for _ in range(maxim):
        strat, rezultat = desfa(val)

        if strat == "necunoscut":
            break

        pasi.append(strat)

        try:
            val = rezultat.decode("utf-8")
        except UnicodeDecodeError:
            return pasi, rezultat

        if not citibil(rezultat):
            break

    return pasi, val.encode("utf-8")


# A5 - Spargerea XOR
def sparge_xor(cale):
    """Incearca toate cheile XOR de la 0 la 255."""
    date = Path(cale).read_bytes()
    rezultate = []

    for k in range(256):
        clar = bytes(b ^ k for b in date)

        if citibil(clar) and b"FLAG{" in clar:
         rezultate.append((k, clar.decode("ascii")))

    return rezultate


# A6 - Hashuri si dictionar
def algoritm_hash(tinta):
    """Identifica algoritmul dupa lungimea hashului."""
    return {32: "md5", 40: "sha1", 64: "sha256"}.get(len(tinta))


def sparge_hashuri(cale_hashuri, cale_wordlist):
    """Cauta parolele folosind dictionarul laboratorului."""
    tinte = Path(cale_hashuri).read_text(
        encoding="utf-8"
    ).splitlines()

    cuvinte = Path(cale_wordlist).read_text(
        encoding="latin1"
    ).splitlines()

    rezultate = []

    for tinta in tinte:
        tinta = tinta.strip().lower()
        algoritm = algoritm_hash(tinta)
        gasit = None

        if algoritm:
            for cuv in cuvinte:
                valoare = hashlib.new(
                    algoritm, cuv.encode("utf-8")
                ).hexdigest()

                if valoare == tinta:
                    gasit = cuv
                    break

        rezultate.append({
            "hash": tinta,
            "algoritm": algoritm,
            "parola": gasit
        })

    return rezultate


# A7 - Programul principal
def main():
    """Ruleaza decoderul si salveaza fisa JSON."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "intrare",
        nargs="?",
        default=str(PROBE / "mesaj.txt")
    )
    parser.add_argument("--fisier", action="store_true")
    args = parser.parse_args()

    print("=== A1: TEXT SI OCTETI ===")
    exercitiul_a1()

    print("\n=== A2: RECUNOASTERE ===")
    print("%2Fetc ->", ghici_strat("%2Fetc"))
    print("48656c6c6f ->", ghici_strat("48656c6c6f"))
    print("U2FsdXQ= ->", ghici_strat("U2FsdXQ="))

    print("\n=== A3: UN STRAT ===")
    print(desfa("U2FsdXQ="))

    print("\n=== A4: STRATURI MULTIPLE ===")
    if args.fisier or args.intrare == str(PROBE / "mesaj.txt"):
        val = Path(args.intrare).read_text(
            encoding="utf-8"
        ).strip()
    else:
        val = args.intrare

    pasi, rezultat = decodeaza_straturi(val)
    text_final = rezultat.decode("utf-8", errors="replace")

    print("Straturi:", " -> ".join(pasi))
    print("Mesaj:", text_final)

    print("\n=== A5: XOR ===")
    xor_rezultate = sparge_xor(PROBE / "xor.bin")

    for cheie, text in xor_rezultate:
        print("Cheie:", cheie, "Text:", text)

    print("\n=== A6: HASHURI ===")
    hash_rezultate = sparge_hashuri(
        PROBE / "hashuri.txt",
        PROBE / "wordlist.txt"
    )

    for item in hash_rezultate:
        print(
            item["algoritm"],
            item["hash"],
            "->",
            item["parola"]
        )

    print("\n=== A7: FISA JSON ===")
    fisa = {
        "intrare": val,
        "straturi": pasi,
        "strat": pasi[0] if pasi else "necunoscut",
        "rezultat": text_final,
        "xor": [
            {"cheie": k, "text": t}
            for k, t in xor_rezultate
        ],
        "hashuri": hash_rezultate
    }

    FISA.write_text(
        json.dumps(fisa, ensure_ascii=False, indent=4),
        encoding="utf-8"
    )

    print("Salvat:", FISA)


if __name__ == "__main__":
    main()
