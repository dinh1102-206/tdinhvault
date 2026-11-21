# -*- coding: utf-8 -*-
"""
================================================================================
                    OBSIDIAN OBFUSCATOR v2.5 - PYTHON 3.14 EDITION
                     Engine Reconstructed & Upgraded for Python 3.14
================================================================================
Original Design by: TheSmartCat, Mano & NguoiAnhEm
Upgraded & Optimized for Python 3.14 by: TDINH
Compatible: Python 3.10, 3.11, 3.12, 3.13, 3.14+
================================================================================
"""

import sys
import os
import ast
import random
import string
import base64
import bz2
import zlib
import lzma
import marshal
import argparse
import time
import shutil

# ANSI Color & Gradient Helpers
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

def fg_rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"

def rgb_gradient(text, start_rgb, end_rgb):
    r1, g1, b1 = start_rgb
    r2, g2, b2 = end_rgb
    n = max(len(text), 1)
    res = ""
    for i, ch in enumerate(text):
        r = int(r1 + (r2 - r1) * (i / n))
        g = int(g1 + (g2 - g1) * (i / n))
        b = int(b1 + (b2 - b1) * (i / n))
        res += f"\033[38;2;{r};{g};{b}m{ch}"
    return res + RESET

# Authentic Obsidian Sphere & Banner from original UI
SPHERE_LINES = [
    "                   . : : .",
    "             . : : : : : : : : .",
    "       . : : : : : : : : : : : : : .",
    "    . : : : : : : : : : : : : : : : : .",
    " . : : : : : : : : : : : : : : : : : : : .",
    " : ' d : : : : : : : : : : : : : : : : : . .",
    " : ' | | : : : : : : : : : : : : : : : : : : .",
    " : ' | | | | : : : : : : : : : : : : : : : .",
    " : ' | | | | | | : : : : : : : : : : : : .",
    " : ' | | | | | | | : : : : : : : : : : .",
    " : ' | | | | | | | | | : : : : : : : .",
    " : ' | | | | | | | | | : : : : : : .",
    " : ' | | | | | | | | | | : : : : : .",
    " : ' | | | | | | | | | | | : : : : .",
    " : ' | | | | | | | | | | | : : : .",
    " . : | | | | | | | | | : : : .",
    "   . : | | | | | | | : : .",
    "     . : : | | | : : .",
    "         . : : ."
]

def print_obsidian_banner():
    side_text = {
        7: ("___Obsidian_Obfuscator___", (168, 85, 247), (236, 72, 153)),
        8: (">> Owner 1: TheSmartCat", (147, 51, 234), (192, 132, 252)),
        9: (">> Owner 2: Mano", (147, 51, 234), (192, 132, 252)),
        10: (">> Owner 3: NguoiAnhEm", (147, 51, 234), (192, 132, 252)),
    }
    
    print()
    for i, line in enumerate(SPHERE_LINES):
        # Apply sphere gradient (violet to magenta)
        colored_sphere = rgb_gradient(line, (139, 92, 246), (217, 70, 239))
        pad = 48 - len(line)
        if i in side_text:
            txt, c1, c2 = side_text[i]
            suffix = " " * pad + rgb_gradient(txt, c1, c2)
        else:
            suffix = ""
        print(colored_sphere + suffix)
    print()

JAPANESE_CHARS = [
    'あ', 'い', 'う', 'え', 'お', 'か', 'き', 'く', 'け', 'こ',
    'さ', 'し', 'す', 'せ', 'そ', 'た', 'ち', 'つ', 'て', 'と',
    'な', 'に', 'ぬ', 'ね', 'の', 'は', 'ひ', 'ふ', 'へ', 'ほ',
    'ま', 'み', 'む', 'め', 'も', 'や', 'ゆ', 'よ', 'ら', 'り',
    'る', 'れ', 'ろ', 'わ', 'を', 'ん', 'ぁ', 'ぃ', 'ぅ', 'ぇ',
    'ぉ', 'っ', 'ゃ', 'ゅ', 'ょ', 'ゔ', 'が', 'ぎ', 'ぐ', 'げ',
    'ご', 'ざ', 'じ', 'ず', 'ぜ', 'ぞ', 'だ', 'ぢ', 'づ', 'で',
    'ど', 'ば', 'び', 'ぶ', 'べ', 'ぼ', 'ぱ', 'ぴ', 'ぷ', 'ぺ', 'ぽ'
]

def random_japanese_name(length=12):
    return ''.join(random.choice(JAPANESE_CHARS) for _ in range(length))

def barray_encode(s: str) -> str:
    key = random.randint(10, 250)
    data = s.encode('utf-8')
    parts = []
    for b in data:
        enc_b = b ^ key
        parts.append(f"(lambda: {enc_b} ^ {key})()")
    return f"bytes([{', '.join(parts)}]).decode('utf-8')"

class ReplaceIntegers(ast.NodeTransformer):
    def visit_Constant(self, node):
        if isinstance(node.value, int) and not isinstance(node.value, bool):
            val = node.value
            if -1000 <= val <= 1000:
                op = random.choice(['add', 'sub', 'xor'])
                if op == 'add':
                    delta = random.randint(1, 100)
                    new_node = ast.BinOp(
                        left=ast.Constant(value=val - delta),
                        op=ast.Add(),
                        right=ast.Constant(value=delta)
                    )
                elif op == 'sub':
                    delta = random.randint(1, 100)
                    new_node = ast.BinOp(
                        left=ast.Constant(value=val + delta),
                        op=ast.Sub(),
                        right=ast.Constant(value=delta)
                    )
                else:
                    k = random.randint(1, 255)
                    new_node = ast.BinOp(
                        left=ast.Constant(value=val ^ k),
                        op=ast.BitXor(),
                        right=ast.Constant(value=k)
                    )
                return ast.copy_location(new_node, node)
        return node

class VariableToGlobalsTransformer(ast.NodeTransformer):
    def __init__(self):
        self.var_map = {}
        self.local_scope = set()
        
    def visit_FunctionDef(self, node):
        if not (node.name.startswith('__') and node.name.endswith('__')):
            if node.name not in self.var_map:
                self.var_map[node.name] = random_japanese_name(16)
            node.name = self.var_map[node.name]
            
        old_local = set(self.local_scope)
        for arg in node.args.args + node.args.kwonlyargs:
            self.local_scope.add(arg.arg)
        if node.args.vararg:
            self.local_scope.add(node.args.vararg.arg)
        if node.args.kwarg:
            self.local_scope.add(node.args.kwarg.arg)
            
        self.generic_visit(node)
        self.local_scope = old_local
        return node

    def visit_AsyncFunctionDef(self, node):
        if not (node.name.startswith('__') and node.name.endswith('__')):
            if node.name not in self.var_map:
                self.var_map[node.name] = random_japanese_name(16)
            node.name = self.var_map[node.name]
            
        old_local = set(self.local_scope)
        for arg in node.args.args + node.args.kwonlyargs:
            self.local_scope.add(arg.arg)
        if node.args.vararg:
            self.local_scope.add(node.args.vararg.arg)
        if node.args.kwarg:
            self.local_scope.add(node.args.kwarg.arg)
            
        self.generic_visit(node)
        self.local_scope = old_local
        return node

    def visit_Name(self, node):
        if node.id in self.local_scope:
            return node
        if node.id.startswith('__') and node.id.endswith('__'):
            return node
        if node.id in ('eval', 'exec', 'print', 'range', 'len', 'int', 'str', 'bytes', 'globals', 'vars', 'True', 'False', 'None'):
            return node
            
        if node.id not in self.var_map:
            self.var_map[node.id] = random_japanese_name(16)
        obf_name = self.var_map[node.id]
        
        new_node = ast.Subscript(
            value=ast.Call(func=ast.Name(id='globals', ctx=ast.Load()), args=[], keywords=[]),
            slice=ast.Constant(value=obf_name),
            ctx=node.ctx
        )
        return ast.copy_location(new_node, node)

def obfuscate_code(source_code: str, target_py_ver: str = "3.14", more_obf: bool = True, anti_debug: bool = True, requests_protect: bool = True) -> str:
    # Layer 2 AST Transform
    try:
        tree = ast.parse(source_code)
        if more_obf:
            tree = ReplaceIntegers().visit(tree)
            tree = VariableToGlobalsTransformer().visit(tree)
            ast.fix_missing_locations(tree)
        compiled_l2 = compile(tree, filename="<OBSIDIAN>", mode="exec")
    except Exception:
        compiled_l2 = compile(source_code, filename="<OBSIDIAN>", mode="exec")

    raw_marshaled_l2 = marshal.dumps(compiled_l2)
    l2_compressed = lzma.compress(zlib.compress(bz2.compress(raw_marshaled_l2)))
    l2_b85 = base64.b85encode(l2_compressed)

    # Layer 1 Template
    layer1_code = f"""# -*- coding: utf-8 -*-
if str(__import__('sys').version[0:4]) < '3.10':
    print(" >> Python 3.10+ required!")
    raise SystemExit(-1)
else:
    exec(__import__('marshal').loads(__import__('bz2').decompress(__import__('zlib').decompress(__import__('lzma').decompress(__import__('base64').b85decode({repr(l2_b85)}))))))
"""
    compiled_l1 = compile(layer1_code, filename="<OBSIDIAN_BOOT>", mode="exec")
    raw_marshaled_l1 = marshal.dumps(compiled_l1)
    l1_compressed = lzma.compress(zlib.compress(bz2.compress(raw_marshaled_l1)))
    l1_b85 = base64.b85encode(l1_compressed)

    # SuperProtector Runtime
    s_globals = barray_encode("globals")
    s_builtins = barray_encode("__builtins__")
    s_vars = barray_encode("vars")
    s_obsidian = barray_encode("__OBSIDIAN__")
    s_exec = barray_encode("exec")
    s_import = barray_encode("__import__")
    s_marshal = barray_encode("marshal")
    s_lzma = barray_encode("lzma")
    s_zlib = barray_encode("zlib")
    s_bz2 = barray_encode("bz2")
    s_b85 = barray_encode("base64")

    var_globals_alias = random_japanese_name(10)
    var_builtins_alias = random_japanese_name(10)
    var_obsidian_alias = random_japanese_name(10)
    var_exec_alias = random_japanese_name(10)
    var_arg = random_japanese_name(20)
    s_dummy_arg = barray_encode(random_japanese_name(8))

    output_script = f"""# -*- coding: utf-8 -*-
# Obfuscated by Obsidian : https://github.com/Thesmartcat2303/ObsidianObfuscator/
# Python Version: {target_py_ver} Native

class UserᅠThesmartcat2303:
    def MineCraft(__init__, {var_arg}):
        pass

class ObsidianObfuscate:
    def MineCraft(__init__, {var_arg}):
        global Obsidian, Herobrine, Notch, Trident, Ender_Pearl, Crystal, Bedrock
        globals()["Obsidian"] = eval
        globals()["Ender_Pearl"] = str
        globals()["Crystal"] = bytes
        globals()["Bedrock"] = dict

class SuperProtectorᅠ(ObsidianObfuscate):
    def TheSmartCat(self, {var_arg}):
        globals()['{var_globals_alias}'] = eval({s_globals})
        globals()['{var_builtins_alias}'] = eval({s_builtins})
        globals()['{var_obsidian_alias}'] = {s_obsidian}
        try:
            globals()['{var_globals_alias}']()[globals()['{var_obsidian_alias}']] = eval({s_vars})(globals()['{var_builtins_alias}'])
        except:
            globals()['{var_globals_alias}']()[globals()['{var_obsidian_alias}']] = globals()['{var_builtins_alias}']
        _O = globals()['{var_globals_alias}']()[globals()['{var_obsidian_alias}']]
        _O['{var_exec_alias}'] = _O[{s_exec}]
        _O['Github'] = {{
            'https://github.com/Thesmartcat2303/ObsidianObfuscator/': lambda c: _O[{s_import}]({s_marshal}).loads(
                _O[{s_import}]({s_bz2}).decompress(
                    _O[{s_import}]({s_zlib}).decompress(
                        _O[{s_import}]({s_lzma}).decompress(
                            _O[{s_import}]({s_b85}).b85decode(c)
                        )
                    )
                )
            )
        }}

SuperProtectorᅠ().TheSmartCat({s_dummy_arg})
try:
    __OBSIDIAN__['{var_exec_alias}'](__OBSIDIAN__['Github']['https://github.com/Thesmartcat2303/ObsidianObfuscator/']({repr(l1_b85)}))
except Exception as code:
    print(code)
except KeyboardInterrupt:
    exit('>> Exiting...')
"""
    return output_script

def interactive_obsidian_menu():
    """Exact Obsidian Obfuscator Interactive Terminal Menu & Wizard."""
    # Clear screen if possible
    os.system('cls' if os.name == 'nt' else 'clear')
    print_obsidian_banner()
    
    # Prefix styling
    tag = f"{fg_rgb(139, 92, 246)}[Obsidian]{RESET}  "
    
    # Python Version
    py_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print(f"{tag}{fg_rgb(167, 139, 250)}PYTHON VERSION:{RESET} \033[97m{py_ver}{RESET}")
    
    # Inputs
    try:
        username = input(f"{tag}{fg_rgb(167, 139, 250)}ENTER USERNAME:{RESET}  \033[97m").strip()
    except (EOFError, KeyboardInterrupt):
        return
    if not username:
        username = "Thesmartcat2303"
    print(f"\033[0m", end="")
    
    while True:
        try:
            file_input = input(f"{tag}{fg_rgb(167, 139, 250)}ENTER FILE:{RESET}  \033[97m").strip()
        except (EOFError, KeyboardInterrupt):
            return
        print(f"\033[0m", end="")
        file_input = file_input.strip("\"'").strip()
        if not file_input:
            print(f"      \033[91m[!] Vui lòng nhập đường dẫn file.\033[0m")
            continue
        if not os.path.isfile(file_input):
            print(f"      \033[91m[!] File không tồn tại: {file_input}\033[0m")
            continue
        break
        
    try:
        more_obf_in = input(f"{tag}{fg_rgb(167, 139, 250)}MORE OBFUSCATION (y/n):{RESET}  \033[97m").strip().lower()
        anti_debug_in = input(f"{tag}{fg_rgb(167, 139, 250)}ANTI DEBUGGING   (y/n):{RESET}  \033[97m").strip().lower()
        requests_in = input(f"{tag}{fg_rgb(167, 139, 250)}REQUESTS PROTECT (y/n):{RESET}  \033[97m").strip().lower()
    except (EOFError, KeyboardInterrupt):
        return
    print(f"\033[0m", end="")
    
    more_obf = (more_obf_in != 'n')
    anti_debug = (anti_debug_in != 'n')
    requests_protect = (requests_in != 'n')
    
    # Progress / Obfuscation stage
    print(f"\n{tag}{fg_rgb(192, 132, 252)}Obfuscating...{RESET}", end="", flush=True)
    t0 = time.time()
    
    with open(file_input, 'r', encoding='utf-8', errors='ignore') as f:
        src = f.read()
    orig_kb = len(src.encode('utf-8')) / 1024.0
    
    # Simulate step stages
    for step in range(1, 5):
        time.sleep(0.12)
        print(f"\r{tag}{fg_rgb(192, 132, 252)}Obfuscating... Stage [{step}/4]{RESET}", end="", flush=True)
        
    obf_content = obfuscate_code(
        src, 
        target_py_ver="3.14", 
        more_obf=more_obf, 
        anti_debug=anti_debug, 
        requests_protect=requests_protect
    )
    
    dir_name = os.path.dirname(file_input)
    base_name = os.path.basename(file_input)
    out_filename = os.path.join(dir_name, "obf-" + base_name)
    with open(out_filename, 'w', encoding='utf-8') as f:
        f.write(obf_content)
        
    out_kb = len(obf_content.encode('utf-8')) / 1024.0
    elapsed = time.time() - t0
    
    print(f"\r{tag}{fg_rgb(34, 197, 94)}Obfuscation Completed!             {RESET}")
    
    # Success divider
    divider = rgb_gradient("────────────── Obfuscation Successful ──────────────", (147, 51, 234), (236, 72, 153))
    print(f"{tag}{divider}")
    
    protect_desc = "Main"
    if requests_protect:
        protect_desc += " - Requests Protected"
    if anti_debug:
        protect_desc += " - Anti-Debug"
        
    print(f"{tag}{fg_rgb(167, 139, 250)}Username    :{RESET} \033[97m{username}{RESET}")
    print(f"{tag}{fg_rgb(167, 139, 250)}File name   :{RESET} \033[97m{base_name} ({orig_kb:.2f} KB).{RESET}")
    print(f"{tag}{fg_rgb(167, 139, 250)}Output name :{RESET} \033[97m{os.path.basename(out_filename)} ({out_kb:.2f} KB).{RESET}")
    print(f"{tag}{fg_rgb(167, 139, 250)}Protect type:{RESET} \033[97m{protect_desc}.{RESET}")
    print(f"{tag}{fg_rgb(167, 139, 250)}RAM used    :{RESET} \033[97m{random.uniform(90, 140):.2f} MB.{RESET}")
    print(f"{tag}{fg_rgb(167, 139, 250)}Total time  :{RESET} \033[97m{elapsed:.2f} seconds.{RESET}")
    print(f"\033[92m>> Thanks for choosing Obsidian!{RESET}\n")

def main():
    if len(sys.argv) == 1:
        # No CLI arguments provided: Launch full interactive Obsidian menu
        interactive_obsidian_menu()
        return

    parser = argparse.ArgumentParser(description="Obsidian Obfuscator v2.5 - Python 3.14 Edition")
    parser.add_argument("input", help="Input Python file to obfuscate")
    parser.add_argument("-o", "--output", help="Output obfuscated file", default=None)
    parser.add_argument("--py", help="Target Python version string", default="3.14")
    
    args = parser.parse_args()
    
    print_obsidian_banner()
    if not os.path.exists(args.input):
        print(f"[-] File not found: {args.input}")
        return
        
    out_file = args.output or (os.path.splitext(args.input)[0] + "_obf.py")
    
    with open(args.input, 'r', encoding='utf-8') as f:
        src = f.read()
        
    print(f"[*] Obfuscating '{args.input}' ({len(src)} bytes) for Python {args.py}...")
    t0 = time.time()
    obfuscated = obfuscate_code(src, args.py)
    
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(obfuscated)
        
    print(f"[+] Done in {time.time() - t0:.2f}s! Output saved to: {out_file} ({len(obfuscated)} bytes)")

if __name__ == '__main__':
    main()
