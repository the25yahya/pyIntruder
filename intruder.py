from library.parser import *
from library.engine import *
from library.lib import *
import argparse
import threading
import sys


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="python fuzzer")
    parser.add_argument('-t', '--threads', type=int, help="Number of threads",default=5)
    parser.add_argument('-w', '--wordlist', type=str, help="Path to the wordlist file",required=True)
    parser.add_argument('-f', '--file', type=str, help="Path to the requestfile")
    parser.add_argument('-o', '--output', type=str, help="Path to the write results")
    parser.add_argument('--http', action='store_true', help="use http instead of https")

    # add subparsers
    subparsers = parser.add_subparsers(dest="mode")
    xss_subparser = subparsers.add_parser("xss",help="xss mode")
    open_redirect_subpsarser = subparsers.add_parser("OR",help="open redirect mode")
    ssti_subparser = subparsers.add_parser("ssti",help="ssti mode")


    args = parser.parse_args()

    # Access the values of the arguments
    threads_arg = args.threads
    output_path = args.output
    wordlist = args.wordlist
    wordlist_length = len(wordlist)
    choice = args.mode
    http_true = args.http if args.http else None

    if not sys.stdin.isatty():
        request = read_stdin()
    elif args.file:
        request = read_file(args.file)
    else:
        parser.error("Either provide input via stdin or specify a file with --file")

    if args.mode == "OR":
        req = Request(request,http_true)
        engine = Engine(wordlist,mode='OR')
        start_fuzz(engine.fuzz,[req.method,req.url],output_path,engine,wordlist_length,threads_arg if threads_arg else None)
    else :
        req = Request(request,http_true)
        engine = Engine(wordlist,mode='fuzzing')
        start_fuzz(engine.fuzz,[req.method,req.url],output_path,engine,wordlist_length,threads_arg if threads_arg else None)
    
