import requests
import os
import random
import time
from itertools import cycle
from fake_useragent import UserAgent

def banner():
    print("\033[1;32m")
    print("=================================================")
    print("""     
  █████   ███   █████ █████   ███   █████ █████   ███   █████            ███████████          ███████████            ██████████
░░███   ░███  ░░███ ░░███   ░███  ░░███ ░░███   ░███  ░░███            ░░███░░░░░░█         ░░███░░░░░███          ░░███░░░░░█
 ░███   ░███   ░███  ░███   ░███   ░███  ░███   ░███   ░███             ░███   █ ░   ██████  ░███    ░███   ██████  ░███  █ ░ 
 ░███   ░███   ░███  ░███   ░███   ░███  ░███   ░███   ░███  ██████████ ░███████    ███░░███ ░██████████   ███░░███ ░██████   
 ░░███  █████  ███   ░░███  █████  ███   ░░███  █████  ███  ░░░░░░░░░░  ░███░░░█   ░███ ░███ ░███░░░░░███ ░███ ░░░  ░███░░█   
  ░░░█████░█████░     ░░░█████░█████░     ░░░█████░█████░               ░███  ░    ░███ ░███ ░███    ░███ ░███  ███ ░███ ░   █
    ░░███ ░░███         ░░███ ░░███         ░░███ ░░███                 █████      ░░██████  █████   █████░░██████  ██████████
     ░░░   ░░░           ░░░   ░░░           ░░░   ░░░                 ░░░░░        ░░░░░░  ░░░░░   ░░░░░  ░░░░░░  ░░░░░░░░░░ 
                                                                                                                   By Bo7                         
                                                                            
                                                                            """)
    print("=================================================\033[0m")

def human_delay(min_time=1, max_time=5):
    delay = random.uniform(min_time, max_time)
    time.sleep(delay)

def get_proxy_list(proxy_file):
    if not os.path.isfile(proxy_file):
        print(f"Proxy list file '{proxy_file}' not found!")
        return []
    
    with open(proxy_file, 'r') as file:
        proxies = file.read().splitlines()
    return proxies

def test_proxies(proxies):
    url = "http://httpbin.org/ip"  # Known URL for testing proxies
    working_proxies = []
    failed_proxies = []

    print("\n\033[1;33mTesting proxies...\033[0m")

    for index, proxy in enumerate(proxies):
        try:
            proxy_dict = {"http": proxy, "https": proxy}
            response = requests.get(url, proxies=proxy_dict, timeout=5)
            if response.status_code == 200:
                print(f"\033[1;32m[OK] Proxy working: {proxy}\033[0m")
                working_proxies.append(proxy)
            else:
                print(f"\033[1;31m[FAIL] Proxy returned status code {response.status_code}: {proxy}\033[0m")
                failed_proxies.append((index, proxy, response.status_code))
        except requests.exceptions.RequestException as e:
            print(f"\033[1;31m[FAIL] Proxy error: {e} - {proxy}\033[0m")
            failed_proxies.append((index, proxy, 'Exception'))
        
        # Prompt user to continue if proxy fails
        if failed_proxies:
            user_continue = input("\033[1;33mOne or more proxies have failed. Do you want to continue with the working proxies? (yes/no):\033[0m ").strip().lower()
            if user_continue != 'yes':
                return working_proxies
    
    if failed_proxies:
        print("\n\033[1;31m--- Failed Proxies ---\033[0m")
        for index, proxy, error in failed_proxies:
            print(f"\033[1;31mOrder: {index + 1}, Proxy: {proxy}, Error: {error}\033[0m")

    return working_proxies

def brute_force_directories_files(url, wordlist, use_proxy=False, proxy_file=None, use_user_agent=False, use_delay=False, extensions=None):
    if not os.path.isfile(wordlist):
        print(f"Wordlist file '{wordlist}' not found!")
        return

    with open(wordlist, 'r') as file:
        paths = file.read().splitlines()

    ua = UserAgent() if use_user_agent else None
    
    proxies = get_proxy_list(proxy_file) if use_proxy and proxy_file else []
    proxies = test_proxies(proxies) if proxies else []
    proxy_pool = cycle(proxies) if proxies else None  

    found = []
    
    if not extensions:
        extensions = [
            "html", "php", "txt", "json", "xml", "js", "css",
            "bak", "old", "backup", "log", "tmp",
            "sql", "db", "config", "cfg", "ini", "yml",
            "passwd", "htpasswd", "htaccess",
            "zip", "tar", "gz", "rar", "7z"
        ]

    for path in paths:
        if proxy_pool and proxies:
            try:
                proxy = {"http": next(proxy_pool), "https": next(proxy_pool)}
            except StopIteration:
                proxy = None
        else:
            proxy = None
        
        headers = {'User-Agent': ua.random} if use_user_agent else {}
        
        dir_url = f"{url}/{path}".strip('/').replace(' ', '%20')
        file_urls = [f"{url}/{path}.{ext}".strip('/').replace(' ', '%20') for ext in extensions]

        print(f"Trying directory URL: {dir_url}")
        try:
            response = requests.get(dir_url, headers=headers, proxies=proxy, timeout=5)
            print_status_code(response.status_code, dir_url)
            if response.status_code == 200:
                found.append(dir_url)

        except requests.exceptions.RequestException as e:
            print(f"\033[1;31mRequest failed for {dir_url}:\033[0m {e}")

        for file_url in file_urls:
            print(f"Trying file URL: {file_url}")
            try:
                response = requests.get(file_url, headers=headers, proxies=proxy, timeout=5)
                print_status_code(response.status_code, file_url)
                if response.status_code == 200:
                    found.append(file_url)

            except requests.exceptions.RequestException as e:
                print(f"\033[1;31mRequest failed for {file_url}:\033[0m {e}")
        
        if use_delay:
            human_delay()

    if found:
        print("\n--- Brute-forcing completed ---")
        print("\033[1;32mFound URLs:\033[0m")
        for url in found:
            print(url)
    else:
        print("\n--- Brute-forcing completed ---")
        print("\033[1;31mNo directories or files found.\033[0m")

def print_status_code(status_code, url):
    if status_code == 200:
        print(f"\033[1;32m[200 OK]\033[0m {url}")
    elif status_code in [301, 302, 307]:
        print(f"\033[1;33m[{status_code} Redirect]\033[0m {url}")
    else:
        print(f"\033[1;31m[{status_code}]\033[0m {url}")

def user_input():
    banner()
    
    target_url = input("\033[1;33mEnter target URL (e.g., http://example.com):\033[0m ").strip()
    wordlist_path = input("\033[1;33mEnter path to wordlist:\033[0m ").strip()

    use_proxy = input("\033[1;33mDo you want to use a proxy? (yes/no):\033[0m ").strip().lower() == 'yes'
    proxy_list = None
    if use_proxy:
        proxy_file = input("\033[1;33mEnter path to proxy list:\033[0m ").strip()
        proxy_list = proxy_file

    use_user_agent = input("\033[1;33mDo you want to use a random user-agent? (yes/no):\033[0m ").strip().lower() == 'yes'
    use_delay = input("\033[1;33mDo you want to add a delay between requests? (yes/no):\033[0m ").strip().lower() == 'yes'

    brute_force_directories_files(
        target_url,
        wordlist_path,
        use_proxy=use_proxy,
        proxy_file=proxy_list,
        use_user_agent=use_user_agent,
        use_delay=use_delay
    )

if __name__ == "__main__":
    user_input()
