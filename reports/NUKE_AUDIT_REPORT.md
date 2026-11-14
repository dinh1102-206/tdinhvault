# Author: tdinh cute
# Research & Analysis by tdinh

# BÁO CÁO PHÂN TÍCH & DEOBFUSCATE MÃ NGUỒN: nuke.py

> **Mức độ nguy hiểm:** ⚠️ **NGUY HIỂM CAO (CRITICAL)**  
> **Phân loại mã:** Discord RAT / Token Grabber / Keylogger / Server Nuker Trojan  
> **Ngụy trang:** `ProxyTool v2.2.0`  
> **Tác giả Obfuscator:** `ENJULY19` (bởi `hngocuyen` / `ngocuyencoder`)  
> **Người thực hiện deobfuscate:** Antigravity  

---

## 1. TỔNG QUAN VỀ MẪU MÃ ĐỘC

File [`input/nuke.py`](file:///d:/THAY%20THẾ/deobf/input/nuke.py) (kích thước ~463 KB) được bọc qua nhiều tầng mã hóa phức tạp sử dụng công cụ **ENJULY19**. Sau khi giải mã hoàn toàn 5 lớp bảo vệ, phát hiện đây là một **Trojan gián điệp và phá hoại Discord**:

- **Gián điệp & Đánh cắp dữ liệu:** Quét LevelDB của Discord (Standard, Canary, PTB) và các trình duyệt (Chrome, Brave, Edge) để cướp Token Discord; cài đặt Keylogger ngầm ghi lại toàn bộ phím bấm của nạn nhân.
- **C2 qua Discord Bot:** Dùng tài khoản Bot Discord để tạo kênh riêng cho từng nạn nhân trong server Discord của kẻ tấn công, tự động gửi IP, thông tin máy, token đánh cắp được và file keylog.
- **Duy trì quyền lực (Persistence):** Tự sao chép vào `AppData`, `LocalAppData`, `ProgramData`, tạo file script `.vbs` ẩn màn hình, gán Registry Run key và tạo Scheduled Task tự kích hoạt mỗi 5 phút.
- **Công cụ phá hoại (Nuker):** Chứa các lệnh `!nuke`, `!massband` để xóa sạch kênh, spam đổi tên server thành **`PHUCKHANG TRADEMARK`**.

---

## 2. CHỈ SỐ NHẬN DIỆN MỐI ĐE DỌA (IOCs)

### 2.1. C2 Infrastructure (Máy chủ điều khiển)
| Loại | Giá trị nhận diện |
| :--- | :--- |
| **Discord Bot Token** | `REDACTED_DISCORD_TOKEN_BY_TDINH` |
| **Discord Bot ID** | `1568474375450140692` |
| **C2 Guild ID (Server)** | `1568475530603270266` |
| **Định dạng Kênh C2** | `COMPUTERNAME-USERNAME` (Ví dụ: `DESKTOP-ABC-Admin`) |
| **Topic Kênh C2** | `Bot - <IP> - <Timestamp>` |

### 2.2. File & Thư mục liên quan
- **Keylog Temp:** `%TEMP%\.syscache.dat`
- **Marker kiểm tra lây nhiễm:** `%APPDATA%\.px_marker`
- **Thư mục cài cắm Persistence:**
  - `%APPDATA%\Microsoft\Windows\System\`
  - `%LOCALAPPDATA%\Microsoft\Windows\INetCache\`
  - `%PROGRAMDATA%\Microsoft\Windows\`
- **Định dạng file persistence:** Tên ngẫu nhiên 8 ký tự với đuôi `.pyw` và `.vbs`.

### 2.3. Registry & Scheduled Task
- **Scheduled Task Name:** `WinProxySvc` (chạy mỗi 5 phút)
- **Registry Key:** `HKCU\Software\Microsoft\Windows\CurrentVersion\Run`
  - Tên giá trị: `WinProxySvc`
  - Lệnh thực thi: Chạy script `.vbs` ẩn để gọi `pythonw.exe`.

---

## 3. CƠ CHẾ BẢO VỆ & QUÁ TRÌNH GIẢI MÃ (DEOBFUSCATION PROCESS)

### Lớp 1: AST Chemical Obfuscation (ENJULY19)
Mã nguồn bị làm rối bởi hàng nghìn biến đặt tên theo công thức hóa học: `mol`, `co2`, `feo2`, `h2so4`, `agno4`, `h3o`,... Tất cả hàm Python cơ bản (`exec`, `compile`, `getattr`, `eval`,...) bị ánh xạ qua một chuỗi lambda đệ quy.

### Lớp 2: Base85 & Đa tầng nén
- Khối dữ liệu payload thực tế được ghép từ 4 chuỗi: `_en + _july + _birth + __19` (447,632 ký tự).
- Chuỗi giải nén tuần tự:
  $$\text{Base85 Decode} \longrightarrow \text{bz2 Decompress} \longrightarrow \text{zlib Decompress}$$
- Kết quả thu được khối Python 3.12 Marshaled Code Object kích thước **2,175,500 bytes** (`output/nuke_extracted.marshaled`).

### Lớp 3: String Decryption (Mã hóa chuỗi ký tự)
Toán tử mã hóa chuỗi trong ENJULY19:
- Các chuỗi không lưu dạng plaintext mà được chia nhỏ thành các byte marker: `b'enjuly19/\xffy<char>'`.
- Mỗi ký tự được giải mã qua phép dịch bit hằng số:
  $$char = chr(c - 16742655) \quad (\text{tức } c - \text{0xFF78FF})$$
- Đã giải mã thành công toàn bộ **354 chuỗi** hằng số bị ẩn.

---

## 4. CHI TIẾT HÀNH VI ĐỘC HẠI TRONG SOURCE CODE

### 4.1. Token Stealer (Đánh cắp Discord Token)
Hàm `_st()` lùng sục tất cả thư mục Local Storage LevelDB:
- `%APPDATA%\discord\Local Storage\leveldb`
- `%APPDATA%\discordcanary\Local Storage\leveldb`
- `%APPDATA%\discordptb\Local Storage\leveldb`
- `%LOCALAPPDATA%\Google\Chrome\User Data\Default\Local Storage\leveldb`
- `%LOCALAPPDATA%\BraveSoftware\Brave-Browser\User Data\Default\Local Storage\leveldb`
- `%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Local Storage\leveldb`

Tìm kiếm bằng biểu thức chính quy:
- Token thường: `[\w-]{24,26}\.[\w-]{6}\.[\w-]{25,110}`
- Encrypted Token DPAPI: `dQw4w9WgXcQ:([A-Za-z0-9+/=]+)`

### 4.2. C2 Channel Creation & Keylogger Exfiltration
- Bot gọi API Discord `POST /guilds/1568475530603270266/channels` tạo kênh văn bản mang tên máy nạn nhân.
- Sau khi có kênh, mã độc gửi ngay:
  - Tên máy tính, username, IP Public (lấy qua `api.ipify.org`).
  - Danh sách Discord Tokens tìm được.
- Chạy thread Keylogger (`pynput.keyboard.Listener`). Cứ mỗi 30 giây, đọc `.syscache.dat` rồi dùng lệnh `curl` upload multipart file log vào kênh Discord C2.

### 4.3. Phá hoại Server (Nuke Module)
Khi kẻ tấn công gõ lệnh trên Discord:
- **`!nuke`**:
  1. Đổi tên Server nạn nhân thành `PHUCKHANG TRADEMARK`.
  2. Lặp qua tất cả channel và delete từng cái một.
  3. Tạo mới 30 kênh text `phuckhang-channel-1..30` và 10 kênh voice `phuckhang-vc-1..10`.
  4. Spam liên tục 15 tin nhắn mỗi kênh với nội dung: `PHUCKHANG TRADEMARK REGISTERED`.
- **`!massband`**:
  - Quét danh sách thành viên và ban toàn bộ người dùng có role thấp hơn Bot.

---

## 5. DANH SÁCH ARTIFACTS ĐÃ TẠO

Các tệp kết quả phân tích và mã nguồn đã được xuất tại thư mục `output/`:

1. [`nuke_deobfuscated.py`](file:///d:/THAY%20THẾ/deobf/output/nuke_deobfuscated.py) - Mã nguồn Python hoàn chỉnh, rõ ràng, đã được defang an toàn.
2. [`nuke_strings.txt`](file:///d:/THAY%20THẾ/deobf/output/nuke_strings.txt) - Danh sách toàn bộ 354 chuỗi giải mã từ bytecode.
3. [`nuke_extracted.marshaled`](file:///d:/THAY%20THẾ/deobf/output/nuke_extracted.marshaled) - Payload bytecode thô sau khi giải nén zlib/bz2.
4. [`nuke_3.12.pyc`](file:///d:/THAY%20THẾ/deobf/output/nuke_3.12.pyc) - File pyc chuẩn cho Python 3.12.
5. [`NUKE_AUDIT_REPORT.md`](file:///d:/THAY%20THẾ/deobf/output/NUKE_AUDIT_REPORT.md) - Báo cáo kiểm định an ninh chi tiết này.
