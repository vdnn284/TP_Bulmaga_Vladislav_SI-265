
# Laborator: funcții, metode și importuri pe web
# Student: Bulmaga Vladislav

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde
DEFAULT_HEADERS = {"User-Agent": "WebLab-BulmagaVladislav"}

import requests
import csv
import time
from datetime import datetime
from urllib.parse import urljoin
import socket
import ssl
import re
from urllib.parse import urlparse


def fetch(url, timeout=TIMEOUT):
    """Descarca o pagina web si returneaza raspunsul HTTP."""
    return requests.get(
        url,
        timeout=timeout,
        headers=DEFAULT_HEADERS
    )


def get_status(url):
    """Returneaza codul HTTP al unei pagini."""
    return fetch(url).status_code


def get_title(html):
    """Extrage titlul din codul HTML al unei pagini."""
    start = html.lower().find("<title>")
    end = html.lower().find("</title>")

    if start == -1 or end == -1 or end < start:
        return ""

    start += len("<title>")
    return html[start:end].strip()


def security_headers(url):
    """Verifica prezenta a cinci antete de securitate HTTP."""
    names = [
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Referrer-Policy"
    ]

    response = fetch(url)

    return {
        name: name in response.headers
        for name in names
    }

# Exercitiul 49. Raport CSV

def check_paths(base, paths):
    """Verifica adresele indicate si returneaza rezultatele."""
    results = []

    for index, path in enumerate(paths):
        url = urljoin(base, path)

        try:
            response = fetch(url)
            status = response.status_code
        except requests.RequestException:
            status = "Eroare"

        results.append((url, status))

        if index < len(paths) - 1:
            time.sleep(1)

    return results


def write_csv_report(base, paths, filename):
    """Salveaza rezultatele verificarii intr-un fisier CSV."""
    results = check_paths(base, paths)

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(["path", "status", "checked_at"])

        for (url, status) in results:
            path = urlparse(url).path or "/"

            writer.writerow([
                path,
                status,
                datetime.now().isoformat()
            ])

    return filename


# Exercitiul 50. Raport complet despre site


def site_report(url):
    """Genereaza un raport complet despre un site web."""
    parsed = urlparse(url)
    host = parsed.hostname

    if parsed.scheme != "https" or not host:
        raise ValueError("Introduceti un URL HTTPS valid.")

    # 1. Codul HTTP si URL-ul final
    response = fetch(url)
    response.raise_for_status()
    final_url = response.url

    # 2. Titlul paginii
    title = get_title(response.text)

    # 3. Adresa IP
    try:
        ip = socket.gethostbyname(host)
    except OSError:
        ip = None

    # 4. Redirectionari pornind de la HTTP
    time.sleep(1)
    http_url = "http://" + host

    try:
        redirect_response = fetch(http_url)

        redirect_chain = [
            {
                "status": item.status_code,
                "url": item.url
            }
            for item in redirect_response.history
        ]

        redirect_chain.append({
            "status": redirect_response.status_code,
            "url": redirect_response.url
        })

    except requests.RequestException:
        redirect_chain = []

    # 5. Scorul antetelor de securitate
    time.sleep(1)
    headers_result = security_headers(final_url)

    security_score = (
        f"{sum(headers_result.values())}/{len(headers_result)}"
    )

    # 6. Zile ramase pana la expirarea certificatului
    try:
        context = ssl.create_default_context()

        with socket.create_connection(
            (host, 443), timeout=TIMEOUT
        ) as sock:
            with context.wrap_socket(
                sock, server_hostname=host
            ) as secure:
                secure.settimeout(TIMEOUT)
                cert = secure.getpeercert()

        expiration = ssl.cert_time_to_seconds(
            cert["notAfter"]
        )

        cert_days_left = int(
            (expiration - time.time()) // 86400
        )

    except (OSError, ssl.SSLError, ValueError, KeyError):
        cert_days_left = None

    # 7. Linkuri interne si externe
    links = re.findall(
        r"""href\s*=\s*["']([^"']+)["']""",
        response.text,
        flags=re.IGNORECASE
    )

    internal = set()
    external = set()

    final_host = urlparse(final_url).hostname

    for link in links:
        absolute = urljoin(final_url, link)
        link_parsed = urlparse(absolute)

        if link_parsed.scheme not in ("http", "https"):
            continue

        if link_parsed.hostname == final_host:
            internal.add(absolute)
        else:
            external.add(absolute)

    # 8. Caile interzise din robots.txt
    time.sleep(1)
    robots_url = urljoin(final_url, "/robots.txt")

    try:
        robots_response = fetch(robots_url)
        robots_response.raise_for_status()

        robots_disallowed = []

        for line in robots_response.text.splitlines():
            line = line.split("#", 1)[0].strip()

            if line.lower().startswith("disallow:"):
                path = line.split(":", 1)[1].strip()

                if path:
                    robots_disallowed.append(path)

    except requests.RequestException:
        robots_disallowed = []

    return {
        "url": url,
        "final_url": final_url,
        "status": response.status_code,
        "title": title,
        "ip": ip,
        "redirect_chain": redirect_chain,
        "security_score": security_score,
        "cert_days_left": cert_days_left,
        "internal_links": sorted(internal),
        "external_links": sorted(external),
        "robots_disallowed": robots_disallowed
    }




# Exercitiul 46. Blocul main
if __name__ == "__main__":
    print("Autotest:", get_status(BASE_URL))
