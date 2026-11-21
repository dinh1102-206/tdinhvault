# Author: tdinh cute
# Decoded & Unlocked by: tdinh
# BlackForge Multi-Tool v1.0 - Fully Unlocked & Offline Version

import os
import sys
import time
from typing import Dict, Optional
from ui import BlackforgeUI, R1, R2, R3, R4, R5, BORDER, WHITE, MUTED, SUCCESS, WARNING, DANGER, RESET, center_text
from tools.token_joiner import run_token_joiner
from tools.phone_spammer import run_spammer
from tools.spammer import run_spammer_msg
from tools.token_remover import run_token_purger
from tools.nuker import run_nuker
from tools.name import run_name_sniper

class BlackForgeLauncher:
    def __init__(self):
        # Bypass LynxAuth authentication completely
        self.auth_data: Dict = {
            "username": "tdinh_vip",
            "expiry": "Lifetime (Unlocked by tdinh cute)",
            "raw": {"status": "success"}
        }

    def start(self):
        while True:
            BlackforgeUI.render_banner()
            
            print(BlackforgeUI.b_top("Control Panel"))
            print(BlackforgeUI.b_row())
            
            usr = self.auth_data.get("username", "tdinh")
            exp = self.auth_data.get("expiry") or "Lifetime"
            print(BlackforgeUI.b_row(f"{R1}Account  {BORDER}│ {WHITE}{usr}{RESET} {BORDER}• Expiry: {R2}{exp}{RESET}"))
            print(BlackforgeUI.b_row(f"{R1}Platform {BORDER}│ {WHITE}Black-Forge Multi-Tool v1.0 (Unlocked){RESET}"))
            
            print(BlackforgeUI.b_row())
            print(BlackforgeUI.b_div("Tools Available"))
            print(BlackforgeUI.b_row())
            
            print(BlackforgeUI.b_row(f"  {BORDER}╭──[{R2} 1 {BORDER}]──{RESET} {WHITE}Discord Token Joiner{RESET}   {MUTED}─── Join tokens to server{RESET}"))
            print(BlackforgeUI.b_row(f"  {BORDER}╭──[{R2} 2 {BORDER}]──{RESET} {WHITE}Phone Bomber / Spammer{RESET} {MUTED}─── SMS/Call flooding utility{RESET}"))
            print(BlackforgeUI.b_row(f"  {BORDER}╭──[{R2} 3 {BORDER}]──{RESET} {WHITE}Discord Msg Spammer{RESET}    {MUTED}─── Spam messages with tokens{RESET}"))
            print(BlackforgeUI.b_row(f"  {BORDER}╭──[{R2} 4 {BORDER}]──{RESET} {WHITE}Token Check{RESET}           {MUTED}─── Remove invalid tokens from file{RESET}"))
            print(BlackforgeUI.b_row(f"  {BORDER}╭──[{R2} 5 {BORDER}]──{RESET} {WHITE}Discord Server Nuker{RESET}   {MUTED}─── Wipe channels & blast msgs{RESET}"))
            print(BlackforgeUI.b_row(f"  {BORDER}╭──[{R2} 6 {BORDER}]──{RESET} {WHITE}Name Sniper{RESET}            {MUTED}─── Find available Discord names{RESET}"))
            print(BlackforgeUI.b_row(f"  {BORDER}╭──[{R2} 7 {BORDER}]──{RESET} {WHITE}Exit Console{RESET}           {MUTED}─── Terminate session and close{RESET}"))
            
            print(BlackforgeUI.b_row())
            print(BlackforgeUI.b_bottom())
            print()

            prompt_line = center_text(f"{BORDER}╭──────────[ {R1}Choose Option{RESET}{BORDER} ]──────────╮{RESET}")
            sub_prompt  = center_text(f"{BORDER}╰─────[ {R2}❯❯{RESET}{BORDER} ]{RESET} ")
            print(prompt_line)
            try:
                cmd = input(sub_prompt).strip()
            except (KeyboardInterrupt, EOFError):
                print(f"\n\n{center_text('Goodbye!')}\n")
                sys.exit(0)

            if cmd == "1":
                run_token_joiner(self.auth_data)
            elif cmd == "2":
                run_spammer()
            elif cmd == "3":
                run_spammer_msg(self.auth_data)
            elif cmd == "4":
                run_token_purger(self.auth_data)
            elif cmd == "5":
                run_nuker(self.auth_data)
            elif cmd == "6":
                run_name_sniper(self.auth_data)
            elif cmd == "7":
                print(f"\n{center_text('Goodbye!')}\n")
                time.sleep(0.5)
                sys.exit(0)
            else:
                print(f"\n{center_text(f'{WARNING}Please enter 1–7.{RESET}')}\n")
                time.sleep(0.5)

if __name__ == "__main__":
    launcher = BlackForgeLauncher()
    launcher.start()
