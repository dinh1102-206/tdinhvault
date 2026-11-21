# Author: tdinh cute
# Decoded & Unlocked by: tdinh
# BlackForge Multi-Tool v1.0 - Fully Unlocked & Offline Version

import os
import sys
import time
from typing import Dict, Optional
from ui import BlackforgeUI, P1, P2, P3, BORDER, WHITE, MUTED, CYAN, SUCCESS, WARNING, DANGER, RESET
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
            "username": "tdinh",
            "expiry": "Lifetime (Unlocked by tdinh cute)",
            "raw": {"status": "success"}
        }

    def start(self):
        while True:
            BlackforgeUI.render_banner()
            
            print(BlackforgeUI.b_top("Control Panel"))
            
            usr = self.auth_data.get("username", "tdinh")
            exp = self.auth_data.get("expiry") or "Lifetime"
            print(BlackforgeUI.b_row(f"{P1}Account  {BORDER}| {WHITE}{usr}{RESET} {BORDER}- Expiry: {P2}{exp}{RESET}"))
            print(BlackforgeUI.b_row(f"{P1}Platform {BORDER}| {WHITE}FORGE TOOL ĐA CHỨC NĂNG (Unlocked){RESET}"))
            
            print(BlackforgeUI.b_div("Tools Available"))
            
            print(BlackforgeUI.b_row(f"{BORDER}[{P2} 1 {BORDER}] {WHITE}Discord Token Joiner{RESET}   {MUTED}- Join tokens to server{RESET}"))
            print(BlackforgeUI.b_row(f"{BORDER}[{P2} 2 {BORDER}] {WHITE}Phone Bomber / Spammer{RESET} {MUTED}- SMS/Call flooding utility{RESET}"))
            print(BlackforgeUI.b_row(f"{BORDER}[{P2} 3 {BORDER}] {WHITE}Discord Msg Spammer{RESET}    {MUTED}- Spam messages with tokens{RESET}"))
            print(BlackforgeUI.b_row(f"{BORDER}[{P2} 4 {BORDER}] {WHITE}Token Check{RESET}           {MUTED}- Remove invalid tokens from file{RESET}"))
            print(BlackforgeUI.b_row(f"{BORDER}[{P2} 5 {BORDER}] {WHITE}Discord Server Nuker{RESET}   {MUTED}- Wipe channels & blast msgs{RESET}"))
            print(BlackforgeUI.b_row(f"{BORDER}[{P2} 6 {BORDER}] {WHITE}Name Sniper{RESET}            {MUTED}- Find available Discord names{RESET}"))
            print(BlackforgeUI.b_row(f"{BORDER}[{P2} 7 {BORDER}] {WHITE}Exit Console{RESET}           {MUTED}- Terminate session and close{RESET}"))
            
            print(BlackforgeUI.b_bottom())
            print()

            margin = BlackforgeUI.get_margin()
            prompt = f"{margin}{CYAN}[?]{RESET} {WHITE}Chọn chức năng (1-7): {RESET}"
            try:
                cmd = input(prompt).strip()
            except (KeyboardInterrupt, EOFError):
                print(f"\n\n{margin}Tạm biệt!\n")
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
                print(f"\n{margin}Tạm biệt!\n")
                time.sleep(0.5)
                sys.exit(0)
            else:
                print(f"\n{margin}{WARNING}Vui lòng chỉ nhập từ 1 đến 7.{RESET}\n")
                time.sleep(0.8)

if __name__ == "__main__":
    launcher = BlackForgeLauncher()
    launcher.start()
