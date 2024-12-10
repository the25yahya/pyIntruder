from library.parser import *
import requests
from library.menu import menu

if __name__ == '__main__':
    def accept_req():
        print("\033[1;31m[*] Paste the HTTP request(use FUZZ as a placeholder for the sentence you want to fuzz), end with an empty line:\033[0m")
        user_input = []
        while True:
            line = input()
            if line == "":
                break
            user_input.append(line)
        return "\n".join(user_input)  # Join lines into a single string

