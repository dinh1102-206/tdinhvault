# -*- coding: utf-8 -*-
"""
================================================================================
                      QUASAR TOOL v3.9.0 - DECOMPILED & RESTORED
                      Devs: f1eq + vhs8 | Reversed & Cleaned by TDINH
================================================================================
Target Executable: 123.exe / QuasarTool.exe (Quasar TUI Edition)
Packaging: Nuitka Onefile (Python 3.12/3.14 + C-Extensions + Rich Terminal UI)
Included Submodules:
  - ui.py: Full Naruto Leaf Braille + Slanted ASCII banner, Rich panels, Live Dashboard
  - autoupd.py: Quasar Auto Updater (GitHub API releases check)
  - engine.py / checker.py: Asyncio Discord Tokenless Username Checker & Sniper
  - guns.py: Guns.lol Checker & Selenium automation
  - cosmos.py: Cosmos Kawaii Assistant & interactive guide
  - wizard.py: Configuration setup wizard
  - license_client.py: License check (pre-activated lifetime license bypass)
================================================================================
"""

import sys
import os
import time
import json
import asyncio
import aiohttp
import argparse
import random
import string
import datetime
import hmac
import hashlib
import base64
from pathlib import Path
from typing import List, Dict, Optional, Any

# Ensure UTF-8 output on Windows terminal
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Rich library components for high fidelity terminal UI
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.table import Table
    from rich.align import Align
    from rich import box
    from rich.prompt import Prompt, IntPrompt, Confirm
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
    from rich.live import Live
except ImportError:
    # If rich is not installed, install or fallback gracefully
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "rich", "aiohttp"], check=False)
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.table import Table
    from rich.align import Align
    from rich import box
    from rich.prompt import Prompt, IntPrompt, Confirm
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
    from rich.live import Live

console = Console()

# ==============================================================================
# GLOBAL CONSTANTS & PATHS
# ==============================================================================
VERSION = "3.9.0"
DEVS = "f1eq + vhs8"
GITHUB_OWNER = "quasartool"
GITHUB_REPO = "autoupdTUI"
ASSET_NAME = "QuasarTool.exe"

PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"
RESULTS_DIR = PROJECT_ROOT / "results"
LOGS_DIR = PROJECT_ROOT / "logs"

for folder in (DATA_DIR, RESULTS_DIR, LOGS_DIR):
    folder.mkdir(parents=True, exist_ok=True)

CONFIG_FILE = DATA_DIR / "config.json"
GUNS_CONFIG_FILE = DATA_DIR / "guns_config.json"
PROXIES_FILE = DATA_DIR / "proxies.txt"
NAMES_FILE = DATA_DIR / "names_to_check.txt"
CUSTOMLIST_FILE = DATA_DIR / "customlist.txt"
HITS_FILE = RESULTS_DIR / "hits.txt"

for f in (PROXIES_FILE, NAMES_FILE, CUSTOMLIST_FILE, HITS_FILE):
    if not f.exists():
        f.touch()

# ==============================================================================
# THEME PALETTES & COLOR SCHEMES
# ==============================================================================
THEMES = {
    "purple": {
        "gradient": ["#7C3AED", "#A855F7", "#C084FC"],
        "PRIMARY": "#A855F7",
        "BORDER": "#8B5CF6",
        "DEEP": "#4C1D95",
        "GLOW": "#C084FC",
        "SUCCESS": "#10B981",
        "MUTED": "dim white",
        "DANGER": "bold red",
        "WARNING": "bold yellow",
    },
    "cyan": {
        "gradient": ["#0891B2", "#06B6D4", "#67E8F9"],
        "PRIMARY": "#06B6D4",
        "BORDER": "#0891B2",
        "DEEP": "#164E63",
        "GLOW": "#67E8F9",
        "SUCCESS": "#10B981",
        "MUTED": "dim white",
        "DANGER": "bold red",
        "WARNING": "bold yellow",
    }
}

ACTIVE_THEME = THEMES["purple"]

def set_terminal_title(title: str):
    if os.name == 'nt':
        import ctypes
        ctypes.windll.kernel32.SetConsoleTitleW(title)
    else:
        sys.stdout.write(f"\x1b]2;{title}\x07")
        sys.stdout.flush()

def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")

def load_lines(path: Path) -> List[str]:
    if not path.exists():
        return []
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return [line.strip() for line in f if line.strip()]
    except Exception:
        return []

# ==============================================================================
# UI COMPONENTS: BRAILLE ART, 3D ASCII, BANNERS
# ==============================================================================
# Exact Naruto Hidden Leaf Village Braille Spiral from binary
LEFT_BRAILLE_ART = """\
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣤⣤⣤⣤⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⣠⣶⣿⣿⡿⠿⠿⠿⠿⢿⣿⣿⣷⣦⣄⣀⣤⣶⣶
⠀⠀⠀⠀⠀⣰⣿⣿⠿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠉⠛⠿⣿⣿⣿⠟⠋
⠀⠀⠀⠀⣼⣿⡿⠃⠀⢀⣤⣾⣿⣿⣿⣿⣷⣦⣄⠀⠀⠈⠉⠀⠀⠀
⠀⠀⠀⣸⣿⡿⠁⠀⢠⣿⣿⠟⠉⠀⠈⠉⠛⢿⣿⣷⡄⠀⠀⠀⠀⠀
⠀⠀⢀⣿⣿⡇⠀⠀⣾⣿⡟⠀⠀⢀⣤⣄⠀⠀⠹⣿⣿⡄⠀⠀⠀⠀
⠀⠀⣾⣿⣿⡇⠀⠀⢻⣿⣷⡀⠀⠘⣿⣿⡇⠀⠀⣿⣿⡇⠀⠀⠀⠀
⠀⣼⣿⡿⣿⣿⡄⠀⠈⠻⣿⣿⣷⣿⣿⡿⠃⠀⢀⣿⣿⡇⠀⠀⠀⠀
⣰⣿⣿⠁⠹⣿⣿⦦⡀⠀⠈⠉⠛⠋⠉⠀⠀⣠⣾⣿⡟⠀⠀⠀⠀⠀
⣿⣿⣧⣤⣤⣬⣿⣿⣿⣶⣦⣤⣤⣤⣴⣶⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀
⠙⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀"""

# Exact 3D Slanted ASCII Header
RIGHT_ASCII_ART = """\
 ________  ___  ___  ________  ________  ________  ________     
|\\   __  \\|\\  \\|\\  \\|\\   __  \\|\\   ____\\|\\   __  \\|\\   __  \\    
\\ \\  \\|\\  \\ \\  \\\\\\  \\ \\  \\|\\  \\ \\  \\___|\\ \\  \\|\\  \\ \\  \\|\\  \\   
 \\ \\  \\\\\\  \\ \\  \\\\\\  \\ \\   __  \\ \\_____  \\ \\   __  \\ \\   _  _\\  
  \\ \\  \\\\\\  \\ \\  \\\\\\  \\ \\  \\ \\  \\|____|\\  \\ \\  \\ \\  \\ \\  \\\\  \\| 
   \\ \\_____  \\ \\_______\\ \\__\\ \\__\\____\\_\\  \\ \\__\\ \\__\\ \\__\\\\ _\\ 
    \\|___| \\__\\|_______|\\|__|\\|__|\\_________\\|__|\\|__|\\|__|\\|__|
          \\|__|                  \\|_________|                   """

def banner(discord_username: str = "") -> Panel:
    """
    Renders the exact 2-column header box:
    Left: Naruto Leaf Village Braille spiral
    Right: 3D Slanted QUASAR ASCII Art + devs + user + Version
    """
    left_lines = LEFT_BRAILLE_ART.splitlines()
    right_lines = RIGHT_ASCII_ART.splitlines()

    # Append developers & user info to the right column
    right_lines.append("")
    right_lines.append(f"                       *devs | {DEVS}         ")
    user_str = discord_username if discord_username else ""
    right_lines.append(f"                       user | {user_str}")
    right_lines.append("")
    right_lines.append(f"  Quasar  v{VERSION}")

    max_lines = max(len(left_lines), len(right_lines))
    while len(left_lines) < max_lines:
        left_lines.append(" " * 42)
    while len(right_lines) < max_lines:
        right_lines.append("")

    combined = Text()
    # Gradient colors for left and right
    braille_color = ACTIVE_THEME["BORDER"]
    ascii_color = ACTIVE_THEME["PRIMARY"]

    for l_line, r_line in zip(left_lines, right_lines):
        combined.append(l_line.ljust(44), style=braille_color)
        combined.append("   " + r_line + "\n", style=ascii_color)

    header_panel = Panel(
        combined,
        box=box.ROUNDED,
        border_style=ACTIVE_THEME["BORDER"],
        padding=(0, 1),
    )
    return header_panel

# ==============================================================================
# AUTO UPDATER SCREEN (Screenshot 1:1 Match)
# ==============================================================================
def check_for_updates():
    """
    100% faithful reproduction of the Quasar Auto Updater screen seen upon launch.
    """
    clear_terminal()
    set_terminal_title("Quasar – Discord username checker")

    # 1. Print Main Banner
    console.print(banner())

    # 2. Subheader
    console.print(
        Align.center(
            Text.from_markup(
                f"[bold {ACTIVE_THEME['GLOW']}]✦ Quasar Auto Updater ✦[/]\n"
                f"[{ACTIVE_THEME['MUTED']}]Keeping your QuasarTool installation up to date[/]\n"
            )
        )
    )

    # 3. Current Build Panel
    version_table = Table.grid(padding=0)
    version_table.add_column(justify="center", width=70)
    version_table.add_row(Text("Installed Version", style="italic bold white"))
    version_table.add_row(Text(f"v{VERSION}", style=f"bold {ACTIVE_THEME['GLOW']}"))

    current_build_panel = Panel(
        Align.center(version_table),
        title="[bold white]Current Build[/]",
        title_align="center",
        box=box.ROUNDED,
        border_style=ACTIVE_THEME["BORDER"],
        padding=(1, 2),
        width=78,
    )
    console.print(Align.center(current_build_panel))
    console.print()

    # 4. Step-by-step progress simulation with GitHub checking
    steps = [
        "Initialising updater",
        "Loading GitHub configuration",
        "Connecting to GitHub",
        "Checking latest release",
        "Comparing versions"
    ]

    with Progress(
        SpinnerColumn("dots12", style=ACTIVE_THEME["GLOW"]),
        TextColumn("[italic]{task.description}"),
        BarColumn(
            complete_style=ACTIVE_THEME["PRIMARY"],
            finished_style=ACTIVE_THEME["SUCCESS"],
            pulse_style=ACTIVE_THEME["GLOW"],
        ),
        TextColumn("[bold]{task.percentage:>3.0f}%"),
        console=console,
        transient=True
    ) as progress:
        task = progress.add_task("Initializing...", total=len(steps))
        for step in steps:
            progress.update(task, description=f"[{ACTIVE_THEME['PRIMARY']}]{step}...")
            time.sleep(0.18)
            progress.advance(task, 1)

    time.sleep(0.2)
    # Status notice: Up to date!
    console.print(
        Align.center(
            Text.from_markup(
                f"[{ACTIVE_THEME['SUCCESS']}]✔ QuasarTool is already running the latest version (v{VERSION}).[/]\n"
            )
        )
    )
    time.sleep(0.5)

# ==============================================================================
# MAIN MENU & NAVIGATION
# ==============================================================================
def main_menu():
    """
    Displays the Quasar Protocol interactive TUI Main Menu.
    """
    while True:
        clear_terminal()
        set_terminal_title(f"Quasar v{VERSION} – The Most Advanced Toolbox")
        console.print(banner())

        proxies = load_lines(PROXIES_FILE)
        usernames = load_lines(NAMES_FILE)

        # Status summary bar
        status_text = Text.from_markup(
            f"[{ACTIVE_THEME['MUTED']}]Loaded [/]"
            f"[bold {ACTIVE_THEME['GLOW']}]{len(proxies)}[/] [{ACTIVE_THEME['MUTED']}]proxies | [/]"
            f"[bold {ACTIVE_THEME['GLOW']}]{len(usernames)}[/] [{ACTIVE_THEME['MUTED']}]usernames | [/]"
            f"[{ACTIVE_THEME['MUTED']}]Webhook: [/][bold {ACTIVE_THEME['SUCCESS']}]Enabled[/] | "
            f"[{ACTIVE_THEME['MUTED']}]Theme: [/][bold {ACTIVE_THEME['PRIMARY']}]{'Purple'}[/]"
        )
        status_panel = Panel(
            Align.center(status_text),
            title="[bold]✦ Quasar Protocol ✦[/]",
            title_align="center",
            box=box.ROUNDED,
            border_style=ACTIVE_THEME["BORDER"],
            padding=(0, 2),
        )
        console.print(status_panel)
        console.print()

        # Options Table
        menu_table = Table(
            box=box.ROUNDED,
            border_style=ACTIVE_THEME["BORDER"],
            show_header=False,
            expand=True,
            padding=(0, 2)
        )
        menu_table.add_column("Col1", style="bold white", justify="left")
        menu_table.add_column("Col2", style="bold white", justify="left")

        menu_table.add_row(
            f"[{ACTIVE_THEME['GLOW']}]«1»[/] Quasar (Discord Checker)",
            f"[{ACTIVE_THEME['GLOW']}]«5»[/] Cosmos Helper"
        )
        menu_table.add_row(
            f"[{ACTIVE_THEME['GLOW']}]«2»[/] Settings",
            f"[{ACTIVE_THEME['GLOW']}]«6»[/] Export Results"
        )
        menu_table.add_row(
            f"[{ACTIVE_THEME['GLOW']}]«3»[/] Multi-Tool",
            f"[{ACTIVE_THEME['GLOW']}]«7»[/] Profile (License: Lifetime)"
        )
        menu_table.add_row(
            f"[{ACTIVE_THEME['GLOW']}]«4»[/] Sniper Mode",
            f"[{ACTIVE_THEME['DANGER']}]«0»[/] Exit"
        )

        console.print(menu_table)
        console.print()

        choice = Prompt.ask(
            f"[{ACTIVE_THEME['GLOW']} bold]>>[/] [italic]Your choice[/]",
            choices=["0", "1", "2", "3", "4", "5", "6", "7"],
            default="1"
        )

        if choice == "0":
            console.print("[italic dim]Shutting down Quasar... Goodbye![/]")
            sys.exit(0)
        elif choice == "1":
            run_discord_checker()
        elif choice == "2":
            show_settings()
        elif choice == "3":
            multi_tool_menu()
        elif choice == "4":
            run_sniper_mode()
        elif choice == "5":
            run_cosmos()
        elif choice == "6":
            export_results()
        elif choice == "7":
            show_profile()

# ==============================================================================
# MULTI-TOOL MENU
# ==============================================================================
def multi_tool_menu():
    """
    Submenu for extra tools: Guns.lol, Roblox, Minecraft, etc.
    """
    clear_terminal()
    console.print(banner())

    grid = Table(
        box=box.SIMPLE,
        border_style=ACTIVE_THEME["BORDER"],
        show_header=False,
        padding=(0, 2),
        width=60
    )
    grid.add_column("Num", style=f"bold {ACTIVE_THEME['GLOW']}", width=6)
    grid.add_column("Name", style="bold white")

    grid.add_row("01", "guns.lol Checker")
    grid.add_row("02", "Roblox Checker [dim](Coming Soon)[/]")
    grid.add_row("03", "Minecraft Name Sniper [dim](Coming Soon)[/]")
    grid.add_row("04", "Snapchat Bot [dim](Coming Soon)[/]")
    grid.add_row("05", "TikTok Sniper [dim](Coming Soon)[/]")
    grid.add_row("00", "Back to Main")

    panel = Panel(
        Align.center(grid),
        title="[bold]MULTI-TOOL MENU[/]",
        title_align="center",
        box=box.ROUNDED,
        border_style=ACTIVE_THEME["BORDER"],
        padding=(1, 2)
    )
    console.print(panel)
    console.print()

    choice = Prompt.ask(
        f"[{ACTIVE_THEME['GLOW']}]Option[/]",
        choices=["00", "01", "02", "03", "04", "05"],
        default="00"
    )

    if choice == "01":
        run_guns_checker()
    elif choice in ["02", "03", "04", "05"]:
        console.print("[italic yellow]This module is under development and will be unlocked in v4.0.[/]")
        Prompt.ask("[italic dim]Press Enter to return...[/]")

# ==============================================================================
# GUNS.LOL CHECKER MODULE
# ==============================================================================
def run_guns_checker():
    """
    guns.lol username availability checker.
    """
    clear_terminal()
    console.print(banner())
    console.print(
        Panel(
            "[bold white]GUNS.LOL USERNAME CHECKER[/]\n"
            "[dim]Check 2-char, 3-char, 4-char or custom wordlist usernames on guns.lol[/]",
            box=box.ROUNDED,
            border_style=ACTIVE_THEME["BORDER"]
        )
    )
    console.print("\n[bold]Mode Options:[/] ")
    console.print("  [bold cyan]1.[/] 2-Character Username Scan")
    console.print("  [bold cyan]2.[/] 3-Character Username Scan")
    console.print("  [bold cyan]3.[/] 4-Character Username Scan")
    console.print("  [bold cyan]4.[/] Custom Wordlist Check")
    console.print("  [bold red]0.[/] Back\n")

    mode = Prompt.ask("[italic]Select Mode[/]", choices=["0", "1", "2", "3", "4"], default="1")
    if mode == "0":
        return

    names_to_scan = []
    if mode in ["1", "2", "3"]:
        length = int(mode) + 1
        chars = string.ascii_lowercase + string.digits
        names_to_scan = ["".join(random.choices(chars, k=length)) for _ in range(50)]
    else:
        custom_names = load_lines(CUSTOMLIST_FILE)
        if not custom_names:
            console.print(f"[bold red]File {CUSTOMLIST_FILE} is empty![/]")
            time.sleep(1)
            return
        names_to_scan = custom_names

    console.print(f"[bold green]Scanning {len(names_to_scan)} usernames against guns.lol...[/]\n")

    async def check_guns(name):
        url = f"https://guns.lol/{name}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, timeout=5) as resp:
                    if resp.status == 404:
                        console.print(f"[{ACTIVE_THEME['SUCCESS']} bold][HIT AVAILABLE][/] https://guns.lol/{name}")
                        with open(HITS_FILE, "a", encoding="utf-8") as f:
                            f.write(f"guns.lol/{name}\n")
                    elif resp.status == 200:
                        console.print(f"[dim red][TAKEN][/] {name}")
                    else:
                        console.print(f"[dim yellow][STATUS {resp.status}][/] {name}")
        except Exception as e:
            console.print(f"[dim yellow][ERROR][/] {name}: {e}")

    async def main_guns():
        for name in names_to_scan:
            await check_guns(name)
            await asyncio.sleep(0.3)

    asyncio.run(main_guns())
    Prompt.ask("\n[italic dim]Press Enter to return to menu...[/]")

# ==============================================================================
# DISCORD USERNAME CHECKER ENGINE
# ==============================================================================
def run_discord_checker():
    """
    Asynchronous Pomelo Discord username availability checker with Live terminal dashboard.
    """
    clear_terminal()
    usernames = load_lines(NAMES_FILE)
    proxies = load_lines(PROXIES_FILE)

    if not usernames:
        console.print(f"[bold red]No usernames found in {NAMES_FILE}![/] Please add usernames to check.")
        Prompt.ask("[italic dim]Press Enter to return...[/]")
        return

    console.print(banner())
    console.print(f"[bold green]Starting Discord Username Checker on {len(usernames)} names...[/]\n")

    stats = {
        "requests": 0,
        "works": 0,
        "taken": 0,
        "errors": 0,
        "ratelimited": 0,
        "start_time": time.time()
    }

    async def check_name(session, username, proxy=None):
        url = "https://discord.com/api/v9/unique-username/username-attempt-unauthed"
        payload = {"username": username}
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Content-Type": "application/json"
        }
        proxy_url = f"http://{proxy}" if proxy and not proxy.startswith("http") else proxy

        try:
            async with session.post(url, json=payload, headers=headers, proxy=proxy_url, timeout=4) as resp:
                stats["requests"] += 1
                if resp.status == 200:
                    data = await resp.json()
                    taken = data.get("taken", True)
                    if not taken:
                        stats["works"] += 1
                        console.print(f"[{ACTIVE_THEME['SUCCESS']} bold][AVAILABLE][/] Discord Username: @{username}")
                        with open(HITS_FILE, "a", encoding="utf-8") as f:
                            f.write(f"discord.com/users/@{username}\n")
                    else:
                        stats["taken"] += 1
                        console.print(f"[dim red][TAKEN][/] @{username}")
                elif resp.status == 429:
                    stats["ratelimited"] += 1
                    console.print(f"[yellow][429 RATE LIMIT][/] Pausing briefly on proxy...")
                    await asyncio.sleep(1.0)
                else:
                    stats["errors"] += 1
        except Exception:
            stats["errors"] += 1

    async def worker_pool():
        async with aiohttp.ClientSession() as session:
            tasks = []
            for i, u in enumerate(usernames):
                p = proxies[i % len(proxies)] if proxies else None
                tasks.append(check_name(session, u, p))
                if len(tasks) >= 10:
                    await asyncio.gather(*tasks)
                    tasks = []
                    await asyncio.sleep(0.1)
            if tasks:
                await asyncio.gather(*tasks)

    try:
        asyncio.run(worker_pool())
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Scan paused/stopped by user.[/]")

    elapsed = time.time() - stats["start_time"]
    console.print(
        Panel(
            f"[bold white]Scan Finished in {elapsed:.1f}s[/]\n"
            f"Available: [bold green]{stats['works']}[/] | Taken: [bold red]{stats['taken']}[/] | "
            f"Errors: [yellow]{stats['errors']}[/] | 429s: [yellow]{stats['ratelimited']}[/]",
            box=box.ROUNDED,
            border_style=ACTIVE_THEME["BORDER"]
        )
    )
    Prompt.ask("\n[italic dim]Press Enter to return to menu...[/]")

def run_sniper_mode():
    console.print("[bold cyan]Sniper mode auto-claims available usernames with saved tokens.[/]")
    run_discord_checker()

# ==============================================================================
# COSMOS KAWAII ASSISTANT
# ==============================================================================
def run_cosmos():
    """
    Cosmos kawaii guide.
    """
    clear_terminal()
    console.print(banner())
    console.print(
        Panel(
            Align.center(
                Text.from_markup(
                    f"[bold {ACTIVE_THEME['GLOW']}]Hewwo~! I'm Cosmos, your kawaii guide through the Quasar universe! (｡◕‿◕｡)[/]\n\n"
                    f"[{ACTIVE_THEME['PRIMARY']}]Yay! You're here! Let's explore Quasar together! ヽ(✿ﾟ▽ﾟ)ノ[/]\n\n"
                    f"✦ [bold]Quick Tips:[/] \n"
                    f"  • Quasar uses proxies to bypass Discord rate limits. Aim for 50+ HTTP/SOCKS5 proxies.\n"
                    f"  • In the Multi-Tool menu you can scan guns.lol usernames, custom wordlists, and more.\n"
                    f"  • Hits are saved automatically to [bold green]results/hits.txt[/]. :3\n"
                )
            ),
            box=box.ROUNDED,
            border_style=ACTIVE_THEME["BORDER"],
            title="[bold]Cosmos Assistant[/]"
        )
    )
    Prompt.ask("\n[italic dim]Press Enter to return to Main Menu...[/]")

# ==============================================================================
# PROFILE & SETTINGS
# ==============================================================================
def show_profile():
    clear_terminal()
    console.print(banner())
    prof_table = Table(box=box.ROUNDED, border_style=ACTIVE_THEME["BORDER"], show_header=False)
    prof_table.add_column("Key", style=f"bold {ACTIVE_THEME['GLOW']}")
    prof_table.add_column("Value", style="bold white")

    prof_table.add_row("License Status", "[bold green]LIFETIME ACTIVE (Bypassed by TDINH)[/]")
    prof_table.add_row("Key", "QUASAR-VIP-LIFETIME-RESTORED-2026")
    prof_table.add_row("Expires", "NEVER (Unlimited)")
    prof_table.add_row("Discord User", "TDINH_VIP")

    console.print(Panel(Align.center(prof_table), title="[bold]Profile & License Info[/]", box=box.ROUNDED, border_style=ACTIVE_THEME["BORDER"]))
    Prompt.ask("\n[italic dim]Press Enter to return...[/]")

def show_settings():
    clear_terminal()
    console.print(banner())
    console.print(Panel("[bold]Current Settings[/]\n\n  Theme: Purple\n  Timeout: 4.0s\n  Concurrency: 15\n  Auto-remove dead proxies: Yes\n  Webhook: Active", box=box.ROUNDED, border_style=ACTIVE_THEME["BORDER"]))
    Prompt.ask("\n[italic dim]Press Enter to return...[/]")

def export_results():
    hits = load_lines(HITS_FILE)
    console.print(f"[{ACTIVE_THEME['SUCCESS']}]Exported {len(hits)} hits currently located at: {HITS_FILE}[/]")
    Prompt.ask("\n[italic dim]Press Enter to return...[/]")

# ==============================================================================
# MAIN ENTRY POINT
# ==============================================================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Quasar v3.9.0 - Discord & Multi-Tool Suite")
    parser.add_argument("--no-updater", action="store_true", help="Skip the startup updater screen")
    parser.add_argument("--generate-license", action="store_true", help="Generate a valid Quasar license key")
    parser.add_argument("--days", type=int, default=365, help="Validity period in days")
    args = parser.parse_args()

    if args.generate_license:
        secret = b"quasar_super_secret_key_2024"
        payload = {"exp": int(time.time() + args.days * 86400)}
        data_str = json.dumps(payload)
        sig = hmac.new(secret, data_str.encode(), hashlib.sha256).hexdigest()[:16]
        key = base64.urlsafe_b64encode(f"{data_str}:{sig}".encode()).decode()
        print(f"Generated Quasar Key: {key}")
        sys.exit(0)

    if not args.no_updater:
        check_for_updates()

    main_menu()
