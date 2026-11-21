"""
=============================================================================
DEOBFUSCATED & CLEAN SOURCE CODE: checktoken.py
Author: tdinh
Decoded by: tdinh cute
Classification: Discord Token Checker (CLEAN / SAFE)
=============================================================================
"""

import requests
import time
import os
from datetime import datetime

# ANSI Color Codes
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
WHITE = '\033[97m'
RESET = '\033[0m'
BOLD = '\033[1m'


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_banner():
    banner = f"""
{CYAN}{'=' * 60}{RESET}
{BOLD}{WHITE}        DISCORD TOKEN CHECKER {RESET}
{CYAN}{'=' * 60}{RESET}
{BOLD}Author:{RESET} {YELLOW}tdinh{RESET}
{BOLD}Decoded by:{RESET} {YELLOW}tdinh cute{RESET}
{CYAN}{'=' * 60}{RESET}
    """
    print(banner)


def check_token(token):
    headers = {
        'Authorization': token.strip(),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    try:
        response = requests.get('https://discord.com/api/v9/users/@me', headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            username = data.get('username', 'Unknown')
            discriminator = data.get('discriminator', '0000')
            user_id = data.get('id', 'Unknown')
            email = data.get('email', 'No email')
            phone = data.get('phone', 'No phone')
            mfa = data.get('mfa_enabled', False)
            guilds_resp = requests.get('https://discord.com/api/v9/users/@me/guilds', headers=headers, timeout=10)
            guild_count = len(guilds_resp.json()) if guilds_resp.status_code == 200 else 0
            return {
                'status': 'ALIVE',
                'status_display': f'{GREEN}ALIVE{RESET}',
                'username': f'{username}#{discriminator}',
                'user_id': user_id,
                'email': email,
                'phone': phone,
                'mfa': 'Enabled' if mfa else 'Disabled',
                'guilds': guild_count,
                'color': GREEN
            }
        elif response.status_code == 401:
            return {
                'status': 'DEAD',
                'status_display': f'{RED}DEAD{RESET}',
                'username': 'Invalid Token',
                'user_id': 'N/A',
                'email': 'N/A',
                'phone': 'N/A',
                'mfa': 'N/A',
                'guilds': 0,
                'color': RED
            }
        else:
            return {
                'status': 'ERROR',
                'status_display': f'{YELLOW}ERROR{RESET}',
                'username': f'HTTP {response.status_code}',
                'user_id': 'N/A',
                'email': 'N/A',
                'phone': 'N/A',
                'mfa': 'N/A',
                'guilds': 0,
                'color': YELLOW
            }
    except requests.exceptions.Timeout:
        return {
            'status': 'TIMEOUT',
            'status_display': f'{YELLOW}TIMEOUT{RESET}',
            'username': 'Connection timeout',
            'user_id': 'N/A',
            'email': 'N/A',
            'phone': 'N/A',
            'mfa': 'N/A',
            'guilds': 0,
            'color': YELLOW
        }
    except Exception as e:
        return {
            'status': 'ERROR',
            'status_display': f'{YELLOW}ERROR{RESET}',
            'username': str(e),
            'user_id': 'N/A',
            'email': 'N/A',
            'phone': 'N/A',
            'mfa': 'N/A',
            'guilds': 0,
            'color': YELLOW
        }


def get_tokens_from_file():
    file_path = input(f'{CYAN}Nhap duong dan file chua token (moi token 1 dong): {RESET}').strip()
    if not os.path.exists(file_path):
        print(f'{RED}File khong ton tai!{RESET}')
        return []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tokens = [line.strip() for line in f if line.strip()]
        if not tokens:
            print(f'{RED}File rong hoac khong co token hop le!{RESET}')
            return []
        print(f'{GREEN}Da doc thanh cong {len(tokens)} token tu file{RESET}')
        return tokens
    except Exception as e:
        print(f'{RED}Loi khi doc file: {e}{RESET}')
        return []


def get_tokens_manual():
    print(f"{CYAN}Nhap token (moi token 1 dong, nhap 'done' de ket thuc):{RESET}")
    tokens = []
    while True:
        token = input(f'{WHITE}Token {len(tokens) + 1}: {RESET}').strip()
        if token.lower() == 'done':
            break
        if token:
            tokens.append(token)
    return tokens


def save_results_to_file(results, live_count, dead_count):
    filename = f"token_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('DISCORD TOKEN CHECKER RESULTS\n')
        f.write(f"Author: tdinh | Decoded by: tdinh cute\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write('=' * 80 + '\n')
        f.write(f'TOTAL: {len(results)} | ALIVE: {live_count} | DEAD: {dead_count}\n')
        f.write('=' * 80 + '\n\n')
        f.write('DETAILS:\n')
        f.write('-' * 80 + '\n')
        for i, res in enumerate(results, 1):
            f.write(f'\n[Token {i}]\n')
            f.write(f"  Status: {res['status']}\n")
            f.write(f"  Username: {res['username']}\n")
            f.write(f"  User ID: {res['user_id']}\n")
            f.write(f"  Email: {res['email']}\n")
            f.write(f"  Phone: {res['phone']}\n")
            f.write(f"  MFA: {res['mfa']}\n")
            f.write(f"  Servers: {res['guilds']}\n")
    print(f'{GREEN}Da luu ket qua vao file: {filename}{RESET}')
    return filename


def main():
    clear_screen()
    print_banner()
    print(f'{CYAN}Chon phuong thuc nhap token:{RESET}')
    print(f'{WHITE}1. Nhap thu cong{RESET}')
    print(f'{WHITE}2. Doc tu file{RESET}')
    choice = input(f'{CYAN}Lua chon (1/2): {RESET}').strip()
    tokens = []
    if choice == '1':
        tokens = get_tokens_manual()
    elif choice == '2':
        tokens = get_tokens_from_file()
    else:
        print(f'{RED}Lua chon khong hop le!{RESET}')
        return
    if not tokens:
        print(f'{RED}Khong co token de kiem tra!{RESET}')
        return
    print(f'\n{CYAN}Dang kiem tra {len(tokens)} token...{RESET}\n')
    time.sleep(1)
    results = []
    live_count = 0
    dead_count = 0
    for idx, token in enumerate(tokens, 1):
        print(f'{CYAN}[{idx}/{len(tokens)}]{RESET} Dang kiem tra... ', end='')
        result = check_token(token)
        results.append(result)
        if result['status'] == 'ALIVE':
            live_count += 1
        elif result['status'] == 'DEAD':
            dead_count += 1
        print(f"{result['status_display']} - {result['username']}")
        time.sleep(0.3)
    print(f"\n{CYAN}{'=' * 80}{RESET}")
    print(f'{BOLD}KET QUA KIEM TRA{RESET}')
    print(f"{CYAN}{'=' * 80}{RESET}\n")
    print(f"{BOLD}{'STT':<4} {'STATUS':<10} {'USERNAME':<35} {'ID':<20} {'SERVER':<8}{RESET}")
    print(f"{CYAN}{'-' * 80}{RESET}")
    for i, res in enumerate(results, 1):
        print(f"{i:<4} {res['status_display']:<18} {res['username']:<35} {res['user_id']:<20} {res['guilds']:<8}")
    print(f"\n{CYAN}{'=' * 80}{RESET}")
    print(f'{GREEN}ALIVE: {live_count}{RESET}   {RED}DEAD: {dead_count}{RESET}   {CYAN}TOTAL: {len(tokens)}{RESET}')
    print(f"{CYAN}{'=' * 80}{RESET}")
    save_choice = input(f'\n{CYAN}Luu ket qua vao file? (y/n): {RESET}').lower()
    if save_choice == 'y':
        save_results_to_file(results, live_count, dead_count)
    print(f'\n{YELLOW}Luu y: Token la thong tin nhay cam, khong chia se cho nguoi khac!{RESET}')
    print(f'{GREEN}Tool duoc phat trien boi tdinh | Decoded by tdinh cute{RESET}')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f'\n{YELLOW}Da dung boi nguoi dung!{RESET}')
