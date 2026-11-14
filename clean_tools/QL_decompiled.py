# Author: tdinh
# Decoded by: tdinh cute
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
            pass


def resize_console(width, height):
    if os.name != 'nt':
        return
    try:
        os.system(f'mode con: cols={width} lines={height}')
    except Exception:
        pass


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
    f'v{LOADER_VERSION}    {DEVELOPER_TEXT}',
    DISCORD_TEXT,
    'Select a version',
    '[1] TUI      Terminal interface',
    '[2] GUI      Graphical interface',
    '[3] Exit',
    '> '
]

LONGEST_LINE = max(len(line) for line in UI_LINES)
CONSOLE_WIDTH = max(66, LONGEST_LINE + 16)
CONSOLE_HEIGHT = 16


def separator():
    print(f"  {GRAY}{'─' * (CONSOLE_WIDTH - 4)}{RESET}")


def header():
    print()
    print(f"  {LIGHT_PURPLE}Quasar Loader{RESET}")
    print(f"  {GRAY}{DISCORD_TEXT}{RESET}")
    print()
    print(f"  {GRAY}v{LOADER_VERSION}    {DEVELOPER_TEXT}{RESET}")
    print()
    separator()
    print()


def draw_menu():
    clear()
    header()
    print(f"  {WHITE}Select a version{RESET}")
    print()
    print(f"  {LIGHT_PURPLE}[1]{RESET} {WHITE}TUI{RESET}{GRAY}      Terminal interface{RESET}")
    print(f"  {LIGHT_PURPLE}[2]{RESET} {WHITE}GUI{RESET}{GRAY}      Graphical interface{RESET}")
    print(f"  {LIGHT_PURPLE}[3]{RESET} {WHITE}Exit{RESET}")
    print()
    separator()
    print()
    print(f"  {LIGHT_PURPLE}>{RESET} ", end='', flush=True)


def open_download(url, version_name):
    clear()
    header()
    print(f"  {LIGHT_PURPLE}{version_name}{RESET}")
    print()
    print(f"  {GRAY}Opening download...{RESET}")
    try:
        opened = webbrowser.open(url)
        print()
        if opened:
            print(f"  {SOFT_PURPLE}Done{RESET}  {GRAY}Download opened in your browser.{RESET}")
        else:
            print(f"  {GRAY}Unable to open your browser automatically.{RESET}")
    except Exception:
        print()
        print(f"  {GRAY}Unable to open your browser automatically.{RESET}")

    print()
    separator()
    print()
    input(f"  {GRAY}Press ENTER to return...{RESET}")


def main():
    enable_colors()
    set_console_title()
    resize_console(CONSOLE_WIDTH, CONSOLE_HEIGHT)

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
                print(f"  {LIGHT_PURPLE}Quasar Loader{RESET}")
                print(f"  {GRAY}Closing...{RESET}")
                time.sleep(0.5)
                clear()
                break
            else:
                clear()
                header()
                print(f"  {GRAY}Invalid selection.{RESET}")
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
