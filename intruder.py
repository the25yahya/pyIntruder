from library.parser import *
import requests
from library.menu import menu
from library.engine import *
from sys import argv
import threading

script,wordlist = argv

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


request = '''
GET /en/search?query=FUZZ HTTP/2
Host: www.coolblue.be
Cookie: locale=en_US; Coolblue-Session=1c3d6f58cfcd914c060dd15574cc16ff; cookie-preferences=eyJ2ZXJzaW9uIjoiMjAyMzExMDciLCJmdW5jdGlvbmFsIjp0cnVlLCJhbmFseXRpY2FsIjp0cnVlLCJtYXJrZXRpbmciOnRydWV9; _gcl_au=1.1.436679891.1727885962; _ga_ZQZHMR2ZYX=GS1.1.1733858035.8.1.1733859635.49.0.0; _ga=GA1.1.1587225301.1727885962; _ga_YX7ZDWWTDS=GS1.1.1728515192.3.1.1728515448.42.0.0; _pin_unauth=dWlkPVpHSXhaR0prTVRZdE1HWmhOQzAwWW1WaExXSTNORFV0TW1FMllqWmlNVEJqWVdJeQ; _fbp=fb.1.1727886042854.456286720827977410; _ce.s=v~2c944e16389bd3503bcfa9cbf6fcebd4de2bb011~lcw~1733859638819~vir~new~lva~1733858054526~vpv~6~v11.cs~169717~v11.s~f25bb2e0-b72a-11ef-9651-79687fdb4d65~v11.sla~1733859638819~v11.send~1733859639186~lcw~1733859639186; _ga_JC55Z9LD2F=GS1.1.1727916533.1.0.1727916606.0.0.0; Secure-Coolblue=41908634a07b8ee3c42bcae0509a846b; PHPSESSID=vkafnmmpbqbkassacnpvik7sep; assignedVariations=FD4Y42dgybxLHMEroExfa7BF9VgAT9CibTDDsix13Qlo4dSwo5CVtyDuOhIIQJrJgz2e3LK9rwmHWkvGWhiKYjt88NnlRJP8GlLbHOVE4ROKEM1naF1qhslA5tBj4WChJZRBxIv540pOamqnz0N7nw5E4meUsfpNGcz1FKvtXdju48DU3BBCU1B4Bpf6LGfYslxltcAjxgS2kgxaEpfJx7mShxqeZJSLd2v4PVyEFpfaTeqqMbAxKyHBBDESvzA8B794d3Lo51r0Zdw39vaYu3N4; wishListRequested=true; _dd_s=rum=0&expire=1733860535397; pc_gs=6; lantern=a3fc31c0-ebea-4bcf-9fb6-eade378fdd34; cebs=1; _ce.clock_data=1432%2C105.71.5.1%2C1%2Ca69b52f9d7f760edf3fd052bcda2542f%2CFirefox%2CMA; cebsp_=5; seenLanguageEmphasis=1; _uetsid=ee7fe9d0b72a11ef8c672959e42a339d; _uetvid=455b485080da11ef8178cd9bbc67b958
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

'''

req = Request(request)
engine = Engine(wordlist)
threads = []
for i in range(5):
    thread = threading.Thread(target=engine.fuzz, args=(req.method, req.url))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

print("\033[1;33m FINISHED FUZZING")