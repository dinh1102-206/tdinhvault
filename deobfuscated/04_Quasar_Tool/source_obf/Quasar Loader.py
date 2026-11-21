# ==============================================================================
# DEOBFUSCATED SOURCE CODE - REVERSED BY TDINH
# ==============================================================================

import sys
import os
import time

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


import ctypes
import os
import sys
import time
import webbrowser

LOADER_VERSION = '1.0.0'
TUI_DOWNLOAD_URL = 'https://github.com/quasartool/QuasarToolTUI/releases/download/QuasarTool/QuasarTool.rar'
GUI_DOWNLOAD_URL = 'https://github.com/quasartool/QuasarToolGUI/releases/download/QuasarTool/QuasarTool.rar'

RESET = '\x1b[0m'
WHITE = '\x1b[97m'
GRAY = '\x1b[38;5;245m'
LIGHT_PURPLE = '\x1b[38;5;183m'
SOFT_PURPLE = '\x1b[38;5;147m'


def enable_colors():
    if os.name == 'nt':
        os.system('')


def set_console_title():
    if os.name == 'nt':
        try:
            ctypes.windll.kernel32.SetConsoleTitleW('Quasar Loader')
        except Exception:
            return None


def resize_console(width, height):
    if os.name != 'nt':
        return
    else:
        try:
            os.system(f'mode con: cols={width} lines={height}')
        except Exception:
            return None


def hide_cursor():
    print('\x1b[?25l', end='')


def show_cursor():
    print('\x1b[?25h', end='')


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


DISCORD_TEXT = 'discord.gg/quas'
DEVELOPER_TEXT = 'devs | vhs8 + f1eq'
UI_LINES = [
    'Quasar Loader',
    DISCORD_TEXT,
    f'v{LOADER_VERSION}',
    DEVELOPER_TEXT,
    'Select a version',
    '[1] TUI      Terminal interface',
    '[2] GUI      Graphical interface',
    '[3] Exit',
    '>'
]
LONGEST_LINE = max((len(line) for line in UI_LINES))
CONSOLE_WIDTH = LONGEST_LINE + 8
CONSOLE_HEIGHT = 18


def separator():
    print(f'  {GRAY}{"─" * (CONSOLE_WIDTH - 4)}{RESET}')


def header():
    print()
    print(f'  {LIGHT_PURPLE}Quasar Loader{RESET}')
    print(f'  {GRAY}discord.gg/quas{RESET}')
    print()
    print(f'  {GRAY}v{LOADER_VERSION}    {DEVELOPER_TEXT}{RESET}')
    print()
    separator()
    print()


def draw_menu():
    clear()
    header()
    print(f'  {WHITE}Select a version{RESET}')
    print()
    print(f'  {LIGHT_PURPLE}[1]{RESET} {WHITE}TUI{RESET}      {GRAY}Terminal interface{RESET}')
    print(f'  {LIGHT_PURPLE}[2]{RESET} {WHITE}GUI{RESET}      {GRAY}Graphical interface{RESET}')
    print(f'  {GRAY}[3] Exit{RESET}')
    print()
    separator()
    print()
    print(f'  {LIGHT_PURPLE}>{RESET} ', end='', flush=True)


def open_download(url, version_name):
    clear()
    header()
    print(f'  {LIGHT_PURPLE}{version_name}{RESET}')
    print()
    print(f'  {GRAY}Opening download...{RESET}')
    try:
        opened = webbrowser.open(url)
        print()
        if opened:
            print(f'  {SOFT_PURPLE}Done{RESET}  {GRAY}Download opened in your browser.{RESET}')
        else:
            print(f'  {GRAY}Unable to open your browser automatically.{RESET}')
    except Exception:
        print()
        print(f'  {GRAY}Unable to open your browser automatically.{RESET}')
    print()
    separator()
    print()
    input(f'  {GRAY}Press ENTER to return...{RESET}')


def main():
    iloveyou()
    enable_colors()
    set_console_title()
    resize_console(CONSOLE_WIDTH, CONSOLE_HEIGHT)
    hide_cursor()
    try:
        while True:
            draw_menu()
            choice = input().strip()
            if choice == '1':
                open_download(TUI_DOWNLOAD_URL, 'TUI Version')
            elif choice == '2':
                open_download(GUI_DOWNLOAD_URL, 'GUI Version')
            elif choice == '3':
                clear()
                print()
                print(f'  {LIGHT_PURPLE}Quasar Loader{RESET}')
                print(f'  {GRAY}Closing...{RESET}')
                time.sleep(0.5)
                clear()
                break
            else:
                clear()
                header()
                print(f'  {GRAY}Invalid selection.{RESET}')
                time.sleep(0.7)
    finally:
        show_cursor()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        show_cursor()
        clear()
        sys.exit(0)
