# Author: tdinh cute
# Research & Analysis by tdinh

# 🔍 BÁO CÁO PHÂN TÍCH & GIẢI MÃ KỸ THUẬT: BLACKFORGE MULTI-TOOL

## 1. Tổng quan mục tiêu (Target Overview)
- **Tên mẫu**: BlackForge Discord Multipurpose Tool v1.0
- **Tập tin phân tích**: `input/BlackForge-Discord-Multipurpose-tool-main.zip`
- **Tập tin binary kèm theo**: `BlackForge.exe` (13,748,203 bytes ~ 13.7 MB)
- **Kiến trúc đóng gói**: PyInstaller (Python 3.14 x64)
- **Thư mục giải mã & trích xuất**:
  - Unpack binary: [`BlackForge.exe_extracted`](file:///d:/THAY%20THẾ/deobf/BlackForge.exe_extracted)
  - Thư mục công cụ mở khóa: [`output/tools_sach/BlackForge_unlocked`](file:///d:/THAY%20THẾ/deobf/output/tools_sach/BlackForge_unlocked)

---

## 2. Kết quả phân tích nhị phân (Binary & Script Analysis)
1. **Đối chiếu giữa `BlackForge.exe` và mã nguồn**:
   - `BlackForge.exe` thực chất là bản đóng gói dạng frozen executable tạo bởi PyInstaller 2.1+ chạy trên Python runtime 3.14.
   - Entry point: `main.pyc` được compile từ chính file `main.py`.
   - Không phát hiện backdoor, stealer ngầm hoặc mã độc nhúng lén bên trong tệp thực thi `BlackForge.exe`.

2. **Cơ chế xác thực bản quyền & HWID (LynxAuth)**:
   - Tool sử dụng nền tảng xác thực bên thứ 3: **LynxAuth** (`https://lynxauth.qzz.io`).
   - **Auth API Endpoint**: `https://api.lynxauth.qzz.io/api/1.0/user_login`
   - **Lynx Owner ID**: `fb56b6a6-8c4a-4dcb-95f9-d0387ea0175b`
   - **Lynx App Secret**: `b50fb2cc3641d041046b0bf820908568`
   - **Thuật toán tính HWID**:
     ```python
     hashlib.sha256(f"{platform.node()}-{platform.processor()}".encode()).hexdigest()
     ```
     Băm SHA-256 chuỗi kết hợp tên máy tính (`platform.node()`) và thông số CPU (`platform.processor()`).

---

## 3. Danh mục các chức năng chi tiết của Tool

| STT | Chức năng | Tập tin xử lý | Cơ chế hoạt động |
| :---: | :--- | :--- | :--- |
| **1** | **Token Joiner** | `tools/token_joiner.py` | Sử dụng danh sách Discord token đăng nhập vào server qua invite code hoặc luồng OAuth2. |
| **2** | **Phone Bomber** | `tools/phone_spammer.py` | Đọc danh sách endpoint SMS OTP từ `utils/api.py` để gửi request dồn dập đến số điện thoại mục tiêu. |
| **3** | **Msg Spammer** | `tools/spammer.py` | Sử dụng token Discord gửi tin nhắn lặp lại với tốc độ cao vào channel chỉ định. |
| **4** | **Token Check / Purger** | `tools/token_remover.py` | Gửi request đến `https://discord.com/api/v10/users/@me` để phân loại token sống/chết và lọc file. |
| **5** | **Discord Nuker** | `tools/nuker.py` | Xóa kênh, tạo kênh mới hàng loạt và gửi tin nhắn spam qua webhook / bot token. |
| **6** | **Name Sniper** | `tools/name.py` | Kiểm tra username Discord khả dụng qua endpoint `/users/@me/pomelo-attempt` và gửi thông báo qua Discord Webhook khi bắt được username hiếm. |

---

## 4. Giải pháp mở khóa hoàn toàn (Unlocked Version)
- Đã tạo bản chạy độc lập không cần kết nối internet tới LynxAuth:
  👉 [main_unlocked.py](file:///d:/THAY%20THẾ/deobf/output/tools_sach/BlackForge_unlocked/main_unlocked.py)
- Khi khởi chạy:
  - Bỏ qua hoàn toàn bước nhập Username / Password / HWID.
  - Tự động gắn quyền tài khoản **`tdinh_vip`** với thời hạn **`Lifetime`**.
  - Mở trực tiếp Control Panel 7 chức năng.

---
*Báo cáo được thực hiện bởi tdinh cute.*
