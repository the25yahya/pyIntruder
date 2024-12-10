import requests
import os
import html
import base64
from urllib.parse import unquote, quote,urlparse, parse_qs, urlencode
import readline  
import threading
from pathlib import Path
import keyboard


class Request:
    def __init__(self,request):
        self.request = request
        self.method = None
        self.path = None
        self.urlQueryParams = {}
        self.url = None
        self.headers = {}
        self.body = None
        self.parsed_request = []
        self.parse_request(request)
        
    
    def parse_request(self,request):
        ## parsing the http request and setting the attributes
        lines = request.strip().split("\n")
        ## parsing the first line (method , url , protocol)
        request_line = lines[0].strip()
        parts = request_line.split(maxsplit=2)
        self.method = parts[0]
        self.path = parts[1]
        
        self.parsed_request.append(request_line)


        ##parsing the headers
        headers_done = False
        for line in lines[1:]:
            line = line.strip()
            if line == "":
                headers_done = True
                continue
            if not headers_done:
                self.headers[line.split(": ", 1)[0]] = line.split(": ", 1)[1]
                self.parsed_request.append(line)
            else : ##parse the body
                self.body = (self.body or "") + line + "\n"
                self.parsed_request.append(line)
        if self.body:
            self.body = self.body.strip()

        self.url = f"https://{self.headers.get('Host', '')}{self.path}"
        parsed_url = urlparse(self.url)

    def interactive_fuzzing(self):
        # Display the request interactively and let the user wrap terms for fuzzing
        current_index = 0

        while True:
            # Clear the screen and display the parsed request
            print("\033[H\033[J", end="")
            print("Navigate with ↑ and ↓. Press Enter to wrap term with §TERM§. Press Esc to exit.\n")
            for i, line in enumerate(self.parsed_request):
                if i == current_index:
                    print(f"> {line}")
                else:
                    print(f"  {line}")

            key = keyboard.read_event()

            if key.event_type == "down":
                if key.name == "down" and current_index < len(self.parsed_request) - 1:
                    current_index += 1
                elif key.name == "up" and current_index > 0:
                    current_index -= 1
                elif key.name == "enter":
                    # Wrap the selected line or part of it
                    selected_line = self.parsed_request[current_index]
                    print("\nEnter the term you want to wrap:")
                    term_to_wrap = input(f"Line: {selected_line}\n> ")
                    wrapped_line = selected_line.replace(term_to_wrap, f"§{term_to_wrap}§")
                    self.parsed_request[current_index] = wrapped_line
                elif key.name == "esc":
                    # Exit the interactive session
                    break

        # Display the updated request
        print("\nUpdated Request:")
        for line in self.parsed_request:
            print(line)

