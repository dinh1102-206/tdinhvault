# ==============================================================================
# DEOBFUSCATED SOURCE CODE - REVERSED BY TDINH
# Target: input/main.py (Tsunami / NgocUyenEncoder - NanhClient Discord Token Refresher)
# ==============================================================================

import sys
import os
import time
import json
import base64
import random
import string
from typing import Optional, Dict
import httpx
import brotli

# Optional Crypto imports (included in original source dependencies)
try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import unpad
except ImportError:
    pass

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


def iloveyou():
    """
    3D Intro Banner - DEOBF BY TDINH
    Hiển thị hiệu ứng mở đầu trước khi chuyển vào luồng chính của file
    """
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


# Alias
def ilove_you():
    iloveyou()


class NanhClient:
    def __init__(self, token: str):
        self.token = token
        self.base_url = 'https://discord.com/api/v9'
        self.new_token = None
        self.handoff_key = None
        self.user_agent = (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        )
        self.build_number = 373618
        self.client = httpx.Client(http2=True, verify=True, timeout=30.0)

    def _decompress_response(self, response: httpx.Response) -> bytes:
        content = response.content
        encoding = response.headers.get('content-encoding', '').lower()
        if encoding == 'br':
            try:
                content = brotli.decompress(content)
            except Exception:
                pass
        return content

    def _sper_properties(self) -> str:
        props = {
            'os': 'Windows',
            'browser': 'Chrome',
            'device': '',
            'system_locale': 'en-US',
            'browser_user_agent': self.user_agent,
            'browser_version': '131.0.0.0',
            'os_version': '10',
            'referrer': '',
            'referring_domain': '',
            'referrer_current': '',
            'referring_domain_current': '',
            'release_channel': 'stable',
            'client_build_number': self.build_number,
            'client_event_source': None,
        }
        return base64.b64encode(json.dumps(props, separators=(',', ':')).encode()).decode()

    def _get_headers(self, with_auth: bool = True, fingerprint: Optional[str] = None) -> Dict[str, str]:
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/json',
            'Origin': 'https://discord.com',
            'Referer': 'https://discord.com/channels/@me',
            'Sec-Ch-Ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': self.user_agent,
            'X-Debug-Options': 'bugReporterEnabled',
            'X-Discord-Locale': 'en-US',
            'X-Discord-Timezone': 'Asia/Ho_Chi_Minh',
            'X-Super-Properties': self._sper_properties(),
        }
        if with_auth and self.token:
            headers['Authorization'] = self.token
        if fingerprint:
            headers['X-Fingerprint'] = fingerprint
        return headers

    def get_fingerprint(self) -> Optional[str]:
        try:
            response = self.client.get(
                f'{self.base_url}/experiments',
                headers=self._get_headers(with_auth=False),
            )
            if response.status_code == 200:
                data = response.json()
                return data.get('fingerprint')
            return None
        except Exception:
            return None

    def check_tk(self) -> Optional[dict]:
        try:
            response = self.client.get(f'{self.base_url}/users/@me', headers=self._get_headers())
            if response.status_code == 200:
                user = response.json()
                print(f"User: {user.get('username')} (ID: {user.get('id')})")
                return user
            else:
                print(f'Token lỗi: {response.status_code}')
                return None
        except Exception:
            return None

    def dec_handoff(self) -> Optional[str]:
        try:
            self.handoff_key = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
            response = self.client.post(
                f'{self.base_url}/auth/handoff',
                headers=self._get_headers(),
                json={'key': self.handoff_key},
            )
            if response.status_code == 200:
                content = self._decompress_response(response)
                try:
                    data = json.loads(content.decode('utf-8'))
                    handoff_token = data.get('handoff_token')
                    if handoff_token:
                        return handoff_token
                    return None
                except Exception:
                    return None
            else:
                content = self._decompress_response(response)
                return None
        except Exception:
            return None

    def change_ex(self, handoff_token: str) -> Optional[str]:
        try:
            fingerprint = self.get_fingerprint()
            payload = {'handoff_token': handoff_token, 'key': self.handoff_key}
            response = self.client.post(
                f'{self.base_url}/auth/handoff/exchange',
                headers=self._get_headers(with_auth=False, fingerprint=fingerprint),
                json=payload,
            )
            if response.status_code == 200:
                content = self._decompress_response(response)
                try:
                    data = json.loads(content.decode('utf-8'))
                    new_token = data.get('token')
                    if new_token:
                        print(f'Token mới: {new_token[:50]}...')
                        self.new_token = new_token
                        return new_token
                    return None
                except Exception:
                    return None
            else:
                content = self._decompress_response(response)
                return None
        except Exception:
            return None

    def get_sess(self) -> Optional[list]:
        try:
            response = self.client.get(f'{self.base_url}/auth/sessions', headers=self._get_headers())
            if response.status_code == 200:
                data = response.json()
                return data.get('user_sessions', [])
            return None
        except Exception:
            return None

    def _logout(self, token_to_logout: str) -> bool:
        try:
            headers = self._get_headers()
            headers['Authorization'] = token_to_logout
            response = self.client.post(
                f'{self.base_url}/auth/logout',
                headers=headers,
                json={'provider': None, 'voip_provider': None},
            )
            return response.status_code in (200, 204)
        except Exception:
            return False

    def _out_ses(self) -> bool:
        try:
            success = self._logout(self.token)
            if success:
                print('Logout token cũ thành công')
                return True
            else:
                print('Lỗi đăng xuất token cũ')
                return False
        except Exception:
            return False

    def verify_nanh(self) -> bool:
        try:
            headers = self._get_headers()
            headers['Authorization'] = self.new_token
            response = self.client.get(f'{self.base_url}/users/@me', headers=headers)
            if response.status_code == 200:
                user = response.json()
                print(f"User: {user.get('username')} (ID: {user.get('id')})")
                return True
            else:
                print(f'Token mới lỗi: {response.status_code}')
                return False
        except Exception:
            return False

    def lam_moi(self) -> Optional[str]:
        user = self.check_tk()
        if not user:
            print('\nToken nhập lỗi')
            return None

        handoff_token = self.dec_handoff()
        if not handoff_token:
            return self.dec_nati()

        new_token = self.change_ex(handoff_token)
        if not new_token:
            return self.dec_nati()

        self._out_ses()

        if self.verify_nanh():
            print(f'\nToken mới: {new_token}')
            return new_token
        return None

    def dec_nati(self):
        try:
            response = self.client.get(
                f'{self.base_url}/users/@me/settings',
                headers=self._get_headers(),
            )
            if response.status_code == 200:
                settings = response.json()
        except Exception:
            pass
        return None

    def __del__(self):
        try:
            self.client.close()
        except Exception:
            pass


def main():
    try:
        with open('tokens.txt', 'r', encoding='utf-8') as f:
            tokens = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print('Thiếu tokens.txt')
        return
    except Exception:
        return

    if not tokens:
        return

    print('Check {0} token\n'.format(len(tokens)))
    new_tokens = []
    for idx, old_token in enumerate(tokens, 1):
        client = NanhClient(old_token)
        new_token = client.lam_moi()
        if new_token:
            new_tokens.append(new_token)
            print('\nToken {0} : thành công'.format(idx))
        else:
            print('\nToken {0} failed'.format(idx))

    if new_tokens:
        with open('new.txt', 'w', encoding='utf-8') as f:
            for nt in new_tokens:
                f.write(nt + '\n')
        print('Đã tự động lưu {0} token vào new.txt'.format(len(new_tokens)))
    else:
        print('Không có token nào được làm mới thành công.')


if __name__ == '__main__':
    iloveyou()
    main()
