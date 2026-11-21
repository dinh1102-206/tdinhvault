# -*- coding: utf-8 -*-
"""
================================================================================
          OBSIDIAN OBFUSCATOR v2.5 - FULL DECOMPILED & RESTORED SOURCE CODE
================================================================================
Original Authors: TheSmartCat & Mano
Repository: https://github.com/Thesmartcat2303/ObsidianObfuscator/
Reverse Engineered, Decompiled & Restored by: TDINH
Compatible: Python 3.10 - Python 3.14+
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

# ══════════════════════════════════════════════════════════════════════════════
#  ASSETS & TERMINAL UI (GRADIENT, BANNER, SPINNER)
# ══════════════════════════════════════════════════════════════════════════════
BANNER_ART = r"""
   ___  _         _     _ _             
  / _ \| |__  ___(_) __| (_) __ _ _ __  
 | | | | '_ \/ __| |/ _` | |/ _` | '_ \ 
 | |_| | |_) \__ \ | (_| | | (_| | | | |
  \___/|_.__/|___/_|\__,_|_|\__,_|_| |_|
        [ Obsidian Obfuscator v2.5 ]
"""

JAPANESE_CHARS = [
    'あ', 'い', 'う', 'え', 'お', 'か', 'き', 'く', 'け', 'こ',
    'さ', 'し', 'す', 'せ', 'そ', 'た', 'ち', 'つ', 'て', 'と',
    'な', 'に', 'ぬ', 'ね', 'の', 'は', 'ひ', 'ふ', 'へ', 'ほ',
    'ま', 'み', 'む', 'め', 'も', 'や', 'ゆ', 'よ', 'ら', 'り',
    'る', 'れ', 'ろ', 'わ', 'ゐ', 'ゑ', 'を', 'ん', 'ゔ', 'が',
    'ぎ', 'ぐ', 'げ', 'ご', 'ざ', 'じ', 'ず', 'ぜ', 'ぞ', 'だ',
    'ぢ', 'づ', 'で', 'ど', 'ば', 'び', 'ぶ', 'べ', 'ぼ', 'ぱ',
    'ぴ', 'ぷ', 'ぺ', 'ぽ', 'ぁ', 'ぃ', 'ぅ', 'ぇ', 'ぉ', 'っ',
    'ゃ', 'ゅ', 'ょ', 'ゎ'
]

def gradient(text: str, start_rgb=(124, 58, 237), end_rgb=(192, 132, 252)) -> str:
    """Applies a smooth linear gradient across the text."""
    lines = text.splitlines()
    out = []
    n = max(1, len(lines))
    for i, line in enumerate(lines):
        t = i / n
        r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * t)
        g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * t)
        b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * t)
        out.append(f"\033[38;2;{r};{g};{b}m{line}\033[0m")
    return "\n".join(out)

def spinner(text: str = "Processing...", duration: float = 1.0):
    chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    start = time.time()
    idx = 0
    while time.time() - start < duration:
        sys.stdout.write(f"\r  \033[35m{chars[idx % len(chars)]}\033[0m {text}")
        sys.stdout.flush()
        idx += 1
        time.sleep(0.08)
    sys.stdout.write("\r" + " " * (len(text) + 10) + "\r")
    sys.stdout.flush()

# ══════════════════════════════════════════════════════════════════════════════
#  OBSIDIAN CORE ENGINE (THE PYCLOAK / OBFUSCATION CORE)
# ══════════════════════════════════════════════════════════════════════════════
class ObsidianCore:
    def __init__(self):
        pass

    def randomlambda(self, length: int = 20) -> str:
        """Generates random Japanese Hiragana identifier names."""
        return ''.join(random.choice(JAPANESE_CHARS) for _ in range(length))

    def int_encode(self, num: int) -> str:
        """
        Encodes an integer into an anonymous XOR lambda expression:
        (lambda arg: arg ^ K)(value) where value = num ^ K.
        """
        xor_const = random.randint(10, 15)
        value = num ^ xor_const
        lambda_name = self.randomlambda(12)
        return f"(lambda {lambda_name} : {lambda_name} ^ {xor_const})({value})"

    def barray_encode(self, string_data: str) -> str:
        """
        Converts a UTF-8 string into an array of byte-wise lambda XOR evaluations:
        bytes([(lambda arg: arg ^ K)(V), ...]).decode('utf-8')
        """
        utf8_bytes = string_data.encode('utf-8')
        encoded_items = [self.int_encode(b) for b in utf8_bytes]
        return f'bytes([{", ".join(encoded_items)}]).decode("utf-8")'

    def ast_to_code(self, node: ast.AST) -> str:
        """Converts an AST tree back to formatted Python source code."""
        return ast.unparse(node)

# ══════════════════════════════════════════════════════════════════════════════
#  AST TRANSFORMERS
# ══════════════════════════════════════════════════════════════════════════════
class ReplaceIntegers(ast.NodeTransformer):
    """
    Transforms integer literals into bitwise arithmetic calculations:
    val -> (val ^ k) ^ k
    """
    def visit_Constant(self, node):
        if isinstance(node.value, int) and not isinstance(node.value, bool):
            val = node.value
            if 0 <= val < 10000:
                k = random.randint(1, 255)
                new_node = ast.BinOp(
                    left=ast.Constant(value=val ^ k),
                    op=ast.BitXor(),
                    right=ast.Constant(value=k)
                )
                return ast.copy_location(new_node, node)
        return node

class VariableToGlobalsTransformer(ast.NodeTransformer):
    """
    Transforms bare variable lookups into explicit globals() indexing.
    """
    def __init__(self):
        self.exclude = {'print', 'range', 'len', 'int', 'str', 'bytes', 'dict', 'list', 'open', 'exit'}

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load) and node.id not in self.exclude and not node.id.startswith('__'):
            # Convert to: globals().get('var_name', var_name)
            new_node = ast.Call(
                func=ast.Attribute(
                    value=ast.Call(func=ast.Name(id='globals', ctx=ast.Load()), args=[], keywords=[]),
                    attr='get',
                    ctx=ast.Load()
                ),
                args=[ast.Constant(value=node.id), ast.Name(id=node.id, ctx=ast.Load())],
                keywords=[]
            )
            return ast.copy_location(new_node, node)
        return node

# ══════════════════════════════════════════════════════════════════════════════
#  MAIN OBFUSCATOR GENERATOR (THE FULL PIPELINE)
# ══════════════════════════════════════════════════════════════════════════════
def obf(source_code: str, target_py_ver: str = "3.14") -> str:
    """
    Compiles source code, applies Obsidian AST passes, and wraps it inside
    the Minecraft-themed self-decrypting runtime environment.
    """
    core = ObsidianCore()

    # Pass 1: AST Transformations
    try:
        tree = ast.parse(source_code)
        tree = ReplaceIntegers().visit(tree)
        ast.fix_missing_locations(tree)
        transformed_code = core.ast_to_code(tree)
    except Exception:
        transformed_code = source_code

    # Pass 2: Bytecode Compilation
    compiled_code = compile(transformed_code, '<Obsidian_Protected>', 'exec')
    marshaled_bytes = marshal.dumps(compiled_code)

    # Pass 3: Multi-Layer Compression (User Payload)
    # Pipeline: lzma -> zlib -> bz2 -> base64 a85
    c_lzma = lzma.compress(marshaled_bytes)
    c_zlib = zlib.compress(c_lzma)
    c_bz2 = bz2.compress(c_zlib)
    c_a85 = base64.a85encode(c_bz2)

    # Pass 4: Inner Runtime Script (Layer 1)
    layer1_code = f"""# Obsidian Protected Runtime
__OBSIDIAN__['exec'](__OBSIDIAN__['__import__']("marshal").loads(__OBSIDIAN__['__import__']("lzma").decompress(__OBSIDIAN__['__import__']("zlib").decompress(__OBSIDIAN__['__import__']('bz2').decompress(__OBSIDIAN__['__import__']('base64').a85decode({repr(c_a85)}))))))
"""

    # Pass 5: Multi-Layer Compression (Layer 1)
    l1_marshaled = marshal.dumps(layer1_code)
    l1_lzma = lzma.compress(l1_marshaled)
    l1_zlib = zlib.compress(l1_lzma)
    l1_bz2 = bz2.compress(l1_zlib)
    l1_b85 = base64.b85encode(l1_bz2)

    # Pass 6: Generate Minecraft Structure Variables
    var_exec = core.randomlambda(25)
    var_globals = core.randomlambda(25)
    var_builtins = core.randomlambda(25)
    var_obsidian = core.randomlambda(25)
    var_arg = core.randomlambda(30)

    # Pass 7: Encrypt All Sensitive Strings via XOR Lambdas
    s_globals = core.barray_encode("globals")
    s_builtins = core.barray_encode("__builtins__")
    s_obsidian = core.barray_encode("__OBSIDIAN__")
    s_vars = core.barray_encode("vars")
    s_exec = core.barray_encode("exec")
    s_import = core.barray_encode("__import__")
    s_marshal = core.barray_encode("marshal")
    s_lzma = core.barray_encode("lzma")
    s_zlib = core.barray_encode("zlib")
    s_bz2 = core.barray_encode("bz2")
    s_b85 = core.barray_encode("base64")
    s_dummy_arg = core.barray_encode(core.randomlambda(16))

    # Pass 8: Assemble Final Obfuscated Script
    final_output = f"""#!/bin/python3
# -*- coding: utf-8 -*-
__OBFUSCATOR__ = ('ObsidianV2.5')[(lambda : 0)()]
__OWNER__ = "TheSmartCat & Mano"
__USER__ = "Thesmartcat2303 - Main - Requests Protected"
__PYTHON__ = "{target_py_ver}"
__WARNING__ = {{
    "_VN_": '''Obfuscator này được tạo ra để bảo vệ code, tuy nhiên nó cũng có thể bị lợi dụng để che giấu mã độc, botnet, keylogger, v.v. Hãy thận trọng khi chạy. Owner sẽ không chịu trách nhiệm!''',
    "_EN_": '''This obfuscator is made to protect code, so it may also be abused to hide malware, botnets, keyloggers, etc. Please be cautious when running it. The owner will not be responsible!'''
}}

# Obfuscated by Obsidian : https://github.com/Thesmartcat2303/ObsidianObfuscator/
# Facebook : https://www.facebook.com/Thesmartcat.2303/

class UserᅠThesmartcat2303:
    def __init__(self, {var_arg}):
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
        globals()['{var_globals}'] = eval({s_globals})
        globals()['{var_builtins}'] = eval({s_builtins})
        globals()['{var_obsidian}'] = {s_obsidian}
        try:
            globals()['{var_globals}']()[globals()['{var_obsidian}']] = eval({s_vars})(globals()['{var_builtins}'])
        except:
            globals()['{var_globals}']()[globals()['{var_obsidian}']] = globals()['{var_builtins}']
        _O = globals()['{var_globals}']()[globals()['{var_obsidian}']]
        _O['{var_exec}'] = _O[{s_exec}]
        _O['Github'] = {{
            'https://github.com/Thesmartcat2303/ObsidianObfuscator/': lambda c: _O[{s_import}]({s_marshal}).loads(
                _O[{s_import}]({s_lzma}).decompress(
                    _O[{s_import}]({s_zlib}).decompress(
                        _O[{s_import}]({s_bz2}).decompress(
                            _O[{s_import}]({s_b85}).b85decode(c)
                        )
                    )
                )
            )
        }}

SuperProtectorᅠ().TheSmartCat({s_dummy_arg})
try:
    __OBSIDIAN__['{var_exec}'](__OBSIDIAN__['Github']['https://github.com/Thesmartcat2303/ObsidianObfuscator/']({repr(l1_b85)}))
except Exception as code:
    print(code)
except KeyboardInterrupt:
    exit('>> Exiting...')
"""
    return final_output

# ══════════════════════════════════════════════════════════════════════════════
#  CLI INTERFACE
# ══════════════════════════════════════════════════════════════════════════════
def main():
    parser = argparse.ArgumentParser(description="Obsidian Obfuscator v2.5 - Full Restored Engine")
    parser.add_argument("input", help="Đường dẫn file Python cần làm mờ (Input file)")
    parser.add_argument("-o", "--output", help="Đường dẫn file sau khi làm mờ (Output file)", default=None)
    parser.add_argument("--py", help="Phiên bản Python mục tiêu", default="3.14")

    args = parser.parse_args()

    print(gradient(BANNER_ART))

    if not os.path.exists(args.input):
        print(f"[-] Không tìm thấy file: {args.input}")
        return

    out_file = args.output or (os.path.splitext(args.input)[0] + "_obsidian_obf.py")

    with open(args.input, 'r', encoding='utf-8', errors='ignore') as f:
        src = f.read()

    print(f"[*] Bắt đầu làm mờ file '{args.input}' ({len(src):,} bytes) cho Python {args.py}...")
    spinner("Đang áp dụng biến đổi AST & mã hóa chuỗi lambda...", duration=0.8)
    spinner("Đang nén đa tầng (LZMA + ZLIB + BZ2 + Base85)...", duration=0.6)

    t0 = time.time()
    result = obf(src, target_py_ver=args.py)

    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(result)

    print(f"\n[+] Hoàn thành xuất sắc trong {time.time()-t0:.2f}s!")
    print(f"[✔] File mã hóa: {out_file} ({len(result):,} bytes)")

if __name__ == '__main__':
    main()
