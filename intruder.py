from library.parser import *
import requests

if __name__ == '__main__':
    def accept_req():
        print("\033[1;31m[*] Paste the HTTP request, end with an empty line:\033[0m")
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

    pyIntruder_mode = input('''\033[1;31m[*]Req has been parsed... choose a mode for pyIntruder (Enter 1 or 2): \033[0m
          \033[3;34m1- Brute Force\033[0m
          \033[3;34m2- Repeater\033[0m
                    : ''')
    if pyIntruder_mode == '1':
        mode = BruteForceEngine(req.request)
        mode.brute_force()