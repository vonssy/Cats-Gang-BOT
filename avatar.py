import requests
import os
import time
import threading
from colorama import *
from datetime import datetime
import pytz

wib = pytz.timezone('Asia/Jakarta')

class Cats:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Host': 'api.catshouse.club',
            'Origin': 'https://cats-frontend.tgapps.store',
            'Priority': 'u=1, i',
            'Referer': 'https://cats-frontend.tgapps.store/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'
        }

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def welcome(self):
        print(
            f"""
        {Fore.GREEN + Style.BRIGHT}Auto Claim {Fore.BLUE + Style.BRIGHT}Cats Gang - BOT [Avatar]
            """
            f"""
        {Fore.GREEN + Style.BRIGHT}Rey? {Fore.YELLOW + Style.BRIGHT}<INI WATERMARK>
            """
        )

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
        
    def user(self, query: str, retries=5, delay=3):
        url = 'https://api.catshouse.club/user'
        self.headers.update({
            'Authorization': f'tma {query}',
            'Content-Type': 'application/json'
        })
        
        for attempt in range(retries):
            try:
                response = self.session.get(url, headers=self.headers)
                response.raise_for_status()
                result = response.json()
                if response.status_code == 200:
                    return result
                else:
                    return None
            except (requests.RequestException, ValueError) as e:
                self.log(f"{Fore.YELLOW+Style.BRIGHT}Failed to Connect to Server (Retrying {attempt + 1}/{retries}){Style.RESET_ALL}")
                time.sleep(delay)
        self.log(f"{Fore.RED+Style.BRIGHT}All Attempts Failed. Connection Problem or Query is Expired{Style.RESET_ALL}")
        return None
    
    def avatar(self, query: str, retries=5, delay=3):
        url = 'https://api.catshouse.club/user/avatar'
        self.headers.update({
            'Authorization': f'tma {query}',
            'Content-Type': 'application/json'
        })

        for attempt in range(retries):
            try:
                response = self.session.get(url, headers=self.headers)
                response.raise_for_status()
                result = response.json()
                if response.status_code == 200:
                    return result
                else:
                    return None
            except (requests.RequestException, ValueError) as e:
                self.log(f"{Fore.YELLOW+Style.BRIGHT}Failed to Connect to Server (Retrying {attempt + 1}/{retries}){Style.RESET_ALL}")
                time.sleep(delay)
        self.log(f"{Fore.RED+Style.BRIGHT}All Attempts Failed. Connection Problem or Query is Expired{Style.RESET_ALL}")
        return None

    def upgrade_avatar(self, query: str, image_filename: str): 
        url = 'https://api.catshouse.club/user/avatar/upgrade'
        
        image_path = os.path.abspath(os.path.join('image', image_filename))

        if not os.path.exists(image_path):
            self.log(f"{Fore.RED + Style.BRIGHT}[ 'image/' Folder or Image File not found: {image_path}{Style.RESET_ALL}")
            return None

        with open(image_path, 'rb') as image_file:
            files = {
                'photo': image_file
            }

            self.headers.pop('Content-Type', None)
            self.headers.update({
                'Authorization': f'tma {query}'
            })

            try:
                print(f"{Fore.YELLOW + Style.BRIGHT}[ Uploading Avatar..... ]{Style.RESET_ALL}", end="\r", flush=True)
                time.sleep(3)
                response = self.session.post(url, headers=self.headers, files=files)

                result = response.json()

                if response.status_code == 200:
                    self.log(
                        f"{Fore.MAGENTA + Style.BRIGHT}[ Avatar{Style.RESET_ALL}"
                        f"{Fore.GREEN + Style.BRIGHT} is Uploaded Successfully {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}] [ Reward{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} {result['rewards']} {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}CATS ]{Style.RESET_ALL}"
                    )
                    return result
                else:
                    self.log(
                        f"{Fore.MAGENTA + Style.BRIGHT}[ Avatar{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} is Already Uploaded Today {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                    )
                    return None
                
            except (requests.RequestException, ValueError) as e:
                self.log(f"{Fore.RED+Style.BRIGHT}[ Query Expired or Failure Uploading: {e}")
                return None

    def avatar_background(self, query: str, image_filename: str):
        thread = threading.Thread(target=self.upgrade_avatar, args=(query, image_filename))
        thread.start()
        thread.join()

    def process_query(self, query: str, image_filename: str):
        try:
            user = self.user(query)
            if user:
                self.log(
                    f"{Fore.MAGENTA+Style.BRIGHT}[ Account{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {user['firstName']} {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} | {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}[ Balance{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {user['totalRewards']} {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}CATS ]{Style.RESET_ALL}"
                )

                avatar = self.avatar(query)
                if avatar:
                    self.avatar_background(query, image_filename)
                else:
                    print(avatar)

            else:
                self.log(f"{Fore.YELLOW+Style.BRIGHT}[ Failed to Fetching This Account ]{Style.RESET_ALL}")
        except (requests.RequestException, ValueError) as e:
            self.log(f"{Fore.RED+Style.BRIGHT}Error: {e}")
            return None

    def main(self):
        try:
            image_filename = input("Enter the avatar filename in the 'image/' folder (ex: cats.jpg): ").strip()

            with open('query.txt', 'r') as file:
                queries = [line.strip() for line in file if line.strip()]

            while True:
                self.clear_terminal()
                self.welcome()
                self.log(
                    f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{len(queries)}{Style.RESET_ALL}"
                )
                self.log(f"{Fore.CYAN + Style.BRIGHT}---------------------------------------------------{Style.RESET_ALL}")

                for query in queries:
                    query = query.strip()
                    if query:
                        print(f"{Fore.YELLOW + Style.BRIGHT}[ Getting User Token... ]{Style.RESET_ALL}", end="\r", flush=True)
                        time.sleep(2)
                        self.process_query(query, image_filename)
                        self.log(f"{Fore.CYAN + Style.BRIGHT}---------------------------------------------------{Style.RESET_ALL}")

                seconds = 1800
                while seconds > 0:
                    formatted_time = self.format_seconds(seconds)
                    print(
                        f"{Fore.CYAN+Style.BRIGHT}[ Wait for{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {formatted_time} {Style.RESET_ALL}"
                        f"{Fore.CYAN+Style.BRIGHT}... ]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(1)
                    seconds -= 1

        except KeyboardInterrupt:
            self.log(f"{Fore.RED + Style.BRIGHT}[ EXIT ] Cats Gang - BOT{Style.RESET_ALL}")
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}An error occurred: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    cats = Cats()
    cats.main()