"""
# Author: tdinh cute
# Decoded by: tdinh cute
# Description: Discord Auto Register & Verification Tool via Temp-Mail (devtai.net)
# Original File: input/regdis.py (Obfuscated via pyobfuscate.com)
"""

import time
import re
import random
import webbrowser
import httpx

EMAIL_API = "https://email.devtai.net/api"
DOMAINS = ["antdev.org", "epmtyfl.me", "sptech.io.vn"]

class DiscordManager:
    def __init__(self):
        self.headers = {
            "authority": "discord.com",
            "accept": "*/*",
            "accept-language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/json",
            "origin": "https://discord.com",
            "referer": "https://discord.com/login",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
        }

    def login_discord(self, email: str, password: str, twofa_key: str = None):
        """
        Authenticate with Discord login API and obtain token (or handle 2FA/TOTP).
        """
        url = "https://discord.com/api/v9/auth/login"
        payload = {
            "login": email,
            "password": password,
            "undelete": False
        }
        with httpx.Client(headers=self.headers, timeout=15.0) as client:
            resp = client.post(url, json=payload)
            data = resp.json()
            
            if "token" in data:
                return data["token"]
            elif data.get("mfa") and twofa_key:
                ticket = data.get("ticket")
                totp_url = "https://discord.com/api/v9/auth/mfa/totp"
                totp_payload = {
                    "code": twofa_key,
                    "ticket": ticket
                }
                totp_resp = client.post(totp_url, json=totp_payload)
                totp_data = totp_resp.json()
                return totp_data.get("token")
            return None

def create_temp_email():
    """Tạo email ảo từ hệ thống devtai.net"""
    domain = random.choice(DOMAINS)
    username = f"user_{random.randint(100000, 999999)}"
    email = f"{username}@{domain}"
    return email

def check_discord_verification_email(email: str, max_attempts: int = 30, delay: int = 3):
    """
    Lắng nghe hộp thư đến từ Discord và trích xuất link xác thực.
    """
    print(f"[*] Đang chờ email xác thực cho: {email}...")
    with httpx.Client(timeout=10.0) as client:
        for attempt in range(max_attempts):
            try:
                # Kiểm tra danh sách thư
                res = client.get(f"{EMAIL_API}/messages?email={email}")
                messages = res.json()
                
                if messages and len(messages) > 0:
                    for msg in messages:
                        sender = msg.get("from", "")
                        subject = msg.get("subject", "")
                        if "discord" in sender.lower() or "discord" in subject.lower():
                            print("\033[92m✓ Đã nhận email từ Discord!\033[0m")
                            msg_id = msg.get("id")
                            msg_detail = client.get(f"{EMAIL_API}/message/{msg_id}").json()
                            body = msg_detail.get("html") or msg_detail.get("text") or ""
                            
                            # Trích xuất link xác thực
                            links = re.findall(r'https?://(?:click\.discord\.com|discord\.com)[^\s"\'<>]+', body)
                            if links:
                                verify_url = links[0]
                                print("\033[92m=== LINK XÁC THỰC DISCORD ===\033[0m")
                                print(verify_url)
                                print("\033[93m⏳ Đang tự động mở link xác thực trong trình duyệt...\033[0m")
                                webbrowser.open(verify_url)
                                return verify_url
                else:
                    print(f"\033[93m[{attempt+1}/{max_attempts}] Chưa có email mới...\033[0m")
            except Exception as e:
                pass
            time.sleep(delay)
            
    print("\n\033[91mHết thời gian – Không tìm thấy link xác thực.\033[0m")
    return None

def save_token(token: str, email: str, password: str):
    """Lưu token ra file discord_tokens.txt"""
    with open("discord_tokens.txt", "a", encoding="utf-8") as f:
        f.write(f"{email}:{password}:{token}\n")
    print(f"\033[92m✓ Đã lưu vào discord_tokens.txt: {token}\033[0m")

def main():
    print("=" * 60)
    print("   DISCORD AUTO-REG HELPER & TOKEN SAVER   ")
    print("   Decoded & Reconstructed by: tdinh cute  ")
    print("=" * 60)
    
    email = create_temp_email()
    print(f"[+] Email tạo tự động: \033[96m{email}\033[0m")
    print("[*] Hãy copy email trên đăng ký Discord.")
    
    # Mở trình duyệt đăng ký
    webbrowser.open("https://discord.com/register")
    
    # Lắng nghe mail
    verify_link = check_discord_verification_email(email)
    
    input("\n\033[96m→ Nhấn Enter sau khi đã xác thực email trên trình duyệt...\033[0m")
    password = input("\nNhập mật khẩu Discord vừa tạo: ")
    
    manager = DiscordManager()
    print("[*] Đang kết nối Discord để lấy Token...")
    token = manager.login_discord(email, password)
    
    if token:
        save_token(token, email, password)
    else:
        print("\033[91m[!] Không lấy được token trực tiếp, hãy check thủ công.\033[0m")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Đã dừng chương trình.")
