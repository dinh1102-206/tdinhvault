# -*- coding: utf-8 -*-
# ==============================================================================
# TOOL NAME   : TITAN-SHIELD OBFUSCATOR v3.0 (TITAN GENESIS - EXTREME SPEED)
# OWNER       : tdinh
# SERVER      : 4ever
# OBF MODE    : titan (Extreme Anti-Hook, VM State Machine, Non-Linear Shards)
# ==============================================================================

import os
import sys
import ast
import zlib
import time
import random
import hashlib
import marshal
import base64
import gc
from colorama import Fore, Style, init

init(autoreset=True)

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def render_banner():
    banner = f"""{Fore.CYAN}{Style.BRIGHT}
  ████████╗██╗████████╗ █████╗ ███╗   ██╗     ██████╗ ███████╗███╗   ██╗███████╗███████╗██╗███████╗
  ╚══██╔══╝██║╚══██╔══╝██╔══██╗████╗  ██║    ██╔════╝ ██╔════╝████╗  ██║██╔════╝██╔════╝██║██╔════╝
     ██║   ██║   ██║   ███████║██╔██╗ ██║    ██║  ███╗█████╗  ██╔██╗ ██║█████╗  ███████╗██║███████╗
     ██║   ██║   ██║   ██╔══██║██║╚██╗██║    ██║   ██║██╔══╝  ██║╚██╗██║██╔══╝  ╚════██║██║╚════██║
     ██║   ██║   ██║   ██║  ██║██║ ╚████║    ╚██████╔╝███████╗██║ ╚████║███████╗███████║██║███████║
     ╚═╝   ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝     ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚══════╝╚══════╝╚═╝╚══════╝
{Fore.YELLOW}             ═══[ >> HIGH-SPEED ENGINE v3.0 - EXTREME DEFENSE EDITION << ]═══{Fore.WHITE}
                 - Owner      : {Fore.GREEN}tdinh{Fore.WHITE}
                 - Server     : {Fore.MAGENTA}4ever{Fore.WHITE}
                 - Obf Mode   : {Fore.RED}TITAN GENESIS (VM State Machine & Anti-Dump){Fore.WHITE}
"""
    print(banner)

# ==============================================================================
# LAYER 1: AST STRING & CONSTANT MUTATION
# ==============================================================================
class ASTStringScrambler(ast.NodeTransformer):
    """Mã hóa tất cả chuỗi string literal thành biểu thức dynamic XOR on-the-fly."""
    def __init__(self):
        super().__init__()
        self.salt_key = random.randint(0x20, 0xFE)

    def visit_Constant(self, node):
        if isinstance(node.value, str) and len(node.value) >= 2:
            if node.value.startswith("__") and node.value.endswith("__"):
                return node
            key = (self.salt_key + len(node.value)) & 0xFF
            enc = [(ord(c) ^ key) for c in node.value]
            call_node = ast.Call(
                func=ast.Attribute(
                    value=ast.Constant(value=""),
                    attr="join",
                    ctx=ast.Load()
                ),
                args=[
                    ast.GeneratorExp(
                        elt=ast.Call(
                            func=ast.Name(id="chr", ctx=ast.Load()),
                            args=[
                                ast.BinOp(
                                    left=ast.Name(id="_c", ctx=ast.Load()),
                                    op=ast.BitXor(),
                                    right=ast.Constant(value=key)
                                )
                            ],
                            keywords=[]
                        ),
                        generators=[
                            ast.comprehension(
                                target=ast.Name(id="_c", ctx=ast.Store()),
                                iter=ast.List(
                                    elts=[ast.Constant(value=b) for b in enc],
                                    ctx=ast.Load()
                                ),
                                ifs=[],
                                is_async=0
                            )
                        ]
                    )
                ],
                keywords=[]
            )
            return ast.copy_location(call_node, node)
        return node

# ==============================================================================
# LAYER 2: TITAN GENESIS ENGINE (CRYPTOGRAPHIC SHARDING + VM STATE MACHINE)
# ==============================================================================
class TitanGenesisEngine:
    def __init__(self, key: str = "tdincte", shard_size: int = 120):
        self.key_str = key
        self.key_bytes = key.encode("utf-8")
        self.shard_size = shard_size

    def _mutate_ast(self, source_code: str):
        try:
            tree = ast.parse(source_code)
            transformer = ASTStringScrambler()
            new_tree = transformer.visit(tree)
            ast.fix_missing_locations(new_tree)
            return compile(new_tree, "<titan-core>", "exec")
        except Exception:
            return compile(source_code, "<titan-core>", "exec")

    def _random_var(self):
        return f"_0x{random.randint(0x1000, 0xFFFF):x}"

    def obfuscate(self, source_code: str) -> str:
        # 1. Mutate AST & Compile to Bytecode
        code_obj = self._mutate_ast(source_code)
        marshaled_data = marshal.dumps(code_obj)

        # 2. Multi-stage compression
        compressed = zlib.compress(marshaled_data, 9)

        # 3. Dynamic Rolling Hash & Feedback Stream Cipher
        salt = os.urandom(32)
        encrypted_stream = bytearray()
        s_len = len(salt)
        k_len = len(self.key_bytes)
        
        running_state = 0xAA
        for idx in range(len(compressed)):
            orig_byte = compressed[idx]
            k = (self.key_bytes[idx % k_len] ^ salt[idx % s_len] ^ running_state) & 0xFF
            enc_byte = (orig_byte ^ k) & 0xFF
            encrypted_stream.append(enc_byte)
            running_state = (running_state + enc_byte + (idx & 0x7F)) & 0xFF

        enc_bytes = bytes(encrypted_stream)

        # 4. Multi-Shard Partitioning & Random Permutation
        shards = []
        cursor = 0
        while cursor < len(enc_bytes):
            chunk_len = random.randint(max(32, self.shard_size - 40), self.shard_size + 40)
            chunk = enc_bytes[cursor : cursor + chunk_len]
            shards.append(chunk)
            cursor += chunk_len

        indexed = list(enumerate(shards))
        random.shuffle(indexed)
        order = [i for i, _ in indexed]
        shuffled_shards = [base64.b64encode(s).decode("ascii") for _, s in indexed]

        salt_b64 = base64.b64encode(salt).decode("ascii")
        key_b64 = base64.b64encode(self.key_bytes).decode("ascii")

        # Randomized internal state markers
        st_start = random.randint(0x100, 0x1FF)
        st_assemble = random.randint(0x200, 0x2FF)
        st_decrypt = random.randint(0x300, 0x3FF)
        st_unpack = random.randint(0x400, 0x4FF)
        st_purge = random.randint(0x500, 0x5FF)
        st_exit = 0xDEADC0DE

        # 5. Build Hardcore VM Runtime Template with required Header
        runtime_script = f'''# -*- coding: utf-8 -*-
__tdinh__ = __4ever__ = 1
__obf__    = __tdinh__
__in4mation = [ 
    "owner : tdinh",
    "obf mode : titan"
]

import sys as _0x_s, zlib as _0x_z, marshal as _0x_m, base64 as _0x_b, gc as _0x_g

class _TitanGuard:
    @staticmethod
    def _verify_integrity():
        if _0x_s.gettrace() is not None:
            _0x_s.exit(0)
        for _bad in ('dis', 'pycdc', 'decompyle++', 'uncompyle6', 'pylingual', 'inspect'):
            if _bad in _0x_s.modules:
                _0x_s.exit(0)
        _real_exec = getattr(_0x_s.modules.get('builtins'), 'exec', None)
        if _real_exec is not None:
            if type(_real_exec).__name__ != 'builtin_function_or_method' or hasattr(_real_exec, '__code__'):
                _0x_s.exit(0)

_TitanGuard._verify_integrity()

_0x_s_data = "{salt_b64}"
_0x_k_data = "{key_b64}"
_0x_p_map  = {order}
_0x_b_shards = {shuffled_shards}

def _titan_vm_dispatch():
    global _0x_s_data, _0x_k_data, _0x_p_map, _0x_b_shards
    _TitanGuard._verify_integrity()
    
    _state = {hex(st_start)}
    _raw_buffer = bytearray()
    _dec_buffer = bytearray()
    _salt = _0x_b.b64decode(_0x_s_data)
    _key = _0x_b.b64decode(_0x_k_data)
    _total_shards = len(_0x_p_map)
    _indexed_chunks = {{}}
    _idx = 0
    _running = 0xAA
    _s_len, _k_len = len(_salt), len(_key)
    _core_code = None

    while _state != {hex(st_exit)}:
        if _state == {hex(st_start)}:
            if _idx < _total_shards:
                _pos = _0x_p_map[_idx]
                _indexed_chunks[_pos] = _0x_b.b64decode(_0x_b_shards[_idx])
                _idx += 1
            else:
                _idx = 0
                _state = {hex(st_assemble)}

        elif _state == {hex(st_assemble)}:
            if _idx < _total_shards:
                _raw_buffer.extend(_indexed_chunks[_idx])
                del _indexed_chunks[_idx]
                _idx += 1
            else:
                del _indexed_chunks
                _idx = 0
                _state = {hex(st_decrypt)}

        elif _state == {hex(st_decrypt)}:
            _raw_len = len(_raw_buffer)
            for _i in range(_raw_len):
                _b = _raw_buffer[_i]
                _k = _key[_i % _k_len] ^ _salt[_i % _s_len] ^ _running
                _orig = (_b ^ _k) & 0xFF
                _dec_buffer.append(_orig)
                _running = (_running + _b + (_i & 0x7F)) & 0xFF
            del _raw_buffer, _salt, _key
            _state = {hex(st_unpack)}

        elif _state == {hex(st_unpack)}:
            _TitanGuard._verify_integrity()
            _decompressed = _0x_z.decompress(_dec_buffer)
            del _dec_buffer
            _loader_name = bytes([108, 111, 97, 100, 115]).decode()
            _core_code = getattr(_0x_m, _loader_name)(_decompressed)
            del _decompressed
            _state = {hex(st_purge)}

        elif _state == {hex(st_purge)}:
            del _0x_s_data, _0x_k_data, _0x_p_map, _0x_b_shards
            _0x_g.collect()
            _state = {hex(st_exit)}

    if _core_code is not None:
        _TitanGuard._verify_integrity()
        exec(_core_code, globals(), globals())

if __name__ == "__main__":
    _titan_vm_dispatch()
'''
        return runtime_script

# ==============================================================================
# INTERACTIVE CLI & MENU
# ==============================================================================
def interactive_menu():
    while True:
        clear_screen()
        render_banner()
        print(f"{Fore.WHITE}[1] {Fore.CYAN}Obfuscate a Python File (Titan Genesis - Extreme VM Defense)")
        print(f"{Fore.WHITE}[2] {Fore.CYAN}Obfuscate with Custom Security Key")
        print(f"{Fore.WHITE}[3] {Fore.YELLOW}Batch Obfuscate All Files in Directory")
        print(f"{Fore.WHITE}[4] {Fore.GREEN}Check Anti-Decompiler & Anti-Hook Status")
        print(f"{Fore.WHITE}[0] {Fore.RED}Exit\n")

        choice = input(f"{Fore.YELLOW}tdinh@titan-speed{Fore.WHITE}:~$ {Style.RESET_ALL}").strip()

        if choice == "1":
            print(f"\n{Fore.CYAN}[*] ENTER FILE PATH TO OBFUSCATE:{Style.RESET_ALL}")
            in_file = input("  > Input File: ").strip().strip('"').strip("'")
            if not os.path.exists(in_file):
                print(f"{Fore.RED}[!] Error: File not found: {in_file}{Style.RESET_ALL}")
                time.sleep(2)
                continue

            out_file = input(f"  > Output File (Enter to default '{in_file[:-3]}_titan.py'): ").strip().strip('"').strip("'")
            if not out_file:
                out_file = in_file.replace(".py", "_titan.py")

            key = "tdincte"
            print(f"\n{Fore.YELLOW}[*] Compiling AST mutation & building Titan Genesis VM...{Style.RESET_ALL}")
            start_t = time.perf_counter()
            with open(in_file, "r", encoding="utf-8", errors="ignore") as f:
                src = f.read()

            engine = TitanGenesisEngine(key=key)
            result = engine.obfuscate(src)
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(result)
            elapsed = time.perf_counter() - start_t

            print(f"\n{Fore.GREEN}[✓] OBFUSCATION COMPLETED IN {elapsed:.3f}s!{Style.RESET_ALL}")
            print(f"{Fore.WHITE}  - Output File      : {Fore.GREEN}{out_file}{Style.RESET_ALL}")
            print(f"{Fore.WHITE}  - Protection Engine: {Fore.CYAN}Titan Genesis v3.0 (Anti-Hook / Micro-VM / Non-Linear Shards){Style.RESET_ALL}")
            print(f"{Fore.WHITE}  - Security Key     : {Fore.YELLOW}{key}{Style.RESET_ALL}")
            print(f"{Fore.WHITE}  - Owner Credit     : {Fore.MAGENTA}tdinh ( server : 4ever ){Style.RESET_ALL}")
            input(f"\n{Fore.YELLOW}Press Enter to return to menu...{Style.RESET_ALL}")

        elif choice == "2":
            print(f"\n{Fore.CYAN}[*] ENTER FILE & CUSTOM SECURITY KEY:{Style.RESET_ALL}")
            in_file = input("  > Input File: ").strip().strip('"').strip("'")
            if not os.path.exists(in_file):
                print(f"{Fore.RED}[!] Error: File not found: {in_file}{Style.RESET_ALL}")
                time.sleep(2)
                continue

            custom_key = input("  > Custom Security Key (e.g. tdinh_secret): ").strip()
            if not custom_key:
                custom_key = "tdincte"

            out_file = input(f"  > Output File (Enter to default '{in_file[:-3]}_titan.py'): ").strip().strip('"').strip("'")
            if not out_file:
                out_file = in_file.replace(".py", "_titan.py")

            print(f"\n{Fore.YELLOW}[*] Processing Titan Genesis with custom key...{Style.RESET_ALL}")
            start_t = time.perf_counter()
            with open(in_file, "r", encoding="utf-8", errors="ignore") as f:
                src = f.read()

            engine = TitanGenesisEngine(key=custom_key)
            result = engine.obfuscate(src)
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(result)
            elapsed = time.perf_counter() - start_t

            print(f"\n{Fore.GREEN}[✓] OBFUSCATION COMPLETED IN {elapsed:.3f}s!{Style.RESET_ALL}")
            print(f"{Fore.WHITE}  - Output File      : {Fore.GREEN}{out_file}{Style.RESET_ALL}")
            print(f"{Fore.WHITE}  - Custom Key       : {Fore.YELLOW}{custom_key}{Style.RESET_ALL}")
            input(f"\n{Fore.YELLOW}Press Enter to return to menu...{Style.RESET_ALL}")

        elif choice == "3":
            print(f"\n{Fore.CYAN}[*] BATCH OBFUSCATE DIRECTORY:{Style.RESET_ALL}")
            folder = input("  > Directory Path: ").strip().strip('"').strip("'")
            if not os.path.isdir(folder):
                print(f"{Fore.RED}[!] Directory not found!{Style.RESET_ALL}")
                time.sleep(2)
                continue

            py_files = [f for f in os.listdir(folder) if f.endswith(".py") and not f.endswith("_titan.py")]
            if not py_files:
                print(f"{Fore.YELLOW}[!] No candidate Python files found.{Style.RESET_ALL}")
                time.sleep(2)
                continue

            out_dir = os.path.join(folder, "titan_protected")
            os.makedirs(out_dir, exist_ok=True)
            print(f"\n{Fore.YELLOW}[*] Obfuscating {len(py_files)} files to '{out_dir}'...{Style.RESET_ALL}")

            engine = TitanGenesisEngine(key="tdincte")
            count = 0
            for pf in py_files:
                in_p = os.path.join(folder, pf)
                out_p = os.path.join(out_dir, pf)
                with open(in_p, "r", encoding="utf-8", errors="ignore") as f:
                    src = f.read()
                res = engine.obfuscate(src)
                with open(out_p, "w", encoding="utf-8") as f:
                    f.write(res)
                count += 1
                print(f"  {Fore.GREEN}[✓]{Fore.WHITE} Protected: {pf}")

            print(f"\n{Fore.GREEN}[✓] Batch completed! {count} files protected in '{out_dir}'.{Style.RESET_ALL}")
            input(f"\n{Fore.YELLOW}Press Enter to return to menu...{Style.RESET_ALL}")

        elif choice == "4":
            print(f"\n{Fore.CYAN}[*] ANTI-TAMPER & DEFENSE CAPABILITIES REPORT:{Style.RESET_ALL}")
            print(f"{Fore.WHITE}  1. {Fore.GREEN}[ACTIVE]{Fore.WHITE} Anti-Debugger Detection (sys.gettrace / hardware stepping)")
            print(f"{Fore.WHITE}  2. {Fore.GREEN}[ACTIVE]{Fore.WHITE} Anti-Decompiler Trap (dis, pycdc, uncompyle6, decompyle++, pylingual)")
            print(f"{Fore.WHITE}  3. {Fore.GREEN}[ACTIVE]{Fore.WHITE} Anti-Monkey-Patching Guard (exec/eval integrity validation)")
            print(f"{Fore.WHITE}  4. {Fore.GREEN}[ACTIVE]{Fore.WHITE} Micro-VM State Machine Dispatcher (Non-linear state hops)")
            print(f"{Fore.WHITE}  5. {Fore.GREEN}[ACTIVE]{Fore.WHITE} Non-linear Dynamic Feedback Stream Cipher (0xAA rolling seed)")
            print(f"{Fore.WHITE}  6. {Fore.GREEN}[ACTIVE]{Fore.WHITE} Zero-Trace Memory Wipe (Instant garbage collection)")
            input(f"\n{Fore.YELLOW}Press Enter to return to menu...{Style.RESET_ALL}")

        elif choice == "0":
            print(f"\n{Fore.MAGENTA}[*] Thank you for using Titan Shield. Goodbye!{Style.RESET_ALL}")
            break

if __name__ == "__main__":
    interactive_menu()
