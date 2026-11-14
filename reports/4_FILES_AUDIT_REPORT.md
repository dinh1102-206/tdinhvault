# Author: tdinh cute
# Research & Analysis by tdinh

# BÁO CÁO PHÂN TÍCH & DEOBFUSCATE 4 FILE MỚI

> **Ngày kiểm tra:** 07/11/2026  
> **Người thực hiện:** Antigravity  
> **Mục tiêu:** Phân tích, bóc tách toàn bộ mã nguồn và xác định mức độ an toàn của 4 file:  
> 1. `checktoken.py`  
> 2. `lumcoin (1).py`  
> 3. `sieudedatoken (1).py`  
> 4. `Treo-obf.py`  

---

## 📊 BẢNG TỔNG HỢP NHANH

| Tên File | Công cụ làm rối (Obfuscator) | Phân loại | Mức độ nguy hiểm | Tóm tắt bản chất |
| :--- | :--- | :--- | :--- | :--- |
| **`checktoken.py`** | PyDNA v3.5.0 (NullByte) | Token Checker | 🟢 **AN TOÀN** (Sạch) | Kiểm tra live/die token Discord nội bộ, không gửi trộm dữ liệu. |
| **`lumcoin (1).py`** | ENJULY19 (`ngocuyen`) | Token Stealer Trojan | 🔴 **CỰC KỲ NGUY HIỂM** | Ngụy trang Tool nhận coin `bot-hosting.net`, trộm Token Discord gửi về Bot C2. |
| **`sieudedatoken (1).py`** | Shenron (`Nguyễn Ngọc Tú`) | Token Stealer Trojan | 🔴 **CỰC KỲ NGUY HIỂM** | Ngụy trang Tool đổi token khi lỗi, trộm sạch file token gửi về Telegram bot. |
| **`Treo-obf.py`** | PyDraw (`Leo Trung Kien`) | Discord Tool | 🟢 **AN TOÀN** (Sạch) | Tool treo spam tin nhắn, đổi bio/username, không có mã độc gián điệp. |

---

## 1. CHI TIẾT FILE 1: checktoken.py (🟢 SẠCH)

* **Kích thước gốc:** 518,747 bytes.
* **Lớp bảo vệ:** `PyDNA Obfuscator v3.5.0 — ULTRA EVAL CHAIN EDITION` (bởi NullByte Research Group). Chứa các biểu thức toán học đánh lạc hướng và chuỗi lambda đệ quy.
* **Phương pháp giải mã:** 
  * Trích xuất khối Base85 tại dòng 78–108 (`_ΨPAYLOAD_Λ_`).
  * Giải nén tuần tự: `base64.b85decode` $\rightarrow$ `bz2.decompress` $\rightarrow$ `zlib.decompress` $\rightarrow$ `utf-8.decode`.
  * Đã khôi phục hoàn chỉnh mã nguồn gốc tại [`output/checktoken_deobfuscated.py`](file:///d:/THAY%20THẾ/deobf/output/checktoken_deobfuscated.py) (86 KB, 2,184 dòng).
* **Hành vi code:**
  * Nhận token qua nhập tay (`get_tokens_manual`) hoặc từ file (`get_tokens_from_file`).
  * Gọi API Discord: `https://discord.com/api/v9/users/@me` và `/guilds` để kiểm tra xem token còn sống hay đã chết.
  * Phân loại Nitro, phone, email, số lượng server và lưu kết quả vào `token_result_<timestamp>.txt`.
  * **Kết luận an ninh:** Không chứa webhook, không có bot token, an toàn để sử dụng.

---

## 2. CHI TIẾT FILE 2: lumcoin (1).py (🔴 MÃ ĐỘC TROJAN)

* **Kích thước gốc:** 528,901 bytes.
* **Lớp bảo vệ:** `ENJULY19` (bởi `hngocuyen / ngocuyencoder`).
* **Phương pháp giải mã:** 
  * Ghép 4 biến `_en + _july + _birth + __19` $\rightarrow$ `b85decode` $\rightarrow$ `bz2` $\rightarrow$ `zlib` $\rightarrow$ thu được bytecode Python 3.12 (`output/lumcoin_extracted.marshaled`, 2.86 MB).
  * Giải mã 232 chuỗi ký tự qua thuật toán `c2h6` và `o2(r - 0xFF78FF)`. Danh sách chuỗi đã lưu tại [`output/lumcoin_decoded_strings.txt`](file:///d:/THAY%20THẾ/deobf/output/lumcoin_decoded_strings.txt).
* **Vỏ bọc lừa đảo:**
  * Tiêu đề: `AUTO CLAIM COIN BOT-HOSTING - BY NG TAN NGHIA` (Treo máy 24/24 - Tự động lượm coin qua ngày trên `bot-hosting.net` qua YesCaptcha).
* **Hành vi ngầm đánh cắp thông tin (C2 Infrastructure):**
  * **Discord Bot Token kẻ tấn công:** `REDACTED_DISCORD_TOKEN_BY_TDINH`
  * **Bot ID:** `1392074867909853317`
  * **Proxy ngầm cài cắm:** `http://aewwwsdp:dzx8a932rd2p@31.59.20.176:6754`
  * Khi nạn nhân nhập Auth Token để "lượm coin", bot ngầm gửi bản tin trộm cắp:
    `📥 NEW LOG: DATA COLLECTED 👤 Name Discord ... 🍪 Auth Token ...` về Discord của kẻ tấn công.

---

## 3. CHI TIẾT FILE 3: sieudedatoken (1).py (🔴 MÃ ĐỘC TRỘM TOKEN)

* **Kích thước gốc:** 155,341 bytes.
* **Lớp bảo vệ:** `Shenron` (Gojo Satoru Theme) bởi `Nguyễn Ngọc Tú` (`ntluvsam` / `facebook.com/Ngocctuucte`).
* **Phương pháp giải mã:**
  * Vượt qua lớp DragonRadar: `a85decode` $\rightarrow$ `bz2` $\rightarrow$ `zlib` $\rightarrow$ `lzma` $\rightarrow$ `output/sieudedatoken_extracted.marshaled` (606 KB).
  * Giải mã 378 chuỗi ký tự bị băm thành tuple mã số nguyên trong `co_consts`. Danh sách chuỗi lưu tại [`output/sieudedatoken_strings.txt`](file:///d:/THAY%20THẾ/deobf/output/sieudedatoken_strings.txt).
* **Vỏ bọc lừa đảo:**
  * Tiêu đề: `Tool Treo Discord Tự Động Change Token Mỗi Khi Token Bị Lỗi`.
  * Yêu cầu nạn nhân: `Nhập file chứa token: `.
* **Hành vi gián điệp gửi qua Telegram (C2 Telegram Infrastructure):**
  * **Telegram Bot Token kẻ tấn công:** `8506404594:AAFIgl06V6bI0HF0RoAdbouFs1zl6Y7MCvg`
  * **Telegram Chat ID nhận dữ liệu:** `7935712363`
  * **Server License / Kill Status:** `http://fi9.bot-hosting.net:21078`
  * Hàm `send_tokens_to_telegram` đọc toàn bộ file token nạn nhân vừa nạp, chia theo từng cụm và âm thầm gửi `POST` tới `https://api.telegram.org/bot8506404594:AAFIgl06V6bI0HF0RoAdbouFs1zl6Y7MCvg/sendMessage` về Telegram của tác giả.

---

## 4. CHI TIẾT FILE 4: Treo-obf.py (🟢 SẠCH)

* **Kích thước gốc:** 528,548 bytes.
* **Lớp bảo vệ:** `PyDraw` (bởi `Leo Trung Kien`).
* **Phương pháp giải mã:**
  * Giải mã khóa SHA256 động kết hợp `sys.maxsize` và hoán vị byte slice.
  * Giải nén kép: `bz2.decompress` $\rightarrow$ `zlib.decompress` $\rightarrow$ thu được 9 code objects trong cấu trúc `dnag` (`output/treo_unpacked.marshaled`).
* **Hành vi code:**
  * Lớp `DiscordTool` cung cấp menu dòng lệnh quản lý tài khoản Discord:
    * `load_tokens_from_file`: Đọc token từ file txt.
    * `load_messages_from_file`: Đọc danh sách tin nhắn.
    * `send_message`: Gửi tin nhắn vào kênh Discord kèm tag người dùng, xử lý rate limit (HTTP 429 `retry_after`).
    * `change_bio / change_username`: Đổi bio và username hàng loạt.
    * `check_tokens`: Kiểm tra token sống/chết.
  * **Kết luận an ninh:** Đây là tool tự động hóa Discord thông thường, hoàn toàn không có mã độc trộm token hay gửi dữ liệu về bên thứ ba.
