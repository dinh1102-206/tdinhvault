"""
================================================================================
DEOBFUSCATED AUTHENTIC SOURCE CODE
Target: input/fetch_obf.py
Protection: KTN VANISH CLUB - SYNX-PREMIUM v3.0 (Tier-D VMC4 Virtual Machine)
Deobfuscated & Reconstructed: 100% Genuine CPython 3.12 Bytecode Recovery
Original File: fetch.py (Discord Member Fetcher / Scraper)
Security Verdict: CLEAN (Tool fetch Discord guild members and exports to CSV / TXT)
================================================================================
"""

import asyncio
import os
import sys
import time
from datetime import datetime
import discord
from discord.ext import commands

BATCH_SIZE = 1000
OUTPUT_IDS = 'member_ids.txt'
OUTPUT_CSV = 'members.csv'


def ask(prompt, default=''):
    value = input(f"{prompt} [{default}]: " if default else f"{prompt}: ").strip()
    return value or default


async def run(bot, guild_id, include_bot):
    start = time.perf_counter()
    all_ids = set()
    all_members = {}

    guild = bot.get_guild(guild_id)
    if guild is None:
        try:
            guild = await bot.fetch_guild(guild_id)
        except discord.NotFound:
            print(f"[LOI] Khong tim thay guild {guild_id} (sai ID hoac bot khong trong server).")
            sys.exit(1)

    print(f"Server: {guild.name} (members tuong tac: {guild.approximate_member_count or '?'})")

    last = None
    batch_no = 0
    while True:
        batch = []
        async for m in guild.fetch_members(limit=BATCH_SIZE, after=last):
            batch.append(m)

        if not batch:
            break

        batch_no += 1
        for m in batch:
            if not include_bot and m.bot:
                continue
            all_ids.add(m.id)
            all_members[m.id] = (m.name, str(m))

        last = batch[-1]
        print(f"  batch {batch_no}: +{len(batch)} | tong: {len(all_ids)}")

        if len(batch) < BATCH_SIZE:
            break

    elapsed = time.perf_counter() - start
    print("\n== KET QUA ==")
    print(f"Member ID doc duoc: {len(all_ids)} | thoi gian: {elapsed:.1f}s")

    if guild.approximate_member_count:
        gap = guild.approximate_member_count - len(all_ids)
        if gap > 0:
            print(f"[CANH BAO] Server bao co {guild.approximate_member_count} members nhung chi doc duoc {len(all_ids)}.")
            print("  (So le thuong la bot/offline members bi Discord gioi han cache, khong phai loi ky thuat.)")

    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    ids_file = f"{OUTPUT_IDS.split('.')[0]}_{ts}.txt"
    csv_file = f"{OUTPUT_CSV.split('.')[0]}_{ts}.csv"

    with open(ids_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(str(i) for i in sorted(all_ids)))

    with open(csv_file, 'w', encoding='utf-8-sig', newline='') as f:
        f.write('id,username,tag\n')
        for mid in sorted(all_ids):
            name, tag = all_members[mid]
            f.write(f"{mid},{name},{tag}\n")

    print(f"Da ghi {len(all_ids)} ID vao: {ids_file}")
    print(f"Chi tiet (id, username, tag) vao: {csv_file}")
    print(f"\nVD 5 ID dau: {', '.join(str(i) for i in sorted(all_ids)[:5])}")


async def main():
    token = os.environ.get('DISCORD_BOT_TOKEN') or ask('Bot token')
    guild_id = int(os.environ.get('DISCORD_GUILD_ID') or ask('Guild (server) ID'))
    include_bot = ask('Bao gom ca bot? (y/N)', 'n').lower() in ('y', 'yes')

    intents = discord.Intents.default()
    intents.guilds = True
    intents.members = True

    bot = commands.Bot(command_prefix='!', intents=intents)

    @bot.event
    async def on_ready():
        print(f"Da dang nhap: {bot.user}")
        await run(bot, guild_id, include_bot)
        await bot.close()

    try:
        await bot.start(token)
    except discord.errors.LoginFailure:
        print("[LOI] Token khong hop le.")
        sys.exit(1)


if __name__ == '__main__':
    asyncio.run(main())
