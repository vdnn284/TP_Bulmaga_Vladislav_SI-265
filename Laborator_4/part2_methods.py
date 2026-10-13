
# Laborator: funcții, metode și importuri pe web
# Student: Bulmaga Vladislav

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

import requests
import time


# Exercitiul 9. Elementele de baza ale raspunsului
print("\n=== Exercitiul 9 ===")

response = requests.get(BASE_URL, timeout=TIMEOUT)

print("Cod de stare:", response.status_code)  # atribut
print("Raspuns OK:", response.ok)              # atribut
print("URL final:", response.url)              # atribut
print("Codificare:", response.encoding)        # atribut


# Exercitiul 10. Tratarea erorilor cu o metoda
print("\n=== Exercitiul 10 ===")

try:
    response.raise_for_status()
    print("Pagina principala nu are erori HTTP.")
except requests.HTTPError as error:
    print("Eroare la pagina principala:", error)

time.sleep(1)

try:
    error_response = requests.get(
        BASE_URL + "/this-page-does-not-exist",
        timeout=TIMEOUT
    )
    error_response.raise_for_status()
    print("Cod HTTP pagina de test:", error_response.status_code)
    print("Serverul nu a raportat o eroare HTTP.")
except requests.HTTPError as error:
    print("Pagina de test a returnat o eroare HTTP:", error)


# Exercitiul 11. Toate antetele
print("\n=== Exercitiul 11 ===")

for name, value in response.headers.items():
    print(f"{name}: {value}")


# Exercitiul 12. Metode de dictionar
print("\n=== Exercitiul 12 ===")

print("Server:", response.headers.get("Server", "lipsește"))
print("Content-Type:", response.headers.get("Content-Type", "lipsește"))
print("content-type:", response.headers.get("content-type", "lipsește"))

# Antetele HTTP nu sunt sensibile la majuscule/minuscule.
# Content-Type si content-type returneaza aceeasi valoare.


# Exercitiul 13. Inlantuirea metodelor de sir
print("\n=== Exercitiul 13 ===")

count_cyber = response.text.lower().count("cyber")
print("Numarul aparitiilor cuvantului cyber:", count_cyber)

# lower() returneaza un sir de caractere cu litere mici.
# Pe rezultatul obtinut putem apela imediat metoda count().


# Exercitiul 14. Gasirea titlului
print("\n=== Exercitiul 14 ===")

html = response.text
html_lower = html.lower()

start = html_lower.find("<title>")
end = html_lower.find("</title>")

if start != -1 and end != -1 and end > start:
    start = start + len("<title>")
    title = html[start:end].strip()
    print("Titlul paginii:", title)
else:
    print("Titlul paginii nu a fost gasit.")


# Exercitiul 15. Numararea liniilor
print("\n=== Exercitiul 15 ===")

lines = html.splitlines()

print("Numarul liniilor HTML:", len(lines))

if lines:
    longest_line = max(lines, key=len)
    print("Lungimea celei mai lungi linii:", len(longest_line))
else:
    print("Pagina nu contine linii HTML.")


# Exercitiul 16. Verificarea HTTPS
print("\n=== Exercitiul 16 ===")

if response.url.startswith("https://"):
    print("Conexiune securizata")
else:
    print("Conexiune nesecurizata")


# Exercitiul 17. Urmarirea redirectionarilor
print("\n=== Exercitiul 17 ===")

time.sleep(1)

redirect_response = requests.get(
    "http://cybercor.org",
    timeout=TIMEOUT
)

if redirect_response.history:
    for redirect in redirect_response.history:
        print("Redirectionare:", redirect.status_code, redirect.url)
else:
    print("Nu au existat redirectionari.")

print("URL final:", redirect_response.url)


# Exercitiul 18. HEAD versus GET
print("\n=== Exercitiul 18 ===")

time.sleep(1)

head_response = requests.head(BASE_URL, timeout=TIMEOUT)

time.sleep(1)

get_response = requests.get(BASE_URL, timeout=TIMEOUT)

print("Lungime HEAD:", len(head_response.content))
print("Lungime GET:", len(get_response.content))

# HEAD cere doar antetele raspunsului, fara corpul paginii.
# GET cere antetele si corpul paginii HTML.


# Exercitiul 19. Cookie-uri
print("\n=== Exercitiul 19 ===")

if response.cookies:
    for cookie in response.cookies:
        print("Nume:", cookie.name)
        print("Secure:", cookie.secure)
else:
    print("Niciun cookie setat.")


# Exercitiul 20. Sesiuni
print("\n=== Exercitiul 20 ===")

session = requests.Session()

session.headers.update({
    "User-Agent": "WebLab-BulmagaVladislav"
})

time.sleep(1)

try:
    session_response = session.get(
        ECHO_URL + "/headers",
        timeout=TIMEOUT
    )

    session_response.raise_for_status()

    data = session_response.json()
    headers = data.get("headers", {})

    print("User-Agent trimis:",
          session.headers.get("User-Agent"))

    print("User-Agent primit de server:",
          headers.get("User-Agent", "lipsește"))

    if headers.get("User-Agent") == session.headers.get("User-Agent"):
        print("Confirmare: antetul a fost trimis corect.")
    else:
        print("Antetul nu a fost confirmat de server.")

except requests.RequestException as error:
    print("Eroare la verificarea sesiunii:", error)

finally:
    session.close()


# Intrebare de verificare:
# response.text este un atribut care contine textul raspunsului.
# response.json() este o metoda care transforma continutul JSON
# intr-un obiect Python si trebuie apelata cu paranteze.

print("\n=== Partea 2 finalizata ===")
