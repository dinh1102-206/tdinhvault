import os
import asyncio
import aiohttp
import time
import discord
import logging
from discord.ext import commands
from itertools import cycle
from io import BytesIO
from typing import Optional
from datetime import datetime, timezone, timedelta

# Disable noisy discord logging
for _name in ('discord', 'discord.client', 'discord.gateway', 'discord.http', 'discord.ws', 'discord.webhook'):
    _lg = logging.getLogger(_name)
    _lg.setLevel(logging.WARNING)
    _lg.propagate = False

logging.getLogger().setLevel(logging.WARNING)

RESET = '\x1b[0m'

def _rgb(r: int, g: int, b: int) -> str:
    return f"\x1b[38;2;{r};{g};{b}m"

def gradient(text: str, start: tuple[int, int, int], end: tuple[int, int, int]) -> str:
    n = len(text)
    if n == 0:
        return ''
    if n == 1:
        return _rgb(*start) + text + RESET
    parts = []
    for i, ch in enumerate(text):
        t = i / (n - 1)
        r = int(start[0] + (end[0] - start[0]) * t)
        g = int(start[1] + (end[1] - start[1]) * t)
        b = int(start[2] + (end[2] - start[2]) * t)
        parts.append(f"{_rgb(r, g, b)}{ch}")
    return ''.join(parts) + RESET

TAG_SUCCESS = gradient('SUCCESS', (0, 255, 130), (0, 200, 60))
TAG_WARN    = gradient('WARN', (255, 200, 0), (255, 120, 0))
TAG_INFO    = gradient('INFO', (100, 200, 255), (0, 90, 255))
TAG_FAIL    = gradient('FAIL', (255, 120, 120), (220, 0, 0))

def log_info(msg: str) -> None:
    print(f"[{TAG_INFO}] {msg}", flush=True)

def log_success(msg: str) -> None:
    print(f"[{TAG_SUCCESS}] {msg}", flush=True)

def log_warn(msg: str) -> None:
    print(f"[{TAG_WARN}] {msg}", flush=True)

def log_fail(msg: str) -> None:
    print(f"[{TAG_FAIL}] {msg}", flush=True)

# Webhook URL for unban logs (leave empty if not needed)
UNBANALL_LOG_WEBHOOK = ''

intents = discord.Intents.all()
proxies = cycle(open('proxies.txt', 'r').read().splitlines()) if os.path.exists('proxies.txt') else cycle([])
bot = commands.Bot(command_prefix='v', help_command=None, intents=intents, case_insensitive=False)
concurrent_requests = 45

async def fetch_avatar_bytes(guild: discord.Guild, session: aiohttp.ClientSession) -> Optional[bytes]:
    if not guild.icon:
        return None
    try:
        async with session.get(str(guild.icon.url)) as resp:
            if resp.status == 200:
                return await resp.read()
            return None
    except Exception:
        return None

async def send_log_report(webhook_url: str, title: str, stats: dict, avatar_bytes: Optional[bytes] = None) -> None:
    if not webhook_url:
        return

    vn_tz = timezone(timedelta(hours=7))
    now_vn = datetime.now(vn_tz)
    formatted_time = now_vn.strftime('%d/%m/%Y %H:%M')

    container = discord.ui.Container(accent_colour=None)

    top_section = discord.ui.Section(
        discord.ui.TextDisplay(f"## {title}\n-# Unban All Reporter"),
        accessory=discord.ui.Thumbnail("attachment://avatar.png") if avatar_bytes else None
    )
    container.add_item(top_section)
    container.add_item(discord.ui.Separator())

    server_info = (
        f"• Server: {stats['server_name']}\n"
        f"• ID: {stats['server_id']}\n"
        f"• Owner: {stats['server_owner']}\n"
        f"• Members: {stats['members_total']}\n"
        f"• Boosts: {stats['boosts']}"
    )
    container.add_item(discord.ui.TextDisplay(server_info))
    container.add_item(discord.ui.Separator())

    results = (
        f"• Unbanned: {stats['unbanned']}\n"
        f"• Failed: {stats['failed']}\n"
        f"• Remaining: {stats['remaining']}\n"
        f"• Time: {stats['total_time']}s"
    )
    container.add_item(discord.ui.TextDisplay(results))
    container.add_item(discord.ui.Separator())

    footer_text = f"-# Vanish Club | {formatted_time}"
    container.add_item(discord.ui.TextDisplay(footer_text))

    layout_view = discord.ui.LayoutView(timeout=None)
    layout_view.add_item(container)

    try:
        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(webhook_url, session=session)
            if avatar_bytes:
                file = discord.File(BytesIO(avatar_bytes), filename='avatar.png')
                await webhook.send(view=layout_view, file=file)
            else:
                await webhook.send(view=layout_view)
            log_success("Unban all report sent via webhook")
    except Exception as e:
        log_fail(f"Failed to send log report: {e}")

class MassUnban:
    def __init__(self, use_proxy: bool = False):
        self.use_proxy = use_proxy
        self.proxy = ('http://' + next(proxies)) if use_proxy else None
        self.version = cycle(['v10', 'v9'])
        self.unbanned = []
        self.failed = []
        self.guild = None
        self.members_total = 0

    async def fetch_bans(self, guildid: str, token: str) -> bool:
        log_info("Fetching bans...")
        bans_list = []
        guild = bot.get_guild(int(guildid))
        if guild is None:
            log_fail("Guild not found. Bot might not be in this guild")
            return False

        self.guild = guild
        self.members_total = guild.member_count

        connector = aiohttp.TCPConnector(limit=concurrent_requests)
        try:
            async with aiohttp.ClientSession(connector=connector) as session:
                after = None
                while True:
                    params = {'limit': 1000}
                    if after:
                        params['after'] = after

                    async with session.get(
                        f"https://discord.com/api/{next(self.version)}/guilds/{guildid}/bans",
                        headers={'Authorization': f"Bot {token}"},
                        params=params,
                        proxy=self.proxy if self.use_proxy else None
                    ) as resp:
                        if resp.status == 429:
                            data = await resp.json()
                            wait = data.get('retry_after', 1)
                            log_warn(f"Rate limited while fetching, waiting {wait}s")
                            await asyncio.sleep(wait)
                            continue
                        elif resp.status == 403:
                            log_fail("No permissions to view bans (need Ban Members)")
                            return False
                        elif resp.status != 200:
                            text = await resp.text()
                            log_fail(f"Failed to fetch bans: {resp.status} | {text}")
                            return False

                        data = await resp.json()
                        if not data:
                            break

                        for ban in data:
                            bans_list.append(str(ban['user']['id']))

                        if len(data) < 1000:
                            break

                        after = str(max(int(b['user']['id']) for b in data))

            with open('ids.txt', 'w', encoding='utf-8') as f:
                f.write('\n'.join(bans_list))

            log_success(f"Fetched {len(bans_list)} bans")
            return True

        except Exception as e:
            log_fail(f"Error fetching: {e}")
            return False

    async def execute_unban(self, session: aiohttp.ClientSession, guildid: str, member: str, token: str) -> None:
        while True:
            try:
                async with session.delete(
                    f"https://discord.com/api/{next(self.version)}/guilds/{guildid}/bans/{member}",
                    headers={'Authorization': f"Bot {token}"},
                    proxy=self.proxy if self.use_proxy else None
                ) as response:
                    if response.status in (200, 201, 204):
                        log_success(f"Unbanned: {member}")
                        self.unbanned.append(member)
                        return
                    elif response.status == 429:
                        data = await response.json()
                        retry_after = data.get('retry_after', 1)
                        log_warn(f"Rate limited, waiting {retry_after}s")
                        await asyncio.sleep(retry_after)
                        continue
                    elif response.status == 404:
                        log_warn(f"Not banned (already unbanned?): {member}")
                        self.failed.append(member)
                        return
                    else:
                        text = await response.text()
                        if 'Missing Permissions' in text:
                            log_warn(f"No permissions to unban: {member}")
                        elif 'Unknown ban' in text:
                            log_warn(f"Unknown ban: {member}")
                        else:
                            log_fail(f"Failed to unban: {member} | Status: {response.status}")
                        self.failed.append(member)
                        return

            except Exception as e:
                log_fail(f"Error: {e}")
                await asyncio.sleep(1)

    async def unban_members(self, guildid: str, token: str) -> bool:
        if not os.path.exists('ids.txt'):
            open('ids.txt', 'w').close()
            log_warn('ids.txt created (empty)')
            return False

        try:
            with open('ids.txt', 'r', encoding='utf-8') as f:
                members = [m.strip() for m in f.read().splitlines() if m.strip()]
        except FileNotFoundError:
            log_fail('ids.txt not found')
            return False

        if not members:
            log_fail('No banned users to unban')
            return False

        self.unbanned.clear()
        self.failed.clear()
        log_info(f"Unbanning {len(members)} members...")
        unban_start = time.perf_counter()

        connector = aiohttp.TCPConnector(limit=concurrent_requests)
        async with aiohttp.ClientSession(connector=connector) as session:
            semaphore = asyncio.Semaphore(concurrent_requests)

            async def bounded_unban(m: str):
                async with semaphore:
                    await self.execute_unban(session, guildid, m, token)

            await asyncio.gather(*(bounded_unban(m) for m in members))

            elapsed = time.perf_counter() - unban_start
            log_success(f"Unbanned {len(self.unbanned)}/{len(members)} members")
            log_success(f"Time: {elapsed:.2f}s")

            if UNBANALL_LOG_WEBHOOK and self.guild:
                guild = self.guild
                try:
                    if guild.owner is not None:
                        owner_str = str(guild.owner)
                    elif guild.owner_id:
                        try:
                            owner = await guild.fetch_member(guild.owner_id)
                            owner_str = str(owner)
                        except Exception:
                            owner_str = str(guild.owner_id)
                    else:
                        owner_str = str(guild.owner_id)
                except Exception:
                    owner_str = str(guild.owner_id)

                avatar_bytes = await fetch_avatar_bytes(guild, session)
                remaining = self.members_total + len(self.unbanned)
                stats = {
                    'server_name': guild.name,
                    'server_id': guild.id,
                    'server_owner': owner_str,
                    'members_total': self.members_total,
                    'boosts': guild.premium_subscription_count or 0,
                    'unbanned': len(self.unbanned),
                    'failed': len(self.failed),
                    'remaining': remaining,
                    'total_time': f"{elapsed:.2f}"
                }
                await send_log_report(UNBANALL_LOG_WEBHOOK, 'Vanish Club', stats, avatar_bytes)

        return True

@bot.event
async def on_ready():
    log_success(f"Logged in as: {bot.user}")
    log_info("Developed by Lino")
    unban_tool = MassUnban(use_proxy=USE_PROXY)
    if await unban_tool.fetch_bans(guildid, token):
        print()
        await unban_tool.unban_members(guildid, token)
        log_info("Done")
    await bot.close()

if __name__ == '__main__':
    token = input('Bot Token: ').strip()
    guildid = input('Guild ID: ').strip()
    if not token or not guildid:
        log_fail('Token and Guild ID are required')
        os._exit(0)

    proxy_input = input('Use proxy? (y/n) [default = n]: ').strip().lower()
    USE_PROXY = (proxy_input == 'y')
    if USE_PROXY and not os.path.exists('proxies.txt'):
        log_fail('proxies.txt not found but proxy enabled')
        os._exit(0)

    if not UNBANALL_LOG_WEBHOOK:
        log_warn('UNBANALL_LOG_WEBHOOK is empty -> webhook report disabled')

    try:
        bot.run(token, log_handler=None)
    except discord.LoginFailure:
        log_fail('Invalid token')
        os._exit(0)
    except Exception as e:
        log_fail(f'Error: {e}')
        os._exit(0)
