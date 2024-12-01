import requests


class Request:
    def __init__(self, request):
        self.request = request
        self.method = None
        self.url = None
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

