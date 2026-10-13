
from checker import (
    SITES,
    build_url,
    is_https,
    show_response,
    check_site,
    scan_sites,
    check_headers,
    retry_check,
)


print("\n========== PARTEA 1 ==========")

print("1. build_url:", build_url("example.com", "login"))
print("2. build_url:", build_url("example.com", "/login"))

print("3. is_https:", is_https(SITES[0]))
print("4. is_https:", is_https(SITES[9]))


print("\n========== PARTEA 2 ==========")

print("1. show_response:")
show_response(SITES[0])

print("2. show_response:")
show_response(SITES[9])


print("\n========== PARTEA 3 ==========")

for url in SITES:
    print("check_site:", url)
    print(check_site(url))


print("\n========== PARTEA 4 ==========")

scan_sites()


print("\n========== PARTEA 5 ==========")

print("1. check_headers:")
print(check_headers(SITES[10]))

print("2. check_headers:")
print(check_headers(SITES[11]))

print("3. check_headers - eroare:")
print(check_headers(SITES[9]))


print("\n========== PARTEA 6 ==========")

print("1. retry_check - 200:")
print(retry_check(SITES[3]))

print("2. retry_check - 404:")
print(retry_check(SITES[6]))

print("3. retry_check - 500:")
print(retry_check(SITES[7]))

print("4. retry_check - 500, doua incercari:")
print(retry_check(SITES[7], attempts=2))

print("5. retry_check - site inaccesibil:")
print(retry_check(SITES[9]))

print("\n========== SFARSIT ==========")
