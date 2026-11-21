import os
import sys
import queue
import random
import string
import threading
import time
from itertools import product
from typing import Dict, List, Optional

import requests

from ui import (
    BlackforgeUI as TerminalUI,
    R1, R2, BORDER, WHITE, MUTED,
    SUCCESS, WARNING, DANGER, RESET, center_text,
)

SILVER = "\033[38;2;160;160;160m"

POMELO_ENDPOINT = "https://discord.com/api/v10/users/@me/pomelo-attempt"
DISCORD_MIN_LEN = 4
DISCORD_MAX_LEN = 32
SETUP_DIR = os.path.join(
    os.path.dirname(sys.executable) if getattr(sys, 'frozen', False)
    else os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "setup"
)

_lock       = threading.Lock()
_checked    = 0
_found      = 0
_stop_event = threading.Event()


def _load_tokens() -> List[str]:
    path = os.path.join(SETUP_DIR, "tokens.txt")
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return [ln.strip() for ln in f if ln.strip()]


def _make_session(token: str) -> requests.Session:
    s = requests.Session()
    s.headers.update({
        "Authorization": token,
        "Content-Type":  "application/json",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Origin":  "https://discord.com",
        "Referer": "https://discord.com/register",
    })
    a = requests.adapters.HTTPAdapter(
        pool_connections=1, pool_maxsize=1, max_retries=0
    )
    s.mount("https://", a)
    s.mount("http://",  a)
    return s


def _build_charset(mode: str) -> str:
    if mode == "1": return string.ascii_lowercase
    if mode == "2": return string.digits
    if mode == "3": return string.ascii_lowercase + string.digits
    if mode == "4": return string.ascii_lowercase + string.digits + "_."
    return string.ascii_lowercase


def _prompt(label: str) -> str:
    print(center_text(f"{BORDER}╭──────────[ {R1}{label}{RESET}{BORDER} ]──────────╮{RESET}"))
    return input(center_text(f"{BORDER}╰─────[ {R2}❯❯{RESET}{BORDER} ]{RESET} ")).strip()


_wh_session = requests.Session()

def _send_webhook(url: str, username: str):
    try:
        _wh_session.post(url, json={
            "content":  None,
            "username": "Black-Forge Sniper",
            "embeds": [{
                "title":       "Name Sniper — HIT",
                "description": f"```\n{username}\n```",
                "color":       0xFF3C3C,
                "fields": [
                    {"name": "Username", "value": f"`{username}`",      "inline": True},
                    {"name": "Length",   "value": f"`{len(username)}`", "inline": True},
                    {"name": "Status",   "value": "AVAILABLE",          "inline": True},
                ],
                "footer":    {"text": "Black-Forge Name Sniper  •  Lynx Modz"},
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            }],
        }, timeout=6)
    except Exception:
        pass

def _worker(token: str, work_q: queue.Queue, webhook_url: str):
    global _checked, _found
    session = _make_session(token)

    while not _stop_event.is_set():
        try:
            username = work_q.get(timeout=1)
        except queue.Empty:
            continue

        if username is None:          # poison pill — shut down
            work_q.task_done()
            return

        try:
            r = session.post(POMELO_ENDPOINT, json={"username": username}, timeout=4)

            if r.status_code == 200:
                taken = r.json().get("taken", True)
                with _lock:
                    _checked += 1
                    c = _checked

                if not taken:
                    with _lock:
                        _found += 1
                    TerminalUI.log(
                        f"{MUTED}[{c:>7}]{RESET}  "
                        f"{SUCCESS}AVAILABLE{RESET}  "
                        f"{R1}>{RESET} {WHITE}{username}{RESET}"
                    )
                    if webhook_url:
                        threading.Thread(
                            target=_send_webhook,
                            args=(webhook_url, username),
                            daemon=True,
                        ).start()
                else:
                    TerminalUI.log(
                        f"{MUTED}[{c:>7}]{RESET}  "
                        f"{DANGER}TAKEN    {RESET}  "
                        f"{R1}>{RESET} {SILVER}{username}{RESET}"
                    )

            elif r.status_code == 429:
                wait = min(float(r.headers.get("Retry-After", 3)), 10)
                TerminalUI.log(f"{WARNING}[RL] Token rate-limited — waiting {wait:.1f}s{RESET}")
                time.sleep(wait)
                work_q.put(username)      

            elif r.status_code == 401:
                TerminalUI.log(f"{DANGER}[AUTH] Token invalid — worker exiting{RESET}")
                work_q.task_done()
                return

        except Exception:
            work_q.put(username)

        work_q.task_done()


def _producer(charset: str, min_len: int, max_len: int,
               work_q: queue.Queue, n_workers: int):
    cs    = len(charset)
    total = sum(cs ** l for l in range(min_len, max_len + 1))

    if total <= 2_000_000:
        names: List[str] = []
        for length in range(min_len, max_len + 1):
            for combo in product(charset, repeat=length):
                names.append("".join(combo))
        random.shuffle(names)
        for name in names:
            if _stop_event.is_set():
                break
            work_q.put(name)
    else:
        seen: set = set()
        while not _stop_event.is_set():
            length = random.randint(min_len, max_len)
            name   = "".join(random.choice(charset) for _ in range(length))
            if name not in seen:
                seen.add(name)
                if len(seen) > 5_000_000:
                    seen.clear()
                work_q.put(name)

    for _ in range(n_workers):
        work_q.put(None)
def run_name_sniper(auth_data: Optional[Dict] = None):
    global _checked, _found
    _checked = 0
    _found   = 0
    _stop_event.clear()

    TerminalUI.render_banner("Name Sniper")

    if auth_data:
        usr = auth_data.get("username", "User")
        exp = auth_data.get("expiry") or "Lifetime"
        print(TerminalUI.b_top("Session"))
        print(TerminalUI.b_row(
            f"{R1}User   {BORDER}| {WHITE}{usr}{RESET}  {BORDER}• Expiry: {R2}{exp}{RESET}"
        ))
        print(TerminalUI.b_bottom())
        print()

    tokens = _load_tokens()
    if not tokens:
        print(center_text(f"{DANGER}No tokens found in setup/tokens.txt{RESET}"))
        print(center_text(f"{MUTED}Add Discord tokens (one per line) first.{RESET}"))
        print()
        input(center_text(f"{MUTED}Press Enter to go back...{RESET}"))
        return

    print(TerminalUI.b_top("Name Sniper — Setup"))
    print(TerminalUI.b_row())
    print(TerminalUI.b_row(
        f"{R1}Tokens  {BORDER}| {WHITE}{len(tokens)} token(s) loaded{RESET}"
    ))
    print(TerminalUI.b_row(
        f"{R1}Mode    {BORDER}| {WHITE}Random username generation — instant webhook on hit{RESET}"
    ))
    print(TerminalUI.b_row())
    print(TerminalUI.b_div("Character Set"))
    print(TerminalUI.b_row())
    print(TerminalUI.b_row(
        f"  {BORDER}╭──[{R2} 1 {BORDER}]──{RESET} {WHITE}Alphabets only            {MUTED}─── a-z{RESET}"
    ))
    print(TerminalUI.b_row(
        f"  {BORDER}╭──[{R2} 2 {BORDER}]──{RESET} {WHITE}Numbers only              {MUTED}─── 0-9{RESET}"
    ))
    print(TerminalUI.b_row(
        f"  {BORDER}╭──[{R2} 3 {BORDER}]──{RESET} {WHITE}Alphanumeric              {MUTED}─── a-z + 0-9{RESET}"
    ))
    print(TerminalUI.b_row(
        f"  {BORDER}╭──[{R2} 4 {BORDER}]──{RESET} {WHITE}Mixed (all Discord chars)  {MUTED}─── a-z + 0-9 + _ .{RESET}"
    ))
    print(TerminalUI.b_row())
    print(TerminalUI.b_bottom())
    print()

    try:
        while True:
            mode = _prompt("Choose charset (1/2/3/4)")
            if mode in ("1", "2", "3", "4"):
                break
            print(center_text(f"{DANGER}Enter 1, 2, 3 or 4{RESET}"))

        while True:
            raw = _prompt(f"Min name length ({DISCORD_MIN_LEN}–{DISCORD_MAX_LEN})")
            if raw.isdigit() and DISCORD_MIN_LEN <= int(raw) <= DISCORD_MAX_LEN:
                min_len = int(raw)
                break
            print(center_text(f"{DANGER}Must be {DISCORD_MIN_LEN}–{DISCORD_MAX_LEN}{RESET}"))

        while True:
            raw = _prompt(f"Max name length ({min_len}–{DISCORD_MAX_LEN})")
            if raw.isdigit() and min_len <= int(raw) <= DISCORD_MAX_LEN:
                max_len = int(raw)
                break
            print(center_text(f"{DANGER}Must be {min_len}–{DISCORD_MAX_LEN}{RESET}"))

        webhook_url = _prompt("Discord Webhook URL (leave blank to skip)")
        if webhook_url and not webhook_url.startswith("https://discord.com/api/webhooks/"):
            print(center_text(f"{WARNING}Invalid webhook — alerts disabled{RESET}"))
            webhook_url = ""

        raw_t = _prompt("Workers per token (1–20, recommended 5)")
        wpt   = int(raw_t) if raw_t.isdigit() and 1 <= int(raw_t) <= 20 else 5

    except (KeyboardInterrupt, EOFError):
        input(center_text(f"{MUTED}Press Enter to go back...{RESET}"))
        return

    charset      = _build_charset(mode)
    n_workers    = len(tokens) * wpt
    total_combos = sum(len(charset) ** l for l in range(min_len, max_len + 1))
    lbl          = {"1": "a-z", "2": "0-9", "3": "a-z + 0-9", "4": "a-z + 0-9 + _ ."}

    print()
    print(TerminalUI.b_top("Configuration"))
    print(TerminalUI.b_row())
    print(TerminalUI.b_row(f"{R1}Charset       {BORDER}| {WHITE}{lbl[mode]}{RESET}"))
    print(TerminalUI.b_row(f"{R1}Length        {BORDER}| {WHITE}{min_len}  →  {max_len}{RESET}"))
    print(TerminalUI.b_row(f"{R1}Combinations  {BORDER}| {WHITE}{total_combos:,}{RESET}"))
    print(TerminalUI.b_row(f"{R1}Tokens        {BORDER}| {WHITE}{len(tokens)}{RESET}"))
    print(TerminalUI.b_row(f"{R1}Workers       {BORDER}| {WHITE}{n_workers}  ({wpt}/token){RESET}"))
    print(TerminalUI.b_row(
        f"{R1}Webhook       {BORDER}| " +
        (f"{SUCCESS}Configured{RESET}" if webhook_url else f"{MUTED}Disabled{RESET}")
    ))
    print(TerminalUI.b_row())
    print(TerminalUI.b_bottom())
    print()

    print(center_text(
        f"{BORDER}╭──────────[ {R1}Start Sniper? (y/n){RESET}{BORDER} ]──────────╮{RESET}"
    ))
    try:
        go = input(center_text(
            f"{BORDER}╰─────[ {R2}❯❯{RESET}{BORDER} ]{RESET} "
        )).strip().lower()
    except (KeyboardInterrupt, EOFError):
        input(center_text(f"{MUTED}Press Enter to go back...{RESET}"))
        return

    if go not in ("y", "yes"):
        print(center_text(f"{WARNING}Cancelled.{RESET}\n"))
        input(center_text(f"{MUTED}Press Enter to go back...{RESET}"))
        return

    print()
    print(TerminalUI.b_top("Sniper — LIVE  (Ctrl+C to stop)"))
    print(TerminalUI.b_row(
        f"{MUTED}Available names print instantly. Ctrl+C to stop.{RESET}"
    ))
    print(TerminalUI.b_div())

    work_q: queue.Queue = queue.Queue(maxsize=n_workers * 8)

    threads: List[threading.Thread] = []
    for tok in tokens:
        for _ in range(wpt):
            t = threading.Thread(
                target=_worker,
                args=(tok, work_q, webhook_url),
                daemon=True,
            )
            t.start()
            threads.append(t)

    prod = threading.Thread(
        target=_producer,
        args=(charset, min_len, max_len, work_q, n_workers),
        daemon=True,
    )
    prod.start()

    try:
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        _stop_event.set()
        print()
        print(center_text(f"{WARNING}Sniper stopped by user.{RESET}"))

    print(TerminalUI.b_div())
    print(TerminalUI.b_row(f"{R1}Checked  {BORDER}| {WHITE}{_checked:,}{RESET}"))
    print(TerminalUI.b_row(
        f"{R1}Found    {BORDER}| " +
        (f"{SUCCESS}{_found}{RESET}" if _found else f"{MUTED}0{RESET}")
    ))
    print(TerminalUI.b_bottom())
    print()

    input(center_text(f"{MUTED}Press Enter to go back...{RESET}"))
