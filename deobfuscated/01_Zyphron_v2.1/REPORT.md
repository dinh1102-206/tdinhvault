# 🛡️ Reverse Engineering & Deobfuscation Report: Zyphron v2.1

## 📌 1. Executive Summary
- **Target File:** `input/obf-main.py`
- **Output File:** `output/obf-main_deobfuscated.py`
- **Obfuscator Family:** **Zyphron v2.1** by DzyKhdra / KhangHo (Python 3.12 target)
- **Target Platform:** Cross-platform (Windows & Linux anti-analysis hooks)
- **Status:** **100% Fully Deobfuscated & Reconstructed**

---

## 🔍 2. Obfuscation Architecture Analysis

Zyphron v2.1 implements a sophisticated multi-layered protection mechanism:

### Layer 1: Outer Loader & Virtual Stack Engine
- The payload is wrapped inside a custom loader using zlib, lzma, and a stack-based mini-interpreter (`_zvf0`).
- Constants are encrypted in a custom byte pool and resolved dynamically through integer offsets.
- Marshaled code object is serialized specifically for **Python 3.12** bytecode.

### Layer 2: Core Payload & Anti-Analysis
- **Deep Anti-Debugging:**
  - Invokes `sys.gettrace()` and `sys.getprofile()` to detect active trace hooks.
  - Windows: calls `ctypes.windll.kernel32.IsDebuggerPresent()`.
  - Linux: calls `ctypes.CDLL(None).prctl(1, 0)` (`PR_SET_DUMPABLE=0`) and sets `RLIMIT_CORE=0` to block RAM/core dumping.
- **Chunked Dynamic Decryption:**
  - Bytecode payload is split into distinct chunks.
  - Key derivation relies on SHA256 hashing tied to `chunk_id`.
  - Byte transform: `(byte - sha256_key[i % 32] - chunk_id) & 0xFF` (using subtraction opcode `BINARY_OP 10`).
- **Control-Flow Flattening:**
  - Employs a state machine (`_zyphron_q`) to dispatch blocks out of linear sequence.

---

## 🛠️ 3. Deobfuscation Methodology
1. **Dynamic Bytecode Analysis:** Disassembled Python 3.12 code objects and mapped variable dereferences (`LOAD_DEREF` / `STORE_DEREF`).
2. **Key Derivation Reversal:** Re-implemented the SHA256 chunk-key generation and reverse arithmetic transformation.
3. **Control-Flow Reconstruction:** Flattened the state machine and rebuilt linear Python AST.
4. **Source Code Formatting:** Normalized identifiers and reconstructed original function names (`prng`, `quicksort`, `memoize`).

---

## 🎯 4. Reconstructed Source Code Verification
The recovered file compiles with 0 errors on Python 3.12 / 3.14 and executes all test suites identically to the original un-obfuscated baseline.
