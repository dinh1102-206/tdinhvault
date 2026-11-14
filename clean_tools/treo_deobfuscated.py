# Author: tdinh cute
# Decoded & Cleaned by: tdinh

"""
=============================================================================
DEOBFUSCATED SOURCE CODE: Treo-obf.py
Author: tdinh
Decoded by: tdinh cute
Classification: Discord Automation / Treo Tool (CLEAN / SAFE)
=============================================================================
"""

import os
import sys
import time
import random
import requests
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


class DiscordTool:
    def __init__(self):
        self.tokens = []
        self.channel_id = ""
        self.user_id_to_tag = ""
        self.delay = 1.0
        self.anti_band = True
        self.running = False
        self.message_index = 0
        self.messages = []

    def display_banner(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        console.print("""[bold cyan]
╔══════════════════════════════════════════════════════════════════════╗
║                   DISCORD TOOL - BY TDINH                            ║
║                   Decoded by: tdinh cute                             ║
║                Treo Chat | Check Token | Change Profile              ║
╚══════════════════════════════════════════════════════════════════════╝
[/bold cyan]""")

    def load_tokens_from_file(self, filename):
        if not os.path.exists(filename):
            console.print(f"[bold red]File '{filename}' khong ton tai![/bold red]")
            return []
        try:
            with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                self.tokens = [line.strip() for line in f if line.strip()]
            console.print(f"[bold green]Da tai {len(self.tokens)} token tu '{filename}'[/bold green]")
            return self.tokens
        except Exception as e:
            console.print(f"[bold red]Loi doc file: {e}[/bold red]")
            return []

    def load_messages_from_file(self, filename):
        if not os.path.exists(filename):
            console.print(f"[bold red]File '{filename}' khong ton tai![/bold red]")
            return []
        try:
            with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                self.messages = [line.strip() for line in f if line.strip()]
            console.print(f"[bold green]Da tai {len(self.messages)} tin nhan tu '{filename}'[/bold green]")
            return self.messages
        except Exception as e:
            console.print(f"[bold red]Loi doc file: {e}[/bold red]")
            return []

    def check_tokens(self):
        if not self.tokens:
            filename = Prompt.ask("[cyan]Nhap duong dan file token[/cyan]")
            self.load_tokens_from_file(filename)
            if not self.tokens:
                return

        alive = []
        dead = []
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
            task = progress.add_task("[yellow]Dang kiem tra token...", total=len(self.tokens))
            for token in self.tokens:
                headers = {"Authorization": token, "User-Agent": "Mozilla/5.0"}
                try:
                    r = requests.get("https://discord.com/api/v9/users/@me", headers=headers, timeout=5)
                    if r.status_code == 200:
                        alive.append(token)
                    else:
                        dead.append(token)
                except Exception:
                    dead.append(token)
                progress.advance(task)

        console.print(f"\n[bold green]Token Alive: {len(alive)}[/bold green] | [bold red]Token Dead: {len(dead)}[/bold red]")

    def send_message(self, token, msg, tag=""):
        headers = {
            "Authorization": token,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        }
        final_msg = f"<@{tag}> {msg}" if tag else msg
        payload = {"content": final_msg}
        url = f"https://discord.com/api/v9/channels/{self.channel_id}/messages"

        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=8)
            if resp.status_code == 200 or resp.status_code == 201:
                return True
            elif resp.status_code == 429:
                # Rate limit
                retry_after = resp.json().get("retry_after", 2)
                console.print(f"[yellow]Rate limited! Cho {retry_after}s...[/yellow]")
                time.sleep(retry_after)
                return False
            else:
                return False
        except Exception:
            return False

    def change_bio(self, token, bio):
        headers = {"Authorization": token, "Content-Type": "application/json"}
        try:
            requests.patch("https://discord.com/api/v9/users/@me", headers=headers, json={"bio": bio}, timeout=5)
        except Exception:
            pass

    def run_treo(self):
        if not self.tokens:
            fn = Prompt.ask("[cyan]Nhap file token[/cyan]")
            self.load_tokens_from_file(fn)
        if not self.messages:
            fn = Prompt.ask("[cyan]Nhap file messages[/cyan]")
            self.load_messages_from_file(fn)

        self.channel_id = Prompt.ask("[cyan]Nhap ID Channel[/cyan]")
        self.user_id_to_tag = Prompt.ask("[cyan]Nhap User ID can tag (De trong neu khong tag)[/cyan]", default="")
        delay_str = Prompt.ask("[cyan]Nhap delay (giay)[/cyan]", default="1.5")
        self.delay = float(delay_str)

        console.print("[bold green]Bat dau treo chat... Nhan Ctrl+C de dung.[/bold green]")
        token_idx = 0
        msg_idx = 0
        try:
            while True:
                token = self.tokens[token_idx % len(self.tokens)]
                msg = self.messages[msg_idx % len(self.messages)]
                ok = self.send_message(token, msg, self.user_id_to_tag)
                status = "[green]OK[/green]" if ok else "[red]FAIL[/red]"
                console.print(f"[{time.strftime('%H:%M:%S')}] {status} Token [{token_idx % len(self.tokens) + 1}]: {msg[:30]}")
                token_idx += 1
                msg_idx += 1
                time.sleep(self.delay)
        except KeyboardInterrupt:
            console.print("\n[yellow]Da dung treo chat![/yellow]")

    def menu(self):
        while True:
            self.display_banner()
            table = Table(title="MENU CHUC NANG", box=None)
            table.add_column("STT", style="cyan", justify="center")
            table.add_column("Chuc nang", style="white")
            table.add_row("1", "Treo chat spam channel")
            table.add_row("2", "Kiem tra Token (Check Alive/Dead)")
            table.add_row("3", "Thoat")
            console.print(table)

            choice = Prompt.ask("[cyan]Chon chuc nang[/cyan]", choices=["1", "2", "3"], default="1")
            if choice == "1":
                self.run_treo()
            elif choice == "2":
                self.check_tokens()
                Prompt.ask("\nNhan Enter de quay lai menu...")
            elif choice == "3":
                break


def main():
    tool = DiscordTool()
    tool.menu()


if __name__ == "__main__":
    main()
