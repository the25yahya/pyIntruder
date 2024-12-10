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
        self.parse_request()
        
    
    def parse_request(self):
        ## parsing the http request and setting the attributes
        lines = self.request.strip().split("\n")
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

        #(self.url)



