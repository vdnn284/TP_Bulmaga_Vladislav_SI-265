
# Laborator: funcții, metode și importuri pe web
# Student: Bulmaga Vladislav

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

import requests
import time


# Exercitiul 21. Prima functie
def fetch(url, timeout=10):
    """Descarca o pagina web si returneaza obiectul raspuns."""
    return requests.get(url, timeout=timeout)


print("\n=== Exercitiul 21 ===")
response = fetch(BASE_URL)
print("Cod de stare:", response.status_code)


# Exercitiul 22. Returnarea unei singure valori
def get_status(url: str) -> int:
    """Returneaza codul de stare HTTP pentru adresa primita."""
    response = fetch(url)
    return response.status_code


print("\n=== Exercitiul 22 ===")

paths = ["/", "/robots.txt", "/sitemap.xml"]

for i, path in enumerate(paths):
    if i > 0:
        time.sleep(1)

    status = get_status(BASE_URL + path)
    print(path, ":", status)


# Exercitiul 23. Parametri impliciti
# Functia fetch definita la exercitiul 21 are deja
# parametrul timeout cu valoare implicita.

print("\n=== Exercitiul 23 ===")

time.sleep(1)
response = fetch(BASE_URL)
print("Timeout implicit:", response.status_code)

time.sleep(1)
response = fetch(BASE_URL, timeout=3)
print("Timeout de 3 secunde:", response.status_code)


# Exercitiul 24. O singura sarcina pe functie
def get_title(html: str) -> str:
    """Extrage si returneaza titlul unei pagini HTML."""
    html_lower = html.lower()

    start = html_lower.find("<title>")
    end = html_lower.find("</title>")

    if start == -1 or end == -1 or end < start:
        return ""

    start += len("<title>")
    return html[start:end].strip()


print("\n=== Exercitiul 24 ===")

time.sleep(1)
response = fetch(BASE_URL)
print("Titlul paginii:", get_title(response.text))


# Exercitiul 25. Docstring-uri
print("\n=== Exercitiul 25 ===")

help(get_title)


# Exercitiul 26. Adnotari de tip
print("\n=== Exercitiul 26 ===")

# get_status(url: str) -> int foloseste adnotari de tip.
# Acestea documenteaza tipurile asteptate, dar Python
# nu le verifica automat in timpul executiei.

try:
    print(get_status(123))
except (requests.RequestException, TypeError, ValueError) as error:
    print("Apelul cu 123 a produs o eroare:", error)

# Adnotarile de tip nu opresc singure transmiterea
# unui argument de tip int in loc de str.


# Exercitiul 27. Fara opriri neasteptate
def page_exists(url: str) -> bool:
    """Verifica daca o pagina raspunde fara erori HTTP."""
    try:
        response = fetch(url)
        response.raise_for_status()
        return True
    except requests.RequestException:
        return False


print("\n=== Exercitiul 27 ===")

time.sleep(1)
print("Pagina principala:", page_exists(BASE_URL))

time.sleep(1)
print(
    "Domeniu inexistent:",
    page_exists("https://this-domain-does-not-exist.invalid")
)


# Exercitiul 28. Returnarea unui dictionar
def check_paths(base: str, paths: list) -> dict:
    """Verifica o lista de cai si returneaza codurile HTTP."""
    results = {}

    for i, path in enumerate(paths):
        if i > 0:
            time.sleep(1)

        try:
            results[path] = get_status(base.rstrip("/") + path)
        except requests.RequestException:
            results[path] = None

    return results


print("\n=== Exercitiul 28 ===")

time.sleep(1)
results = check_paths(
    BASE_URL,
    ["/", "/robots.txt", "/sitemap.xml"]
)

print("Rezultate:", results)


# Exercitiul 29. Argumente cu nume
def get_header(url: str, name: str, default="lipsește"):
    """Returneaza valoarea unui antet HTTP sau valoarea implicita."""
    response = fetch(url)
    return response.headers.get(name, default)


print("\n=== Exercitiul 29 ===")

time.sleep(1)
print("Server:", get_header(BASE_URL, name="Server"))


# Exercitiul 30. Antete de securitate
def security_headers(url: str) -> dict:
    """Verifica prezenta a cinci antete de securitate HTTP."""
    headers_to_check = [
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Referrer-Policy"
    ]

    response = fetch(url)

    return {
        header: header in response.headers
        for header in headers_to_check
    }


print("\n=== Exercitiul 30 ===")

time.sleep(1)
security_results = security_headers(BASE_URL)

for header, present in security_results.items():
    print(header, ":", present)


# Exercitiul 31. Functii care apeleaza functii
def score_headers(results: dict) -> str:
    """Returneaza scorul antetelor prezente, de forma 3/5."""
    present = sum(results.values())
    total = len(results)
    return f"{present}/{total}"


print("\n=== Exercitiul 31 ===")

time.sleep(1)
print(
    "Scor securitate:",
    score_headers(security_headers(BASE_URL))
)


# Exercitiul 32. Doua functii, o sarcina
def fetch_robots(base: str):
    """Returneaza continutul robots.txt sau None daca lipseste."""
    url = base.rstrip("/") + "/robots.txt"

    try:
        response = fetch(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException:
        return None


def disallowed_paths(robots_text):
    """Extrage valorile directivelor Disallow din robots.txt."""
    if robots_text is None:
        return []

    paths = []

    for line in robots_text.splitlines():
        line = line.strip()

        if line.lower().startswith("disallow:"):
            path = line.split(":", 1)[1].strip()
            paths.append(path)

    return paths


print("\n=== Exercitiul 32 ===")

time.sleep(1)
robots_text = fetch_robots(BASE_URL)

print("Cai interzise:", disallowed_paths(robots_text))
print("Test cu None:", disallowed_paths(None))


# Exercitiul 33. Oricate argumente
def response_times(*urls) -> dict:
    """Masoara timpul de raspuns pentru fiecare URL primit."""
    results = {}

    for i, url in enumerate(urls):
        if i > 0:
            time.sleep(1)

        try:
            start = time.perf_counter()
            fetch(url)
            end = time.perf_counter()

            results[url] = end - start
        except requests.RequestException:
            results[url] = None

    return results


print("\n=== Exercitiul 33 ===")

time.sleep(1)
times = response_times(
    BASE_URL,
    BASE_URL + "/robots.txt"
)

for url, seconds in times.items():
    print(url, ":", seconds, "secunde")


# Exercitiul 34. Argumente cu nume colectate
def log(message: str, **details):
    """Afiseaza un mesaj urmat de detaliile primite."""
    output = message

    for name, value in details.items():
        output += f" | {name}={value}"

    print(output)


print("\n=== Exercitiul 34 ===")

log("verificat", url=BASE_URL, status=200)


# Intrebare de verificare:
# print() afiseaza o valoare in terminal.
# return trimite valoarea inapoi catre codul care
# a apelat functia, pentru a putea fi reutilizata.

print("\n=== Partea 3 finalizata ===")
