#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
          ⚡ DISCORD MEMBER SCRAPER & FETCHER SUITE (MENU TUI) ⚡
================================================================================
Tool: Discord Guild Member Scraper / Fetcher with Interactive CLI Menu
Author: Deobfuscated from KTN Synx-Premium v3.0 (Tier-D VMC4)
Target: Discord Bot API (discord.py 2.x / Python 3.10+)
================================================================================
"""

import asyncio
import os
import sys
import time
import json
import csv
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple

# Enable ANSI colors on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if os.name == 'nt':
    os.system('')

try:
    import discord
    from discord.ext import commands
except ImportError:
    print("[!] Thiếu thư viện discord.py. Vui lòng cài đặt: pip install discord.py")
    sys.exit(1)

# Color Constants
C_RESET = "\033[0m"
C_BOLD = "\033[1m"
C_GOLD = "\033[38;2;255;215;0m"
C_CYAN = "\033[38;2;0;229;255m"
C_GREEN = "\033[38;2;0;230;118m"
C_RED = "\033[38;2;255;68;68m"
C_YELLOW = "\033[38;2;255;214;0m"
C_GRAY = "\033[38;2;140;140;140m"
C_PURPLE = "\033[38;2;213;0;249m"

CONFIG_FILE = "fetch_config.json"
DEFAULT_OUTPUT_DIR = "fetch_results"

# ==============================================================================
# CONFIGURATION MANAGER
# ==============================================================================
def load_config() -> dict:
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "bot_token": os.environ.get("DISCORD_BOT_TOKEN", ""),
        "last_guild_id": os.environ.get("DISCORD_GUILD_ID", ""),
        "batch_size": 1000,
        "include_bot": False,
        "output_dir": DEFAULT_OUTPUT_DIR,
    }

def save_config(cfg: dict) -> None:
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"  {C_RED}[!] Không thể lưu cấu hình: {e}{C_RESET}")

def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")

def get_terminal_width() -> int:
    return max(80, shutil.get_terminal_size((80, 24)).columns)

def print_banner(bot_user: Optional[str] = None, guild_count: int = 0) -> None:
    clear_screen()
    w = min(84, get_terminal_width())
    banner_art = [
        "███████╗███████╗████████╗ ██████╗██╗  ██╗    ███╗   ███╗███████╗███╗   ██╗██╗   ██╗",
        "██╔════╝██╔════╝╚══██╔══╝██╔════╝██║  ██║    ████╗ ████║██╔════╝████╗  ██║██║   ██║",
        "█████╗  █████╗     ██║   ██║     ███████║    ██╔████╔██║█████╗  ██╔██╗ ██║██║   ██║",
        "██╔══╝  ██╔══╝     ██║   ██║     ██╔══██║    ██║╚██╔╝██║██╔══╝  ██║╚██╗██║██║   ██║",
        "██║     ███████╗   ██║   ╚██████╗██║  ██║    ██║ ╚═╝ ██║███████╗██║ ╚████║╚██████╔╝",
        "╚═╝     ╚══════╝   ╚═╝    ╚═════╝╚═╝  ╚═╝    ╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝ ╚═════╝ "
    ]
    print(f"{C_GOLD}{C_BOLD}")
    for line in banner_art:
        print(line.center(w))
    print(f"{C_CYAN}═" * w + f"{C_RESET}")
    title = "⚡ DISCORD MEMBER SCRAPER & FETCHER SUITE ⚡"
    print(f"{C_GOLD}{C_BOLD}{title.center(w)}{C_RESET}")
    if bot_user:
        status = f"Bot: {C_GREEN}{bot_user}{C_RESET} | Servers: {C_GREEN}{guild_count}{C_RESET}"
    else:
        status = f"Status: {C_YELLOW}Chưa đăng nhập Bot{C_RESET}"
    print(status.center(w + 10))
    print(f"{C_CYAN}═" * w + f"{C_RESET}\n")

def print_menu() -> None:
    menu_lines = [
        "╭────────────────────────────────────────────────────────────────────────╮",
        "│  [1]  🚀  Fetch / Cào danh sách Members của Server (Xuất TXT & CSV)   │",
        "│  [2]  🌐  Xem danh sách các Server Bot đang tham gia (Guilds List)    │",
        "│  [3]  📊  Tra cứu thông tin chi tiết Server (Guild Info & Analytics)   │",
        "│  [4]  📜  Cào danh sách Kênh & Roles của Server (Channels / Roles)     │",
        "│  [5]  ⚙️   Cài đặt Cấu hình (Đổi Bot Token, Thư mục lưu, Batch size)   │",
        "│  [0]  🚪  Thoát chương trình                                          │",
        "╰────────────────────────────────────────────────────────────────────────╯"
    ]
    for line in menu_lines:
        print(f"   {C_CYAN}{line}{C_RESET}")
    print()

# ==============================================================================
# DISCORD BOT CLIENT MANAGER
# ==============================================================================
class FetcherBot:
    def __init__(self, token: str):
        self.token = token
        intents = discord.Intents.default()
        intents.guilds = True
        intents.members = True
        self.bot = commands.Bot(command_prefix="!", intents=intents)
        self.ready_event = asyncio.Event()

        @self.bot.event
        async def on_ready():
            self.ready_event.set()

    async def start(self):
        try:
            await self.bot.start(self.token)
        except discord.errors.LoginFailure:
            raise RuntimeError("Bot Token không hợp lệ hoặc đã bị vô hiệu hóa.")
        except discord.errors.PrivilegedIntentsRequired:
            raise RuntimeError(
                "Lỗi Privileged Intents: Bạn cần BẬT 'SERVER MEMBERS INTENT' "
                "trong Discord Developer Portal (tab Bot -> Privileged Gateway Intents)!"
            )

    async def close(self):
        if not self.bot.is_closed():
            await self.bot.close()

# ==============================================================================
# CORE ACTIONS
# ==============================================================================
async def action_fetch_members(bot: commands.Bot, cfg: dict):
    print_banner(str(bot.user), len(bot.guilds))
    print(f"  {C_GOLD}{C_BOLD}🚀 CÀO DANH SÁCH MEMBERS CỦA SERVER{C_RESET}\n")

    # Select Guild
    guild = None
    if bot.guilds:
        print(f"  {C_CYAN}Danh sách Server Bot có mặt:{C_RESET}")
        for i, g in enumerate(bot.guilds, 1):
            print(f"    [{i:02d}] {g.name} (ID: {g.id}) - {g.member_count or '?'} members")
        print("    [0]  Nhập ID Server khác thủ công")

        choice = input(f"\n  {C_GOLD}[?] Chọn Server (số thứ tự hoặc 0): {C_RESET}").strip()
        try:
            idx = int(choice)
            if 1 <= idx <= len(bot.guilds):
                guild = bot.guilds[idx - 1]
        except ValueError:
            pass

    if not guild:
        gid_str = input(f"  {C_CYAN}[?] Nhập Guild ID: {C_RESET}").strip()
        if not gid_str.isdigit():
            print(f"  {C_RED}[✖] Guild ID không hợp lệ!{C_RESET}")
            input(f"\n  {C_GRAY}Nhấn Enter để quay lại...{C_RESET}")
            return
        gid = int(gid_str)
        guild = bot.get_guild(gid)
        if not guild:
            try:
                print(f"  {C_GRAY}[*] Đang tìm nạp Server qua API...{C_RESET}")
                guild = await bot.fetch_guild(gid)
            except discord.NotFound:
                print(f"  {C_RED}[✖] Không tìm thấy Server {gid}. Bot chưa vào server hoặc ID sai!{C_RESET}")
                input(f"\n  {C_GRAY}Nhấn Enter để quay lại...{C_RESET}")
                return
            except discord.Forbidden:
                print(f"  {C_RED}[✖] Bot không có quyền truy cập Server này (Missing Access).{C_RESET}")
                input(f"\n  {C_GRAY}Nhấn Enter để quay lại...{C_RESET}")
                return

    # Filter Bot Option
    inc_bot_input = input(f"  {C_CYAN}[?] Bao gồm cả tài khoản Bot? (y/N) [Mặc định: n]: {C_RESET}").strip().lower()
    include_bot = inc_bot_input in ('y', 'yes')

    batch_size = cfg.get("batch_size", 1000)
    out_dir = Path(cfg.get("output_dir", DEFAULT_OUTPUT_DIR))
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n  {C_GREEN}━━━ BẮT ĐẦU CÀO DỮ LIỆU: {guild.name} (ID: {guild.id}) ━━━{C_RESET}")
    print(f"  {C_GRAY}Batch size: {batch_size} | Lấy tài khoản Bot: {include_bot}{C_RESET}\n")

    t_start = time.perf_counter()
    all_ids = set()
    all_members = {}

    last = None
    batch_no = 0

    try:
        while True:
            batch = []
            async for m in guild.fetch_members(limit=batch_size, after=last):
                batch.append(m)

            if not batch:
                break

            batch_no += 1
            added_this_batch = 0
            for m in batch:
                if not include_bot and m.bot:
                    continue
                all_ids.add(m.id)
                all_members[m.id] = {
                    "username": m.name,
                    "global_name": getattr(m, "global_name", None) or m.name,
                    "bot": m.bot,
                    "joined_at": m.joined_at.strftime("%Y-%m-%d %H:%M:%S") if m.joined_at else "",
                    "created_at": m.created_at.strftime("%Y-%m-%d %H:%M:%S") if m.created_at else "",
                    "top_role": m.top_role.name if m.top_role else "",
                }
                added_this_batch += 1

            last = batch[-1]
            elapsed = time.perf_counter() - t_start
            print(
                f"  {C_CYAN}Batch {batch_no:03d}:{C_RESET} "
                f"+{len(batch):4d} fetched | +{added_this_batch:4d} hợp lệ | "
                f"Tổng: {C_GREEN}{len(all_ids):6d}{C_RESET} | {elapsed:.1f}s"
            )

            if len(batch) < batch_size:
                break

    except discord.Forbidden:
        print(f"\n  {C_RED}[✖] Lỗi: Bot thiếu quyền 'Server Members Intent' hoặc không có quyền xem thành viên!{C_RESET}")
        print(f"  {C_YELLOW}Vào Discord Dev Portal -> Ứng dụng -> Bot -> Bật 'Server Members Intent'.{C_RESET}")
        input(f"\n  {C_GRAY}Nhấn Enter để quay lại...{C_RESET}")
        return
    except Exception as e:
        print(f"\n  {C_RED}[✖] Lỗi trong quá trình fetch: {e}{C_RESET}")
        input(f"\n  {C_GRAY}Nhấn Enter để quay lại...{C_RESET}")
        return

    elapsed = time.perf_counter() - t_start
    print(f"\n  {C_GOLD}{C_BOLD}✦ HOÀN TẤT THU THẬP: {len(all_ids)} members trong {elapsed:.2f} giây!{C_RESET}")

    # Warning on gap
    if guild.approximate_member_count and guild.approximate_member_count > len(all_ids):
        gap = guild.approximate_member_count - len(all_ids)
        print(
            f"  {C_YELLOW}[!] Chênh lệch: Server báo {guild.approximate_member_count} members "
            f"nhưng fetch được {len(all_ids)} (Lệch {gap} do offline / bot ẩn).{C_RESET}"
        )

    # Save outputs
    clean_guild_name = "".join(c for c in guild.name if c.isalnum() or c in " _-").strip() or "guild"
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    ids_file = out_dir / f"ids_{clean_guild_name}_{guild.id}_{ts}.txt"
    csv_file = out_dir / f"members_{clean_guild_name}_{guild.id}_{ts}.csv"
    json_file = out_dir / f"members_{clean_guild_name}_{guild.id}_{ts}.json"

    # 1. TXT
    with open(ids_file, "w", encoding="utf-8") as f:
        f.write("\n".join(str(i) for i in sorted(all_ids)))

    # 2. CSV
    with open(csv_file, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "username", "global_name", "is_bot", "top_role", "joined_at", "created_at"])
        for mid in sorted(all_ids):
            data = all_members[mid]
            writer.writerow([
                mid,
                data["username"],
                data["global_name"],
                "Yes" if data["bot"] else "No",
                data["top_role"],
                data["joined_at"],
                data["created_at"],
            ])

    # 3. JSON
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump({
            "guild_id": guild.id,
            "guild_name": guild.name,
            "total_fetched": len(all_ids),
            "elapsed_seconds": round(elapsed, 2),
            "members": [{ "id": mid, **all_members[mid] } for mid in sorted(all_ids)]
        }, f, ensure_ascii=False, indent=2)

    print(f"\n  {C_GREEN}[✔] Đã lưu danh sách IDs  : {C_GOLD}{ids_file}{C_RESET}")
    print(f"  {C_GREEN}[✔] Đã lưu chi tiết CSV   : {C_GOLD}{csv_file}{C_RESET}")
    print(f"  {C_GREEN}[✔] Đã lưu tệp chuẩn JSON : {C_GOLD}{json_file}{C_RESET}")

    sample_ids = [str(i) for i in sorted(all_ids)[:5]]
    print(f"\n  {C_CYAN}Mẫu 5 ID đầu tiên:{C_RESET} {', '.join(sample_ids)}")

    # Update config
    cfg["last_guild_id"] = str(guild.id)
    save_config(cfg)

    input(f"\n  {C_GRAY}Nhấn Enter để quay lại menu...{C_RESET}")

async def action_list_guilds(bot: commands.Bot):
    print_banner(str(bot.user), len(bot.guilds))
    print(f"  {C_GOLD}{C_BOLD}🌐 DANH SÁCH CÁC SERVER BOT ĐANG THAM GIA{C_RESET}\n")

    if not bot.guilds:
        print(f"  {C_RED}[!] Bot hiện không ở trong bất kỳ server nào.{C_RESET}")
        input(f"\n  {C_GRAY}Nhấn Enter để quay lại...{C_RESET}")
        return

    print(f"  {'#':<4} {'Tên Server':<30} {'Guild ID':<20} {'Members':<10} {'Owner':<15}")
    print(f"  {'-'*4} {'-'*30} {'-'*20} {'-'*10} {'-'*15}")

    for idx, g in enumerate(bot.guilds, 1):
        owner_name = str(g.owner) if g.owner else "Unknown"
        name = g.name[:28] + ".." if len(g.name) > 28 else g.name
        print(f"  {idx:<4} {name:<30} {g.id:<20} {g.member_count or '?':<10} {owner_name:<15}")

    input(f"\n  {C_GRAY}Nhấn Enter để quay lại menu...{C_RESET}")

async def action_guild_info(bot: commands.Bot):
    print_banner(str(bot.user), len(bot.guilds))
    print(f"  {C_GOLD}{C_BOLD}📊 TRA CỨU THÔNG TIN CHI TIẾT SERVER{C_RESET}\n")

    gid_str = input(f"  {C_CYAN}[?] Nhập Guild ID cần tra cứu: {C_RESET}").strip()
    if not gid_str.isdigit():
        print(f"  {C_RED}[✖] Guild ID không hợp lệ!{C_RESET}")
        input(f"\n  {C_GRAY}Nhấn Enter để quay lại...{C_RESET}")
        return

    gid = int(gid_str)
    guild = bot.get_guild(gid)
    if not guild:
        try:
            guild = await bot.fetch_guild(gid)
        except Exception as e:
            print(f"  {C_RED}[✖] Lỗi: {e}{C_RESET}")
            input(f"\n  {C_GRAY}Nhấn Enter để quay lại...{C_RESET}")
            return

    print(f"\n  {C_GREEN}✦ THÔNG TIN SERVER: {guild.name}{C_RESET}")
    print(f"    • ID Server           : {guild.id}")
    print(f"    • Chủ sở hữu (Owner)  : {guild.owner} (ID: {guild.owner_id})")
    print(f"    • Ngày khởi tạo       : {guild.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"    • Tổng thành viên     : {guild.member_count or '?'}")
    print(f"    • Cấp độ Nitro Boost  : Tier {guild.premium_tier} ({guild.premium_subscription_count} boosts)")
    print(f"    • Số kênh Text        : {len(guild.text_channels)}")
    print(f"    • Số kênh Voice       : {len(guild.voice_channels)}")
    print(f"    • Tổng số Vai trò     : {len(guild.roles)}")
    print(f"    • Cấp độ bảo mật (2FA): {guild.verification_level}")

    input(f"\n  {C_GRAY}Nhấn Enter để quay lại menu...{C_RESET}")

async def action_scrape_channels_roles(bot: commands.Bot, cfg: dict):
    print_banner(str(bot.user), len(bot.guilds))
    print(f"  {C_GOLD}{C_BOLD}📜 CÀO DANH SÁCH KÊNH & VAI TRÒ (ROLES){C_RESET}\n")

    if not bot.guilds:
        print(f"  {C_RED}[!] Bot không ở trong server nào!{C_RESET}")
        input(f"\n  {C_GRAY}Nhấn Enter để quay lại...{C_RESET}")
        return

    for i, g in enumerate(bot.guilds, 1):
        print(f"    [{i:02d}] {g.name} (ID: {g.id})")

    choice = input(f"\n  {C_GOLD}[?] Chọn Server: {C_RESET}").strip()
    try:
        idx = int(choice)
        guild = bot.guilds[idx - 1]
    except Exception:
        print(f"  {C_RED}[✖] Lựa chọn không hợp lệ!{C_RESET}")
        input(f"\n  {C_GRAY}Nhấn Enter để quay lại...{C_RESET}")
        return

    out_dir = Path(cfg.get("output_dir", DEFAULT_OUTPUT_DIR))
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    clean_name = "".join(c for c in guild.name if c.isalnum() or c in " _-").strip() or "guild"

    # Export Channels
    ch_file = out_dir / f"channels_{clean_name}_{guild.id}_{ts}.txt"
    with open(ch_file, "w", encoding="utf-8") as f:
        f.write(f"# Channels for Guild: {guild.name} ({guild.id})\n")
        f.write(f"# ID, Type, Name\n")
        for ch in guild.channels:
            f.write(f"{ch.id},{ch.type},{ch.name}\n")

    # Export Roles
    role_file = out_dir / f"roles_{clean_name}_{guild.id}_{ts}.txt"
    with open(role_file, "w", encoding="utf-8") as f:
        f.write(f"# Roles for Guild: {guild.name} ({guild.id})\n")
        f.write(f"# ID, Position, Permissions, Name\n")
        for r in guild.roles:
            f.write(f"{r.id},{r.position},{r.permissions.value},{r.name}\n")

    print(f"\n  {C_GREEN}[✔] Đã cào {len(guild.channels)} Kênh -> {C_GOLD}{ch_file}{C_RESET}")
    print(f"  {C_GREEN}[✔] Đã cào {len(guild.roles)} Vai trò -> {C_GOLD}{role_file}{C_RESET}")

    input(f"\n  {C_GRAY}Nhấn Enter để quay lại menu...{C_RESET}")

def action_settings(cfg: dict) -> None:
    while True:
        print_banner()
        print(f"  {C_GOLD}{C_BOLD}⚙️ CÀI ĐẶT CẤU HÌNH TOOL{C_RESET}\n")
        masked_token = (cfg.get("bot_token", "")[:10] + "..." + cfg.get("bot_token", "")[-5:]) if len(cfg.get("bot_token", "")) > 15 else (cfg.get("bot_token") or "Chưa cấu hình")
        print(f"  [1] Bot Token       : {C_CYAN}{masked_token}{C_RESET}")
        print(f"  [2] Batch Size      : {C_CYAN}{cfg.get('batch_size', 1000)}{C_RESET}")
        print(f"  [3] Thư mục Output  : {C_CYAN}{cfg.get('output_dir', DEFAULT_OUTPUT_DIR)}{C_RESET}")
        print(f"  [0] Quay lại menu chính")

        sub = input(f"\n  {C_GOLD}[?] Chọn mục cần đổi (0-3): {C_RESET}").strip()
        if sub == '0':
            break
        elif sub == '1':
            new_token = input(f"  {C_CYAN}Nhập Bot Token mới: {C_RESET}").strip()
            if new_token:
                cfg["bot_token"] = new_token
                save_config(cfg)
                print(f"  {C_GREEN}[✔] Đã cập nhật Token!{C_RESET}")
                time.sleep(1)
        elif sub == '2':
            new_batch = input(f"  {C_CYAN}Nhập Batch size mới (khuyến nghị 1000): {C_RESET}").strip()
            if new_batch.isdigit():
                cfg["batch_size"] = int(new_batch)
                save_config(cfg)
                print(f"  {C_GREEN}[✔] Đã cập nhật Batch size!{C_RESET}")
                time.sleep(1)
        elif sub == '3':
            new_dir = input(f"  {C_CYAN}Nhập thư mục lưu kết quả mới: {C_RESET}").strip()
            if new_dir:
                cfg["output_dir"] = new_dir
                save_config(cfg)
                print(f"  {C_GREEN}[✔] Đã cập nhật Output dir!{C_RESET}")
                time.sleep(1)

# ==============================================================================
# MAIN ASYNC CONTROLLER
# ==============================================================================
async def main_async():
    cfg = load_config()

    while True:
        token = cfg.get("bot_token", "").strip()
        if not token:
            print_banner()
            print(f"  {C_YELLOW}[!] Chưa tìm thấy Discord Bot Token trong cấu hình.{C_RESET}")
            token = input(f"  {C_CYAN}[?] Vui lòng nhập Bot Token của bạn: {C_RESET}").strip()
            if not token:
                print(f"  {C_RED}[✖] Bạn phải nhập Bot Token để tiếp tục!{C_RESET}")
                time.sleep(1.5)
                continue
            cfg["bot_token"] = token
            save_config(cfg)

        print_banner()
        print(f"  {C_CYAN}[*] Đang đăng nhập Discord Bot Gateway...{C_RESET}")
        
        fetcher = FetcherBot(token)
        bot_task = asyncio.create_task(fetcher.start())

        try:
            # Wait for bot on_ready with timeout 15s
            await asyncio.wait_for(fetcher.ready_event.wait(), timeout=15.0)
        except asyncio.TimeoutError:
            print(f"\n  {C_RED}[✖] Quá thời gian kết nối tới Discord Gateway (Timeout 15s).{C_RESET}")
            print(f"  {C_YELLOW}Vui lòng kiểm tra lại kết nối mạng hoặc tính hợp lệ của Token.{C_RESET}")
            await fetcher.close()
            cfg["bot_token"] = ""
            save_config(cfg)
            input(f"\n  {C_GRAY}Nhấn Enter để thử lại...{C_RESET}")
            continue
        except Exception as e:
            print(f"\n  {C_RED}[✖] Lỗi đăng nhập: {e}{C_RESET}")
            await fetcher.close()
            cfg["bot_token"] = ""
            save_config(cfg)
            input(f"\n  {C_GRAY}Nhấn Enter để thử lại...{C_RESET}")
            continue

        bot = fetcher.bot

        # Interactive loop while bot is online
        while True:
            print_banner(str(bot.user), len(bot.guilds))
            print_menu()

            choice = input(f"  {C_GOLD}{C_BOLD}discord-fetcher:~$ {C_RESET}").strip()
            if choice == '1':
                await action_fetch_members(bot, cfg)
            elif choice == '2':
                await action_list_guilds(bot)
            elif choice == '3':
                await action_guild_info(bot)
            elif choice == '4':
                await action_scrape_channels_roles(bot, cfg)
            elif choice == '5':
                action_settings(cfg)
                # If token was changed, break to reconnect
                if cfg.get("bot_token") != token:
                    break
            elif choice in ('0', 'q', 'exit'):
                print(f"\n  {C_GOLD}Đang ngắt kết nối Bot và thoát... Tạm biệt!{C_RESET}\n")
                await fetcher.close()
                return
            else:
                print(f"  {C_RED}Lựa chọn không hợp lệ!{C_RESET}")
                time.sleep(1)

        await fetcher.close()

def main():
    try:
        asyncio.run(main_async())
    except KeyboardInterrupt:
        print(f"\n\n  {C_GOLD}Đã nhận lệnh Ctrl+C. Tạm biệt!{C_RESET}\n")

if __name__ == "__main__":
    main()
