import os
import sys
import time
import getpass
import hashlib
import zipfile
from pathlib import Path
from itertools import cycle
from rich.console import Console
from rich.panel import Panel
from time import sleep
from colorama import Fore, init

# Initialize
init(autoreset=True)
console = Console()
colors = cycle([Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.CYAN, Fore.MAGENTA, Fore.BLUE])

# Constants
CORRECT_PASSWORD_HASH = "12ac0460c44b1523f0213f9ab4fe320c716a7841d77dce1690d5ebfa51fb6a4c"

# Banner Art
ascii_banner = '''

 ██████╗██╗   ██╗██████╗ ███████╗██████╗                            
██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗                           
██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝                           
██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗                           
╚██████╗   ██║   ██████╔╝███████╗██║  ██║                           
 ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝                           
                                                                    
███████╗ ██████╗ █████╗ ███╗   ██╗███╗   ██╗███████╗██████╗ ███████╗
██╔════╝██╔════╝██╔══██╗████╗  ██║████╗  ██║██╔════╝██╔══██╗██╔════╝
███████╗██║     ███████║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝███████╗
╚════██║██║     ██╔══██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗╚════██║
███████║╚██████╗██║  ██║██║ ╚████║██║ ╚████║███████╗██║  ██║███████║
╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚══════╝
                                                                    
███████╗██╗██████╗                                                  
╚══███╔╝██║██╔══██╗                                                 
  ███╔╝ ██║██████╔╝                                                 
 ███╔╝  ██║██╔═══╝                                                  
███████╗██║██║                                                      
╚══════╝╚═╝╚═╝                                                      
                                                                    
 ██████╗██████╗  █████╗  ██████╗██╗  ██╗                            
██╔════╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝                            
██║     ██████╔╝███████║██║     █████╔╝                             
██║     ██╔══██╗██╔══██║██║     ██╔═██╗                             
╚██████╗██║  ██║██║  ██║╚██████╗██║  ██╗                            
 ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝                            
                                                                    

'''

zip_crack_scene = '''
🔓 ZIP CRACK STARTING...
[==                    ] 10%
[========              ] 45%
[==================    ] 85%
[====================>] 100%
✔ ZIP CRACK SUCCESS!
'''

payload_scene = '''
🚀 PASSWORD CRACKING START...
[▓▓                    ] 20%
[▓▓▓▓▓▓                ] 50%
[▓▓▓▓▓▓▓▓▓▓▓           ] 75%
[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓] 100%
✔ PASSWORD CRACKING FILE CREATED SUCCESS!
'''

access_scene = '''
🟢 ACCESS GRANTED
Welcome to the secure system.
> Decrypting files...
> Extracting secrets...
> Mission complete.
'''

# Utils
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_ascii_blink(ascii_art, repeat=6, delay=0.25):
    for _ in range(repeat):
        clear()
        print(next(colors) + ascii_art)
        time.sleep(delay)

def typewriter(text, delay=0.04):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def hacker_intro():
    clear()
    print("\033[1;32mInitializing Secure Tool...\033[0m")
    time.sleep(1)
    print("\033[1;31m[🔐] Access Restricted\033[0m")
    time.sleep(1)
    print("\033[1;36m[🧠] Authentication Required...\033[0m")
    time.sleep(1)

def get_password():
    print("\n\033[1;33mEnter Password to Continue:\033[0m")
    return getpass.getpass(">> ")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def launch_visuals():
    show_ascii_blink(ascii_banner)
    clear()
    typewriter(Fore.LIGHTGREEN_EX + zip_crack_scene)
    time.sleep(1)
    clear()
    typewriter(Fore.LIGHTYELLOW_EX + payload_scene)
    time.sleep(1)
    clear()
    typewriter(Fore.LIGHTCYAN_EX + access_scene)
    time.sleep(1)

# ZIP Cracker Class
class ZipPasswordCracker:
    def __init__(self, zip_path, wordlist_path):
        self.zip_path = Path(zip_path).resolve()
        self.wordlist_path = Path(wordlist_path).resolve()
        self.extract_dir = self.zip_path.parent / f"{self.zip_path.stem}_extracted"

    def is_encrypted(self):
        try:
            with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
                for zinfo in zip_ref.infolist():
                    if zinfo.flag_bits & 0x1:
                        return True
        except zipfile.BadZipFile:
            console.print("[bold red]❌ Not a valid ZIP file.")
        return False

    def crack(self):
        if not self.zip_path.exists():
            console.print(f"[red]❌ ZIP file not found: {self.zip_path}")
            return False

        if not self.wordlist_path.exists():
            console.print(f"[red]❌ Wordlist not found: {self.wordlist_path}")
            return False

        console.print(Panel.fit(f"[bold cyan]📦 Target ZIP: {self.zip_path.name}"))

        if not self.is_encrypted():
            console.print("[green]🔓 ZIP is not password protected. Extracting...")
            with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
                zip_ref.extractall(self.extract_dir)
            console.print(f"[green]✅ Extracted to: {self.extract_dir}")
            return True

        console.print("[yellow]🔐 ZIP is password protected. Cracking...")

        with open(self.wordlist_path, "r", encoding="utf-8", errors="ignore") as file:
            for i, line in enumerate(file):
                password = line.strip()
                console.print(f"[bold blue]🔍 Trying password:[/bold blue] [white]{password}[/white]", end='\r')
                try:
                    with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
                        zip_ref.extractall(self.extract_dir, pwd=password.encode())
                    console.print(f"\n[bold green]✅ Password found: '{password}'[/bold green]")
                    console.print(f"[green]📂 Extracted to: {self.extract_dir}")
                    return True
                except Exception:
                    sleep(0.01)
                    continue

        console.print("\n[bold red]❌ Failed to crack the ZIP file.")
        return False

# Main Function
def main():
    hacker_intro()
    password = get_password().strip()
    hashed = hash_password(password)

    if hashed == CORRECT_PASSWORD_HASH:
        launch_visuals()

        # Get input ZIP and wordlist path
        if len(sys.argv) == 3:
            zip_file = sys.argv[1]
            wordlist = sys.argv[2]
        else:
            console.print("[cyan]\n📂 Enter ZIP file path:[/cyan]")
            zip_file = input(">> ").strip()
            console.print("[cyan]📜 Enter wordlist path:[/cyan]")
            wordlist = input(">> ").strip()

        cracker = ZipPasswordCracker(zip_file, wordlist)
        success = cracker.crack()
        sys.exit(0 if success else 1)
    else:
        print("\n\033[1;31m[✖] Access Denied! Tool Locked.\033[0m")
        sys.exit()

if __name__ == "__main__":
    main()
