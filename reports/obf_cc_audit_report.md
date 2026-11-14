# Author: tdinh cute
# Research & Analysis by tdinh

# BÁO CÁO PHÂN TÍCH & GIẢI MÃ MÃ NGUỒN: OBF-CC.PY

- **Tệp phân tích:** [`input/obf-cc.py`](file:///d:/THAY%20THẾ/deobf/input/obf-cc.py)
- **Tác giả:** `tdinh`
- **Decoded by:** `tdinh cute`
- **Thời gian phân tích:** 07/11/2026
- **Kết luận:** **MÃ ĐỘC NGUY HIỂM (DISCORD TOKEN STEALER / RAT TRONG VỎ BỌC WAR BOT)**

---

## 1. THÔNG TIN OBFUSCATION
- **Tên Obfuscator:** Shenron (Dragon Ball Theme) - của Nguyễn Xuân Trịnh.
- **Tầng mã hóa bên ngoài:**
  - Base64 `a85decode` (Ascii85)
  - `bz2.decompress`
  - `zlib.decompress`
  - `lzma.decompress`
  - Bytecode marshaled Python 3.12 (`marshal.loads`)
- **Tầng mã hóa chuỗi bên trong (String Obfuscation):**
  - Mọi chuỗi (string) trong mã nguồn đều bị băm thành các tuple số nguyên Unicode và tái tạo động thông qua các lambda gọi `goku().join(chr(x) for x in tuple_ints)`.
  - Có các đoạn bẫy kiểm tra hook runtime như `Hook hả con trai`, bẫy `sys.exit`, `print`, `exec`, `input`.

---

## 2. BẢN CHẤT MÃ NGUỒN & CƠ CHẾ ĐÁNH CẮP TOKEN
File ban đầu được quảng cáo và ngụy trang dưới dạng **"WAR BOT - ĐA TOKEN - SPAM NO LIMIT"** (Tool spam/flood tin nhắn Discord số lượng lớn bằng nhiều token).

Tuy nhiên, bên trong mã nguồn cài cắm **2 cửa sau (Backdoor)** gửi toàn bộ token Discord về webhook của kẻ tấn công:

1. **Khi người dùng nhập token thủ công (`get_tokens_from_user`):**
   - Ngay khi người dùng gõ từng token vào terminal, hàm `send_token_to_webhook(token)` được kích hoạt âm thầm.
2. **Khi người dùng đọc token từ file `tokens.txt` (`load_tokens_from_file`):**
   - Khi load file, chương trình đọc từng dòng và gọi `send_token_to_webhook` gửi toàn bộ danh sách token về C2 Server.
3. **Thu thập thông tin cá nhân kèm theo:**
   - Hàm `send_token_to_webhook` truy vấn API `https://discord.com/api/v10/users/@me` bằng token để lấy `Username` và `User ID`.
   - Đóng gói thành Discord Embed màu đỏ với tiêu đề `🔑 TOKEN MỚI ĐƯỢC NHẬP`, gửi về Webhook kèm thời gian cụ thể.

---

## 3. THÔNG TIN C2 WEBHOOK ĐÃ PHÁT HIỆN
- **C2 Discord Webhook URL:**
  `https://discord.com/api/webhooks/1526829712922509373/5JvP7UH9ifQvuuKXc6ITum-24PDRsLGsvzk_GPZY8Wz9IcpDYgzpRnPog11yqBp8CJtd`
- **Trạng thái kiểm tra trực tiếp:**
  - Kết quả: `HTTP 404 Not Found` - `{"message": "Unknown Webhook", "code": 10015}`.
  - Webhook này đã bị Discord vô hiệu hóa / xóa khỏi hệ thống.

---

## 4. DANH MỤC FILE KẾT QUẢ ĐÃ XỬ LÝ

| Loại | Tệp | Mô tả |
| :--- | :--- | :--- |
| **Bản phân tích mã độc (Cách ly)** | [`output/chua_file_co_ma_doc/obf_cc_malware_analysis.py`](file:///d:/THAY%20THẾ/deobf/output/chua_file_co_ma_doc/obf_cc_malware_analysis.py) | Giữ nguyên logic cửa sau nhưng đã **defang C2 webhook** để nghiên cứu mã độc an toàn. |
| **Bản Tool sạch (Đã làm sạch)** | [`output/tools_sach/warbot_discord_clean.py`](file:///d:/THAY%20THẾ/deobf/output/tools_sach/warbot_discord_clean.py) | Đã **gỡ bỏ 100% mã độc / token stealer**, bảo toàn toàn bộ tính năng War Bot, check live/die, spam đa luồng. |
| **Báo cáo chi tiết** | [`output/chua_file_co_ma_doc/obf_cc_audit_report.md`](file:///d:/THAY%20THẾ/deobf/output/chua_file_co_ma_doc/obf_cc_audit_report.md) | Tài liệu phân tích kỹ thuật chi tiết. |
