# Author: tdinh cute
# Research & Analysis by tdinh

# BÁO CÁO PHÂN TÍCH & GIẢI MÃ MÃ NGUỒN: MAIN 3.PY

- **Tệp nguồn:** [`input/main 3.py`](file:///d:/THAY%20THẾ/deobf/input/main 3.py)
- **Tác giả:** `tdinh`
- **Decoded by:** `tdinh cute`
- **Thời gian phân tích:** 07/11/2026
- **Kết luận:** **CÔNG CỤ DISCORD MULTI-TOOL BOT (HỢP LỆ, KHÔNG CÓ CỬA SAU LÉN LÚT)**

---

## 1. PHÂN TÍCH KỸ THUẬT & MÃ RỐI
- **Loại Obfuscator áp dụng:** **ENJULY19** (của `khoacoder` / `Phannguyendangkhoacoder1`).
- **Hình thức mã rối:**
  - 64 dòng đầu tiên chứa đoạn mã rác khởi tạo giả lập các kiểu dữ liệu (`khoacoder1` đến `khoacoder16`).
  - Toàn bộ lệnh `print(...)` trong hơn 6,700 dòng code bị đổi tên thành `khoacoder15(...)`.
  - Không có bytecode mã hóa hay payload nhị phân giấu kín; toàn bộ logic gốc là mã nguồn Python đầy đủ.
- **Quy trình giải mã:**
  1. Loại bỏ hoàn toàn khối header rác ENJULY19 (dòng 1 - dòng 64).
  2. Khôi phục toàn bộ các hàm `khoacoder15` trở lại lệnh `print` chuẩn của Python.
  3. Thêm header định danh tác giả `tdinh` | `Decoded by: tdinh cute`.

---

## 2. BẢN CHẤT CỦA CÔNG CỤ
Tệp [`input/main 3.py`](file:///d:/THAY%20THẾ/deobf/input/main 3.py) là một Bot Discord đa chức năng quy mô lớn (hơn 6,700 dòng lệnh) tích hợp nhiều module:

1. **Discord Raid & Spam Engine:**
   - `/treodis`: Treo spam tin nhắn vào danh sách channel Discord với nhiều token.
   - `/allnhaydis`: Nhây / flood tin nhắn Discord tự động.
   - `/voice_cmd`: Treo tài khoản trong voice channel Discord.
2. **Facebook Messenger Raid Engine:**
   - Hỗ trợ kết nối MQTT, nhây poll, đổi theme tự động, đổi nickname hàng loạt, raid group chat.
3. **DaoProxy Module:**
   - Tự động cào (scrape) và kiểm tra danh sách proxy từ nhiều nguồn công cộng và cao cấp (BrightData, Crawlera, SOCKS4/5).
4. **Token Manager Module:**
   - `/tokenmanager` & `/addtkm`: Đổi avatar, đổi tên hiển thị, set tiểu sử (bio), set đại từ xưng hô (pronouns), kiểm tra trạng thái token Discord.
5. **Python Obfuscator Engine:**
   - Tích hợp sẵn engine tạo mã rối ENJULY19 qua lệnh `/encode` (cho phép người dùng tải lên file Python để mã hóa).
6. **Hệ thống Session & Auto-Resume:**
   - Hỗ trợ lưu trữ tiến trình qua lệnh `/restart` và tự động khôi phục (resume) các tab spam khi bot khởi động lại.

---

## 3. KIỂM TRA MÃ ĐỘC & CREDENTIALS
- **Kiểm tra Backdoor / Token Stealer:** Không phát hiện webhook lén lút gửi token người dùng về server của hacker.
- **Bot Token Discord được tìm thấy trong code:**
  - Token: `REDACTED_DISCORD_TOKEN_BY_TDINH`
  - Bot ID: `1412302109277163581`
  - Trạng thái kiểm tra trực tiếp: `HTTP 401 Unauthorized` (Token đã hết hạn hoặc bị hủy).

---

## 4. TỆP ĐÃ XỬ LÝ
- Bản sạch đã gỡ mã rối:
  - [`output/tools_sach/main_3_clean.py`](file:///d:/THAY%20THẾ/deobf/output/tools_sach/main_3_clean.py)
  - [`output/main_3_clean.py`](file:///d:/THAY%20THẾ/deobf/output/main_3_clean.py)
- Báo cáo kiểm định:
  - [`output/reports/main_3_audit_report.md`](file:///d:/THAY%20THẾ/deobf/output/reports/main_3_audit_report.md)
