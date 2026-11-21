import os
import sys
import threading
import requests
from typing import Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from ui import BlackforgeUI as TerminalUI, R1, R2, BORDER, WHITE, MUTED, SUCCESS, WARNING, DANGER, RESET, center_text

ROOT_DIR  = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETUP_DIR = os.path.join(ROOT_DIR, "setup")

HTTP_SESSION = requests.Session()
_adapter = requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100)
HTTP_SESSION.mount("https://", _adapter)
HTTP_SESSION.mount("http://", _adapter)

DISCORD_BASE = "https://discord.com/api/v10"
DISCORD_HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "X-Discord-Locale": "en-US",
    "Origin": "https://discord.com",
}


def _get_user_profile(token: str) -> Optional[Dict]:
    try:
        r = HTTP_SESSION.get(
            f"{DISCORD_BASE}/users/@me",
            headers={"Authorization": token},
            timeout=5,
        )
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None


def _load_tokens(filename: str = "tokens.txt") -> List[str]:
    path = os.path.join(SETUP_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return [ln.strip() for ln in f if ln.strip()]


def _save_tokens(tokens: List[str], filename: str = "tokens.txt"):
    path = os.path.join(SETUP_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        for t in tokens:
            f.write(f"{t}\n")


def run_token_purger(auth_data: Optional[Dict] = None):
    TerminalUI.render_banner("Token Purger")

    tokens = _load_tokens("tokens.txt")

    if not tokens:
        print(center_text(f"{DANGER}No tokens found in tokens.txt{RESET}\n"))
        input(center_text(f"{MUTED}Press Enter to go back...{RESET}"))
        return

    total = len(tokens)
    valid_tokens:   List[str] = []
    invalid_tokens: List[str] = []
    lock = threading.Lock()

    if auth_data:
        usr = auth_data.get("username", "Authenticated User")
        exp = auth_data.get("expiry") or "Lifetime"
        print(TerminalUI.b_top("Session"))
        print(TerminalUI.b_row(f"{R1}User   {BORDER}| {WHITE}{usr}{RESET} {BORDER}• Expiry: {R2}{exp}{RESET}"))
        print(TerminalUI.b_bottom())
        print()

    print(TerminalUI.b_top("Token Purger"))
    print(TerminalUI.b_row(f"{R1}Checking {WHITE}{total}{R1} token(s) for validity...{RESET}"))
    print(TerminalUI.b_div())

    def worker(idx: int, t: str):
        prof = _get_user_profile(t)
        if not prof:
            with lock:
                invalid_tokens.append(t)
            TerminalUI.log(
                f"{MUTED}[{idx:>3}/{total}]{RESET} {DANGER}X {RESET}"
                f"{WHITE}{t[:22]}...{RESET} {DANGER}INVALID TOKEN{RESET}"
            )
        else:
            username = f"{prof.get('username')}#{prof.get('discriminator', '0000')}"
            with lock:
                valid_tokens.append(t)
            TerminalUI.log(
                f"{MUTED}[{idx:>3}/{total}]{RESET} {R2}v {RESET}"
                f"{WHITE}{username:<22}{RESET} {SUCCESS}VALID TOKEN{RESET}"
            )

    max_workers = min(50, max(10, total))
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futs = [pool.submit(worker, i + 1, tok) for i, tok in enumerate(tokens)]
        for _ in as_completed(futs):
            pass

    print(TerminalUI.b_div())
    print(TerminalUI.b_row(
        f"{R2}v {len(valid_tokens)} Valid{RESET}  {BORDER}|{RESET}  "
        f"{DANGER}X {len(invalid_tokens)} Invalid{RESET}"
    ))
    print(TerminalUI.b_bottom())
    print()

    if not invalid_tokens:
        print(center_text(f"{SUCCESS}v No invalid tokens found — tokens.txt is already clean!{RESET}\n"))
        input(center_text(f"{MUTED}Press Enter to go back...{RESET}"))
        return

    confirm_prompt = center_text(
        f"{BORDER}╭──────────[ {R1}Remove {len(invalid_tokens)} invalid token(s)? (y/n)"
        f"{RESET}{BORDER} ]──────────╮{RESET}"
    )
    confirm_in = center_text(f"{BORDER}╰─────[ {R2}❯❯{RESET}{BORDER} ]{RESET} ")
    print(confirm_prompt)
    try:
        choice = input(confirm_in).strip().lower()
    except (KeyboardInterrupt, EOFError):
        input(center_text(f"{MUTED}Press Enter to go back...{RESET}"))
        return

    if choice in ("y", "yes"):
        _save_tokens(valid_tokens, "tokens.txt")
        print()
        print(center_text(
            f"{SUCCESS}v Successfully removed {len(invalid_tokens)} "
            f"invalid token(s) from tokens.txt!{RESET}\n"
        ))
    else:
        print()
        print(center_text(f"{WARNING}⚠ Purge cancelled — tokens.txt was not modified.{RESET}\n"))

    input(center_text(f"{MUTED}Press Enter to go back...{RESET}"))
