import requests


class Engine:
    def __init__(self,wordlist):
        self.wordlist = wordlist

    def fuzz(self,method,url):
        if method == 'GET' or method == 'get':
            with open(str(self.wordlist),'r') as file:
                for line in file:
                    fuzz_url = url.replace('FUZZ',line) if 'FUZZ' in url else url
                    req = requests.get(fuzz_url)
                    print(f"\033[1;31m[*] Sending request :\033[0m \033[1;32m{req.request.method}\033[0m \033[1;33m{req.request.url}\033[0m")
                    print(req.status_code)
