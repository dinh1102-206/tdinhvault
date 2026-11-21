# Author: tdinh cute
# Decoded by: tdinh cute
# Target: tool.py (Discord Token Checker & Manager)

import os
import sys
import time
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from typing import List, Tuple

DEFAULT_TOKEN_FILE = 'tokens.txt'
API_URL = 'https://discord.com/api/v9/users/@me'
TIMEOUT = 10
MAX_RETRY = 2
MAX_WORKERS = 5
RATE_LIMIT_DELAY = 0.2

HEADERS_TEMPLATE = {
    'Content-Type': 'application/json'
}

COLOR_RESET = '\x1b[0m'
COLOR_RED_BLACK = '\x1b[91;40m'
COLOR_GREEN_BLACK = '\x1b[92;40m'
COLOR_YELLOW = '\x1b[93m'

lock = Lock()

def check_token(token: str) -> Tuple[bool, int, str]:
    headers = HEADERS_TEMPLATE.copy()
    headers['Authorization'] = token.strip()
    
    for attempt in range(MAX_RETRY):
        try:
            resp = requests.get(API_URL, headers=headers, timeout=TIMEOUT)
            code = resp.status_code
            if code == 200:
                return (True, code, token)
            elif code in (401, 403):
                return (False, code, token)
            elif code == 429:
                delay = float(resp.headers.get('Retry-After', 1)) + 0.5
                time.sleep(delay)
            else:
                time.sleep(0.5)
        except (requests.ConnectionError, requests.Timeout):
            time.sleep(0.5)
            
    return (False, 0, token)

def print_colored(text: str, color: str) -> None:
    with lock:
        print(f"{color}{text}{COLOR_RESET}")

def show_menu(current_file: str) -> int:
    print("\n==================================================")
    print(f"{COLOR_YELLOW}   CHECK TOKEN TOOL  - MENU{COLOR_RESET}")
    print("==================================================")
    print(f"File hiện tại: {current_file}")
    print("1. CheckTokenV1 ")
    print("2. CheckTokenV2 ")
    print("3. KillTokenAll ")
    print("4. Chọn file token khác")
    print("5. Thoát")
    print("==================================================")
    
    while True:
        try:
            choice = int(input("Nhập lựa chọn (1-5): ").strip())
            if 1 <= choice <= 5:
                return choice
            print("Lựa chọn không hợp lệ.")
        except ValueError:
            print("Lựa chọn không hợp lệ.")

def select_token_file() -> str:
    path = input("(Enter để dùng mặc định 'tokens.txt'): ").strip()
    if not path:
        path = DEFAULT_TOKEN_FILE
    return path

def read_tokens(file_path: str) -> List[str]:
    if not os.path.isfile(file_path):
        print(f"LỖI: Không tìm thấy file '{file_path}'")
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def write_tokens(file_path: str, tokens: List[str]) -> None:
    with open(file_path, 'w', encoding='utf-8') as f:
        for t in tokens:
            f.write(t + '\n')

def kill_all_tokens(file_path: str) -> None:
    tokens = read_tokens(file_path)
    if not tokens:
        print("Không có token để xử lý.")
        return
        
    print(f"Đang tiến hành vô hiệu hóa (kill) {len(tokens)} token...")
    # Kill token logic via API logout/change
    for tok in tokens:
        try:
            h = {'Authorization': tok.strip()}
            requests.post('https://discord.com/api/v9/auth/logout', headers=h, timeout=5)
        except Exception:
            pass
    print("Hoàn tất!")

def process_tokens(file_path: str, auto_delete: bool = False) -> None:
    tokens = read_tokens(file_path)
    if not tokens:
        print("Không có token để kiểm tra.")
        return
        
    valid_tokens = []
    invalid_tokens = []
    
    print(f"Đang kiểm tra {len(tokens)} token với {MAX_WORKERS} luồng...")
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_token = {executor.submit(check_token, t): t for t in tokens}
        for future in as_completed(future_to_token):
            is_valid, code, tok = future.result()
            if is_valid:
                valid_tokens.append(tok)
                print_colored(f"[LIVE] {tok[:30]}... (Status: {code})", COLOR_GREEN_BLACK)
            else:
                invalid_tokens.append(tok)
                print_colored(f"[DIE]  {tok[:30]}... (Status: {code})", COLOR_RED_BLACK)
            time.sleep(RATE_LIMIT_DELAY)
            
    print("\n--------------------------------------------------")
    print(f"Tổng kết: {len(valid_tokens)} LIVE | {len(invalid_tokens)} DIE")
    if auto_delete:
        write_tokens(file_path, valid_tokens)
        print(f"Đã tự động cập nhật file '{file_path}' (chỉ giữ token LIVE).")
    print("--------------------------------------------------")

def main():
    try:
        import requests
    except ImportError:
        print("LỖI: Cài requests: pip3 install requests")
        sys.exit(1)
        
    current_file = DEFAULT_TOKEN_FILE
    if not os.path.isfile(current_file):
        print(f"File mặc định '{current_file}' không tồn tại.")
        current_file = select_token_file()
        
    while True:
        choice = show_menu(current_file)
        if choice == 5:
            print("Thoát.")
            break
        elif choice == 4:
            current_file = select_token_file()
        elif choice == 1:
            process_tokens(current_file, auto_delete=False)
            input("\nNhấn Enter để tiếp tục...")
        elif choice == 2:
            process_tokens(current_file, auto_delete=True)
            input("\nNhấn Enter để tiếp tục...")
        elif choice == 3:
            kill_all_tokens(current_file)
            input("\nNhấn Enter để tiếp tục...")

if __name__ == '__main__':
    main()
