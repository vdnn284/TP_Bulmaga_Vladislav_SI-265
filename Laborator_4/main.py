
# Laborator: functii, metode si importuri pe web
# Student: Bulmaga Vladislav

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

import webtools
from webtools import get_title, security_headers, DEFAULT_HEADERS
import time
import argparse
import json


# Exercitiul 48. Argumente din linia de comanda
parser = argparse.ArgumentParser(
    description="Analiza unei pagini web"
)

parser.add_argument(
    "url",
    nargs="?",
    default=BASE_URL,
    help="Adresa site-ului pentru analiza"
)

args = parser.parse_args()
url = args.url

print("\n=== Exercitiul 48 ===")
print("URL introdus:", url)


# Exercitiul 44. Importarea propriului modul
print("\n=== Exercitiul 44 ===")

response = webtools.fetch(url)
title = webtools.get_title(response.text)

print("Titlul paginii:", title)
print("Cod HTTP:", response.status_code)


# Exercitiul 45. Importarea anumitor functii
print("\n=== Exercitiul 45 ===")

# Importul selectiv permite apelarea functiilor
# fara a scrie numele modulului webtools.
#
# Daca definim aici o functie proprie get_title(),
# aceasta va inlocui numele importat in main.py.
# webtools.get_title() ramane disponibil.

print("Titlu extras direct:", get_title(response.text))

time.sleep(1)
results = security_headers(url)

print("Antete de securitate:")

for name, present in results.items():
    print(name, ":", present)


# Exercitiul 46. Blocul main
# Autotestul se executa numai cand rulam direct webtools.py.
# Cand importam webtools in acest fisier, autotestul nu ruleaza.


# Exercitiul 47. Constante de modul
print("\n=== Exercitiul 47 ===")
print("DEFAULT_HEADERS:", DEFAULT_HEADERS)


# Exercitiul 49. Generarea raportului CSV
print("\n=== Exercitiul 49 ===")

paths = ["/", "/robots.txt", "/sitemap.xml"]

time.sleep(1)

filename = webtools.write_csv_report(
    url,
    paths,
    "report.csv"
)

print("Fisier creat:", filename)
print("Primele 3 linii:")

with open(filename, "r", encoding="utf-8") as file:
    for index, line in enumerate(file):
        if index == 3:
            break
        print(line.strip())


# Exercitiul 50. Raport final JSON
print("\n=== Exercitiul 50 ===")

time.sleep(1)
report = webtools.site_report(url)

with open("report.json", "w", encoding="utf-8") as file:
    json.dump(report, file, indent=2, ensure_ascii=False)

print("=== Raport site:", url, "===")
print("Cod de stare:", report["status"])
print("URL final:", report["final_url"])
print("Titlu:", report["title"])
print("Adresa IP:", report["ip"])

print("Redirectionari:")
if report["redirect_chain"]:
    for item in report["redirect_chain"]:
        print(" ", item["status"], "->", item["url"])
else:
    print("  Nu au fost obtinute redirectionari.")

print("Scor securitate:", report["security_score"])
print("Certificat SSL - zile ramase:", report["cert_days_left"])
print("Linkuri interne:", len(report["internal_links"]))
print("Linkuri externe:", len(report["external_links"]))
print("Cai interzise:", report["robots_disallowed"])

print("Salvat in report.json")
print("\n=== Laborator finalizat ===")
