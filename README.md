# ⚡ tdinh's Vault (`tdinhvault`)
> **Created & Maintained by:** `tdinh cute`  
> **Purpose:** Personal vault for Reverse Engineering, Malware Analysis Reports, Deobfuscated Source Codes & Clean Security Tools.

---

## 📂 Repository Structure

The vault is strictly organized into 3 isolated categories:

```text
tdinhvault/
├── reports/                 # Comprehensive technical reverse engineering & security audit reports
├── clean_tools/             # Safe, deobfuscated and fully reconstructed utility scripts & tools
└── neutralized_malware/     # Disarmed malware samples for security researchers (defanged & inert)
```

---

## 📑 1. Audit Reports (`/reports`)
| Report Name | Description |
| :--- | :--- |
| **`QUASAR_TOOL_AUDIT_REPORT.md`** | Deep reverse engineering of Quasar Loader (PyInstaller) & Quasar Tuner (Nuitka x64). |
| **`malware_exe_audit_report.md`** | Static & dynamic unpacking analysis of PE/EXE malware droppers. |
| **`dupemod_stealer_report.md`** | Investigation of Discord stealer disguised as a Minecraft mod. |
| **`EVS_GENERATOR_AUDIT_REPORT.md`** | Deobfuscation and flow analysis of token/account generators. |
| **`NUKE_AUDIT_REPORT.md`** | Detailed report on Discord server nuker scripts. |
| **`obf_cc_audit_report.md`** | Analysis of multi-layer obfuscated Python payloads. |
| **`xuanthang_audit_report.md`** | Deobfuscation of batch stealer / stager malware. |
| **`4_FILES_AUDIT_REPORT.md`** | Multi-target reverse engineering audit summary. |

---

## 🛠️ 2. Clean Tools (`/clean_tools`)
- **`QL_decompiled.py`**: 100% decompiled and reconstructed Python source code of Quasar Loader v1.0.0.
- **`regtoken_decoded.py`**: Clean reconstructed Discord token registration logic.
- **`warbot_discord_clean.py`**: Cleaned and formatted utility Discord bot script.
- **`spam_clean.py` & `treo_deobfuscated.py`**: Cleaned and deobfuscated automation scripts.
- **`deobfuscator_29a_infector.py`**: Security tool for stripping 29a obfuscation layers.

---

## 🛡️ 3. Neutralized Malware (`/neutralized_malware`)
All files in this folder are **completely disarmed, neutralized, and defanged**:
- Harmless execution block on line 1 (`RuntimeError`).
- URLs defanged (`hxxps://`, `[.]`).
- Safe for academic research, threat intelligence, and pattern matching.

---

## 👤 Author & Attribution
- **Author:** `tdinh cute`
- **License:** Open for Educational & Research Purposes.
