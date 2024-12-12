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
    parser.add_argument('-o', '--output', type=str, help="Path to the write results")
    parser.add_argument('--http', action='store_true', help="use http instead of https")
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
                        -M OR for open redirect
    ''')
    args = parser.parse_args()

    # Access the values of the arguments
    threads_arg = args.threads
    output_path = args.output
    wordlist = args.wordlist
    choice = args.mode
    http_true = args.http if args.http else None

    if not sys.stdin.isatty():
        request = read_stdin()
    elif args.file:
        request = read_file(args.file)

    if choice =='fuzzing':
        #request = accept_req()
        req = Request(request,http_true,mode='fuzzing')
        engine = Engine(wordlist)
        threads = []
        try:
            for i in range(threads_arg if threads_arg else 5):
                thread = threading.Thread(target=engine.fuzz, args=(req.method, req.url))
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()

        except KeyboardInterrupt:
            print("\nProcess interrupted. Saving results...")
            engine.write_output(output_path if output_path else "pyIntruder_results.txt")
            sys.exit(0)  # Exit cleanly after saving results
        engine.write_output(output_path if output_path else "pyIntruder_results.txt")
        print("\033[1;33m FINISHED FUZZING")
    
    elif choice == 'OR':
        pass