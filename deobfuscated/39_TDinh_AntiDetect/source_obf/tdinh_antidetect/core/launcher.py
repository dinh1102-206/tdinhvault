# Author: tdinh cute
# Browser Launcher Engine

import os
import subprocess
import random
import zlib
from core.fingerprint_injector import generate_stealth_extension
from core.proxy_auth_injector import generate_proxy_auth_extension

CHROME_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe")
]

EDGE_PATHS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
]

def find_browser(b_type: str = "Chrome") -> str:
    candidates = CHROME_PATHS if b_type.lower() == "chrome" else EDGE_PATHS
    for p in candidates:
        if os.path.exists(p):
            return p
    # Fallback
    for p in CHROME_PATHS + EDGE_PATHS:
        if os.path.exists(p):
            return p
    return None

class BrowserLauncher:
    def __init__(self, base_dir: str):
        self.base_dir = base_dir
        self.profiles_dir = os.path.join(base_dir, "profiles")
        self.ext_dir = os.path.join(base_dir, "extensions")
        self.running_processes = {}

    def launch(self, profile: dict):
        pid = profile["id"]
        p_name = profile.get("name", pid)
        browser_type = profile.get("browser", "Chrome")
        browser_exe = find_browser(browser_type)
        if not browser_exe:
            raise RuntimeError(f"Không tìm thấy trình duyệt {browser_type} trên máy tính!")

        # Dedicated isolated profile directory
        profile_path = os.path.join(self.profiles_dir, pid)
        os.makedirs(profile_path, exist_ok=True)

        loaded_extensions = []

        # 1. Generate Stealth Fingerprint extension
        if profile.get("canvas_noise", True):
            # Seed based on profile ID
            seed = zlib.crc32(pid.encode())
            p_ext_dir = os.path.join(self.ext_dir, f"stealth_{pid}")
            generate_stealth_extension(p_ext_dir, canvas_seed=seed, audio_seed=seed + 100)
            loaded_extensions.append(p_ext_dir)

        # 2. Parse and handle Proxy
        proxy_str = profile.get("proxy", "").strip()
        proxy_arg = None
        if proxy_str:
            # Format: host:port or host:port:user:pass
            parts = proxy_str.split(":")
            if len(parts) == 2:
                proxy_arg = f"--proxy-server={parts[0]}:{parts[1]}"
            elif len(parts) == 4:
                host, port, user, pwd = parts
                proxy_arg = f"--proxy-server={host}:{port}"
                p_auth_dir = os.path.join(self.ext_dir, f"auth_{pid}")
                generate_proxy_auth_extension(p_auth_dir, user, pwd)
                loaded_extensions.append(p_auth_dir)

        # Build Arguments
        args = [
            browser_exe,
            f"--user-data-dir={profile_path}",
            "--disable-blink-features=AutomationControlled",
            "--disable-infobars",
            "--no-first-run",
            "--no-default-browser-check",
            "--password-store=basic",
            "--webrtc-ip-handling-policy=disable_non_proxied_udp"
        ]

        # User-Agent
        ua = profile.get("user_agent")
        if ua:
            args.append(f"--user-agent={ua}")

        # Proxy
        if proxy_arg:
            args.append(proxy_arg)

        # Extensions
        if loaded_extensions:
            ext_paths = ",".join(loaded_extensions)
            args.append(f"--load-extension={ext_paths}")

        # Start Page: whoer.net or iphey to verify fingerprint
        args.append("https://iphey.com")

        print(f"Launching profile {p_name} ({pid})...")
        proc = subprocess.Popen(args)
        self.running_processes[pid] = proc
        return proc

    def stop(self, pid: str):
        if pid in self.running_processes:
            try:
                self.running_processes[pid].terminate()
            except Exception:
                pass
            del self.running_processes[pid]
            return True
        return False
