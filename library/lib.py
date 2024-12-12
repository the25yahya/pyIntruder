import sys
import threading

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


def start_fuzz(target_func, func_args,output_path,engine, threads_num=None):
        threads = []
        try:
            for i in range(threads_num if threads_num else 5):
                thread = threading.Thread(target=target_func, args=(func_args[0], func_args[1]))
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