# ⚡ tdinh's Vault (`tdinhvault`)
> **Created & Maintained by:** `tdinh cute`  
> **Purpose:** Personal vault for Reverse Engineering, Malware Analysis Reports, Deobfuscated Source Codes & Clean Security Tools.

---

## 📂 Repository Structure

The vault is organized into dedicated categories:

```text
tdinhvault/
├── deobfuscated/            # Isolated folders per tool: source obf, deobfuscated clean source, and dedicated report
├── reports/                 # Comprehensive technical reverse engineering & security audit reports
├── clean_tools/             # Safe, deobfuscated and fully reconstructed utility scripts & tools
└── neutralized_malware/     # Disarmed malware samples for security researchers (defanged & inert)
```

---

## 📦 Deobfuscated Tools Directory (`/deobfuscated`)

Every tool is isolated in its own dedicated directory containing **Source Obfuscated**, **Clean Deobfuscated Source**, and its **Dedicated Audit Report (`REPORT.md`)**:

| Tool Directory | Description | Obfuscator / Target | Status |
| :--- | :--- | :--- | :--- |
| **`01_Zyphron_v2.1`** | Custom Stack Mini-VM + Chunked Decryption + Anti-Debug | Zyphron v2.1 (Python 3.12) | ✅ 100% Reconstructed |
| **`02_PyMeo_v2`** | Discord Token Grabber / Stealer unpacking | PyMeo v2 (NGOCUYENCODER) | ✅ Unpacked & Neutralized |
| **`03_Browser_Extension_ContentJS`** | Chrome Extension Content Script Deobfuscation | Hex-packed / String Array Rotation | ✅ Clean & Formatted |
| **`04_Quasar_Tool`** | Quasar Loader & Quasar Tuner GUI / TUI | PyInstaller + Nuitka | ✅ Fully Reconstructed |
| **`05_Discord_Nuker`** | Discord Server Nuker Automation Script | Dynamic eval/exec packing | ✅ Clean Deobfuscated |
| **`06_Token_Automation_Suite`** | CheckToken, Lumcoin, Treo, SieuDeDaToken | Multi-layer string rotation | ✅ Fully Restructured |
| **`07_Titan_Shield_Stealth`** | Titan Shield Virtual Stack Machine payload | Titan Shield / Stealth VM | ✅ VM Flattened & Cleaned |
| **`08_Tool_Raid_Bypass_Anti`** | Discord Raid Bot Anti-Bypass Automation | Multi-layer packaging | ✅ Core Logic Extracted |
| **`09_EVS_Generator`** | EVS Account & Token Generator scripts | FlowAuth / Lua | ✅ Decrypted Secrets |
| **`10_BlackForge_Multipurpose`** | BlackForge Discord Multipurpose Tool | PyInstaller / Unlocked | ✅ Unlocked & Reconstructed |
| **`11_TikTok_Sender_XuanThang`** | Batch Stealer / TikTok Automation Stager | Custom Stager | ✅ Cleaned & Defanged |
| **`12_Obf_CC`** | Multi-layer obfuscated Python payload | Custom Obf-CC | ✅ Deobfuscated & Analyzed |
| **`13_DupeMod_Stealer`** | Minecraft Fake Dupe Mod Discord Stealer | Java / Fernflower decompiled | ✅ Decompiled & Documented |
| **`14_Main_Py_Stealer`** | Multi-vector Discord Token Stealer | Multi-layer exec packing | ✅ Cleaned & Disarmed |
| **`15_Ceker_Hook_Mobile`** | Mobile Discord Webhook Checker & Spammer | Packer / Encrypted Strings | ✅ Clean Reconstructed |
| **`16_GPM_Login_Global`** | GPM Anti-detect Browser Tools | PE / .NET | ✅ Audited & Logged |
| **`17_Installer_Malware`** | PE Dropper & Secondary Stage Stager | PE32 Dropper | ✅ Unpacked & Audited |

---

## 📑 Audit Reports (`/reports`)
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

## 🛠️ Clean Tools (`/clean_tools`)
- **`QL_decompiled.py`**: 100% decompiled and reconstructed Python source code of Quasar Loader v1.0.0.
- **`regtoken_decoded.py`**: Clean reconstructed Discord token registration logic.
- **`warbot_discord_clean.py`**: Cleaned and formatted utility Discord bot script.
- **`spam_clean.py` & `treo_deobfuscated.py`**: Cleaned and deobfuscated automation scripts.
- **`deobfuscator_29a_infector.py`**: Security tool for stripping 29a obfuscation layers.

---

## 🛡️ Neutralized Malware (`/neutralized_malware`)
All samples are **completely disarmed, neutralized, and defanged**:
- Harmless execution block on line 1 (`RuntimeError`).
- URLs defanged (`hxxps://`, `[.]`).
- Safe for academic research, threat intelligence, and pattern matching.

---

## 👤 Author & Attribution
- **Author:** `tdinh cute`
- **License:** Open for Educational & Research Purposes.
