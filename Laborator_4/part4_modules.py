
# Laborator: funcții, metode și importuri pe web
# Student: Bulmaga Vladislav

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

import requests
import time
import re
import hashlib
import json
import socket
import ssl

from datetime import datetime, timezone
from urllib.parse import urlparse, urljoin
from html.parser import HTMLParser


# Exercitiul 35. Descompunerea unui URL
def parse_url(url):
    """Descompune un URL in componentele sale."""
    return urlparse(url)


print("\n=== Exercitiul 35 ===")

parsed = parse_url("https://cybercor.org/path?x=1#top")

print("Scheme:", parsed.scheme)
print("Netloc:", parsed.netloc)
print("Path:", parsed.path)
print("Query:", parsed.query)
print("Fragment:", parsed.fragment)


# Exercitiul 36. Compunerea URL-urilor
def make_absolute_links(base, links):
    """Transforma legaturile relative in URL-uri absolute."""
    return [urljoin(base, link) for link in links]


print("\n=== Exercitiul 36 ===")

relative_links = ["/about", "contact.html", "../index.html"]
absolute_links = make_absolute_links(BASE_URL, relative_links)

for relative, absolute in zip(relative_links, absolute_links):
    print(relative, "->", absolute)


# Descarcam pagina o singura data pentru exercitiile 37-39.
print("\n=== Descarcarea paginii HTML ===")

response = requests.get(BASE_URL, timeout=TIMEOUT)
response.raise_for_status()
html = response.text

print("Cod HTTP:", response.status_code)


# Exercitiul 37. Extragerea legaturilor
def extract_links(html):
    """Extrage legaturile href fara duplicate."""
    links = re.findall(r'href="([^"]+)"', html)
    return list(dict.fromkeys(links))


print("\n=== Exercitiul 37 ===")

links = extract_links(html)

print("Numarul legaturilor unice:", len(links))

for link in links:
    print(link)


# Exercitiul 38. Legaturi interne si externe
def split_links(links, domain):
    """Separa legaturile interne de cele externe."""
    internal = []
    external = []

    base_domain = urlparse(domain).netloc

    for link in links:
        full_url = urljoin(domain, link)

        if urlparse(full_url).scheme not in ("http", "https"):
            continue

        link_domain = urlparse(full_url).netloc

        if link_domain == base_domain:
            internal.append(full_url)
        else:
            external.append(full_url)

    return internal, external


print("\n=== Exercitiul 38 ===")

internal, external = split_links(links, BASE_URL)

print("Legaturi interne:", len(internal))
for link in internal:
    print(link)

print("Legaturi externe:", len(external))
for link in external:
    print(link)


# Exercitiul 39. Propriile metode
class ImageFinder(HTMLParser):
    """Parser HTML care colecteaza sursele imaginilor."""

    def __init__(self):
        """Initializeaza lista imaginilor."""
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        """Prelucreaza fiecare tag HTML de deschidere."""
        if tag.lower() == "img":
            src = dict(attrs).get("src")

            if src is not None:
                self.images.append(src)


print("\n=== Exercitiul 39 ===")

# Testam mai intai parserul pe HTML cunoscut.
test_html = """
<html><body>
  <img src="/logo.png" alt="Logo">
  <IMG SRC="poza.jpg">
  <img alt="imagine fara src">
  <img src="https://cdn.example.com/banner.webp" />
  <a href="/despre">Aceasta nu este o imagine</a>
</body></html>
"""

test_finder = ImageFinder()
test_finder.feed(test_html)

print("Imagini din test:", test_finder.images)

assert test_finder.images == [
    "/logo.png",
    "poza.jpg",
    "https://cdn.example.com/banner.webp"
], "Parserul nu a gasit exact imaginile asteptate"

print("Testul a trecut!")

# Aplicam parserul pe pagina reala.
finder = ImageFinder()
finder.feed(html)

print("Imagini gasite pe site:", len(finder.images))

for src in finder.images:
    print(src)

print("Numar tag-uri <img:", html.lower().count("<img"))

# Metoda handle_starttag() este apelata automat
# de HTMLParser atunci cand folosim feed().


# Exercitiul 40. Amprenta paginii
def page_fingerprint(url):
    """Calculeaza amprenta SHA256 a continutului unei pagini."""
    response = requests.get(url, timeout=TIMEOUT)
    response.raise_for_status()

    return hashlib.sha256(response.content).hexdigest()


print("\n=== Exercitiul 40 ===")

time.sleep(1)
fingerprint1 = page_fingerprint(BASE_URL)

time.sleep(1)
fingerprint2 = page_fingerprint(BASE_URL)

print("Prima amprenta:", fingerprint1)
print("A doua amprenta:", fingerprint2)
print("Sunt identice:", fingerprint1 == fingerprint2)

# Amprentele pot fi diferite daca se modifica
# continutul paginii intre cele doua descarcari.


# Exercitiul 41. Salvarea in JSON
def save_headers(headers, filename):
    """Salveaza antetele HTTP intr-un fisier JSON."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(dict(headers), file, indent=2)


def load_headers(filename):
    """Citeste antetele salvate intr-un fisier JSON."""
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


print("\n=== Exercitiul 41 ===")

save_headers(response.headers, "headers.json")
loaded_headers = load_headers("headers.json")

print("Fisier creat: headers.json")
print("Server:", loaded_headers.get("Server", "lipsește"))


# Exercitiul 42. Interogare DNS
def resolve(hostname):
    """Returneaza adresa IPv4 a unui domeniu."""
    return socket.gethostbyname(hostname)


print("\n=== Exercitiul 42 ===")

try:
    ip_address = resolve("cybercor.org")
    print("Adresa IP:", ip_address)
except socket.gaierror as error:
    print("Eroare DNS:", error)


# Exercitiul 43. Expirarea certificatului SSL
def cert_days_left(hostname):
    """Returneaza numarul de zile pana la expirarea certificatului."""
    context = ssl.create_default_context()

    with socket.create_connection((hostname, 443), timeout=TIMEOUT) as sock:
        with context.wrap_socket(
            sock,
            server_hostname=hostname
        ) as secure_socket:

            secure_socket.settimeout(TIMEOUT)
            certificate = secure_socket.getpeercert()
            expiration = certificate["notAfter"]

    expiration_timestamp = ssl.cert_time_to_seconds(expiration)
    expiration_date = datetime.fromtimestamp(
        expiration_timestamp,
        tz=timezone.utc
    )

    now = datetime.now(timezone.utc)
    remaining = expiration_date - now

    return remaining.days


print("\n=== Exercitiul 43 ===")

try:
    days = cert_days_left("cybercor.org")
    print("Zile ramase pana la expirare:", days)
except (OSError, ssl.SSLError, KeyError, ValueError) as error:
    print("Nu s-a putut verifica certificatul:", error)


print("\n=== Partea 4 finalizata ===")
