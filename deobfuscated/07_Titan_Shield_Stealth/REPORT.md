# 🛡️ Deobfuscation Report: Titan Shield & Titan Stealth

## 📌 1. Executive Summary
- **Target Files:** `titan_shield.py`, `titan_shield_titan_stealth.py`
- **Output File:** `output/titan_shield_deobfuscated.py`
- **Family:** Titan Shield VM Obfuscator
- **Status:** **Fully Deobfuscated & Verified**

---

## 🔍 2. Obfuscation Architecture
- **Virtual Stack Machine:** Replaces Python standard control flow with bytecode handlers and an internal stack frame.
- **Stealth Injection:** Hooks system exception handlers and environment variables to detect virtualized analysis environments.
- **Constant Encryption:** Encrypts strings and numerical literals using multi-stage XOR and byte rotation.

---

## 🛠️ 3. Deobfuscation
1. Extracted raw payload from virtual dispatch loop.
2. Recovered original function definitions and control flow.
3. Cleaned and structured the resulting Python code into `titan_shield_deobfuscated.py`.
