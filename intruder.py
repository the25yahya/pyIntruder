from library.parser import *
import requests

if __name__ == '__main__':
    def accept_req():
        print("[*] Paste the HTTP request, end with an empty line:")
        user_input = []
        while True:
            line = input()
            if line == "":
                break
            user_input.append(line)
        return "\n".join(user_input)  # Join lines into a single string

    # Accept HTTP request
    http_req = accept_req()

    # Initialize the Request class and parse the request
    req = Request(http_req)
    print("HTTP Method:", req.method)
    print("URL:", req.url)
    print("Headers:", req.headers)
