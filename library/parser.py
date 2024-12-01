import requests
import os
import html
import base64
from urllib.parse import unquote, quote,urlparse, parse_qs
import readline  # Enable path autocompletion
from pathlib import Path


class Request:
    def __init__(self, request):
        self.request = request
        self.method = None
        self.url = None
        self.urlQueryParams = {}
        self.headers = {}
        self.body = None
        self.parse_request(request)  # Automatically parse the request

    def parse_request(self, request):
        """
        Parse the raw HTTP request and set the class attributes.
        """
        # Split the request into lines
        lines = request.strip().split("\n")
        
        # Parse the first line (method, URL, and protocol)
        request_line = lines[0].strip()
        parts = request_line.split(maxsplit=2)
        if len(parts) >= 2:
            self.method, self.url = parts[:2]
            parsed_url = urlparse(self.url)
            self.urlQueryParams = {
                key: [unquote(v) for v in values]
                for key, values in parse_qs(parsed_url.query).items()
            }
        
        # Parse headers and body
        headers_done = False
        for line in lines[1:]:
            line = line.strip()
            
            # Empty line indicates the start of the body
            if line == "":
                headers_done = True
                continue
            
            if not headers_done:  # Parse headers
                if ": " in line:
                    key, value = line.split(": ", 1)
                    self.headers[key] = value
            else:  # Parse body
                self.body = (self.body or "") + line + "\n"
        
        # Trim the body
        if self.body:
            self.body = self.body.strip()

class BruteForceEngine(Request):
    def __init__(self, request):
        super().__init__(request) 
        self.wordlist = None# Inherit parsed data from Request
    
    def _autocomplete(self, text, state):
        """
        Autocomplete file paths.
        """
        directory, _, partial_filename = text.rpartition('/')
        if not directory:
            directory = '.'
        
        # List files and directories in the specified directory
        try:
            matches = [f for f in os.listdir(directory) if f.startswith(partial_filename)]
            return os.path.join(directory, matches[state]) if state < len(matches) else None
        except FileNotFoundError:
            return None
    
    def brute_force(self):
        # Enable autocomplete for file paths
        readline.set_completer(self._autocomplete)
        readline.parse_and_bind("tab: complete")

        while True:
            self.wordlist = input("\033[1;31m[*]Enter wordlist path: \033[0m")
            # Check if the file exists at the given path
            if os.path.exists(self.wordlist) and os.path.isfile(self.wordlist):
                break  # Exit the loop if file is valid
            else:
                print(f"\033[1;31m[!] Error: The file at {self.wordlist} does not exist or is not a valid file. Please try again.\033[0m")

        # Proceed with brute-forcing logic using the valid wordlist
        print("Brute forcing the URL with query parameters:", self.urlQueryParams)
        # Use self.urlQueryParams for brute-forcing or any other logic