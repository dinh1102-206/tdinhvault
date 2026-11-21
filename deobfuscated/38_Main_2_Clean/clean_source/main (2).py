# ==============================================================================
# DEOBFUSCATED SOURCE CODE - REVERSED BY TDINH
# ==============================================================================

import sys
import math
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


# Whiscat Obfuscator Shield (đã vô hiệu hóa lệnh tự hủy file để an toàn khi chạy)
def _shield_70698():
    return


def calculate_stats(numbers):
    n = len(numbers)
    if n == 0:
        return (0, 0)
    mean = sum(numbers) / n
    variance = sum(((x - mean) ** 2 for x in numbers)) / n
    std_dev = math.sqrt(variance)
    return (mean, std_dev)


def main():
    # Chạy intro banner trước khi vào nội dung chính
    iloveyou()

    data = [12, 15, 23, 42, 56, 78, 99]
    avg, sd = calculate_stats(data)

    print((lambda b: bytes([x ^ 127 for x in b]).decode('utf-8', 'surrogatepass'))(b'BBB_,\x0b\x1e\x0b\x16\x0c\x0b\x16\x1c\x1e\x13_>\x11\x1e\x13\x06\x0c\x16\x0c_BBB'))
    print((lambda b: bytes([x ^ 127 for x in b]).decode('utf-8', 'surrogatepass'))(b';\x1e\x0b\x1e\x0c\x1a\x0bE_') + str(data))
    print((lambda b: bytes([x ^ 127 for x in b]).decode('utf-8', 'surrogatepass'))(b'>\t\x1a\r\x1e\x18\x1aE_') + str(avg))
    print((lambda b: bytes([x ^ 127 for x in b]).decode('utf-8', 'surrogatepass'))(b',\x0b\x1e\x11\x1b\x1e\r\x1b_;\x1a\t\x16\x1e\x0b\x16\x10\x11E_') + str(sd))
    print((lambda b: bytes([x ^ 127 for x in b]).decode('utf-8', 'surrogatepass'))(b',\x0b\x1e\x0b\n\x0cE_,\n\x1c\x1c\x1a\x0c\x0c^'))


if __name__ == '__main__':
    main()
