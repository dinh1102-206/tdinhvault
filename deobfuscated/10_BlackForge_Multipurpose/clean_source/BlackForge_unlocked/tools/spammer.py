import os
import sys
import time
import threading
import requests
from typing import List, Tuple, Optional, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed
from ui import BlackforgeUI as TerminalUI, R1, R2, R3, R4, R5, BORDER, WHITE, MUTED, SUCCESS, WARNING, DANGER, RESET, center_text

DISCORD_API = "https://discord.com/api/v9"

ROOT_DIR    = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETUP_DIR   = os.path.join(ROOT_DIR, "setup")


def _load_tokens() -> List[str]:
    path = os.path.join(SETUP_DIR, "tokens.txt")
    if not os.path.isfile(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return [ln.strip() for ln in f if ln.strip() and not ln.strip().startswith("#")]


def _validate_token(token: str) -> Optional[Dict]:
    try:
        r = requests.get(
            f"{DISCORD_API}/users/@me",
            headers={"Authorization": token, "Content-Type": "application/json"},
            timeout=5,
        )
        return r.json() if r.status_code == 200 else None
    except requests.RequestException:
        return None


def _load_messages() -> List[str]:
    path = os.path.join(SETUP_DIR, "msg.txt")
    if not os.path.isfile(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return [ln.strip() for ln in f if ln.strip()]


def _make_session(token: str) -> requests.Session:
    s = requests.Session()
    s.headers.update({
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "X-Discord-Locale": "en-US",
        "Origin": "https://discord.com",
    })
    return s


def _send_message(session: requests.Session, channel_id: str, content: str) -> Tuple[bool, Optional[float], int]:
    try:
        r = session.post(
            f"{DISCORD_API}/channels/{channel_id}/messages",
            json={"content": content},
            timeout=5,
        )
        if r.status_code in (200, 201):
            return True, None, r.status_code
        elif r.status_code == 429:
            try:
                data = r.json()
                ra = float(data.get("retry_after", 1.5))
            except Exception:
                ra = 1.5
            return False, ra, 429
        else:
            return False, None, r.status_code
    except requests.RequestException:
        return False, None, 0


def _login_tokens() -> List[Tuple[str, Dict]]:
    raw = _load_tokens()
    if not raw:
        return []

    total = len(raw)
    print(TerminalUI.b_top("Validating Tokens"))
    print(TerminalUI.b_row(f"{R1}Checking {WHITE}{total}{R1} token(s)...{RESET}"))
    print(TerminalUI.b_div())

    valid: List[Tuple[str, Dict]] = []
    lock = threading.Lock()

    def worker(idx: int, t: str):
        user = _validate_token(t)
        if user:
            uname = f"{user.get('username', '?')}#{user.get('discriminator', '0000')}"
            with lock:
                valid.append((t, user))
            TerminalUI.log(f"{MUTED}[{idx:>3}/{total}]{RESET} {R2}✔ {RESET}{WHITE}{uname:<22}{RESET} {SUCCESS}VALID{RESET}")
        else:
            TerminalUI.log(f"{MUTED}[{idx:>3}/{total}]{RESET} {DANGER}✗ {RESET}{WHITE}{t[:22]}...{RESET} {DANGER}INVALID{RESET}")

    workers = min(50, max(10, total))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futs = [pool.submit(worker, i + 1, tok) for i, tok in enumerate(raw)]
        for _ in as_completed(futs):
            pass

    print(TerminalUI.b_div())
    print(TerminalUI.b_row(
        f"{SUCCESS}✔ {len(valid)} valid{RESET}  {BORDER}│{RESET}  "
        f"{DANGER}✗ {total - len(valid)} invalid{RESET}"
    ))
    print(TerminalUI.b_bottom())
    print()
    return valid


def _spam_messages(
    valid_tokens: List[Tuple[str, Dict]],
    channel_id: str,
    messages: List[str],
    delay: float = 0.8,
    is_brutal: bool = False,
):
    stop_event = threading.Event()
    sent_total  = 0
    lock        = threading.Lock()

    def listen_for_exit():
        while not stop_event.is_set():
            try:
                if input().strip().lower() == "/exit":
                    stop_event.set()
                    break
            except (EOFError, KeyboardInterrupt):
                stop_event.set()
                break

    num_tokens = len(valid_tokens)
    if is_brutal:
        step_delay = 0.0
        mode_label = "BRUTAL (1-by-1 Token Rotation — Untouched Max Speed)"
    else:
        step_delay = delay
        mode_label = f"{delay:.1f}s delay (1-by-1 Token Rotation)"

    def token_rotation_worker():
        nonlocal sent_total
        token_pool = []
        for t, u in valid_tokens:
            token_pool.append({
                "token": t,
                "user": u,
                "uname": u.get("username", "?"),
                "session": _make_session(t),
                "cooldown_until": 0.0,
            })

        tok_idx = 0
        msg_idx = 0
        num_msgs = len(messages)

        while not stop_event.is_set() and token_pool:
            now = time.time()
            selected_item = None
            pool_size = len(token_pool)

            for attempt in range(pool_size):
                item = token_pool[(tok_idx + attempt) % pool_size]
                if item["cooldown_until"] <= now:
                    selected_item = item
                    tok_idx = (tok_idx + attempt + 1) % pool_size
                    break

            if not selected_item:
                stop_event.wait(0.1)
                continue

            msg = messages[msg_idx % num_msgs]
            msg_idx += 1

            ok, retry_after, status_code = _send_message(selected_item["session"], channel_id, msg)

            if ok:
                with lock:
                    sent_total += 1
                    count = sent_total
                TerminalUI.log(f"{MUTED}[{count:>4}]{RESET} {R2}✔ {RESET}{WHITE}{selected_item['uname']:<20}{RESET} {MUTED}→{RESET} {WHITE}{msg[:45]}{RESET}")
            elif status_code == 429 and retry_after is not None:
                selected_item["cooldown_until"] = time.time() + retry_after
                TerminalUI.log(f"{MUTED}[ RATELIMIT ]{RESET} {WARNING}⚠ {RESET}{WHITE}{selected_item['uname']:<20}{RESET} {WARNING}Rate limited ({retry_after:.1f}s — rotating token){RESET}")
            elif status_code == 404:
                TerminalUI.log(f"{MUTED}[ 404 NOT FOUND ]{RESET} {DANGER}✗ {RESET}{WHITE}{selected_item['uname']:<20}{RESET} {DANGER}Invalid Channel ID or account not in server!{RESET}")
                stop_event.set()
                break
            elif status_code in (401, 403):
                TerminalUI.log(f"{MUTED}[ ERROR {status_code} ]{RESET} {DANGER}✗ {RESET}{WHITE}{selected_item['uname']:<20}{RESET} {DANGER}Token blocked (removed from pool){RESET}")
                token_pool.remove(selected_item)
                if not token_pool:
                    break
            else:
                TerminalUI.log(f"{MUTED}[ FAILED ]{RESET} {DANGER}✗ {RESET}{WHITE}{selected_item['uname']:<20}{RESET} {DANGER}Failed (HTTP {status_code}){RESET}")

            if step_delay > 0.0 and not stop_event.is_set():
                stop_event.wait(step_delay)

    print(TerminalUI.b_top("Spamming"))
    print(TerminalUI.b_row(f"{R1}Mode     {BORDER}│ {WHITE}{mode_label}{RESET}"))
    print(TerminalUI.b_row(f"{R1}Channel  {BORDER}│ {WHITE}{channel_id}{RESET}"))
    print(TerminalUI.b_row(f"{R1}Tokens   {BORDER}│ {WHITE}{len(valid_tokens)}{RESET}"))
    print(TerminalUI.b_row(f"{R1}Messages {BORDER}│ {WHITE}{len(messages)}{RESET}"))
    print(TerminalUI.b_div())
    print(TerminalUI.b_row(f"{WARNING}⚠ Press Ctrl+C or type /exit + Enter to stop{RESET}"))
    print(TerminalUI.b_div())

    exit_thread = threading.Thread(target=listen_for_exit, daemon=True)
    exit_thread.start()

    worker_thread = threading.Thread(target=token_rotation_worker, daemon=True)
    worker_thread.start()

    try:
        while not stop_event.is_set():
            stop_event.wait(0.5)
    except (KeyboardInterrupt, EOFError):
        stop_event.set()

    worker_thread.join(timeout=2)

    print(TerminalUI.b_div())
    print(TerminalUI.b_row(f"{WARNING}⚠ Stopped.  Total messages sent: {WHITE}{sent_total}{RESET}"))
    print(TerminalUI.b_bottom())
    print()


def run_spammer_msg(auth_data: Optional[Dict] = None):
    valid_tokens: List[Tuple[str, Dict]] = []

    while True:
        TerminalUI.render_banner("Discord Message Spammer")

        tok_count = len(valid_tokens)
        msg_count = len(_load_messages()) if valid_tokens else 0

        print(TerminalUI.b_top("Status"))
        print(TerminalUI.b_row())

        if auth_data:
            usr = auth_data.get("username", "Authenticated User")
            exp = auth_data.get("expiry") or "Lifetime"
            print(TerminalUI.b_row(f"{R1}User    {BORDER}│ {WHITE}{usr}{RESET} {BORDER}• Expiry: {R2}{exp}{RESET}"))

        tok_str = f"{R2}{tok_count} loaded{RESET}" if tok_count else f"{DANGER}none — load via option 1{RESET}"
        msg_str = f"{R2}{msg_count} messages{RESET}" if msg_count else f"{MUTED}add lines to setup/msg.txt{RESET}"

        print(TerminalUI.b_row(f"{R1}Tokens  {BORDER}│ {tok_str}"))
        print(TerminalUI.b_row(f"{R1}Messages{BORDER}│ {msg_str}"))

        print(TerminalUI.b_row())
        print(TerminalUI.b_div("Options"))
        print(TerminalUI.b_row())

        print(TerminalUI.b_row(f"  {BORDER}╭──[{R2} 1 {BORDER}]──{RESET} {WHITE}Load & Validate Tokens{RESET}  {MUTED}─── Read setup/tokens.txt{RESET}"))
        print(TerminalUI.b_row(f"  {BORDER}╭──[{R2} 2 {BORDER}]──{RESET} {WHITE}Spam Messages{RESET}           {MUTED}─── Start spamming a channel{RESET}"))
        print(TerminalUI.b_row(f"  {BORDER}╭──[{R2} 3 {BORDER}]──{RESET} {WHITE}Back to Main Menu{RESET}        {MUTED}─── Return to Black-Forge{RESET}"))

        print(TerminalUI.b_row())
        print(TerminalUI.b_bottom())
        print()

        prompt_line = center_text(f"{BORDER}╭──────────[ {R1}Choose Option{RESET}{BORDER} ]──────────╮{RESET}")
        sub_prompt  = center_text(f"{BORDER}╰─────[ {R2}❯❯{RESET}{BORDER} ]{RESET} ")
        print(prompt_line)
        try:
            cmd = input(sub_prompt).strip()
        except (KeyboardInterrupt, EOFError):
            break

        if cmd == "1":
            TerminalUI.render_banner("Discord Message Spammer")
            valid_tokens = _login_tokens()
            if not valid_tokens:
                print(center_text(f"{DANGER}No valid tokens found in setup/tokens.txt{RESET}\n"))
            input(center_text(f"{MUTED}Press Enter to go back...{RESET}"))

        elif cmd == "2":
            TerminalUI.render_banner("Discord Message Spammer")

            if not valid_tokens:
                print(center_text(f"{DANGER}No tokens loaded. Use option 1 first.{RESET}\n"))
                input(center_text(f"{MUTED}Press Enter to go back...{RESET}"))
                continue

            messages = _load_messages()
            if not messages:
                print(center_text(f"{DANGER}No messages found in setup/msg.txt{RESET}\n"))
                input(center_text(f"{MUTED}Press Enter to go back...{RESET}"))
                continue

            ch_prompt = center_text(f"{BORDER}╭──────────[ {R1}Enter Channel ID{RESET}{BORDER} ]──────────╮{RESET}")
            ch_in     = center_text(f"{BORDER}╰─────[ {R2}❯❯{RESET}{BORDER} ]{RESET} ")
            print(ch_prompt)
            try:
                channel_id = input(ch_in).strip()
            except (KeyboardInterrupt, EOFError):
                continue

            if not channel_id.isdigit():
                print(center_text(f"{DANGER}Invalid channel ID.{RESET}\n"))
                input(center_text(f"{MUTED}Press Enter to go back...{RESET}"))
                continue

            TerminalUI.render_banner("Discord Message Spammer")
            print(TerminalUI.b_top("Spam Mode"))
            print(TerminalUI.b_row())
            print(TerminalUI.b_row(f"  {BORDER}╭──[{R2} 1 {BORDER}]──{RESET} {WHITE}Brutal Safe{RESET} {MUTED}─── Max Speed via Token Change (Anti-Ban){RESET}"))
            print(TerminalUI.b_row(f"  {BORDER}╭──[{R2} 2 {BORDER}]──{RESET} {WHITE}Safe Fast{RESET}             {MUTED}─── 0.8s delay per token{RESET}"))
            print(TerminalUI.b_row(f"  {BORDER}╭──[{R2} 3 {BORDER}]──{RESET} {WHITE}Slow{RESET}                  {MUTED}─── 3.0s delay per token{RESET}"))
            print(TerminalUI.b_row(f"  {BORDER}╭──[{R2} 4 {BORDER}]──{RESET} {WHITE}Custom{RESET}                {MUTED}─── Enter custom delay{RESET}"))
            print(TerminalUI.b_row())
            print(TerminalUI.b_bottom())
            print()
            print(prompt_line)
            try:
                mode_choice = input(sub_prompt).strip()
            except (KeyboardInterrupt, EOFError):
                continue

            is_brutal = False
            spam_delay = 0.8

            if mode_choice == "1":
                is_brutal = True
            elif mode_choice == "2":
                spam_delay = 0.8
            elif mode_choice == "3":
                spam_delay = 3.0
            elif mode_choice == "4":
                del_prompt = center_text(f"{BORDER}╭──────────[ {R1}Enter Delay (seconds){RESET}{BORDER} ]──────────╮{RESET}")
                print(del_prompt)
                try:
                    raw_del = input(sub_prompt).strip()
                    spam_delay = float(raw_del)
                except Exception:
                    spam_delay = 0.8
                    print(center_text(f"{WARNING}Invalid input, defaulting to 0.8s.{RESET}\n"))
            else:
                is_brutal = True
                print(center_text(f"{WARNING}Defaulting to Brutal Spam.{RESET}\n"))

            TerminalUI.render_banner("Discord Message Spammer")
            _spam_messages(valid_tokens, channel_id, messages, spam_delay, is_brutal=is_brutal)
            try:
                input(center_text(f"{MUTED}Press Enter to go back...{RESET}"))
            except (KeyboardInterrupt, EOFError):
                pass

        elif cmd == "3":
            break

        else:
            print(f"\n{center_text(f'{WARNING}Please enter 1, 2, or 3.{RESET}')}\n")
            time.sleep(0.5)


def main():
    run_spammer_msg()


if __name__ == "__main__":
    main()
