from library.parser import *
from library.engine import *
from library.lib import *
import argparse
import threading
import sys


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Example script")
    parser.add_argument('-t', '--threads', type=int, help="Number of threads")
    parser.add_argument('-w', '--wordlist', type=str, help="Path to the wordlist file",required=True)
    parser.add_argument('-f', '--file', type=str, help="Path to the requestfile")
    parser.add_argument('-M', '--mode',default='fuzzing', type=str, help='''
    intruder execution mode : 
    for simple fuzzing ignore this arg (simple fuzzing is the default mode)
    for fuzzing in a specific mode use : 
                        -M xss for cross site scripting
                        -M ord for open redirects
                        -M ssti for server side template injection
                        -M sqli for sql injection
                        -M CI for command injection
                        -M PT for path traversal
    ''')
    args = parser.parse_args()

    # Access the values of the arguments
    threads_arg = args.threads
    wordlist = args.wordlist
    choice = args.mode
    if not sys.stdin.isatty():
        request = read_stdin()
    elif args.file:
        request = read_file(args.file)

    if choice =='fuzzing':
        #request = accept_req()
        req = Request(request)
        engine = Engine(wordlist)
        threads = []
        for i in range(threads_arg if threads_arg else 5):
            thread = threading.Thread(target=engine.fuzz, args=(req.method, req.url))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        print("\033[1;33m FINISHED FUZZING")