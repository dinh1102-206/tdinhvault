# ==============================================================================
# TOOL NAME   : SPAM ADVANCED - AEHB Modern Edition (v4.5)
# REVERSED & RECONSTRUCTED FULL CLEAN SOURCE CODE
# CREDIT      : tdinh ( server : 4ever )
# LICENSE KEY : tdincte
# NOTE        : Reconstructed cleanly in Python from the native x64 PE binary
#               All malicious stealer logic (exfiltrating system telemetry & saved tokens
#               to Telegram bot 8274395689:AAFlnM0Umv8ZXG9K-BDj3I4HYZjP2CLg4-A) has been
#               PERMANENTLY REMOVED and neutralised.
# ==============================================================================

import os
import sys
import time
import json
import random
import threading
import requests
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from typing import List, Dict, Optional

# ==============================================================================
# CONFIGURATION & CONSTANTS
# ==============================================================================
TOOL_CREDIT = "tdinh ( server : 4ever )"
TOOL_KEY = "tdincte"
DISCORD_API_BASE = "https://discord.com/api/v10"
DISCORD_INVITE = "https://discord.gg/zQPVS3zHB"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
]

def get_discord_headers(token: str) -> Dict[str, str]:
    return {
        "Authorization": token,
        "User-Agent": random.choice(USER_AGENTS),
        "Content-Type": "application/json",
        "Origin": "https://discord.com",
        "Referer": "https://discord.com/channels/@me",
        "X-Discord-Locale": "en-US",
        "X-Discord-Timezone": "Asia/Ho_Chi_Minh",
        "X-Debug-Options": "bugReporterEnabled"
    }

# ==============================================================================
# CORE DISCORD ENGINE
# ==============================================================================
class DiscordEngine:
    @staticmethod
    def check_token(token: str) -> Dict:
        url = f"{DISCORD_API_BASE}/users/@me"
        headers = get_discord_headers(token)
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.status_code == 200:
                user_data = resp.json()
                uid = user_data.get("id", "Unknown")
                username = f"{user_data.get('username', '')}#{user_data.get('discriminator', '0')}"
                verified = user_data.get("verified", False)
                phone = user_data.get("phone", None) is not None
                mfa = user_data.get("mfa_enabled", False)
                nitro = "Yes" if user_data.get("premium_type", 0) > 0 else "No"

                # Check billing
                billing = "No"
                try:
                    b_resp = requests.get(f"{DISCORD_API_BASE}/users/@me/billing/payment-sources", headers=headers, timeout=8)
                    if b_resp.status_code == 200 and len(b_resp.json()) > 0:
                        billing = "Yes"
                except Exception:
                    pass

                # Check Guild count
                guilds_count = 0
                try:
                    g_resp = requests.get(f"{DISCORD_API_BASE}/users/@me/guilds", headers=headers, timeout=8)
                    if g_resp.status_code == 200:
                        guilds_count = len(g_resp.json())
                except Exception:
                    pass

                return {
                    "valid": True,
                    "token": token,
                    "id": uid,
                    "username": username,
                    "verified": verified,
                    "phone": phone,
                    "mfa": mfa,
                    "nitro": nitro,
                    "billing": billing,
                    "guilds": guilds_count
                }
            else:
                return {"valid": False, "token": token, "error": f"HTTP {resp.status_code}"}
        except Exception as e:
            return {"valid": False, "token": token, "error": str(e)}

    @staticmethod
    def send_channel_message(token: str, channel_id: str, content: str) -> bool:
        url = f"{DISCORD_API_BASE}/channels/{channel_id}/messages"
        headers = get_discord_headers(token)
        payload = {"content": content, "tts": False}
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=10)
            return resp.status_code in [200, 201]
        except Exception:
            return False

    @staticmethod
    def send_webhook_message(webhook_url: str, content: str) -> bool:
        payload = {"content": content}
        headers = {"Content-Type": "application/json"}
        try:
            resp = requests.post(webhook_url, json=payload, headers=headers, timeout=10)
            return resp.status_code in [200, 204]
        except Exception:
            return False

# ==============================================================================
# MODERN UI APPLICATION
# ==============================================================================
class DiscordToolModernApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("SPAM ADVANCED - AEHB Modern Edition (v4.5)")
        self.root.geometry("1020x680")
        self.root.configure(bg="#0f111a")

        self.tokens: List[str] = []
        self.selected_tokens: List[str] = []
        self.is_running = False
        self.stop_requested = False

        self.setup_styles()
        self.show_login_key_modal()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background="#0f111a", borderwidth=0)
        style.configure("TNotebook.Tab", background="#1a1c29", foreground="#a0a5b5", font=("Segoe UI", 10, "bold"), padding=[16, 8])
        style.map("TNotebook.Tab", background=[("selected", "#5865F2")], foreground=[("selected", "#ffffff")])

    def show_login_key_modal(self):
        self.auth_frame = tk.Frame(self.root, bg="#0f111a")
        self.auth_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=640, height=480)

        # Card container
        card = tk.Frame(self.auth_frame, bg="#161826", highlightbackground="#5865F2", highlightthickness=1)
        card.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        title_lbl = tk.Label(card, text="SPAM ADVANCED", font=("Segoe UI", 20, "bold"), fg="#ffffff", bg="#161826")
        title_lbl.pack(pady=(35, 5))

        sub_lbl = tk.Label(card, text=f"AEHB Modern Edition • Credit: {TOOL_CREDIT}", font=("Segoe UI", 10), fg="#8c92a4", bg="#161826")
        sub_lbl.pack(pady=(0, 25))

        hwid_box = tk.Frame(card, bg="#0d0e15", padx=15, pady=10, highlightbackground="#2d3148", highlightthickness=1)
        hwid_box.pack(fill=tk.X, padx=40, pady=5)
        tk.Label(hwid_box, text="MACHINE HWID:", font=("Consolas", 10), fg="#72767d", bg="#0d0e15").pack(side=tk.LEFT)
        self.hwid_var = tk.StringVar(value="F99436AA88047F4A")
        tk.Label(hwid_box, textvariable=self.hwid_var, font=("Consolas", 11, "bold"), fg="#FAA61A", bg="#0d0e15").pack(side=tk.RIGHT)

        tk.Label(card, text="ENTER ACCESS KEY:", font=("Segoe UI", 10, "bold"), fg="#dcddde", bg="#161826").pack(anchor=tk.W, padx=40, pady=(20, 5))
        self.key_entry = tk.Entry(card, font=("Segoe UI", 11), bg="#202234", fg="#ffffff", insertbackground="#ffffff", relief=tk.FLAT)
        self.key_entry.pack(fill=tk.X, padx=40, ipady=6)
        self.key_entry.focus()
        self.key_entry.bind("<Return>", lambda e: self.verify_key())

        btn_box = tk.Frame(card, bg="#161826")
        btn_box.pack(fill=tk.X, padx=40, pady=25)

        act_btn = tk.Button(btn_box, text="ACTIVATE", font=("Segoe UI", 10, "bold"), bg="#5865F2", fg="#ffffff", activebackground="#4752C4", relief=tk.FLAT, cursor="hand2", command=self.verify_key)
        act_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=(0, 5))

        copy_btn = tk.Button(btn_box, text="COPY HWID", font=("Segoe UI", 10), bg="#2d3148", fg="#ffffff", activebackground="#3c4260", relief=tk.FLAT, cursor="hand2", command=self.copy_hwid)
        copy_btn.pack(side=tk.RIGHT, fill=tk.X, expand=True, ipady=8, padx=(5, 0))

    def copy_hwid(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.hwid_var.get())
        messagebox.showinfo("Copied", "Machine HWID copied to clipboard!")

    def verify_key(self):
        entered = self.key_entry.get().strip()
        if entered == TOOL_KEY:
            self.auth_frame.destroy()
            self.build_main_gui()
        else:
            messagebox.showerror("Access Denied", "Key không chính xác! Vui lòng nhập key: tdincte")

    # ==============================================================================
    # MAIN GUI TABS
    # ==============================================================================
    def build_main_gui(self):
        # Header banner
        header = tk.Frame(self.root, bg="#161826", height=60)
        header.pack(fill=tk.X)

        title = tk.Label(header, text="⚡ SPAM ADVANCED v4.5", font=("Segoe UI", 14, "bold"), fg="#5865F2", bg="#161826")
        title.pack(side=tk.LEFT, padx=20, pady=15)

        credit = tk.Label(header, text=f"Reversed & Cleaned by {TOOL_CREDIT}", font=("Segoe UI", 10, "italic"), fg="#43b581", bg="#161826")
        credit.pack(side=tk.RIGHT, padx=20)

        # Tabs container
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # 1. Configuration Tab
        self.tab_config = tk.Frame(self.notebook, bg="#161826")
        self.notebook.add(self.tab_config, text=" ⚙ Configuration ")
        self.build_config_tab()

        # 2. Spam Messages Tab
        self.tab_spam = tk.Frame(self.notebook, bg="#161826")
        self.notebook.add(self.tab_spam, text=" ● Spam Messages ")
        self.build_spam_tab()

        # 3. Tag Spam Tab
        self.tab_tag = tk.Frame(self.notebook, bg="#161826")
        self.notebook.add(self.tab_tag, text=" ◆ Tag Spam ")
        self.build_tag_tab()

        # 4. Server Raid Tab
        self.tab_raid = tk.Frame(self.notebook, bg="#161826")
        self.notebook.add(self.tab_raid, text=" ■ Server RAID ")
        self.build_raid_tab()

        # 5. Token Checker Tab
        self.tab_checker = tk.Frame(self.notebook, bg="#161826")
        self.notebook.add(self.tab_checker, text=" ✔ Token Checker ")
        self.build_checker_tab()

    # --- TAB 1: CONFIGURATION ---
    def build_config_tab(self):
        lbl = tk.Label(self.tab_config, text="TOKEN LIST / SINGLE TOKEN (one per line):", font=("Segoe UI", 10, "bold"), fg="#dcddde", bg="#161826")
        lbl.pack(anchor=tk.W, padx=20, pady=(15, 5))

        self.config_tokens_text = scrolledtext.ScrolledText(self.tab_config, font=("Consolas", 10), bg="#202234", fg="#ffffff", insertbackground="#ffffff", height=10)
        self.config_tokens_text.pack(fill=tk.X, padx=20, pady=5)

        # Webhook URL input
        wh_lbl = tk.Label(self.tab_config, text="WEBHOOK URL (optional for Webhook mode):", font=("Segoe UI", 10, "bold"), fg="#dcddde", bg="#161826")
        wh_lbl.pack(anchor=tk.W, padx=20, pady=(10, 5))
        self.webhook_entry = tk.Entry(self.tab_config, font=("Consolas", 10), bg="#202234", fg="#ffffff", insertbackground="#ffffff")
        self.webhook_entry.pack(fill=tk.X, padx=20, ipady=4)

        btn_box = tk.Frame(self.tab_config, bg="#161826")
        btn_box.pack(fill=tk.X, padx=20, pady=15)

        save_btn = tk.Button(btn_box, text="SAVE TOKENS (Check & Add)", font=("Segoe UI", 10, "bold"), bg="#43b581", fg="#ffffff", relief=tk.FLAT, cursor="hand2", command=self.save_config_tokens)
        save_btn.pack(side=tk.LEFT, padx=(0, 10), ipady=6, ipadx=15)

        clr_btn = tk.Button(btn_box, text="CLEAR INPUT", font=("Segoe UI", 10), bg="#f04747", fg="#ffffff", relief=tk.FLAT, cursor="hand2", command=lambda: self.config_tokens_text.delete("1.0", tk.END))
        clr_btn.pack(side=tk.LEFT, ipady=6, ipadx=10)

        # Status
        self.config_status_lbl = tk.Label(self.tab_config, text="Tokens loaded: 0", font=("Segoe UI", 10), fg="#72767d", bg="#161826")
        self.config_status_lbl.pack(anchor=tk.W, padx=20, pady=5)

    def save_config_tokens(self):
        raw = self.config_tokens_text.get("1.0", tk.END).strip().split("\n")
        new_tokens = [t.strip() for t in raw if t.strip()]
        if not new_tokens:
            messagebox.showwarning("Empty", "Vui lòng dán ít nhất 1 token!")
            return

        for t in new_tokens:
            if t not in self.tokens:
                self.tokens.append(t)

        self.config_status_lbl.config(text=f"Total Saved Tokens: {len(self.tokens)}", fg="#43b581")
        self.config_tokens_text.delete("1.0", tk.END)
        messagebox.showinfo("Saved", f"Đã lưu thành công {len(new_tokens)} token vào hệ thống!")

    # --- TAB 2: SPAM MESSAGES ---
    def build_spam_tab(self):
        f = tk.Frame(self.tab_spam, bg="#161826")
        f.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

        # Target Channel ID
        tk.Label(f, text="TARGET CHANNEL ID:", font=("Segoe UI", 10, "bold"), fg="#dcddde", bg="#161826").pack(anchor=tk.W)
        self.spam_chan_entry = tk.Entry(f, font=("Consolas", 10), bg="#202234", fg="#ffffff", insertbackground="#ffffff")
        self.spam_chan_entry.pack(fill=tk.X, pady=(2, 10), ipady=4)

        # Delay
        tk.Label(f, text="DELAY (MS):", font=("Segoe UI", 10, "bold"), fg="#dcddde", bg="#161826").pack(anchor=tk.W)
        self.spam_delay_entry = tk.Entry(f, font=("Consolas", 10), bg="#202234", fg="#ffffff", insertbackground="#ffffff")
        self.spam_delay_entry.insert(0, "1000")
        self.spam_delay_entry.pack(fill=tk.X, pady=(2, 10), ipady=4)

        # Content
        tk.Label(f, text="MESSAGES TO SPAM (one per line):", font=("Segoe UI", 10, "bold"), fg="#dcddde", bg="#161826").pack(anchor=tk.W)
        self.spam_msg_text = scrolledtext.ScrolledText(f, font=("Segoe UI", 10), bg="#202234", fg="#ffffff", insertbackground="#ffffff", height=6)
        self.spam_msg_text.insert(tk.END, "Hello from tdinh (server: 4ever)!\nSPAM ADVANCED AEHB Modern\nWorking perfectly!")
        self.spam_msg_text.pack(fill=tk.X, pady=(2, 10))

        # Controls
        ctrl = tk.Frame(f, bg="#161826")
        ctrl.pack(fill=tk.X, pady=5)
        self.spam_start_btn = tk.Button(ctrl, text="▶ START SPAM", font=("Segoe UI", 10, "bold"), bg="#5865F2", fg="#ffffff", relief=tk.FLAT, cursor="hand2", command=self.start_spam_thread)
        self.spam_start_btn.pack(side=tk.LEFT, padx=(0, 10), ipady=6, ipadx=15)
        self.spam_stop_btn = tk.Button(ctrl, text="■ STOP", font=("Segoe UI", 10, "bold"), bg="#f04747", fg="#ffffff", relief=tk.FLAT, cursor="hand2", command=self.stop_execution)
        self.spam_stop_btn.pack(side=tk.LEFT, ipady=6, ipadx=15)

        # Log
        self.spam_log = scrolledtext.ScrolledText(f, font=("Consolas", 9), bg="#0d0e15", fg="#a0a5b5", height=10)
        self.spam_log.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

    def log(self, widget: scrolledtext.ScrolledText, text: str):
        widget.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {text}\n")
        widget.see(tk.END)

    def start_spam_thread(self):
        chan = self.spam_chan_entry.get().strip()
        wh = self.webhook_entry.get().strip()
        if not chan and not wh:
            messagebox.showwarning("Missing", "Vui lòng nhập Channel ID hoặc Webhook URL!")
            return
        if not chan and not self.tokens:
            messagebox.showwarning("No Tokens", "Không có token nào được lưu trong tab Configuration!")
            return

        msgs = [m.strip() for m in self.spam_msg_text.get("1.0", tk.END).strip().split("\n") if m.strip()]
        if not msgs:
            messagebox.showwarning("No Messages", "Vui lòng nhập nội dung spam!")
            return

        delay = int(self.spam_delay_entry.get().strip() or "1000") / 1000.0
        self.is_running = True
        self.stop_requested = False
        threading.Thread(target=self.run_spam_worker, args=(chan, wh, msgs, delay), daemon=True).start()

    def run_spam_worker(self, chan: str, wh: str, msgs: List[str], delay: float):
        self.log(self.spam_log, f">> SPAM started (Threads: {len(self.tokens) or 1})")
        while self.is_running and not self.stop_requested:
            msg = random.choice(msgs)
            if wh:
                ok = DiscordEngine.send_webhook_message(wh, msg)
                self.log(self.spam_log, f"[Webhook] Sent: {msg[:30]}... ({'OK' if ok else 'FAIL'})")
            else:
                for token in self.tokens:
                    if self.stop_requested:
                        break
                    ok = DiscordEngine.send_channel_message(token, chan, msg)
                    self.log(self.spam_log, f"[{token[:10]}...] Sent: {msg[:25]}... ({'OK' if ok else 'FAIL'})")
                    time.sleep(delay)
            time.sleep(delay)
        self.log(self.spam_log, ">> SPAM stopped.")

    def stop_execution(self):
        self.stop_requested = True
        self.is_running = False

    # --- TAB 3: TAG SPAM ---
    def build_tag_tab(self):
        f = tk.Frame(self.tab_tag, bg="#161826")
        f.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

        tk.Label(f, text="TARGET CHANNEL ID:", font=("Segoe UI", 10, "bold"), fg="#dcddde", bg="#161826").pack(anchor=tk.W)
        self.tag_chan_entry = tk.Entry(f, font=("Consolas", 10), bg="#202234", fg="#ffffff", insertbackground="#ffffff")
        self.tag_chan_entry.pack(fill=tk.X, pady=(2, 10), ipady=4)

        tk.Label(f, text="USER ID TO TAG (MENTION):", font=("Segoe UI", 10, "bold"), fg="#dcddde", bg="#161826").pack(anchor=tk.W)
        self.tag_uid_entry = tk.Entry(f, font=("Consolas", 10), bg="#202234", fg="#ffffff", insertbackground="#ffffff")
        self.tag_uid_entry.pack(fill=tk.X, pady=(2, 10), ipady=4)

        tk.Label(f, text="WORDS TO SPAM WITH TAG (one per line):", font=("Segoe UI", 10, "bold"), fg="#dcddde", bg="#161826").pack(anchor=tk.W)
        self.tag_msg_text = scrolledtext.ScrolledText(f, font=("Segoe UI", 10), bg="#202234", fg="#ffffff", insertbackground="#ffffff", height=5)
        self.tag_msg_text.insert(tk.END, "alo ban oi\nday som di\nchao mung ban den voi server 4ever")
        self.tag_msg_text.pack(fill=tk.X, pady=(2, 10))

        ctrl = tk.Frame(f, bg="#161826")
        ctrl.pack(fill=tk.X, pady=5)
        tk.Button(ctrl, text="▶ START TAG SPAM", font=("Segoe UI", 10, "bold"), bg="#5865F2", fg="#ffffff", relief=tk.FLAT, cursor="hand2", command=self.start_tag_spam_thread).pack(side=tk.LEFT, padx=(0, 10), ipady=6, ipadx=15)
        tk.Button(ctrl, text="■ STOP", font=("Segoe UI", 10, "bold"), bg="#f04747", fg="#ffffff", relief=tk.FLAT, cursor="hand2", command=self.stop_execution).pack(side=tk.LEFT, ipady=6, ipadx=15)

        self.tag_log = scrolledtext.ScrolledText(f, font=("Consolas", 9), bg="#0d0e15", fg="#a0a5b5", height=10)
        self.tag_log.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

    def start_tag_spam_thread(self):
        chan = self.tag_chan_entry.get().strip()
        uid = self.tag_uid_entry.get().strip()
        if not chan or not uid:
            messagebox.showwarning("Missing", "Vui lòng nhập Channel ID và User ID cần tag!")
            return
        if not self.tokens:
            messagebox.showwarning("No Tokens", "Không có token nào được lưu trong tab Configuration!")
            return

        words = [w.strip() for w in self.tag_msg_text.get("1.0", tk.END).strip().split("\n") if w.strip()]
        self.is_running = True
        self.stop_requested = False
        threading.Thread(target=self.run_tag_worker, args=(chan, uid, words), daemon=True).start()

    def run_tag_worker(self, chan: str, uid: str, words: List[str]):
        self.log(self.tag_log, f">> TAG SPAM started on user <@{uid}>")
        mention = f"<@{uid}>"
        while self.is_running and not self.stop_requested:
            for token in self.tokens:
                if self.stop_requested:
                    break
                w = random.choice(words) if words else ""
                content = f"{mention} {w}"
                ok = DiscordEngine.send_channel_message(token, chan, content)
                self.log(self.tag_log, f"[{token[:10]}...] Tagged: {content[:30]} ({'OK' if ok else 'FAIL'})")
                time.sleep(1.0)
        self.log(self.tag_log, ">> TAG SPAM stopped.")

    # --- TAB 4: SERVER RAID ---
    def build_raid_tab(self):
        f = tk.Frame(self.tab_raid, bg="#161826")
        f.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

        tk.Label(f, text="TARGET CHANNEL ID:", font=("Segoe UI", 10, "bold"), fg="#dcddde", bg="#161826").pack(anchor=tk.W)
        self.raid_chan_entry = tk.Entry(f, font=("Consolas", 10), bg="#202234", fg="#ffffff", insertbackground="#ffffff")
        self.raid_chan_entry.pack(fill=tk.X, pady=(2, 10), ipady=4)

        tk.Label(f, text="RAID MESSAGES (one per line):", font=("Segoe UI", 10, "bold"), fg="#dcddde", bg="#161826").pack(anchor=tk.W)
        self.raid_msg_text = scrolledtext.ScrolledText(f, font=("Segoe UI", 10), bg="#202234", fg="#ffffff", insertbackground="#ffffff", height=5)
        self.raid_msg_text.insert(tk.END, "# RAID SERVER\nLINK EXPIRED\nServer is dead!\nCredit: tdinh (server: 4ever)")
        self.raid_msg_text.pack(fill=tk.X, pady=(2, 10))

        ctrl = tk.Frame(f, bg="#161826")
        ctrl.pack(fill=tk.X, pady=5)
        tk.Button(ctrl, text="▶ START RAID", font=("Segoe UI", 10, "bold"), bg="#5865F2", fg="#ffffff", relief=tk.FLAT, cursor="hand2", command=self.start_raid_thread).pack(side=tk.LEFT, padx=(0, 10), ipady=6, ipadx=15)
        tk.Button(ctrl, text="■ STOP", font=("Segoe UI", 10, "bold"), bg="#f04747", fg="#ffffff", relief=tk.FLAT, cursor="hand2", command=self.stop_execution).pack(side=tk.LEFT, ipady=6, ipadx=15)

        self.raid_log = scrolledtext.ScrolledText(f, font=("Consolas", 9), bg="#0d0e15", fg="#a0a5b5", height=10)
        self.raid_log.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

    def start_raid_thread(self):
        chan = self.raid_chan_entry.get().strip()
        if not chan:
            messagebox.showwarning("Missing", "Vui lòng nhập Channel ID!")
            return
        if not self.tokens:
            messagebox.showwarning("No Tokens", "Không có token nào được lưu trong tab Configuration!")
            return

        msgs = [m.strip() for m in self.raid_msg_text.get("1.0", tk.END).strip().split("\n") if m.strip()]
        self.is_running = True
        self.stop_requested = False
        threading.Thread(target=self.run_raid_worker, args=(chan, msgs), daemon=True).start()

    def run_raid_worker(self, chan: str, msgs: List[str]):
        self.log(self.raid_log, f">> SERVER RAID started ({len(self.tokens)} tokens attacking)")
        while self.is_running and not self.stop_requested:
            for token in self.tokens:
                if self.stop_requested:
                    break
                m = random.choice(msgs) if msgs else "# RAID SERVER"
                ok = DiscordEngine.send_channel_message(token, chan, m)
                self.log(self.raid_log, f"[{token[:10]}...] Sent: {m[:25]} ({'OK' if ok else 'FAIL'})")
                time.sleep(0.5)
        self.log(self.raid_log, ">> SERVER RAID stopped.")

    # --- TAB 5: TOKEN CHECKER ---
    def build_checker_tab(self):
        f = tk.Frame(self.tab_checker, bg="#161826")
        f.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

        tk.Label(f, text="TOKENS TO CHECK (one per line):", font=("Segoe UI", 10, "bold"), fg="#dcddde", bg="#161826").pack(anchor=tk.W)
        self.checker_input = scrolledtext.ScrolledText(f, font=("Consolas", 10), bg="#202234", fg="#ffffff", insertbackground="#ffffff", height=6)
        self.checker_input.pack(fill=tk.X, pady=(2, 10))

        ctrl = tk.Frame(f, bg="#161826")
        ctrl.pack(fill=tk.X, pady=5)
        tk.Button(ctrl, text="▶ CHECK ALL", font=("Segoe UI", 10, "bold"), bg="#43b581", fg="#ffffff", relief=tk.FLAT, cursor="hand2", command=self.start_check_tokens).pack(side=tk.LEFT, padx=(0, 10), ipady=6, ipadx=15)
        tk.Button(ctrl, text="EXPORT LIVE TOKENS", font=("Segoe UI", 10), bg="#2d3148", fg="#ffffff", relief=tk.FLAT, cursor="hand2", command=self.export_live_tokens).pack(side=tk.LEFT, ipady=6, ipadx=10)

        # Treeview Results
        cols = ("Status", "Token", "User", "Nitro", "Billing", "MFA", "Phone", "Guilds")
        self.tree = ttk.Treeview(f, columns=cols, show="headings", height=10)
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=90, anchor=tk.CENTER)
        self.tree.column("Token", width=220)
        self.tree.column("User", width=140)
        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)

    def start_check_tokens(self):
        raw = self.checker_input.get("1.0", tk.END).strip().split("\n")
        to_check = [t.strip() for t in raw if t.strip()]
        if not to_check:
            to_check = self.tokens
        if not to_check:
            messagebox.showwarning("Empty", "Không có token nào để kiểm tra!")
            return

        for row in self.tree.get_children():
            self.tree.delete(row)

        threading.Thread(target=self.run_checker_worker, args=(to_check,), daemon=True).start()

    def run_checker_worker(self, token_list: List[str]):
        self.live_tokens_found = []
        for t in token_list:
            res = DiscordEngine.check_token(t)
            if res.get("valid"):
                self.live_tokens_found.append(t)
                self.tree.insert("", tk.END, values=(
                    "LIVE",
                    t[:25] + "...",
                    res.get("username"),
                    res.get("nitro"),
                    res.get("billing"),
                    "Yes" if res.get("mfa") else "No",
                    "Yes" if res.get("phone") else "No",
                    res.get("guilds")
                ))
            else:
                self.tree.insert("", tk.END, values=("DEAD", t[:25] + "...", "-", "-", "-", "-", "-", "-"))
            time.sleep(0.3)
        messagebox.showinfo("Done", f"Đã check xong! Live: {len(self.live_tokens_found)} | Dead: {len(token_list) - len(self.live_tokens_found)}")

    def export_live_tokens(self):
        if not hasattr(self, "live_tokens_found") or not self.live_tokens_found:
            messagebox.showwarning("No Live", "Chưa có token Live nào để xuất!")
            return
        with open("live_tokens.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(self.live_tokens_found))
        messagebox.showinfo("Exported", f"Đã xuất {len(self.live_tokens_found)} live tokens ra file live_tokens.txt")

# ==============================================================================
# ENTRY POINT
# ==============================================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = DiscordToolModernApp(root)
    root.mainloop()
