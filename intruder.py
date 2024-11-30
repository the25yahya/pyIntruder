import requests

def accept_req():
    print("[*] Paste the HTTP request, end with an empty line:")
    user_input = []
    while True:
        line = input()
        if line == "":
            break
        user_input.append(line)
    return user_input

http_req = accept_req()

def parse_http_request(request_lines):
    # List to hold all the tuples
    parsed_data = []

    # List of HTTP methods to check
    http_methods = {"GET", "PUT", "POST", "DELETE", "PATCH", "HEAD", "OPTIONS"}

    for line in request_lines:
        # Skip empty lines
        if not line.strip():
            continue

        # Case 1: If the first word is an HTTP method
        words = line.split(maxsplit=1)
        if words[0] in http_methods:
            method, rest = words
            parsed_data.append((method, rest))

        # Case 2: If a word is followed by ": "
        elif ": " in line:
            key, value = line.split(": ", maxsplit=1)
            parsed_data.append((key, value))
    
    return parsed_data

parsed_req = parse_http_request(http_req)
print(parsed_req)
