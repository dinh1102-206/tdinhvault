import os
import re
import sys
import shutil
import threading
from colorama import init, Fore, Style

init(autoreset=True)

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

RESET = Style.RESET_ALL

# 100% standard ANSI safe colors (no 24-bit TrueColor parsing conflicts)
P1 = Fore.LIGHTMAGENTA_EX
P2 = Fore.MAGENTA
P3 = Fore.LIGHTMAGENTA_EX
P4 = Fore.MAGENTA
P5 = Fore.LIGHTBLACK_EX

R1 = Fore.LIGHTMAGENTA_EX
R2 = Fore.MAGENTA
R3 = Fore.MAGENTA
R4 = Fore.LIGHTBLACK_EX
R5 = Fore.LIGHTBLACK_EX
R6 = Fore.LIGHTBLACK_EX

ROW_COLORS = [Fore.LIGHTMAGENTA_EX, Fore.LIGHTMAGENTA_EX, Fore.MAGENTA, Fore.MAGENTA, Fore.LIGHTBLACK_EX, Fore.LIGHTBLACK_EX, Fore.LIGHTBLACK_EX, Fore.LIGHTBLACK_EX, Fore.LIGHTBLACK_EX, Fore.LIGHTBLACK_EX]

WHITE  = Fore.LIGHTWHITE_EX
SILVER = Fore.WHITE
MUTED  = Fore.LIGHTBLACK_EX
BORDER = Fore.LIGHTBLACK_EX
CYAN   = Fore.LIGHTCYAN_EX

SUCCESS = Fore.LIGHTGREEN_EX
WARNING = Fore.LIGHTYELLOW_EX
DANGER  = Fore.LIGHTRED_EX

ANSI_REGEX = re.compile(r'\x1b\[[0-9;]*[a-zA-Z]')
PRINT_LOCK = threading.Lock()

def get_term_width() -> int:
    try:
        return shutil.get_terminal_size((90, 24)).columns
    except Exception:
        return 90

def visible_len(text: str) -> int:
    return len(ANSI_REGEX.sub('', text))

def center_text(text: str, total_w: int = None) -> str:
    w = total_w or get_term_width()
    v_len = visible_len(text)
    margin = max(0, (w - v_len) // 2)
    return " " * margin + text

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class BlackforgeUI:
    BOX_WIDTH = 74
    INNER_WIDTH = BOX_WIDTH - 2  # 72

    @classmethod
    def get_margin(cls) -> str:
        w = get_term_width()
        margin = max(0, (w - cls.BOX_WIDTH) // 2)
        return " " * margin

    @classmethod
    def render_banner(cls, subtitle: str = ""):
        clear()
        print()

        figure = [
            "⠀⠀⠀⠀⣠⣤⣶⣶⣶⣤⣄⡀",
            "⠀⠀⣴⣾⣿⣿⣿⣿⣿⣧⡀⠈",
            "⠀⣼⣿⣿⣿⣿⣿⣿⣿⡿⠁⠀",
            "⢰⡿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀",
            "⠘⣽⡿⠿⠿⣿⣿⣿⣿⣿⣦⣤",
            "⠀⣟⠀⠀⠀⣸⣿⡏⠀⠀⠀⢹",
            "⠀⣿⣷⣶⣾⡿⠁⠙⣄⣀⣀⣠",
            "⠀⠙⠙⢿⡿⣷⣶⣤⣿⣿⡿⠿",
            "⠀⠀⠀⠺⡏⡏⡏⡏⡏⠉⠁⠀",
            "⠀⠀⠀⠀⠀⠀⠁⠁⠀⠀⠀⠀",
        ]

        forge_art = [
            "████████╗██████╗ ██╗███╗   ██╗",
            "╚══██╔══╝██╔══██╗██║████╗  ██║",
            "   ██║   ██║  ██║██║██╔██╗ ██║",
            "   ██║   ██║  ██║██║██║╚██╗██║",
            "   ██║   ██████╔╝██║██║ ╚████║",
            "   ╚═╝   ╚═════╝ ╚═╝╚═╝  ╚═══╝",
        ]

        fig_rows   = len(figure)
        forge_rows = len(forge_art)
        gap        = "   "

        pad_top      = (fig_rows - forge_rows) // 2
        pad_bottom   = fig_rows - forge_rows - pad_top
        forge_padded = ([""] * pad_top) + forge_art + ([""] * pad_bottom)
        forge_max_w  = max(len(l) for l in forge_art)

        margin = cls.get_margin()
        for idx in range(fig_rows):
            col        = ROW_COLORS[min(idx, len(ROW_COLORS) - 1)]
            fig_part   = f"{col}{figure[idx]}{RESET}"
            forge_line = forge_padded[idx]
            forge_part = f"{col}{forge_line}{RESET}" if forge_line else (" " * forge_max_w)
            line_str   = fig_part + gap + forge_part
            v_len      = visible_len(line_str)
            w          = get_term_width()
            line_margin = " " * max(0, (w - v_len) // 2)
            print(line_margin + line_str)

        print()
        BETA_TAG = f"{BORDER}[{P1} BETA VERSION {BORDER}]{RESET}"
        if subtitle:
            sub = f"{P1}> {WHITE}{subtitle}{RESET}{P1} <{RESET}  {BETA_TAG}"
        else:
            sub = f"{P1}> {WHITE}FORGE TOOL ĐA CHỨC NĂNG  |  BY TDIN CTE{RESET}{P1} <{RESET}  {BETA_TAG}"
        v_sub = visible_len(sub)
        sub_margin = " " * max(0, (get_term_width() - v_sub) // 2)
        print(sub_margin + sub)
        print()

    @classmethod
    def b_top(cls, title: str = "") -> str:
        margin = cls.get_margin()
        if title:
            lbl = f" [ {title} ] "
            v = len(lbl)
            l = (cls.INNER_WIDTH - v) // 2
            r = cls.INNER_WIDTH - v - l
            return f"{margin}{BORDER}╔{'═' * l}{CYAN}{lbl}{BORDER}{'═' * r}╗{RESET}"
        return f"{margin}{BORDER}╔{'═' * cls.INNER_WIDTH}╗{RESET}"

    @classmethod
    def b_bottom(cls) -> str:
        margin = cls.get_margin()
        return f"{margin}{BORDER}╚{'═' * cls.INNER_WIDTH}╝{RESET}"

    @classmethod
    def b_div(cls, label: str = "") -> str:
        margin = cls.get_margin()
        if label:
            lbl = f" {label} "
            v = len(lbl)
            l = (cls.INNER_WIDTH - v) // 2
            r = cls.INNER_WIDTH - v - l
            return f"{margin}{BORDER}╠{'═' * l}{MUTED}{lbl}{BORDER}{'═' * r}╣{RESET}"
        return f"{margin}{BORDER}╠{'═' * cls.INNER_WIDTH}╣{RESET}"

    @classmethod
    def b_row(cls, text: str = "") -> str:
        margin = cls.get_margin()
        content_width = cls.INNER_WIDTH - 4
        p = max(0, content_width - visible_len(text))
        return f"{margin}{BORDER}║  {RESET}{text}{' ' * p}  {BORDER}║{RESET}"

    @classmethod
    def log(cls, msg: str):
        with PRINT_LOCK:
            print(cls.b_row(msg))
