
import requests

SITES = [
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


# Partea 1
def build_url(host, path):
    return "https://" + host + "/" + path.lstrip("/")


def is_https(url):
    return url.startswith("https://")


# Partea 2
def show_response(url):
    try:
        response = requests.get(url, timeout=5)
        print("Status:", response.status_code)
        print("Content-Type:", response.headers.get("Content-Type", "unknown"))
    except requests.RequestException as error:
        print("Eroare:", str(error))


# Partea 3
def check_site(url):
    try:
        response = requests.get(url, timeout=5)
        return {
            "status": response.status_code,
            "content_type": response.headers.get("Content-Type", "unknown"),
            "length": len(response.content),
            "server": response.headers.get("Server", "unknown"),
        }
    except requests.RequestException as error:
        return {
            "status": None,
            "error": str(error),
        }


# Partea 4
def scan_sites():
    results = []

    for url in SITES:
        result = check_site(url)
        results.append((url, result))

    successful = [
        (url, result)
        for url, result in results
        if result["status"] == 200
    ]

    successful.sort(
        key=lambda item: item[1]["length"],
        reverse=True
    )

    for url, result in successful:
        print(
            f"{url} -> {result['status']}, "
            f"{result['length']} octeti"
        )

    print(
        f"Reusite: {len(successful)} | "
        f"Esuate: {len(results) - len(successful)}"
    )


# Partea 5
def check_headers(url):
    try:
        response = requests.get(url, timeout=5)

        present = []
        missing = []

        for header in SECURITY_HEADERS:
            if header.lower() in {
                name.lower() for name in response.headers
            }:
                present.append(header)
            else:
                missing.append(header)

        score = int(
            len(present) * 100 / len(SECURITY_HEADERS)
        )

        return {
            "present": present,
            "missing": missing,
            "score": score,
        }

    except requests.RequestException as error:
        return {
            "status": None,
            "error": str(error),
        }


# Partea 6
def retry_check(url, attempts=3):
    if attempts <= 0:
        return {
            "status": None,
            "attempts": 0,
            "error": "Numarul de incercari trebuie sa fie pozitiv",
        }

    last_status = None
    last_error = None

    for number in range(1, attempts + 1):
        try:
            response = requests.get(url, timeout=5)
            last_status = response.status_code
            last_error = None

            if last_status < 500:
                return {
                    "status": last_status,
                    "attempts": number,
                }

        except requests.RequestException as error:
            last_error = str(error)

    result = {
        "status": last_status,
        "attempts": attempts,
    }

    if last_status is None and last_error is not None:
        result["error"] = last_error

    return result
