
# Laborator: funcții, metode și importuri pe web
# Student: Bulmaga Vladislav

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

import requests
import urllib.request
import time


# Exercitiul 1. Primul import
print("\n=== Exercitiul 1 ===")

print("Versiunea requests:", requests.__version__)

# requests este o biblioteca externa si necesita pip install requests.
# urllib face parte din biblioteca standard Python si nu necesita instalare.


# Exercitiul 2. Doua stiluri de import
print("\n=== Exercitiul 2 ===")

response = requests.get(BASE_URL, timeout=TIMEOUT)
print("Status cu requests.get:", response.status_code)

time.sleep(1)

from requests import get

response = get(BASE_URL, timeout=TIMEOUT)
print("Status cu get:", response.status_code)

# import requests arata clar din ce biblioteca provine functia.
# from requests import get permite apelarea mai scurta a functiei.


# Exercitiul 3. Alias-uri
print("\n=== Exercitiul 3 ===")

import requests as rq

time.sleep(1)

response = rq.get(BASE_URL, timeout=TIMEOUT)
print("Status cu alias rq:", response.status_code)

# Aliasurile sunt utile cand numele modulelor sunt lungi.
# Aliasurile neclare pot face codul mai greu de inteles.




# Exercitiul 4. Doar biblioteca standard
print("\n=== Exercitiul 4 ===")

time.sleep(1)

from urllib.error import HTTPError, URLError

try:
    request = urllib.request.Request(
        BASE_URL,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
        print("Status:", response.status)
        html = response.read().decode("utf-8", errors="replace")
        print("Primele 200 de caractere:")
        print(html[:200])

except HTTPError as error:
    print("Status HTTP:", error.code)
    print("Serverul a refuzat cererea:", error.reason)

except URLError as error:
    print("Eroare de conexiune:", error.reason)




# Exercitiul 5. Priviti in interiorul unui modul
print("\n=== Exercitiul 5 ===")

print(dir(requests))

# requests.get este o functie.
# requests.Session este o clasa.
# requests.exceptions este un modul.


# Exercitiul 6. Cititi documentatia
print("\n=== Exercitiul 6 ===")

help(requests.get)

# Parametrul timeout stabileste timpul maxim de asteptare
# pentru operatiile de conectare si citire.

time.sleep(1)

response = requests.get(BASE_URL, timeout=TIMEOUT)
print("Status cu timeout:", response.status_code)


# Exercitiul 7. Cronometrarea unei cereri
print("\n=== Exercitiul 7 ===")

time.sleep(1)

start = time.perf_counter()

response = requests.get(BASE_URL, timeout=TIMEOUT)

end = time.perf_counter()

durata = end - start

print("Durata cu perf_counter:", durata, "secunde")
print("Durata cu response.elapsed:",
      response.elapsed.total_seconds(), "secunde")

# perf_counter masoara durata intregului apel requests.get.
# response.elapsed masoara timpul pana la primirea antetelor
# raspunsului HTTP, deci valorile pot fi diferite.


# Exercitiul 8. Cand un import esueaza
print("\n=== Exercitiul 8 ===")

try:
    import bs4
    print("Modulul bs4 este instalat.")
except ImportError:
    print("Instalati modulul cu: pip install beautifulsoup4")


# Intrebare de verificare:
# Modulul este un fisier Python care contine cod reutilizabil.
# Pachetul grupeaza module Python.
# Biblioteca este o colectie de cod reutilizabil,
# care poate contine module si pachete.

print("\n=== Partea 1 finalizata ===")
