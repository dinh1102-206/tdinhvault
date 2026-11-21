# ⚡ tdinh's Vault (`tdinhvault`)
> **Created & Maintained by:** `tdinh cute`  
> **Purpose:** Personal vault for Reverse Engineering, Malware Analysis Reports, Deobfuscated Source Codes & Clean Security Tools.

---

## 📂 Repository Structure

```text
tdinhvault/
├── deobfuscated/            # 42+ Isolated tool folders (Source Obf, Clean Source & Dedicated REPORT.md)
├── reports/                 # Comprehensive technical reverse engineering & security audit reports
├── clean_tools/             # Safe, deobfuscated and fully reconstructed utility scripts & tools
└── neutralized_malware/     # Disarmed malware samples for security researchers (defanged & inert)
```

---

## 📦 Complete Deobfuscated Tools Directory (`/deobfuscated`)

Every tool is strictly isolated in its own folder containing:
1. **`source_obf/`**: Original obfuscated / packed source code or binary payload.
2. **`clean_source/`**: Fully reconstructed, deobfuscated, formatted and neutralized source code.
3. **`REPORT.md`**: Dedicated in-depth reverse engineering & audit report.

| # | Tool Directory | Description | Protection / Family | Status |
| :-: | :--- | :--- | :--- | :--- |
| **01** | `01_Zyphron_v2.1` | Stack Mini-VM + Chunked Decryption + Anti-Debug | Zyphron v2.1 (Python 3.12) | ✅ 100% Reconstructed |
| **02** | `02_PyMeo_v2` | Discord Token Grabber / Stealer unpacking | PyMeo v2 (NGOCUYENCODER) | ✅ Unpacked & Neutralized |
| **03** | `03_Browser_Extension_ContentJS` | Chrome Extension Content Script Deobfuscation | Hex-packed / Array Rotation | ✅ Clean & Formatted |
| **04** | `04_Quasar_Tool` | Quasar Loader & Quasar Tuner GUI / TUI | PyInstaller + Nuitka | ✅ Fully Reconstructed |
| **05** | `05_Discord_Nuker` | Discord Server Nuker Automation Script | Dynamic eval/exec packing | ✅ Clean Deobfuscated |
| **06** | `06_Token_Automation_Suite` | CheckToken, Lumcoin, Treo, SieuDeDaToken | Multi-layer string rotation | ✅ Fully Restructured |
| **07** | `07_Titan_Shield_Stealth` | Titan Shield Virtual Stack Machine payload | Titan Shield / Stealth VM | ✅ VM Flattened & Cleaned |
| **08** | `08_Tool_Raid_Bypass_Anti` | Discord Raid Bot Anti-Bypass Automation | Multi-layer packaging | ✅ Core Logic Extracted |
| **09** | `09_EVS_Generator` | EVS Account & Token Generator scripts | FlowAuth / Lua | ✅ Decrypted Secrets |
| **10** | `10_BlackForge_Multipurpose` | BlackForge Discord Multipurpose Tool | PyInstaller / Unlocked | ✅ Unlocked & Reconstructed |
| **11** | `11_TikTok_Sender_XuanThang` | Batch Stealer / TikTok Automation Stager | Custom Stager | ✅ Cleaned & Defanged |
| **12** | `12_Obf_CC` | Multi-layer obfuscated Python payload | Custom Obf-CC | ✅ Deobfuscated & Analyzed |
| **13** | `13_DupeMod_Stealer` | Minecraft Fake Dupe Mod Discord Stealer | Java / Fernflower decompiled | ✅ Decompiled & Documented |
| **14** | `14_Main_Py_Stealer` | Multi-vector Discord Token Stealer | Multi-layer exec packing | ✅ Cleaned & Disarmed |
| **15** | `15_Ceker_Hook_Mobile` | Mobile Discord Webhook Checker & Spammer | Packer / Encrypted Strings | ✅ Clean Reconstructed |
| **16** | `16_GPM_Login_Global` | GPM Anti-detect Browser Tools | PE / .NET | ✅ Audited & Logged |
| **17** | `17_Installer_Malware` | PE Dropper & Secondary Stage Stager | PE32 Dropper | ✅ Unpacked & Audited |
| **18** | `18_Obsidian_Obfuscator` | Obsidian 3.11/3.12 VM & Control-Flow Flattening | Obsidian Custom VM | ✅ Fully Decompiled |
| **19** | `19_VKietDZ_Stealer` | VKietDZ Discord Token Grabber & Logger | Layered marshal / Base64 | ✅ Unpacked & Neutralized |
| **20** | `20_Obf_ToolDis` | Discord ToolDis Multi-layer Pack | Recursive Lambda Bytecode | ✅ Clean Source Recovered |
| **21** | `21_Discord_Tool_Cracked` | Discord Tool v1.0.0 Electron/PyInstaller | Auth & License Bypass | ✅ 100% Cracked & Clean |
| **22** | `22_RegToken_V75` | Discord Registration Token Generator | Custom Token Gen Logic | ✅ Source Reconstructed |
| **23** | `23_RegDis_Automation` | Discord Register Automation Tool | Obfuscated Python | ✅ Deobfuscated & Verified |
| **24** | `24_Spam_Clean_Bot` | Discord Message Flooding & Spammer Bot | String Pool Obfuscation | ✅ Cleaned & Formatted |
| **25** | `25_WarBot_Discord` | WarBot Discord Raid Tool | Multi-layer exec | ✅ Clean Deobfuscated |
| **26** | `26_NhayNuke_Bot` | NhayNuke Server Destruction Bot | Bytecode compilation | ✅ Clean Decompiled |
| **27** | `27_2_Py_Obfuscated` | 2.py Multi-layer Obfuscated Script | String Encryption / Marshal | ✅ Extracted & Analyzed |
| **28** | `28_50cn_Tool` | 50cn Chinese Multi-purpose Utility | Dynamic Code Execution | ✅ Unpacked & Documented |
| **29** | `29_AIOLauncher` | AIO Game & Utility Launcher | Electron / Native Wrapper | ✅ Unpacked & Extracted |
| **30** | `30_LocMod_V11_Proxy` | LocMod Android APK Proxy Injection | Dalvik / Smali / Native | ✅ Decompiled & Decrypted |
| **31** | `31_Token_Researcher` | Discord Token Research & Validation Tool | Obfuscated Python | ✅ Clean Source Recovered |
| **32** | `32_Tool_Decompiled` | Tool.py Utility Script | Base64 / Zlib / Exec | ✅ Decompiled & Cleaned |
| **33** | `33_ProSniper_Bot` | Discord Nitro & Vanity URL Sniper | Real-time WebSocket Gateway | ✅ Fully Reconstructed |
| **34** | `34_Tool_Auto_Lam_Nhiem_Vu_Discord` | Discord Quest & Task Automation Bot | Encrypted Payloads | ✅ Clean Deobfuscated |
| **35** | `35_DisV2_Bot` | DisV2 Discord Automation Bot | Multi-layer Packer | ✅ Deobfuscated & Clean |
| **36** | `36_Sana_Automation` | Sana Discord Automation Script | Obfuscated Script | ✅ Extracted & Cleaned |
| **37** | `37_Main_3_Clean` | Main 3 Stealer & Exfiltration Script | Multi-layer eval | ✅ Neutralized & Cleaned |
| **38** | `38_Main_2_Clean` | Main (2) Automation Script | Exec/Marshal layers | ✅ Unpacked & Formatted |
| **39** | `39_TDinh_AntiDetect` | Anti-Detect Browser & Fingerprint Core | Modular Python Framework | ✅ Complete Clean Source |
| **40** | `40_Deobfuscator_29a_Infector` | 29a Infector / Virus Stripper Engine | Security Deobfuscation Tool | ✅ Fully Operational |
| **41** | `41_Extracted_VBA_Runner` | Malicious VBA Macro Payload Runner | Office Macro Dropper | ✅ Analyzed & Defanged |
| **42** | `42_VideoStar_UnlockPro` | VideoStar iOS Pro Tweak | Objective-C Runtime Hook | ✅ Reconstructed Tweak |

---

## 🛡️ Neutralized Malware Notice
All malicious files and stealer payloads in this repository are **strictly defanged and neutralized**:
- Discord webhook URLs and bot tokens have been sanitized or masked to avoid misuse and bypass automated scanners.
- Harmless execution guards (`RuntimeError("DEFANGED")`) are injected at execution entrypoints.
- Repository is strictly intended for **Security Research, Malware Analysis & Educational Purposes**.

---

## 👤 Author & Attribution
- **Author:** `tdinh cute`
- **License:** Open for Educational & Research Purposes.
