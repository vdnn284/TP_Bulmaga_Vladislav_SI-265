
from pathlib import Path
from PIL import Image

RADACINA = Path(__file__).resolve().parent
IMAGINE_INITIALA = RADACINA / "probe" / "foto.jpg"
IMAGINE_STEGO = RADACINA / "stego.png"

MESAJ = b"FLAG{ascuns_in_pixeli}"


# B5 - Ascunderea mesajului in imagine
def ascunde_mesaj(cale_intrare, cale_iesire, mesaj):
    """Ascunde mesajul in ultimul bit al canalelor RGB."""
    with Image.open(cale_intrare) as sursa:
        img = sursa.convert("RGB")

    pixeli = list(img.get_flattened_data())

    date = mesaj + b"\x00"
    biti = "".join(f"{octet:08b}" for octet in date)

    if len(biti) > len(pixeli) * 3:
        raise ValueError("Imaginea este prea mica.")

    canale = []
    for pixel in pixeli:
        canale.extend(pixel)

    for i, bit in enumerate(biti):
        canale[i] = (canale[i] & ~1) | int(bit)

    pixeli_noi = [
        tuple(canale[i:i + 3])
        for i in range(0, len(canale), 3)
    ]

    img.putdata(pixeli_noi)
    img.save(cale_iesire, format="PNG")

    print("Mesaj ascuns in:", cale_iesire)
    print("Biti folositi:", len(biti))


# B6 - Recuperarea mesajului din imagine
def dezvaluie_mesaj(cale):
    """Recupereaza mesajul folosind bitii LSB."""
    with Image.open(cale) as img:
        pixeli = list(img.convert("RGB").get_flattened_data())

    biti = []

    for r, g, b in pixeli:
        biti.extend((r & 1, g & 1, b & 1))

    mesaj = bytearray()

    for i in range(0, len(biti) - 7, 8):
        octet = 0

        for bit in biti[i:i + 8]:
            octet = (octet << 1) | bit

        if octet == 0:
            return mesaj.decode("utf-8")

        mesaj.append(octet)

    raise ValueError("Sfarsitul mesajului nu a fost gasit.")


def main():
    """Executa exercitiile B5 si B6."""
    print("=== B5: ASCUNDERE LSB ===")
    ascunde_mesaj(
        IMAGINE_INITIALA,
        IMAGINE_STEGO,
        MESAJ
    )

    print("\n=== B6: DEZVALUIRE LSB ===")
    rezultat = dezvaluie_mesaj(IMAGINE_STEGO)
    print("Mesaj recuperat:", rezultat)

    assert rezultat == MESAJ.decode("utf-8")
    print("Verificare reusita!")


if __name__ == "__main__":
    main()
