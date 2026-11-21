# 🛡️ Deobfuscation Report: Browser Extension Content Script

## 📌 1. Executive Summary
- **Target File:** `input/content.js`
- **Output File:** `output/content_deobfuscated.js`
- **Language / Runtime:** JavaScript (Chrome Extension Manifest v3 Content Script)
- **Status:** **100% Deobfuscated & Cleaned**

---

## 🔍 2. Obfuscation Techniques
- **Hex Encoded Strings & Array Shuffling:** Strings stored in a global array mutated via self-executing rotation functions.
- **Member Expression Obfuscation:** Standard DOM and fetch calls replaced with computed property names (`window['_0x...']`).
- **Control-Flow Flattening:** Loops and branching dispatch via switch-case sequences.

---

## 🛠️ 3. Deobfuscation Methodology
1. Evaluated string array rotation statically to recover plaintext string literals.
2. Normalized computed member expressions (`obj['key']` -> `obj.key`).
3. Reconstructed async/await flow and formatted readable code.
