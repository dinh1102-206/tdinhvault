"""
# Author: tdinh cute
# Decoded by: tdinh cute
# Original File: input/chomaythkdu.py (Originally obfuscated with Pyarmor 9.2.5 trial)
# Tool Name: SANA VIP TOOL - Discord Multi-Token Channel Spammer
# Developer Credit in Code: NGUYEN VAN TRONG (FB: NGUYEN VAN TRONG) / SANA
# License Key: sana09
"""

import os
import ssl
import json
import time
import asyncio
import random
import base64
import aiohttp
import certifi
import getpass
from colorama import Fore, Style, init
from datetime import datetime, timedelta
from collections import defaultdict
from typing import List, Dict, Optional, Tuple
import logging

init(autoreset=True)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SanaDiscordTool")

MAX_RETRIES = 5
REQUEST_TIMEOUT = 15
RATE_LIMIT_BUFFER = 0.5

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
]

def cls():
    os.system("cls" if os.name == "nt" else "clear")

def show_sana_menu():
    banner_lines = [
        "    ██████╗  █████╗ ███╗   ██╗ █████╗     ██╗   ██╗██╗██████╗ ",
        "    ██╔════╝ ██╔══██╗████╗  ██║██╔══██╗    ██║   ██║██║██╔══██╗",
        "    ███████╗ ███████║██╔██╗ ██║███████║    ██║   ██║██║██████╔╝",
        "    ╚════██║ ██╔══██║██║╚██╗██║██╔══██║    ╚██╗ ██╔╝██║██╔═══╝ ",
        "    ███████║ ██║  ██║██║ ╚████║██║  ██║     ╚████╔╝ ██║██║     ",
        "    ╚══════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝      ╚═══╝  ╚═╝╚═╝     "
    ]
    print(Fore.CYAN + Style.BRIGHT + "\n".join(banner_lines))
    print(Fore.YELLOW + "    --- SANA VIP TOOL - MUA CODE LIÊN HỆ FB: NGUYEN VAN TRONG ---")
    print(Fore.CYAN + "-----------------------------------------------------------------")

def banner():
    show_sana_menu()

def input_tool_key():
    cls()
    banner()
    print(Fore.CYAN + "\nnhap key de xai tool cua  anh SANA")
    # HARDCODED KEY IN CODE: 'sana09' (Bypassed by tdinh cute)
    key = input(Fore.YELLOW + "> Key (Mặc định: sana09): " + Style.RESET_ALL).strip()
    if not key:
        key = "sana09"
    if key == "sana09":
        print(Fore.GREEN + "key cua SANA da dung...\n")
        time.sleep(1)
        return True
    else:
        print(Fore.RED + "dit me may key sai - mua key inbox 0934746209.")
        return False

class MessageLoader:
    def __init__(self, filenames: List[str], mode: str = "full", add_header: bool = False):
        self.messages = []
        self.message_counts = defaultdict(int)
        self.total_sent = 0
        self.mode = mode
        self.add_header = add_header

        for filename in filenames:
            if os.path.exists(filename):
                with open(filename, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if mode == "full":
                        self.messages.append(content)
                    else:
                        for line in content.split("\n"):
                            if line.strip():
                                self.messages.append(line.strip())
        if not self.messages:
            self.messages.append("Default message")
        print(f"Loaded {len(self.messages)} messages from {len(filenames)} files (mode: {mode})")

    def get_random(self) -> str:
        msg = random.choice(self.messages)
        self.total_sent += 1
        self.message_counts[msg] += 1
        if self.add_header and not msg.startswith("#"):
            rand_prefix = "#" * random.randint(1, 3) + " "
            msg = rand_prefix + msg
        return msg

    def get_stats(self) -> dict:
        return {
            "total_sent": self.total_sent,
            "unique_messages": len(self.messages),
            "distribution": dict(self.message_counts)
        }

class TokenValidator:
    def __init__(self, ssl_context):
        self.ssl_context = ssl_context

    async def check_token(self, session: aiohttp.ClientSession, token: str) -> Optional[str]:
        token = token.strip()
        headers = {
            "Authorization": token,
            "User-Agent": random.choice(USER_AGENTS)
        }
        try:
            timeout = aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
            async with session.get("https://discord.com/api/v10/users/@me", headers=headers, ssl=self.ssl_context, timeout=timeout) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    user = data.get("username", "Unknown")
                    return token
                return None
        except Exception as e:
            logger.debug(f"Token check error: {e}")
            return None

    async def validate_tokens(self, raw_tokens: List[str]) -> List[str]:
        print(Fore.YELLOW + f"check token... {len(raw_tokens)} tokens..." + Style.RESET_ALL)
        connector = aiohttp.TCPConnector(ssl=self.ssl_context, limit=100)
        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = [self.check_token(session, t) for t in raw_tokens]
            results = await asyncio.gather(*tasks)
            valid = [r for r in results if r is not None]
            print(Fore.GREEN + f"token hop le : {len(valid)}/{len(raw_tokens)}" + Style.RESET_ALL)
            return valid

class GiautenLimiter:
    def __init__(self, tokens: List[str], channel: str, message_loader: MessageLoader, delays: Dict[str, float]):
        self.tokens = tokens
        self.channel = channel
        self.message_loader = message_loader
        self.delays = delays
        self.channel_name = "Unknown"
        self.running = True
        self.start_time = datetime.now()
        self.stats = {"total_sent": 0, "total_failed": 0, "rate_limits": 0}
        self.token_stats = defaultdict(lambda: {"sent": 0, "failed": 0, "rate_limited": 0})
        self.channel_limits = defaultdict(lambda: {"remaining": 5, "reset_at": datetime.now(), "is_limited": False})
        self.global_limit = {"remaining": 50, "reset_at": datetime.now(), "is_limited": False}
        self.lock = asyncio.Lock()
        
        self.ssl_context = ssl.create_default_context(cafile=certifi.where())
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE

    async def can_send(self, channel_id: str) -> bool:
        async with self.lock:
            now = datetime.now()
            if self.global_limit["is_limited"] and now < self.global_limit["reset_at"]:
                return False
            chan = self.channel_limits[channel_id]
            if chan["is_limited"] and now < chan["reset_at"]:
                return False
            return True

    async def update_from_headers(self, channel_id: str, headers):
        async with self.lock:
            now = datetime.now()
            if headers.get("X-RateLimit-Global"):
                retry_after = float(headers.get("Retry-After", 1.0))
                self.global_limit["is_limited"] = True
                self.global_limit["reset_at"] = now + timedelta(seconds=retry_after + RATE_LIMIT_BUFFER)
            if "X-RateLimit-Remaining" in headers:
                rem = int(headers.get("X-RateLimit-Remaining", 1))
                reset_after = float(headers.get("X-RateLimit-Reset-After", 1.0))
                chan = self.channel_limits[channel_id]
                chan["remaining"] = rem
                if rem == 0:
                    chan["is_limited"] = True
                    chan["reset_at"] = now + timedelta(seconds=reset_after + RATE_LIMIT_BUFFER)

    def _generate_headers(self, token: str) -> dict:
        build_num = random.randint(270000, 280000)
        super_props = {
            "os": "Windows",
            "browser": "Chrome",
            "device": "",
            "system_locale": "en-US",
            "browser_user_agent": random.choice(USER_AGENTS),
            "browser_version": "121.0.0.0",
            "os_version": "10",
            "referrer": "https://discord.com/",
            "referring_domain": "discord.com",
            "referrer_current": "",
            "referring_domain_current": "",
            "release_channel": "stable",
            "client_build_number": build_num,
            "client_event_source": None,
            "design_id": 0
        }
        encoded_props = base64.b64encode(json.dumps(super_props).encode()).decode()

        return {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9,vi;q=0.8",
            "Authorization": token,
            "Content-Type": "application/json",
            "User-Agent": super_props["browser_user_agent"],
            "X-Super-Properties": encoded_props,
            "X-Discord-Locale": "en-US",
            "X-Discord-Timezone": "Asia/Ho_Chi_Minh",
            "Origin": "https://discord.com",
            "Referer": f"https://discord.com/channels/@me/{self.channel}",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin"
        }

    async def get_channel_info(self, session: aiohttp.ClientSession, token: str):
        headers = {
            "Authorization": token,
            "User-Agent": random.choice(USER_AGENTS)
        }
        try:
            async with session.get(f"https://discord.com/api/v10/channels/{self.channel}", headers=headers, ssl=self.ssl_context) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    self.channel_name = data.get("name", "Unknown")
        except Exception:
            pass

    async def send_message(self, session: aiohttp.ClientSession, token: str, idx: int):
        while not await self.can_send(self.channel):
            await asyncio.sleep(0.5)

        nonce = str((int(time.time() * 1000) - 1420070400000) * 4194304 + random.randint(0, 4095))
        content = self.message_loader.get_random()
        payload = {"content": content, "tts": False, "nonce": nonce, "flags": 0}
        headers = self._generate_headers(token)

        for attempt in range(MAX_RETRIES):
            try:
                url = f"https://discord.com/api/v10/channels/{self.channel}/messages"
                async with session.post(url, json=payload, headers=headers, ssl=self.ssl_context, timeout=REQUEST_TIMEOUT) as resp:
                    await self.update_from_headers(self.channel, resp.headers)
                    if resp.status == 200:
                        self.stats["total_sent"] += 1
                        self.token_stats[token]["sent"] += 1
                        print(Fore.GREEN + f"[{idx:02d}] {token[:20]}... | SANA VIP Da Gui | Sent: {self.stats['total_sent']:03d} | Channel: {self.channel_name}" + Style.RESET_ALL)
                        return True
                    elif resp.status == 429:
                        self.stats["rate_limits"] += 1
                        data = await resp.json()
                        retry = data.get("retry_after", 1.0)
                        await asyncio.sleep(float(retry))
                    elif resp.status in (401, 403):
                        print(Fore.RED + f"Token {token[:20]} loi auth ({resp.status})" + Style.RESET_ALL)
                        return False
            except Exception as e:
                await asyncio.sleep(0.5)
        self.stats["total_failed"] += 1
        return False

    async def spam_worker(self, token: str, idx: int):
        connector = aiohttp.TCPConnector(ssl=self.ssl_context)
        delay = self.delays.get(token, 1.0)
        async with aiohttp.ClientSession(connector=connector) as session:
            await self.get_channel_info(session, token)
            while self.running:
                await self.send_message(session, token, idx)
                await asyncio.sleep(delay + random.uniform(0.1, 0.5))

    async def run(self):
        print(Fore.GREEN + f"Thưa Bố Erik Đang Spam Vào Kênh: {self.channel}" + Style.RESET_ALL)
        tasks = [asyncio.create_task(self.spam_worker(t, i+1)) for i, t in enumerate(self.tokens)]
        try:
            await asyncio.gather(*tasks)
        except asyncio.CancelledError:
            self.running = False

    def print_stats(self):
        duration = (datetime.now() - self.start_time).total_seconds()
        speed = self.stats["total_sent"] / max(1.0, duration)
        print(Fore.CYAN + f"\nThống Kê:\n  Tổng gửi: {self.stats['total_sent']}\n  Thất bại: {self.stats['total_failed']}\n  Rate limits: {self.stats['rate_limits']}\n  Thời gian: {duration:.1f}s\n  Tốc độ: {speed:.2f} msg/s" + Style.RESET_ALL)

def main():
    if not input_tool_key():
        return

    token_file = input(Fore.YELLOW + "Mời cha sana Nhập Tên File Token: " + Style.RESET_ALL).strip()
    if not os.path.exists(token_file):
        print(Fore.RED + "Đéo Có File!" + Style.RESET_ALL)
        return

    with open(token_file, "r", encoding="utf-8") as f:
        tokens = [line.strip() for line in f if line.strip()]

    if not tokens:
        print(Fore.RED + "Đéo Có Token Kìa Thằng Ngu!" + Style.RESET_ALL)
        return

    ssl_ctx = ssl.create_default_context(cafile=certifi.where())
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE

    validator = TokenValidator(ssl_ctx)
    valid_tokens = asyncio.run(validator.validate_tokens(tokens))
    if not valid_tokens:
        print(Fore.RED + "Đéo Có Token Nào Hợp Lệ!" + Style.RESET_ALL)
        return

    channel_id = input(Fore.YELLOW + "Mời Bố Erik Nhập Id Kênh: " + Style.RESET_ALL).strip()
    if not channel_id:
        print(Fore.RED + "Mày Đéo Nhập Id Kênh À!" + Style.RESET_ALL)
        return

    print(Fore.CYAN + "Mời Bố Erik Nhập Tên File Ngôn ('ok' để dừng nhé):" + Style.RESET_ALL)
    msg_files = []
    while True:
        fn = input("  File: ").strip()
        if fn.lower() == "ok":
            break
        if os.path.exists(fn):
            msg_files.append(fn)
            print(Fore.GREEN + "  Đã thêm" + Style.RESET_ALL)
        else:
            print(Fore.RED + "File Ngôn Đéo Tồn Tại" + Style.RESET_ALL)

    if not msg_files:
        print(Fore.RED + "Đéo Có 1 File Tin Nhắn À Thằng Lồn!" + Style.RESET_ALL)
        return

    print("\nChọn Mode Gửi Tin Nhắn:\n1 - Full Ngôn\n2 - Từng Dòng")
    mode_choice = input("Che Do 1-2: ").strip()
    mode = "full" if mode_choice == "1" else "lines"

    add_hash = input("Thêm # vào đầu tin nhắn không thg ngu (y/n): ").strip().lower() == "y"
    loader = MessageLoader(msg_files, mode=mode, add_header=add_hash)

    print("\nChọn chế độ delay:\n1 > ghi delay rieng cua may\n2 > che do treo nhanh (1.0s)\n3 > che do treo slow (3.0s)\n4 > che do treo tru (5.0s)")
    delay_choice = input("che do 1-4: ").strip()
    delays = {}
    if delay_choice == "1":
        for i, t in enumerate(valid_tokens):
            val = float(input(f"  [{i+1:02d}] {t[:20]}... delay (s): ") or 1.0)
            delays[t] = max(0.2, val)
    elif delay_choice == "2":
        delays = {t: 1.0 for t in valid_tokens}
    elif delay_choice == "3":
        delays = {t: 3.0 for t in valid_tokens}
    else:
        delays = {t: 5.0 for t in valid_tokens}

    print(Fore.GREEN + "tool by SANA VIP loading..." + Style.RESET_ALL)
    limiter = GiautenLimiter(valid_tokens, channel_id, loader, delays)
    try:
        asyncio.run(limiter.run())
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\nstop loading by SANA VIP..." + Style.RESET_ALL)
    finally:
        limiter.print_stats()

if __name__ == "__main__":
    main()
