# 🛡️ Reverse Engineering & Deobfuscation Report: PyMeo v2

## 📌 1. Executive Summary
- **Target File:** `input/22222222.py`
- **Output Files:** `output/pymeov2_deobfuscated.py`, `output/odkjqwdid12.py`
- **Obfuscator Family:** **PyMeo v2** (PYMEOMEO OBF by NGOCUYENCODER)
- **Threat Type:** Discord Token Stealer / Automation / Webhook Logger
- **Status:** **100% Fully Unpacked & Neutralized**

---

## 🔍 2. Obfuscation Architecture Analysis
- **Multi-layer Packing:** Successive rounds of `base64`, `zlib`, and `marshal.loads()` embedded inside dynamic `exec()` wrappers.
- **Key Validation Bypass:** Contains an online licensing/key-check call to `https://sever.ngocbansub.com/keyencuyen/keyencuyen.php?key=...`.
- **Inner Payload:** An asynchronous Discord automation bot and credential grabber that exfiltrates system data, user tokens, and IP information to Discord Webhooks.

---

## 🚨 3. Extracted Indicators of Compromise (IoCs)
- **Author Profiles:**
  - Facebook: `https://www.facebook.com/datishnu1907`
  - Telegram: `https://t.me/huynhngocuyenn`
  - Zalo: `0335102378`
- **C2 & Key Server:**
  - `https://sever.ngocbansub.com/keyencuyen/`
- **Exfiltration Webhooks:** Neutralized and documented during analysis.

---

## 🛠️ 4. Deobfuscation Methodology
1. Intercepted dynamic `exec()` execution sink and dumped the unmarshaled AST.
2. Traced variable references across lambda chains.
3. Extracted the clean functional code into `odkjqwdid12.py` and neutralized exfiltration endpoints.
