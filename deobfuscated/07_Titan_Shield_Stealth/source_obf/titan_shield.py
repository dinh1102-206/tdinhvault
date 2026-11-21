# -*- coding: utf-8 -*-
# ==============================================================================
# TOOL NAME   : TITAN-SHIELD OBFUSCATOR v5.0 (STEALTH MATRIX & STACK-VM)
# OWNER       : tdinh
# SERVER      : 4ever
# OBF MODE    : titan (Stealth Binary Stream, Transient Stack-VM, Zero-Trace)
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
import struct
import gc
from colorama import Fore, Style, init

init(autoreset=True)

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def render_banner():
    banner = f"""{Fore.CYAN}{Style.BRIGHT}
  ████████╗██╗████████╗ █████╗ ███╗   ██╗    ███████╗████████╗███████╗ █████╗ ██╗  ████████╗██╗  ██╗
  ╚══██╔══╝██║╚══██╔══╝██╔══██╗████╗  ██║    ██╔════╝╚══██╔══╝██╔════╝██╔══██╗██║  ╚══██╔══╝██║  ██║
     ██║   ██║   ██║   ███████║██╔██╗ ██║    ███████╗   ██║   █████╗  ███████║██║     ██║   ███████║
     ██║   ██║   ██║   ██╔══██║██║╚██╗██║    ╚════██║   ██║   ██╔══╝  ██╔══██║██║     ██║   ██╔══██║
     ██║   ██║   ██║   ██║  ██║██║ ╚████║    ███████║   ██║   ███████╗██║  ██║███████╗██║   ██║  ██║
     ╚═╝   ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝    ╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝   ╚═╝  ╚═╝
{Fore.YELLOW}             ═══[ >> TITAN STEALTH MATRIX ENGINE v5.0 - ZERO-TRACE VM << ]═══{Fore.WHITE}
                 - Owner      : {Fore.GREEN}tdinh{Fore.WHITE}
                 - Server     : {Fore.MAGENTA}4ever{Fore.WHITE}
                 - Obf Mode   : {Fore.RED}TITAN STEALTH (Dense Binary Stream & Forward-Hash Chain){Fore.WHITE}
"""
    print(banner)

# ==============================================================================
# LAYER 1: AST STRING & LITERAL OBFUSCATION
# ==============================================================================
class ASTStringScrambler(ast.NodeTransformer):
    def __init__(self):
        super().__init__()
        self.salt = random.randint(0x20, 0xEE)

    def visit_Constant(self, node):
        if isinstance(node.value, str) and len(node.value) >= 2:
            if node.value.startswith("__") and node.value.endswith("__"):
                return node
            key = (self.salt + len(node.value)) & 0xFF
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
# LAYER 2: TITAN STEALTH COMPILER (DENSE BINARY PACKING & FORWARD HASH)
# ==============================================================================
class TitanStealthCompiler:
    def __init__(self, master_key: str = "tdincte", max_chunk_stmts: int = 2):
        self.master_key = master_key.encode("utf-8")
        self.max_chunk_stmts = max_chunk_stmts

    def _mutate_ast(self, tree: ast.AST):
        try:
            scrambler = ASTStringScrambler()
            new_tree = scrambler.visit(tree)
            ast.fix_missing_locations(new_tree)
            return new_tree
        except Exception:
            return tree

    def compile(self, source_code: str) -> str:
        tree = ast.parse(source_code)
        mutated_tree = self._mutate_ast(tree)
        stmts = mutated_tree.body

        blocks = []
        current_block = []
        for stmt in stmts:
            current_block.append(stmt)
            if len(current_block) >= self.max_chunk_stmts or isinstance(stmt, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                blocks.append(current_block)
                current_block = []
        if current_block:
            blocks.append(current_block)

        # Dynamic polymorphic opcodes
        OP_EXEC = 0x4F
        OP_FLUSH = 0x52
        OP_HALT = 0xDE

        master_salt = os.urandom(32)
        running_key = hashlib.sha256(self.master_key + master_salt).digest()

        # DENSE BINARY PACKING (Eliminates obvious tuple lists & brackets)
        # Format per frame: [1 byte op][1 byte salt][4 bytes length][N bytes ciphertext]
        binary_stream = bytearray()

        for idx, blk in enumerate(blocks):
            sub_mod = ast.Module(body=blk, type_ignores=[])
            code_obj = compile(sub_mod, f"<titan-core-{idx}>", "exec")
            raw_marshaled = marshal.dumps(code_obj)
            compressed = zlib.compress(raw_marshaled, 9)

            b_salt = random.randint(1, 255)
            enc_bytes = bytearray()
            k_len = len(running_key)
            for i, b in enumerate(compressed):
                k = running_key[i % k_len] ^ b_salt
                enc_bytes.append(b ^ k)

            binary_stream.extend(struct.pack(">BBI", OP_EXEC, b_salt, len(enc_bytes)))
            binary_stream.extend(enc_bytes)

            running_key = hashlib.sha256(running_key + bytes([b_salt]) + raw_marshaled).digest()

            if idx % 8 == 0:
                binary_stream.extend(struct.pack(">BBI", OP_FLUSH, random.randint(1, 255), 0))

        binary_stream.extend(struct.pack(">BBI", OP_HALT, 0, 0))

        # Compress entire binary stream into a single dense opaque blob
        dense_blob_b64 = base64.b64encode(zlib.compress(binary_stream, 9)).decode("ascii")
        master_salt_b64 = base64.b64encode(master_salt).decode("ascii")
        master_key_b64 = base64.b64encode(self.master_key).decode("ascii")

        # Stealth Minimalist Runtime Template
        runtime_script = f'''# -*- coding: utf-8 -*-
__tdinh__ = __4ever__ = 1
__obf__    = __tdinh__
__in4mation = [ 
    "owner : tdinh",
    "obf mode : titan"
]

import sys as _I, zlib as _Z, marshal as _M, base64 as _B, hashlib as _H, struct as _S, gc as _G

if _I.gettrace() or any(m in _I.modules for m in ['dis','pycdc','uncompyle6','decompyle++','pylingual','inspect']): _I.exit(0)
_E = getattr(_I.modules.get('builtins'), 'exec', None)
if _E and (type(_E).__name__ != 'builtin_function_or_method' or hasattr(_E, '__code__')): _I.exit(0)

_K = "{master_key_b64}"
_T = "{master_salt_b64}"
_D = "{dense_blob_b64}"

def _titan_entry():
    global _K, _T, _D
    _k = _H.sha256(_B.b64decode(_K) + _B.b64decode(_T)).digest()
    _b = _Z.decompress(_B.b64decode(_D))
    _o, _l, _env, _ld = 0, len(_b), globals(), bytes([108,111,97,100,115]).decode()
    del _K, _T, _D
    while _o < _l:
        _op, _s, _sz = _S.unpack_from('>BBI', _b, _o); _o += 6
        if _op == 0xDE: break
        elif _op == 0x52: _G.collect()
        elif _op == 0x4F:
            _p = _b[_o:_o+_sz]; _o += _sz
            _kl = len(_k)
            _raw = _Z.decompress(bytes([x ^ _k[i % _kl] ^ _s for i, x in enumerate(_p)]))
            _k = _H.sha256(_k + bytes([_s]) + _raw).digest()
            exec(getattr(_M, _ld)(_raw), _env, _env)
            del _raw
    del _b; _G.collect()

if __name__ == "__main__":
    _titan_entry()
'''
        return runtime_script

# ==============================================================================
# INTERACTIVE CLI & MENU
# ==============================================================================
def interactive_menu():
    while True:
        clear_screen()
        render_banner()
        print(f"{Fore.WHITE}[1] {Fore.CYAN}Obfuscate File (Titan Stealth Matrix - Dense Binary Stream)")
        print(f"{Fore.WHITE}[2] {Fore.CYAN}Obfuscate with Custom Key")
        print(f"{Fore.WHITE}[3] {Fore.YELLOW}Batch Obfuscate Folder")
        print(f"{Fore.WHITE}[4] {Fore.GREEN}Check Stealth Matrix Security Architecture")
        print(f"{Fore.WHITE}[0] {Fore.RED}Exit\n")

        choice = input(f"{Fore.YELLOW}tdinh@titan-stealth{Fore.WHITE}:~$ {Style.RESET_ALL}").strip()

        if choice == "1":
            print(f"\n{Fore.CYAN}[*] ENTER FILE PATH TO OBFUSCATE:{Style.RESET_ALL}")
            in_file = input("  > Input File: ").strip().strip('"').strip("'")
            if not os.path.exists(in_file):
                print(f"{Fore.RED}[!] Error: File not found: {in_file}{Style.RESET_ALL}")
                time.sleep(2)
                continue

            out_file = input(f"  > Output File (Enter to default '{in_file[:-3]}_titan_stealth.py'): ").strip().strip('"').strip("'")
            if not out_file:
                out_file = in_file.replace(".py", "_titan_stealth.py")

            key = "tdincte"
            print(f"\n{Fore.YELLOW}[*] Packing into dense binary stream with forward secrecy...{Style.RESET_ALL}")
            start_t = time.perf_counter()
            with open(in_file, "r", encoding="utf-8", errors="ignore") as f:
                src = f.read()

            compiler = TitanStealthCompiler(master_key=key)
            result = compiler.compile(src)
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(result)
            elapsed = time.perf_counter() - start_t

            print(f"\n{Fore.GREEN}[✓] STEALTH OBFUSCATION COMPLETED IN {elapsed:.3f}s!{Style.RESET_ALL}")
            print(f"{Fore.WHITE}  - Output File      : {Fore.GREEN}{out_file}{Style.RESET_ALL}")
            print(f"{Fore.WHITE}  - Architecture     : {Fore.CYAN}Titan Stealth Matrix v5.0 (Dense Binary Blob + Forward Hash Ratchet){Style.RESET_ALL}")
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

            custom_key = input("  > Custom Security Key (default: tdincte): ").strip()
            if not custom_key:
                custom_key = "tdincte"

            out_file = input(f"  > Output File (Enter to default '{in_file[:-3]}_titan_stealth.py'): ").strip().strip('"').strip("'")
            if not out_file:
                out_file = in_file.replace(".py", "_titan_stealth.py")

            print(f"\n{Fore.YELLOW}[*] Compiling Titan Stealth Matrix...{Style.RESET_ALL}")
            start_t = time.perf_counter()
            with open(in_file, "r", encoding="utf-8", errors="ignore") as f:
                src = f.read()

            compiler = TitanStealthCompiler(master_key=custom_key)
            result = compiler.compile(src)
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

            py_files = [f for f in os.listdir(folder) if f.endswith(".py") and not f.endswith("_titan_stealth.py")]
            if not py_files:
                print(f"{Fore.YELLOW}[!] No candidate Python files found.{Style.RESET_ALL}")
                time.sleep(2)
                continue

            out_dir = os.path.join(folder, "titan_stealth_protected")
            os.makedirs(out_dir, exist_ok=True)
            print(f"\n{Fore.YELLOW}[*] Obfuscating {len(py_files)} files into Stealth Matrix...{Style.RESET_ALL}")

            compiler = TitanStealthCompiler(master_key="tdincte")
            count = 0
            for pf in py_files:
                in_p = os.path.join(folder, pf)
                out_p = os.path.join(out_dir, pf)
                with open(in_p, "r", encoding="utf-8", errors="ignore") as f:
                    src = f.read()
                res = compiler.compile(src)
                with open(out_p, "w", encoding="utf-8") as f:
                    f.write(res)
                count += 1
                print(f"  {Fore.GREEN}[✓]{Fore.WHITE} Protected: {pf}")

            print(f"\n{Fore.GREEN}[✓] Batch completed! {count} files protected in '{out_dir}'.{Style.RESET_ALL}")
            input(f"\n{Fore.YELLOW}Press Enter to return to menu...{Style.RESET_ALL}")

        elif choice == "4":
            print(f"\n{Fore.CYAN}[*] TITAN STEALTH MATRIX ARCHITECTURE:{Style.RESET_ALL}")
            print(f"{Fore.WHITE}  1. {Fore.GREEN}[ACTIVE]{Fore.WHITE} Dense Binary Stream Packing (Xóa bỏ hoàn toàn mảng tuple)")
            print(f"{Fore.WHITE}  2. {Fore.GREEN}[ACTIVE]{Fore.WHITE} No Whole-File Bytecode (Không có khối bytecode CPython chuẩn nào)")
            print(f"{Fore.WHITE}  3. {Fore.GREEN}[ACTIVE]{Fore.WHITE} Forward Secrecy Hash Ratchet (Key[N+1] = SHA256(Key[N] + Chunk[N]))")
            print(f"{Fore.WHITE}  4. {Fore.GREEN}[ACTIVE]{Fore.WHITE} Transient Execution & Immediate Memory Purge")
            print(f"{Fore.WHITE}  5. {Fore.GREEN}[ACTIVE]{Fore.WHITE} Compact Mangled Stealth Bootstrap Loader (Không lộ code logic)")
            input(f"\n{Fore.YELLOW}Press Enter to return to menu...{Style.RESET_ALL}")

        elif choice == "0":
            print(f"\n{Fore.MAGENTA}[*] Thank you for using Titan Stealth. Goodbye!{Style.RESET_ALL}")
            break

if __name__ == "__main__":
    interactive_menu()
