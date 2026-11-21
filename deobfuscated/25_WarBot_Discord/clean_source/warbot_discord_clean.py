#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ==============================================================================
# Tool: WarBot Discord (Multi-Token Spam & War Bot)
# Author: tdinh
# Decoded by: tdinh cute
# Status: Cleaned & Secured (Tất cả mã độc / webhook token stealer đã bị loại bỏ)
# ==============================================================================

import os
import sys
import json
import time
import random
import threading
import requests
from datetime import datetime

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    class Fore:
        RED = '\033[91m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        BLUE = '\033[94m'
        MAGENTA = '\033[95m'
        CYAN = '\033[96m'
        WHITE = '\033[97m'
    class Style:
        RESET_ALL = '\033[0m'

VERSION = '5.0'
AUTHOR = 'tdinh'
DECODED_BY = 'tdinh cute'
TITLE = '🔥 WAR SIÊU VIP - CLEAN EDITION'

BANNER_ART = r"""
    ╔═══════════════════════════════════════════════════════════════════════════╗
    ║                                                                           ║
    ║   ██████╗ ██╗███████╗ ██████╗ ██████╗ ██████╗ ██╗    ██╗ █████╗ ██████╗  ║
    ║   ██╔══██╗██║██╔════╝██╔════╝██╔═══██╗██╔══██╗██║    ██║██╔══██╗██╔══██╗ ║
    ║   ██║  ██║██║███████╗██║     ██║   ██║██████╔╝██║ █╗ ██║███████║██████╔╝ ║
    ║   ██║  ██║██║╚════██║██║     ██║   ██║██╔══██╗██║███╗██║██╔══██║██╔══██╗ ║
    ║   ██████╔╝██║███████║╚██████╗╚██████╔╝██║  ██║╚███╔███╔╝██║  ██║██║  ██║ ║
    ║   ╚═════╝ ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ║
    ║                                                                           ║
    ║              🔥🔥🔥 WAR BOT - ĐA TOKEN 🔥🔥🔥                             ║
    ║           ⚡ SPAM NO LIMIT - ĐÈ CHAT - KHÔNG GIỚI HẠN ⚡                  ║
    ║                                                                           ║
    ╚═══════════════════════════════════════════════════════════════════════════╝
"""

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    clear()
    print(f"{Fore.RED}{BANNER_ART}{Style.RESET_ALL}")
    print(f"    📌 Version: {Fore.YELLOW}{VERSION}{Style.RESET_ALL} | Author: {Fore.CYAN}{AUTHOR}{Style.RESET_ALL} | Decoded by: {Fore.MAGENTA}{DECODED_BY}{Style.RESET_ALL}")
    print(f"    {Fore.RED}{'═' * 75}{Style.RESET_ALL}\n")

def print_status(icon, message, color=None):
    if color is None:
        color = Fore.WHITE
    print(f"    {icon} {color}{message}{Style.RESET_ALL}")

def print_success(msg):
    print_status('✅', msg, Fore.GREEN)

def print_error(msg):
    print_status('❌', msg, Fore.RED)

def print_warning(msg):
    print_status('⚠️', msg, Fore.YELLOW)

def print_info(msg):
    print_status('ℹ️', msg, Fore.CYAN)

def print_war(msg):
    print_status('🔥', msg, Fore.RED)

def print_vip(msg):
    print_status('💎', msg, Fore.MAGENTA)

def print_stat(label, value, color=None):
    if color is None:
        color = Fore.CYAN
    print(f"    ├─ {Fore.CYAN}{label}: {color}{value}{Style.RESET_ALL}")

def print_header(title):
    line = '═' * 55
    print(f"\n    {Fore.MAGENTA}╔{line}╗{Style.RESET_ALL}")
    print(f"    {Fore.MAGENTA}║ {Fore.CYAN}{title.center(53)} {Fore.MAGENTA}║{Style.RESET_ALL}")
    print(f"    {Fore.MAGENTA}╚{line}╝{Style.RESET_ALL}")

def print_menu(number, text, desc=None):
    print(f"    {Fore.YELLOW}[{number}] {Fore.WHITE}{text}{Style.RESET_ALL}")
    if desc:
        print(f"        {Fore.MAGENTA}└─ {desc}{Style.RESET_ALL}")

def check_token(token):
    """Kiểm tra token Discord có hợp lệ (live) không qua API Discord."""
    try:
        headers = {
            'Authorization': token,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get('https://discord.com/api/v10/users/@me', headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return True, data.get('username', 'Unknown'), data.get('id', 'Unknown')
        return False, None, None
    except Exception:
        return False, None, None

def check_all_tokens(tokens):
    """Kiểm tra toàn bộ danh sách token và lọc ra token live."""
    print_header('🔍 KIỂM TRA TOKEN')
    print()
    valid_tokens = []
    for i, token in enumerate(tokens, 1):
        print(f"    ⏳ Đang kiểm tra token {i}/{len(tokens)}...", end='\r')
        is_valid, username, user_id = check_token(token)
        if is_valid:
            print(f"    ✅ Token {i}: {username} ({user_id}) hợp lệ     ")
            valid_tokens.append(token)
        else:
            print(f"    ❌ Token {i}: không hợp lệ     ")
    print()
    print_stat('Token hợp lệ', str(len(valid_tokens)), Fore.GREEN)
    print_stat('Token không hợp lệ', str(len(tokens) - len(valid_tokens)), Fore.RED)
    return valid_tokens

def get_tokens_from_user():
    """Nhập token thủ công từ bàn phím (ĐÃ LOẠI BỎ TOKEN STEALER)."""
    print_header('🔑 NHẬP TOKEN DISCORD')
    print_info('Nhập token (mỗi token 1 dòng)')
    print_vip('🔒 Token chỉ lưu cục bộ, an toàn 100%')
    print(f"{Fore.YELLOW}    (Nhập 'done' hoặc để trống và enter để kết thúc){Style.RESET_ALL}\n")
    tokens = []
    while True:
        token = input(f"    [{len(tokens) + 1}] > ").strip()
        if not token or token.lower() == 'done':
            break
        tokens.append(token)
        print_success(f"Đã thêm token #{len(tokens)}")
    return tokens

def load_tokens_from_file(filename='tokens.txt'):
    """Tải token từ file txt (ĐÃ LOẠI BỎ TOKEN STEALER)."""
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            tokens = [line.strip() for line in f if line.strip()]
        return tokens
    except Exception as e:
        print_error(f"Lỗi đọc file: {e}")
        return []

def save_tokens_to_file(tokens, filename='tokens.txt'):
    """Lưu token ra file txt."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(tokens))
        print_success(f"Đã lưu {len(tokens)} token vào {filename}")
        return True
    except Exception as e:
        print_error(f"Lỗi lưu file: {e}")
        return False

class WarBot:
    def __init__(self, tokens, channel_id, content, image_url='', delay=0.05, count=9999, mention_ids=None):
        self.tokens = tokens
        self.channel_id = channel_id
        self.content = content
        self.image_url = image_url
        self.delay = max(0.01, delay)
        self.count = count
        self.mention_ids = mention_ids or []
        self.running = True
        self.stats = {'sent': 0, 'success': 0, 'fail': 0}
        self.lock = threading.Lock()
        self.token_index = 0
        self.content_list = [c.strip() for c in content.split('|') if c.strip()]
        self.image_list = [img.strip() for img in image_url.split('|') if img.strip()] if image_url else []

    def get_next_token(self):
        with self.lock:
            token = self.tokens[self.token_index % len(self.tokens)]
            self.token_index += 1
            return token

    def send_message(self, token, content, image_url=None):
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        payload = {
            'content': content,
            'tts': False
        }
        if self.mention_ids:
            payload['allowed_mentions'] = {
                'parse': ['users', 'roles']
            }
        if image_url:
            payload['embeds'] = [{
                'image': {'url': image_url},
                'color': 0xFF0000
            }]
        try:
            url = f"https://discord.com/api/v10/channels/{self.channel_id}/messages"
            response = requests.post(url, headers=headers, json=payload, timeout=5)
            if response.status_code in (200, 204):
                return True, None
            elif response.status_code == 429:
                data = response.json()
                retry_after = data.get('retry_after', 1)
                return False, f"rate_limit:{retry_after}"
            else:
                return False, f"HTTP {response.status_code}"
        except Exception as e:
            return False, str(e)

    def worker(self, thread_id):
        while self.running and self.stats['sent'] < self.count:
            token = self.get_next_token()
            content = random.choice(self.content_list)
            if self.mention_ids:
                mentions = ' '.join(f"<@{uid}>" for uid in self.mention_ids)
                content = f"{content} {mentions}"
            image = random.choice(self.image_list) if self.image_list else None
            success, error = self.send_message(token, content, image)
            with self.lock:
                self.stats['sent'] += 1
                if success:
                    self.stats['success'] += 1
                else:
                    self.stats['fail'] += 1

            if not success and error and error.startswith('rate_limit'):
                try:
                    retry = float(error.split(':')[1])
                    time.sleep(min(retry, 2.0))
                except Exception:
                    time.sleep(0.05)

            time.sleep(self.delay)

    def start(self, threads=3):
        print_header('🔥 BẮT ĐẦU WAR SPAM')
        print_stat('Channel ID', self.channel_id, Fore.CYAN)
        print_stat('Số lần spam', str(self.count), Fore.YELLOW)
        print_stat('Delay', f"{self.delay * 1000:.0f}ms", Fore.MAGENTA)
        print_stat('Token', str(len(self.tokens)), Fore.GREEN)
        print_stat('Threads', str(threads), Fore.BLUE)
        print_war('🔥🔥🔥 BẮT ĐẦU WAR - ĐÈ CHAT 🔥🔥🔥')
        print()

        self.running = True
        start_time = time.time()
        thread_list = []
        num_threads = min(threads, len(self.tokens)) if len(self.tokens) > 0 else 1

        for i in range(num_threads):
            t = threading.Thread(target=self.worker, args=(i,))
            t.daemon = True
            t.start()
            thread_list.append(t)

        try:
            while self.running and self.stats['sent'] < self.count:
                elapsed = max(time.time() - start_time, 0.001)
                speed = self.stats['sent'] / elapsed
                print(f"\r    📤 {Fore.CYAN}{self.stats['sent']}{Style.RESET_ALL} | "
                      f"✅ {Fore.GREEN}{self.stats['success']}{Style.RESET_ALL} | "
                      f"❌ {Fore.RED}{self.stats['fail']}{Style.RESET_ALL} | "
                      f"⚡ {Fore.YELLOW}{speed:.1f} msg/s{Style.RESET_ALL}", end='')
                time.sleep(0.3)
        except KeyboardInterrupt:
            self.running = False
            print_warning('\n    ⏹ Đã dừng spam!')

        self.running = False
        for t in thread_list:
            t.join(timeout=1.0)

        print('\n')
        print_header('✅ KẾT THÚC WAR')
        elapsed = max(time.time() - start_time, 0.001)
        speed = self.stats['sent'] / elapsed
        print_stat('Tổng tin đã gửi', str(self.stats['sent']), Fore.CYAN)
        print_stat('Thành công', str(self.stats['success']), Fore.GREEN)
        print_stat('Thất bại', str(self.stats['fail']), Fore.RED)
        print_stat('Tốc độ trung bình', f"{speed:.1f} msg/s", Fore.YELLOW)
        print()

def main():
    while True:
        banner()
        print_header('🔥 WAR BOT - ĐA TOKEN')
        print_menu('1', 'Nhập token thủ công', 'Nhanh Gọn, đa token')
        print_menu('2', 'Tải token từ file', 'tokens.txt - Đa token')
        print_menu('3', 'Thoát')
        print()

        choice = input('    Chọn (1-3): ').strip()
        tokens = []

        if choice == '1':
            tokens = get_tokens_from_user()
        elif choice == '2':
            tokens = load_tokens_from_file('tokens.txt')
            if tokens:
                print_success(f"Đã tải {len(tokens)} token từ file")
            else:
                print_error("Không có token trong file!")
                input("\n    Nhấn Enter để tiếp tục...")
                continue
        elif choice == '3':
            print_info("👋 Thoát!")
            break
        else:
            print_error("Lựa chọn không hợp lệ!")
            input("\n    Nhấn Enter để tiếp tục...")
            continue

        if not tokens:
            print_error("Không có token hợp lệ!")
            input("\n    Nhấn Enter để tiếp tục...")
            continue

        print()
        ans = input('    🔍 Kiểm tra token? (y/n): ').strip().lower()
        if ans == 'y':
            tokens = check_all_tokens(tokens)
            if not tokens:
                print_error("Không có token hợp lệ!")
                input("\n    Nhấn Enter để tiếp tục...")
                continue

        print_header('📌 CẤU HÌNH WAR')
        channel_id = input('    Channel ID: ').strip()
        if not channel_id:
            print_error("Channel ID không được để trống!")
            input("\n    Nhấn Enter để tiếp tục...")
            continue

        print('    Nội dung spam (dùng | để random):')
        content = input('    ▶ ').strip()
        if not content:
            content = '🔥 WAR SIÊU VIP! 💀'

        print('    Link ảnh/GIF (để trống nếu không có):')
        image_url = input('    ▶ ').strip()

        print('    ID người tag (cách nhau dấu phẩy):')
        mention_input = input('    ▶ ').strip()
        mention_ids = [m.strip() for m in mention_input.split(',') if m.strip()]

        delay_input = input('    Delay (ms, mặc định 50): ').strip()
        delay = (int(delay_input) if delay_input else 50) / 1000.0

        count_input = input('    Số lần spam (mặc định 9999): ').strip()
        count = int(count_input) if count_input else 9999

        threads_input = input('    Số thread (mặc định 3): ').strip()
        threads = int(threads_input) if threads_input else 3

        while True:
            bot = WarBot(
                tokens=tokens,
                channel_id=channel_id,
                content=content,
                image_url=image_url,
                delay=delay,
                count=count,
                mention_ids=mention_ids
            )
            bot.start(threads=threads)

            print_header('📌 SAU WAR')
            print_menu('1', 'War tiếp với cùng cài đặt')
            print_menu('2', 'Quay lại menu chính')
            print_menu('3', 'Thoát')
            print()

            post_choice = input('    Chọn (1-3): ').strip()
            if post_choice == '1':
                continue
            elif post_choice == '2':
                break
            elif post_choice == '3':
                print_info("👋 Thoát!")
                return
            else:
                break

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n\n    👋 Thoát!')
    except Exception as e:
        print(f"\n    ❌ Lỗi: {e}")
        input('\n    Nhấn Enter để thoát...')
