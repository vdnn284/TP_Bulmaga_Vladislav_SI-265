
import re
import zipfile
from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

RADACINA = Path(__file__).resolve().parent
PROBE = RADACINA / "probe"


# B1 - Identificarea tipului real al fisierului
def tip_real(cale):
    """Identifica fisierul dupa primii octeti."""
    with open(cale, "rb") as f:
        cap = f.read(8)

    if cap.startswith(b"%PDF"):
        return "pdf"
    if cap.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if cap.startswith(b"\xff\xd8"):
        return "jpeg"
    if cap.startswith(b"PK\x03\x04"):
        return "zip/docx"

    return "necunoscut"


# B2 - Extragerea textului dintr-un fisier binar
def extrage_strings(cale):
    """Extrage secvente ASCII imprimabile."""
    date = Path(cale).read_bytes()
    secvente = re.findall(rb"[ -~]{4,}", date)
    return [s.decode("ascii") for s in secvente]


# B3 - Metadate EXIF si GPS
def in_zecimal(valori, emisfera):
    """Transforma gradele, minutele si secundele in grade zecimale."""
    grade, minute, secunde = [float(x) for x in valori]
    rezultat = grade + minute / 60 + secunde / 3600

    if emisfera in ("S", "W"):
        rezultat = -rezultat

    return rezultat


def citeste_exif(cale):
    """Afiseaza metadatele si coordonatele GPS."""
    with Image.open(cale) as img:
        exif = img.getexif()

        print("Metadate EXIF:")
        for tag, valoare in exif.items():
            print(TAGS.get(tag, tag), "=", valoare)

        gps = exif.get_ifd(0x8825)

    if not gps:
        print("Nu exista coordonate GPS.")
        return None

    gps_date = {
        GPSTAGS.get(tag, tag): valoare
        for tag, valoare in gps.items()
    }

    print("Date GPS:", gps_date)

    lat = gps_date.get("GPSLatitude")
    lat_ref = gps_date.get("GPSLatitudeRef")
    lon = gps_date.get("GPSLongitude")
    lon_ref = gps_date.get("GPSLongitudeRef")

    if not all((lat, lat_ref, lon, lon_ref)):
        print("Date GPS incomplete.")
        return None

    latitudine = in_zecimal(lat, lat_ref)
    longitudine = in_zecimal(lon, lon_ref)

    print("Latitudine:", round(latitudine, 6))
    print("Longitudine:", round(longitudine, 6))

    return latitudine, longitudine


# B4 - Extragerea arhivei ZIP ascunse
def extrage_zip(cale, iesire):
    """Gaseste semnatura ZIP si extrage arhiva."""
    date = Path(cale).read_bytes()
    pozitie = date.find(b"PK\x03\x04")

    if pozitie == -1:
        print("Nu s-a gasit arhiva ZIP.")
        return None

    Path(iesire).write_bytes(date[pozitie:])
    print("Arhiva extrasa de la octetul:", pozitie)

    with zipfile.ZipFile(iesire, "r") as arhiva:
        print("Fisiere in arhiva:", arhiva.namelist())

        for nume in arhiva.namelist():
            print("Continut", nume, ":")
            print(arhiva.read(nume).decode("utf-8"))

    return pozitie


def main():
    """Executa exercitiile B1-B4."""
    print("=== B1: MAGIC BYTES ===")
    for nume in ("foto.jpg", "ascuns.png"):
        print(nume, "->", tip_real(PROBE / nume))

    print("\n=== B2: STRINGS ===")
    for text in extrage_strings(PROBE / "ascuns.png"):
        print(text)

    print("\n=== B3: EXIF SI GPS ===")
    citeste_exif(PROBE / "foto.jpg")

    print("\n=== B4: FILE CARVING ===")
    extrage_zip(
        PROBE / "ascuns.png",
        RADACINA / "gasit.zip"
    )


if __name__ == "__main__":
    main()
