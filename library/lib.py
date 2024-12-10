import sys

def accept_req():
        print("\033[1;31m[*] Paste the HTTP request(use FUZZ as a placeholder for the sentence you want to fuzz), end with an empty line:\033[0m")
        user_input = []
        while True:
            line = input()
            if line == "":
                break
            user_input.append(line)
        return "\n".join(user_input)  

def read_stdin():
    req = []
    for line in sys.stdin:
        req.append(line.strip())  
    return "\n".join(req)  

def read_file(file_path):
    with open(file_path,'r') as file :
         request = file.read()
    return request