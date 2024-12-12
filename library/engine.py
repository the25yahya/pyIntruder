import requests
import re

class Engine:
    def __init__(self, wordlist,mode):
        self.wordlist = wordlist
        self.reqs_responses = []  
        self.mode = mode
        self.success_payloads = None

    def fuzz(self, method, url):
        if self.mode == 'fuzzing':
            if method.upper() == 'GET':  
                with open(str(self.wordlist), 'r') as file:
                    for line in file:
                        fuzz_url = url.replace('FUZZ', line.strip()) if 'FUZZ' in url else url
                        req = requests.get(fuzz_url)
                        
                        # Prepare the dictionary to store important details of the request
                        req_details = {
                            'method': req.request.method,
                            'url': req.request.url,
                            'status_code': req.status_code,
                            'headers': dict(req.headers),  
                            'reason': req.reason
                        }
                        content_type = req.headers.get('Content-Type', '').lower()
                        if 'image' in content_type or 'application/octet-stream' in content_type:
                            # Handle binary data (image)
                            req_details['body'] = req.content  # Use the raw binary content
                        else:
                            # Handle textual data (JSON or text)
                            if req.status_code == 200:
                                try:
                                    req_details['body'] = req.json()  # Try to parse as JSON
                                except ValueError:
                                    req_details['body'] = req.text  # Fallback to plain text
                            else:
                                req_details['body'] = req.text  # For non-200 status codes, use text
                        
                        # Print request details 
                        print(f"\033[1;31m[*] Sending request :\033[0m \033[1;32m{req.request.method}\033[0m \033[1;33m{req.request.url}\033[0m")
                        print(f"Status Code: {req.status_code}")
                        
                        # Append the dictionary to the list of responses
                        self.reqs_responses.append(req_details)
        elif self.mode == 'OR':
            url_regex = r'(https?://[^\s]+)'
            self.success_payloads = []
            if method.upper() == 'GET':  
                with open(str(self.wordlist), 'r') as file:
                    for line in file:
                        fuzz_url = url.replace('FUZZ', line.strip()) if 'FUZZ' in url else url
                        req = requests.get(fuzz_url,allow_redirects=True)
                        
                        # Prepare the dictionary to store important details of the request
                        req_details = {
                            'method': req.request.method,
                            'url': req.request.url,
                            'status_code': req.status_code,
                            'headers': dict(req.headers),  
                            'reason': req.reason
                        }
                        
                        match = re.search(url_regex,line)
                        if match:
                            redirect_url = match.group(0)
                        else:
                            redirect_url = None
                        # Print request details 
                        print(f"\033[1;31m[*] Sending request :\033[0m \033[1;32m{req.request.method}\033[0m \033[1;33m{req.request.url}\033[0m")
                        print(f"\031[1;31m[*] payload : {line}, url : {redirect_url}\033[0m")
                        print(f"Status Code: {req.status_code}")

                        if req.history and redirect_url :
                            for resp in req.history:
                                if resp.url == redirect_url:
                                    self.success_payloads.append({
                                        "url" : resp.url,
                                        "payload" : line
                                    })
                        # Append the dictionary to the list of responses
                        self.reqs_responses.append(req_details)
                        print(self.success_payloads)


    def write_output(self, output_file):
        # Writing the collected request details to the output file
        with open(output_file, 'w') as file:
            for req_detail in self.reqs_responses:
                file.write(f"Method: {req_detail['method']}\n")
                file.write(f"URL: {req_detail['url']}\n")
                file.write(f"Status Code: {req_detail['status_code']}\n")
                file.write(f"Reason: {req_detail['reason']}\n")
                file.write(f"Headers: {req_detail['headers']}\n")
                file.write(f"Body: {req_detail['body']}\n")
                file.write("\n" + "="*50 + "\n")
