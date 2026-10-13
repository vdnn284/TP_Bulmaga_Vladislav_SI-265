# Laboratorul 5 – Informații invizibile: forensics și steganografie

**Student:** Bulmaga Vladislav  
**Grupa:** SI-265  
**Disciplina:** Tehnici de programare

## Descriere

În acest laborator am realizat programe Python pentru decodarea informațiilor, analiza fișierelor binare și steganografie.

## Fișierele laboratorului

- `arsenal/forensics/decode.py` – decodare Base64, hex, URL, XOR și hashuri.
- `arsenal/forensics/fisa.json` – rezultatele decoderului.
- `teste/test_decode.py` – testarea decodării Base64.
- `forensics.py` – identificarea tipurilor de fișiere, analiza EXIF/GPS și extragerea unei arhive ZIP.
- `stego.py` – ascunderea și recuperarea mesajelor prin LSB.
- `stego.png` – imaginea cu mesajul ascuns.
- `probe/` – fișierele utilizate în exerciții.
- `gasit.zip` – arhiva recuperată.
- `raport.md` – raportul complet al laboratorului.

## Instalare și rulare

Este necesar Python 3 și biblioteca Pillow.

Instalarea bibliotecii:

`py -m pip install pillow`

Executarea programelor din folderul `Laborator_5`:

`py arsenal/forensics/decode.py`

`py -m teste.test_decode`

`py forensics.py`

`py stego.py`

## Concluzie

Am aplicat metode de decodare, analiză forensic și steganografie folosind Python. Programele au fost testate, iar mesajele ascunse au fost recuperate cu succes.