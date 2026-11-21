import os
import sys
import time
import json
import requests
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from ui import BlackforgeUI as TerminalUI, R1, R2, R3, R4, R5, BORDER, WHITE, MUTED, SUCCESS, WARNING, DANGER, RESET, center_text

ROOT_DIR   = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETUP_DIR  = os.path.join(ROOT_DIR, "setup")
CONFIG_PATH = os.path.join(SETUP_DIR, "config.json")

def load_config() -> Dict[str, str]:
    default_cfg = {
        "BOT_TOKEN": "",
        "CLIENT_ID": "",
        "CLIENT_SECRET": ""
    }
    if not os.path.exists(CONFIG_PATH):
        return default_cfg
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return {
                "BOT_TOKEN": str(data.get("BOT_TOKEN", "")).strip(),
                "CLIENT_ID": str(data.get("CLIENT_ID", "")).strip(),
                "CLIENT_SECRET": str(data.get("CLIENT_SECRET", "")).strip()
            }
    except Exception:
        import json
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {
                    "BOT_TOKEN": str(data.get("BOT_TOKEN", "")).strip(),
                    "CLIENT_ID": str(data.get("CLIENT_ID", "")).strip(),
                    "CLIENT_SECRET": str(data.get("CLIENT_SECRET", "")).strip()
                }
        except Exception:
            return default_cfg

CONFIG = load_config()
BOT_TOKEN: str = CONFIG["BOT_TOKEN"]
CLIENT_ID: str = CONFIG["CLIENT_ID"]

HTTP_SESSION = requests.Session()
adapter = requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100)
HTTP_SESSION.mount("https://", adapter)
HTTP_SESSION.mount("http://", adapter)

@dataclass
class TokenState:
    raw_token: str
    user_id: Optional[str] = None
    username: Optional[str] = None
    access_token: Optional[str] = None
    status: str = "UNVERIFIED"

class TokenRepository:
    def __init__(self):
        self._tokens: Dict[str, TokenState] = {}

    def load_from_file(self, filename: str = "tokens.txt") -> List[str]:
        path = os.path.join(SETUP_DIR, filename)
        if not os.path.exists(path):
            return []
        with open(path, "r", encoding="utf-8") as f:
            lines = [ln.strip() for ln in f if ln.strip()]
        for t in lines:
            if t not in self._tokens:
                self._tokens[t] = TokenState(raw_token=t)
        return lines

    def save_to_file(self, valid_tokens: List[str], filename: str = "tokens.txt"):
        path = os.path.join(SETUP_DIR, filename)
        with open(path, "w", encoding="utf-8") as f:
            for t in valid_tokens:
                f.write(f"{t}\n")
        self._tokens = {t: self._tokens[t] for t in valid_tokens if t in self._tokens}

    def get(self, token: str) -> TokenState:
        if token not in self._tokens:
            self._tokens[token] = TokenState(raw_token=token)
        return self._tokens[token]

    def stats(self) -> Dict[str, int]:
        vals = list(self._tokens.values())
        return {
            "total": len(vals),
            "verified": sum(1 for x in vals if x.user_id is not None),
            "authorized": sum(1 for x in vals if x.access_token is not None),
            "joined": sum(1 for x in vals if x.status == "JOINED"),
            "failed": sum(1 for x in vals if x.status in ("INVALID", "AUTH_FAILED", "JOIN_FAILED"))
        }

class DiscordClient:
    BASE_URL = "https://discord.com/api/v10"
    HEADERS = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "X-Discord-Locale": "en-US",
        "Origin": "https://discord.com",
    }

    @classmethod
    def get_user_profile(cls, user_token: str) -> Optional[Dict]:
        try:
            r = HTTP_SESSION.get(f"{cls.BASE_URL}/users/@me", headers={"Authorization": user_token}, timeout=5)
            return r.json() if r.status_code == 200 else None
        except Exception:
            return None

    @classmethod
    def authorize_user(cls, user_token: str) -> Optional[str]:
        url = f"{cls.BASE_URL}/oauth2/authorize"
        params = {
            "client_id": CLIENT_ID,
            "response_type": "token",
            "scope": "guilds.join identify",
            "redirect_uri": "https://discord.com"
        }
        payload = {"authorize": True, "permissions": "0"}
        headers = {**cls.HEADERS, "Authorization": user_token, "Referer": "https://discord.com/oauth2/authorize"}
        try:
            r = HTTP_SESSION.post(url, json=payload, params=params, headers=headers, timeout=6, allow_redirects=False)
            if r.status_code == 200:
                d = r.json()
                loc = d.get("location", "")
                if "access_token=" in loc:
                    frag = loc.split("#", 1)[-1] if "#" in loc else loc.split("?", 1)[-1]
                    return dict(p.split("=", 1) for p in frag.split("&") if "=" in p).get("access_token")
                return d.get("access_token")
            return None
        except Exception:
            return None

    @classmethod
    def add_to_guild(cls, guild_id: str, access_token: str, user_id: str) -> Tuple[int, Dict]:
        url = f"{cls.BASE_URL}/guilds/{guild_id}/members/{user_id}"
        headers = {"Authorization": f"Bot {BOT_TOKEN}", "Content-Type": "application/json"}
        try:
            r = HTTP_SESSION.put(url, json={"access_token": access_token}, headers=headers, timeout=6)
            return r.status_code, (r.json() if r.text.strip() else {})
        except Exception as e:
            return 0, {"error": str(e)}

    @classmethod
    def check_bot(cls) -> Tuple[bool, str]:
        if not BOT_TOKEN:
            return False, "EMPTY BOT_TOKEN"
        try:
            r = HTTP_SESSION.get(f"{cls.BASE_URL}/users/@me", headers={"Authorization": f"Bot {BOT_TOKEN}"}, timeout=4)
            if r.status_code == 200:
                d = r.json()
                return True, f"{d.get('username')}#{d.get('discriminator', '0000')}"
            return False, f"HTTP {r.status_code}"
        except Exception as e:
            return False, str(e)

    @classmethod
    def check_guild(cls, guild_id: str) -> Tuple[bool, str]:
        if not guild_id:
            return False, "EMPTY GUILD_ID"
        try:
            r = HTTP_SESSION.get(f"{cls.BASE_URL}/guilds/{guild_id}", headers={"Authorization": f"Bot {BOT_TOKEN}"}, timeout=4)
            if r.status_code == 200:
                return True, r.json().get("name", guild_id)
            return False, f"HTTP {r.status_code}"
        except Exception as e:
            return False, str(e)

class TokenJoinerEngine:
    def __init__(self):
        self.repo = TokenRepository()

    def verify_flow(self, tokens: List[str]):
        total = len(tokens)
        print(TerminalUI.b_top("Verifying Tokens"))
        print(TerminalUI.b_row(f"{R1}Checking {WHITE}{total}{R1} token(s)...{RESET}"))
        print(TerminalUI.b_div())

        def worker(idx: int, t: str):
            st = self.repo.get(t)
            prof = DiscordClient.get_user_profile(t)
            if not prof:
                st.status = "INVALID"
                TerminalUI.log(f"{MUTED}[{idx:>3}/{total}]{RESET} {DANGER}✗ {RESET}{WHITE}{t[:22]}...{RESET} {DANGER}INVALID TOKEN{RESET}")
                return

            st.user_id = prof.get("id")
            st.username = f"{prof.get('username')}#{prof.get('discriminator', '0000')}"

            auth_token = DiscordClient.authorize_user(t)
            if auth_token:
                st.access_token = auth_token
                st.status = "AUTHORIZED"
                TerminalUI.log(
                    f"{MUTED}[{idx:>3}/{total}]{RESET} {R2}✔ {RESET}{WHITE}{st.username:<22}{RESET} "
                    f"{R1}AUTH OK{RESET} {MUTED}({auth_token[:12]}...){RESET}"
                )
            else:
                st.status = "AUTH_FAILED"
                TerminalUI.log(
                    f"{MUTED}[{idx:>3}/{total}]{RESET} {WARNING}⚠ {RESET}{WHITE}{st.username:<22}{RESET} "
                    f"{WARNING}AUTH FAILED{RESET}"
                )

        workers = min(50, max(10, total))
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futs = [pool.submit(worker, i + 1, tok) for i, tok in enumerate(tokens)]
            for _ in as_completed(futs):
                pass

        st = self.repo.stats()
        print(TerminalUI.b_div())
        print(TerminalUI.b_row(
            f"{R2}✔ {st['authorized']} authorized{RESET}  {BORDER}│{RESET}  "
            f"{WARNING}⚠ {st['verified'] - st['authorized']} failed auth{RESET}  {BORDER}│{RESET}  "
            f"{DANGER}✗ {st['failed']} invalid{RESET}"
        ))
        print(TerminalUI.b_bottom())
        print()

    def join_flow(self, tokens: List[str], guild_id: str):
        total = len(tokens)
        print(TerminalUI.b_top("Adding to Server"))
        print(TerminalUI.b_row(f"{R1}Joining server — Guild ID: {WHITE}{guild_id}{RESET}"))
        print(TerminalUI.b_div())

        def worker(idx: int, t: str):
            st = self.repo.get(t)

            if not st.user_id:
                prof = DiscordClient.get_user_profile(t)
                if not prof:
                    st.status = "INVALID"
                    TerminalUI.log(f"{MUTED}[{idx:>3}/{total}]{RESET} {DANGER}✗ {RESET}{WHITE}Token #{idx}{RESET} {DANGER}INVALID{RESET}")
                    return
                st.user_id = prof.get("id")
                st.username = f"{prof.get('username')}#{prof.get('discriminator', '0000')}"

            if not st.access_token:
                at = DiscordClient.authorize_user(t)
                if not at:
                    st.status = "AUTH_FAILED"
                    TerminalUI.log(f"{MUTED}[{idx:>3}/{total}]{RESET} {WARNING}⚠ {RESET}{WHITE}{st.username:<22}{RESET} {WARNING}AUTH FAILED{RESET}")
                    return
                st.access_token = at

            for _ in range(3):
                code, res = DiscordClient.add_to_guild(guild_id, st.access_token, st.user_id)
                if code == 201:
                    st.status = "JOINED"
                    TerminalUI.log(f"{MUTED}[{idx:>3}/{total}]{RESET} {R2}✔ {RESET}{WHITE}{st.username:<22}{RESET} {R1}JOINED{RESET}")
                    return
                elif code in (200, 204):
                    st.status = "ALREADY_MEMBER"
                    TerminalUI.log(f"{MUTED}[{idx:>3}/{total}]{RESET} {MUTED}● {RESET}{WHITE}{st.username:<22}{RESET} {MUTED}ALREADY IN SERVER{RESET}")
                    return
                elif code == 429:
                    ra = float(res.get("retry_after", 1.5))
                    time.sleep(ra + 0.1)
                    continue
                else:
                    msg = res.get("message", f"HTTP {code}")
                    st.status = "JOIN_FAILED"
                    TerminalUI.log(f"{MUTED}[{idx:>3}/{total}]{RESET} {DANGER}✗ {RESET}{WHITE}{st.username:<22}{RESET} {DANGER}{msg[:28]}{RESET}")
                    return

            st.status = "JOIN_FAILED"
            TerminalUI.log(f"{MUTED}[{idx:>3}/{total}]{RESET} {DANGER}✗ {RESET}{WHITE}{st.username:<22}{RESET} {DANGER}TIMEOUT{RESET}")

        workers = min(50, max(10, total))
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futs = [pool.submit(worker, i + 1, tok) for i, tok in enumerate(tokens)]
            for _ in as_completed(futs):
                pass

        st = self.repo.stats()
        print(TerminalUI.b_div())
        print(TerminalUI.b_row(
            f"{R2}✔ {st['joined']} Joined{RESET}  {BORDER}│{RESET}  "
            f"{DANGER}✗ {st['failed']} Failed{RESET}"
        ))
        print(TerminalUI.b_bottom())
        print()

def run_token_joiner(auth_data: Optional[Dict] = None):
    engine = TokenJoinerEngine()
    
    while True:
        TerminalUI.render_banner("Token Discord Joiner")
        
        b_ok, b_info = DiscordClient.check_bot()
        tokens = engine.repo.load_from_file("tokens.txt")
        st = engine.repo.stats()
        
        print(TerminalUI.b_top("Status"))
        print(TerminalUI.b_row())

        b_str = f"{R2}● Online {RESET}{WHITE}{b_info}{RESET}" if b_ok else f"{MUTED}● Offline {RESET}{DANGER}{b_info}{RESET}"
        print(TerminalUI.b_row(f"{R1}Bot    {BORDER}│ {b_str}"))

        if auth_data:
            usr = auth_data.get("username", "Authenticated User")
            exp = auth_data.get("expiry") or "Lifetime"
            print(TerminalUI.b_row(f"{R1}User   {BORDER}│ {WHITE}{usr}{RESET} {BORDER}• Expiry: {R2}{exp}{RESET}"))

        summary = (
            f"{WHITE}{st['total']}{RESET} loaded  {BORDER}•{RESET} "
            f"{R2}{st['authorized']}{RESET} ready  {BORDER}•{RESET} "
            f"{SUCCESS}{st['joined']}{RESET} joined  {BORDER}•{RESET} "
            f"{MUTED}{st['failed']}{RESET} failed"
        )
        print(TerminalUI.b_row(f"{R1}Tokens {BORDER}│ {summary}"))

        print(TerminalUI.b_row())
        print(TerminalUI.b_div("Options"))
        print(TerminalUI.b_row())

        print(TerminalUI.b_row(f"  {BORDER}╭──[{R2} 1 {BORDER}]──{RESET} {WHITE}Verify Tokens{RESET}     {MUTED}─── Check tokens & fetch access keys{RESET}"))
        print(TerminalUI.b_row(f"  {BORDER}╭──[{R2} 2 {BORDER}]──{RESET} {WHITE}Add to Server{RESET}     {MUTED}─── Join target server with tokens{RESET}"))
        print(TerminalUI.b_row(f"  {BORDER}╭──[{R2} 3 {BORDER}]──{RESET} {WHITE}Back to Main Menu{RESET}  {MUTED}─── Return to Black-forge menu{RESET}"))

        print(TerminalUI.b_row())
        print(TerminalUI.b_bottom())
        print()

        prompt_line = center_text(f"{BORDER}╭──────────[ {R1}Choose Option{RESET}{BORDER} ]──────────╮{RESET}")
        sub_prompt  = center_text(f"{BORDER}╰─────[ {R2}❯❯{RESET}{BORDER} ]{RESET} ")
        print(prompt_line)
        try:
            cmd = input(sub_prompt).strip()
        except (KeyboardInterrupt, EOFError):
            return

        if cmd == "1":
            TerminalUI.render_banner("Token Discord Joiner")
            if not CLIENT_ID:
                print(center_text(f"{DANGER}CLIENT_ID is missing in config.json{RESET}\n"))
            elif tokens:
                engine.verify_flow(tokens)
            else:
                print(center_text(f"{DANGER}No tokens found in tokens.txt{RESET}\n"))
            input(center_text(f"{MUTED}Press Enter to go back...{RESET}"))

        elif cmd == "2":
            TerminalUI.render_banner("Token Discord Joiner")
            if not b_ok:
                print(center_text(f"{DANGER}Bot token is invalid. Check config.json{RESET}\n"))
            elif not CLIENT_ID:
                print(center_text(f"{DANGER}CLIENT_ID is missing in config.json{RESET}\n"))
            elif not tokens:
                print(center_text(f"{DANGER}No tokens found in tokens.txt{RESET}\n"))
            else:
                g_prompt = center_text(f"{BORDER}╭──────────[ {R1}Enter Guild ID{RESET}{BORDER} ]──────────╮{RESET}")
                g_in = center_text(f"{BORDER}╰─────[ {R2}❯❯{RESET}{BORDER} ]{RESET} ")
                print(g_prompt)
                try:
                    target_guild = input(g_in).strip()
                except (KeyboardInterrupt, EOFError):
                    continue

                if not target_guild:
                    print(center_text(f"{DANGER}Guild ID cannot be empty.{RESET}\n"))
                else:
                    g_ok, g_info = DiscordClient.check_guild(target_guild)
                    if not g_ok:
                        print(center_text(f"{DANGER}Guild unreachable ({g_info}). Make sure bot is in server.{RESET}\n"))
                    else:
                        print(center_text(f"{SUCCESS}Guild verified: {WHITE}{g_info}{RESET}\n"))
                        time.sleep(0.6)
                        TerminalUI.render_banner("Token Discord Joiner")
                        engine.join_flow(tokens, target_guild)

            input(center_text(f"{MUTED}Press Enter to go back...{RESET}"))

        elif cmd == "3":
            break
        else:
            print(f"\n{center_text(f'{WARNING}Please enter 1, 2, or 3.{RESET}')}\n")
            time.sleep(0.5)
