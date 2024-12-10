import threading
from library.parser import *



class BruteforceEngine(Request):
    def __init__(self,request,thread_count=5):
        super().__init__(request)
        self.thread_count=thread_count
        self.lock = threading.Lock()
        self.wordlist = None

    def brute_force(self):

        
        
        while True:
            self.wordlist = input("\033[1;31m[*]Enter wordlist path: \033[0m")
            self.wordlist = self.wordlist.strip('"').strip("'").replace("\\ ", " ")

            if os.path.exists(self.wordlist) and os.path.isfile(self.wordlist):
                break
            else:
                print(f"\033[1;31m[!] Error: The file at {self.wordlist} does not exist or is not a valid file. Please try again.\033[0m")
        
        ## load wordlist
        with open(self.wordlist,"r") as wordlist:
            words = wordlist.read().splitlines()

        ## divide wordlist
        chunk_size = len(words) // self.thread_count
        threads = []
        for i in range(self.thread_count):
            start = i * chunk_size
            end = (i + 1) * chunk_size if i < self.thread_count - 1 else len(words)
            thread_words = words[start:end]
            thread = threading.Thread(target=self._thread_worker, args=(thread_words,))
            threads.append(thread)
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        print("Brute force complete.")

    def _thread_worker(self,words):
        for word in words:
            fuzzed_request = self._generate_fuzzed_request(word)
            self._send_request(fuzzed_request)
    
    def _generate_fuzzed_request(self, fuzz_value):
        """
        Generate a request with the `FUZZ` keyword replaced by the given value.
        """
        fuzz_placeholder = fuzz_value

        # Replace FUZZ in URL query parameters
        fuzzed_url = self.url
        for key, values in self.urlQueryParams.items():
            fuzzed_values = [
                fuzz_placeholder if "FUZZ" in v else v for v in values
            ]
            self.urlQueryParams[key] = fuzzed_values

        # Reconstruct the URL with updated query parameters
        base_url = self.url.split("?")[0]
        query = urlencode(self.urlQueryParams, doseq=True)
        fuzzed_url = f"{base_url}?{query}" if query else base_url

        # Replace FUZZ in headers
        fuzzed_headers = {
            key: value.replace("FUZZ", fuzz_placeholder)
            for key, value in self.headers.items()
        }

        # Replace FUZZ in body
        fuzzed_body = (
            self.body.replace("FUZZ", fuzz_placeholder)
            if self.body else None
        )

        # Reconstructed fuzzed request
        return {
            "method": self.method,
            "url": fuzzed_url,
            "headers": fuzzed_headers,
            "body": fuzzed_body,
        }

    def _send_request(self, fuzzed_request):
        """
        Send the fuzzed request using the `requests` library.
        """
        try:
            response = requests.request(
                method=fuzzed_request["method"],
                url=fuzzed_request["url"],
                headers=fuzzed_request["headers"],
                data=fuzzed_request["body"]
            )
            with self.lock:
                print(f"Response for {fuzzed_request['url']}: {response.status_code}")
        except Exception as e:
            with self.lock:
                print(f"Error sending request: {e}")