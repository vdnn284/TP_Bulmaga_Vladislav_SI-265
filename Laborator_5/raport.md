# Laboratorul 5 – Informații invizibile: forensics și steganografie

**Disciplina:** Tehnici de programare  
**Student:** Bulmaga Vladislav  
**Grupa:** SI-265  
**Universitatea:** Universitatea Tehnică a Moldovei

## 1. Scopul lucrării

Studierea metodelor de decodare a informațiilor și analiza fișierelor binare folosind limbajul Python. Identificarea metadatelor și aplicarea steganografiei pentru ascunderea și recuperarea mesajelor.

## 2. Lucrarea A – Decoderul universal

### A1. Text și octeți

Am transformat textul `Salut` în octeți, apoi în format hexazecimal.

**Rezultate:**
- Text: `Salut`
- Octeți: `b'Salut'`
- Primul octet: `83`
- Hex: `53616c7574`

### A2–A3. Recunoașterea și decodarea

Programul identifică trei tipuri de codare: URL, hexazecimal și Base64.

Exemple:
- `%2Fetc` → URL
- `48656c6c6f` → hex
- `U2FsdXQ=` → Base64 → `Salut`

### A4. Decodarea mai multor straturi

Programul a identificat și eliminat trei straturi de codare:

`Base64 → Base64 → hex`

**Mesaj recuperat:** `FLAG{straturi_de_encoding}`

### A5. XOR cu cheie de un octet

Au fost încercate cele 256 de valori posibile ale cheii XOR.

**Cheia corectă:** `128` (`0x80`)

**Mesaj recuperat:** `Un singur octet tine tot secretul... gaseste-l! FLAG{xor_un_octet}`

 Rezultatele au fost filtrate după caracterele imprimabile și prezența secvenței `FLAG{`. A fost identificată cheia corectă `128` (`0x80`), iar mesajul original a fost recuperat.

### A6. Identificarea parolelor prin dicționar

Programul a comparat hashurile MD5 cu parolele din `wordlist.txt`.

| Hash MD5 | Parola găsită |
|---|---|
| `5f4dcc3b5aa765d61d8327deb882cf99` | password |
| `8621ffdbc5698829397d97767ac13db3` | dragon |
| `d8578edf8458ce06fbc5bb76a58c5ca4` | qwerty |
| `0d107d09f5bbe40cade3de5c71e9e9b7` | letmein |
| `d0763edaa9d9bd2a9516280e9044d885` | monkey |

### A7. Automatizare și testare

Am creat programul `decode.py`, care acceptă argumente din terminal și generează fișierul `fisa.json`.

Am verificat funcția de decodare Base64 cu `test_decode.py`.

**Rezultat:** `Testul Base64 a trecut!`

## 3. Lucrarea B – Forensics și steganografie

### B1. Identificarea tipului real al fișierelor

Am verificat semnăturile binare ale fișierelor.

- `foto.jpg` → JPEG
- `ascuns.png` → PNG

### B2. Extragerea textului din fișierul binar

Am căutat secvențe de caractere imprimabile în `ascuns.png`.

Printre rezultatele identificate:

`IHDR`, `IDATx`, `IEND`, `secret.txt`, `FLAG{ascuns_prin_carving}`.

### B3. Analiza metadatelor EXIF și GPS

Metadatele identificate în `foto.jpg`:

- Producător: Apple
- Model: iPhone 13
- Data: 14.09.2026, ora 10:30:00
- Latitudine: `47.016667° N`
- Longitudine: `28.8575° E`

Coordonatele indică o locație din Chișinău și sunt date de test introduse în imagine de generatorul laboratorului.

### B4. Extragerea arhivei ascunse

Am identificat semnătura ZIP în `ascuns.png`, începând de la octetul `782`.

Arhiva a fost recuperată în fișierul `gasit.zip`.

**Fișier găsit:** `secret.txt`

**Conținut:** `FLAG{ascuns_prin_carving}`

### B5. Ascunderea mesajului prin LSB

Am utilizat metoda Least Significant Bit pentru a modifica ultimii biți ai canalelor RGB.

Imaginea rezultată a fost salvată ca `stego.png`.

**Biți utilizați:** `184`

### B6. Recuperarea mesajului

Am citit ultimii biți ai pixelilor și am reconstruit mesajul.

**Mesaj recuperat:** `FLAG{ascuns_in_pixeli}`

**Rezultat:** `Verificare reusita!`

## 4. Concluzie

În cadrul laboratorului am realizat un decoder universal și programe pentru analiza fișierelor. Am utilizat Base64, hexazecimal, URL encoding, XOR și verificarea hashurilor prin dicționar.

Am identificat tipurile reale ale fișierelor, am extras metadate EXIF și GPS și am recuperat o arhivă ascunsă într-o imagine. Prin metoda LSB am ascuns și recuperat un mesaj.

Exercițiile au fost executate în Python, iar rezultatele au fost verificate în terminal.