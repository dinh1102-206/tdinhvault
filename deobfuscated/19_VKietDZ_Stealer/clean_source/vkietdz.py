# Decompiled and Deobfuscated by TDINH
import base64
from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
import random
import ssl
import sys
import threading
import time
from curl_cffi import requests as curl_requests


def iloveyou():
    print(r"""
\033[38;2;255;0;128m  _____  ______ ____  ____  ______   ______     __  _______ _____ _____ _   _ _    _ 
\033[38;2;255;0;128m |  __ \|  ____/ __ \|  _ \|  ____| |  _ \ \   / / |__   __|  __ \_   _| \ | | |  | |
\033[38;2;255;0;128m | |  | | |__ | |  | | |_) | |__    | |_) \ \_/ /     | |  | |  | || | |  \| | |__| |
\033[38;2;255;0;128m | |  | |  __|| |  | |  _ <|  __|   |  _ < \   /      | |  | |  | || | | . ` |  __  |
\033[38;2;255;0;128m | |__| | |___| |__| | |_) | |      | |_) | | |       | |  | |__| || |_| |\  | |  | |
\033[38;2;255;0;128m |_____/|______\____/|____/|_|      |____/  |_|       |_|  |_____/_____|_| \_|_|  |_|
\033[0m""")

def ilove_you():
    iloveyou()

VN_TZ = timezone(timedelta(hours=7))

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.3; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0"
]

IMPERSONATE = 'chrome120'
REQUEST_TIMEOUT = 15
MAX_RETRIES = 3
RETRY_BASE_DELAY = 1.0
RETRY_EXPONENTIAL_BASE = 2.0
RETRY_MAX_DELAY = 60.0
RETRY_JITTER = 0.5

session_pool = {}
session_pool_lock = threading.Lock()

def _get_auto_delay_pattern():
    """
    Pattern delay cua che do 'Da Set Delay San'.
    Gia tri thuc da duoc ma hoa XOR -> khong lo so trong source code.
    """
    _enc = b'zzyy{{'
    return [b ^ 100 for b in _enc]

def log_error(token, error_message):
    masked = mask_token(token) if token else "???"
    print(f"\033[91m[ERROR] Token {masked} : {error_message}\033[0m")

def log_success(token, channel_id):
    pass

def log_failed_token(token):
    with open("tokenloi.txt", "a", encoding="utf-8") as f:
        f.write(f"Token Khong Dang Nhap Duoc: {token}\n")

def log_die_token(token):
    """Ghi token bị chết (die) vào file die.txt"""
    with open("die.txt", "a", encoding="utf-8") as f:
        f.write(f"{token}\n")

def get_current_time():
    return datetime.now(VN_TZ).strftime("%H:%M:%S")

def mask_token(token):
    if len(token) < 10:
        return "Invalid"
    return f"{token[:5]}...{token[-5:]}"

def print_banner():
    banner = r"""

/\/\   ____            ____    /\/\

 |/\/\   / __ \          / __ \  |/\/\ 

       | |  | |_      _| |  | |      

       | |  | \ \ /\ / / |  | |      

       | |__| |\ V  V /| |__| |      

        \____/  \_/\_/  \____/       

    """
    print(banner)
    print("                 Văn Kiệt Bá Đạo")

def generate_fingerprint(token):
    return hashlib.blake2b(token.encode(), digest_size=8).hexdigest()

def get_enhanced_headers(token):
    build_number = random.randint(313000, 313100)
    ua = random.choice(USER_AGENTS)
    super_properties = {
        "os": "Windows",
        "browser": "Chrome",
        "device": "",
        "system_locale": "en-US",
        "browser_user_agent": ua,
        "browser_version": "133.0.0.0",
        "os_version": "10",
        "referrer": "",
        "referring_domain": "",
        "release_channel": "stable",
        "client_build_number": build_number
    }
    encoded_props = base64.b64encode(json.dumps(super_properties).encode()).decode()
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": ua,
        "X-Super-Properties": encoded_props,
        "X-Fingerprint": generate_fingerprint(token),
        "X-Discord-Locale": "en-US",
        "X-Discord-Timezone": "Asia/Ho_Chi_Minh",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Origin": "https://discord.com",
        "Referer": "https://discord.com/channels/@me",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin"
    }
    return headers

def get_channel_name(channel_id, token):
    headers = get_enhanced_headers(token)
    try:
        resp = curl_requests.get(
            f"https://discord.com/api/v10/channels/{channel_id}",
            headers=headers,
            timeout=REQUEST_TIMEOUT,
            impersonate=IMPERSONATE,
            verify=False
        )
        if resp.status_code == 200:
            return resp.json().get("name", "Unknown")
        return "Unknown"
    except Exception:
        return "Unknown"

def get_session_for_thread():
    thread_id = threading.get_ident()
    with session_pool_lock:
        if thread_id not in session_pool:
            session_pool[thread_id] = curl_requests.Session()
        return session_pool[thread_id]

def check_token(token):
    max_check_retries = 3
    headers = get_enhanced_headers(token)
    for attempt in range(max_check_retries):
        try:
            resp = curl_requests.get(
                "https://discord.com/api/v10/users/@me",
                headers=headers,
                timeout=REQUEST_TIMEOUT,
                impersonate=IMPERSONATE,
                verify=False
            )
            status = resp.status_code
            if status == 200:
                data = resp.json()
                username = data.get("username", data.get("global_name", "Unknown"))
                return True, username
            elif status in (401, 403):
                log_die_token(token)
                return False, "Token khong hop le hoac bi khoa"
            elif status == 429:
                try:
                    retry_after = resp.json().get("retry_after", 5)
                except Exception:
                    retry_after = 5
                wait_time = float(retry_after) + random.uniform(1.0, 3.0)
                print(f"\033[93m[WAIT] Token {mask_token(token)} bi 429, doi {wait_time:.2f}s...\033[0m")
                time.sleep(wait_time)
                continue
            else:
                pass
        except Exception:
            time.sleep(random.uniform(1.0, 3.0))
            continue
    log_failed_token(token)
    return False, "Rate limit / Loi ket noi"

def choose_delay_mode():
    while True:
        print("Chon che do delay:")
        print("[1] Delay chung")
        print("[2] Delay rieng")
        print("[3] Random delay")
        print("[4] Da Set Delay San")
        choice = input("Nhap lua chon (1/2/3/4): ").strip()
        if choice in ("1", "2", "3", "4"):
            return int(choice)
        print("Vui long nhap 1, 2, 3 hoac 4!")

def get_delays(tokens, mode):
    delays = {}
    if mode == 1:
        while True:
            try:
                d = float(input("Nhap delay chung (giay): ").strip())
                for t in tokens:
                    delays[t] = d
                break
            except ValueError:
                print("Vui long nhap so hop le")
    elif mode == 2:
        print("Nhap delay cho tung token:")
        for i, t in enumerate(tokens, 1):
            while True:
                try:
                    d = float(input(f"Token {mask_token(t)} [{i}] delay (giay): ").strip())
                    delays[t] = d
                    break
                except ValueError:
                    print("Vui long nhap so hop le")
    elif mode == 3:
        print("Nhap khoang delay cho tung token:")
        for i, t in enumerate(tokens, 1):
            while True:
                try:
                    min_d = float(input(f"Token {mask_token(t)} [{i}] delay min (giay): ").strip())
                    max_d = float(input(f"Token {mask_token(t)} [{i}] delay max (giay): ").strip())
                    if min_d <= max_d:
                        delays[t] = (min_d, max_d)
                        break
                    print("Delay min phai <= delay max!")
                except ValueError:
                    print("Vui long nhap so hop le")
    elif mode == 4:
        pattern = _get_auto_delay_pattern()
        total = len(pattern)
        for i, t in enumerate(tokens):
            delays[t] = pattern[i % total]
        print(f"Da ap dung delay san cho {len(tokens)} token.")
    return delays

def choose_message_files():
    txt_files = [f for f in os.listdir() if f.endswith(".txt")]
    if not txt_files:
        print("Khong tim thay file .txt nao!")
        return []
    print("Cac file co san:")
    for i, f in enumerate(txt_files, 1):
        print(f"{i}. {f}")
    selected = []
    while True:
        choice = input("Chon file (nhap so hoac ten, 'done' de ket thuc): ").strip()
        if choice.lower() == 'done':
            if not selected:
                print("Can chon it nhat mot file!")
                continue
            break
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(txt_files):
                file_to_add = txt_files[idx]
                if file_to_add not in selected:
                    selected.append(file_to_add)
                    print(f"Da them: {file_to_add}")
                else:
                    print("File da duoc chon")
            else:
                print("Ten file khong hop le")
        else:
            file_to_add = choice if choice.endswith(".txt") else choice + ".txt"
            if os.path.exists(file_to_add):
                if file_to_add not in selected:
                    selected.append(file_to_add)
                    print(f"Da them: {file_to_add}")
                else:
                    print("File da duoc chon")
            else:
                print("Ten file khong hop le")
    return selected

class MessageLoader:
    def __init__(self, file_paths):
        self.messages = []
        for path in file_paths:
            if os.path.exists(path):
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read().strip()
                        if content:
                            for line in content.splitlines():
                                line = line.strip()
                                if line:
                                    self.messages.append(line)
                except Exception as e:
                    log_error("system", f"load_messages {path}: {e}")
        if not self.messages:
            self.messages = ["Văn Kiệt"]

    def get_random_message(self):
        return random.choice(self.messages)

class DiscordSpammer:
    def __init__(self, message_loader, channels, tokens, delay_data, delay_mode, messages_per_send):
        self.message_loader = message_loader
        self.channels = channels
        self.tokens = tokens
        self.delay_data = delay_data
        self.delay_mode = delay_mode
        self.messages_per_send = max(1, messages_per_send)
        self.running = False
        self._lock = threading.Lock()
        self.channel_names = {}
        self.total_sent = 0

    def _get_channel_name(self, channel, token):
        with self._lock:
            if channel not in self.channel_names:
                self.channel_names[channel] = get_channel_name(channel, token)
            return self.channel_names[channel]

    def _send_single_message(self, token, channel, message):
        session = get_session_for_thread()
        headers = get_enhanced_headers(token)
        nonce = str((int(time.time() * 1000) - 1420070400000) * 4194304 + random.randint(0, 4194303))
        payload = {
            "content": message,
            "nonce": nonce,
            "tts": False
        }
        url = f"https://discord.com/api/v10/channels/{channel}/messages"
        for attempt in range(MAX_RETRIES):
            try:
                resp = session.post(
                    url,
                    headers=headers,
                    json=payload,
                    timeout=REQUEST_TIMEOUT,
                    verify=False
                )
                status = resp.status_code
                if 200 <= status < 300:
                    return True
                if status == 429:
                    try:
                        retry_after = resp.json().get("retry_after", 2.0)
                    except Exception:
                        retry_after = 2.0
                    time.sleep(float(retry_after) + 0.5)
                    continue
                if status in (401, 403):
                    log_error(token, f"Loi {status} khi gui tin nhan")
                    return False
                delay = min(RETRY_BASE_DELAY * (RETRY_EXPONENTIAL_BASE ** attempt), RETRY_MAX_DELAY)
                delay += random.uniform(-RETRY_JITTER, RETRY_JITTER)
                time.sleep(max(0.5, delay))
            except Exception:
                delay = min(RETRY_BASE_DELAY * (RETRY_EXPONENTIAL_BASE ** attempt), RETRY_MAX_DELAY)
                delay += random.uniform(-RETRY_JITTER, RETRY_JITTER)
                time.sleep(max(0.5, delay))
        log_error(token, f"Loi khi gui tin nhan sau {MAX_RETRIES} lan thu")
        return False

    def _send_batch(self, token, channel):
        for _ in range(self.messages_per_send):
            if not self.running:
                break
            msg = self.message_loader.get_random_message()
            success = self._send_single_message(token, channel, msg)
            if success:
                with self._lock:
                    self.total_sent += 1
                short_token = token[:5] if len(token) >= 5 else token
                channel_name = self._get_channel_name(channel, token)
                current_time = get_current_time()
                print(f"\033[92m[{current_time}] > [Success] > {channel_name} > {short_token} > Van Kiet\033[0m")
            time.sleep(0.05)

    def worker(self, token):
        channel_index = 0
        while self.running:
            try:
                channel = self.channels[channel_index % len(self.channels)]
                self._send_batch(token, channel)
                channel_index += 1
                if self.delay_mode == 3:
                    min_d, max_d = self.delay_data.get(token, (1.0, 3.0))
                    delay = random.uniform(min_d, max_d)
                else:
                    delay = self.delay_data.get(token, 1.0)
                time.sleep(delay)
            except Exception as e:
                log_error(token, f"Worker error: {e}")
                time.sleep(1)

    def start(self):
        self.running = True
        threads = []
        for token in self.tokens:
            t = threading.Thread(target=self.worker, args=(token,), daemon=True)
            threads.append(t)
            t.start()
        return threads

    def stop(self):
        self.running = False

def main():
    print_banner()
    token_file = "tokens.txt"
    if not os.path.exists(token_file):
        print(f"Khong tim thay file '{token_file}'!")
        return
    try:
        with open(token_file, "r", encoding="utf-8") as f:
            raw_tokens = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"Loi doc file: {e}")
        return
    if not raw_tokens:
        print(f"Khong co token nao trong {token_file}!")
        return
    print(f"Da load {len(raw_tokens)} token.")
    print("\nDang kiem tra token...\n")
    valid_tokens = []
    invalid_count = 0
    die_count = 0
    rate_limit_count = 0
    for i, token in enumerate(raw_tokens, 1):
        print(f"\033[94mDang check ({i}/{len(raw_tokens)}): {mask_token(token)}\033[0m")
        is_valid, reason = check_token(token)
        if is_valid:
            print(f"\033[92m[LIVE] {mask_token(token)} ({reason})\033[0m")
            valid_tokens.append(token)
        elif "khong hop le" in reason or "khoa" in reason:
            print(f"\033[91m[DIE ] {mask_token(token)} -> die.txt\033[0m")
            die_count += 1
        elif "Rate limit" in reason or "429" in reason:
            print(f"\033[93m[RATE] {mask_token(token)} -> Loi 429 (Khong ghi file)\033[0m")
            rate_limit_count += 1
        else:
            print(f"\033[93m[FAIL] {mask_token(token)} -> {reason}\033[0m")
            invalid_count += 1
        time.sleep(1.5)
    print(f"\nToken hop le: {len(valid_tokens)}")
    print(f"Token die (da ghi die.txt): {die_count}")
    print(f"Token bi rate limit (khong ghi file): {rate_limit_count}")
    print(f"Token loi khac (khong ghi die.txt): {invalid_count}\n")
    if not valid_tokens:
        print("Khong co token hop le nao!")
        return
    print("\nNhap Channel ID de spam (nhap 'done' de ket thuc):")
    selected_channels = []
    while True:
        cid = input("> Channel ID (hoac 'done'): ").strip()
        if cid.lower() == 'done':
            break
        if cid.isdigit():
            if cid not in selected_channels:
                selected_channels.append(cid)
                print(f"Da them channel: {cid}")
            else:
                print("Channel da ton tai!")
        else:
            print("Vui long nhap Channel ID hop le!")
    if not selected_channels:
        print("Chua nhap channel nao!")
        return
    msg_files = choose_message_files()
    if not msg_files:
        print("Khong co file tin nhan nao, su dung mac dinh.")
        with open("default.txt", "w", encoding="utf-8") as f:
            f.write("Văn Kiệt")
        msg_files = ["default.txt"]
    loader = MessageLoader(msg_files)
    while True:
        try:
            per_send = int(input("So tin nhan moi lan gui (mac dinh 1): ").strip() or "1")
            if per_send > 0:
                break
        except ValueError:
            pass
        print("Vui long nhap so hop le!")
    delay_mode = choose_delay_mode()
    delays = get_delays(valid_tokens, delay_mode)
    spammer = DiscordSpammer(
        message_loader=loader,
        channels=selected_channels,
        tokens=valid_tokens,
        delay_data=delays,
        delay_mode=delay_mode,
        messages_per_send=per_send
    )
    os.system("cls" if os.name == 'nt' else "clear")
    print_banner()
    print(f"So channel: {len(selected_channels)}")
    print(f"So token: {len(valid_tokens)}")
    print(f"So tin nhan moi lan gui: {per_send}")
    print("\nDang chay... (Ctrl+C de dung)")
    threads = spammer.start()
    try:
        while spammer.running:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nDang dung...")
        spammer.stop()
        print("Da dung!")

if __name__ == '__main__':
    ilove_you()
    main()
