# BÁO CÁO GIẢI MÃ & PHÂN TÍCH MÃ ĐỘC: OBF-TK.PY (UNIVERSER v3.0)

- **Target File:** `input/obf-tk.py` (Kích thước: 897,078 bytes)
- **Tên gốc xác định:** `token_spammer.py` (Discord Token Spammer & Stealer)
- **Tác giả / Kẻ phát tán:** **Nguyễn Hoàng Thanh Duy** (biệt danh: `duyk11`)
- **Công cụ Obfuscate:** **Universer v3.0** (bởi Lê Tiến Dũng & Nguyễn Hoàng Khánh Nam - *"Universer Xưng Bá Võ Lâm"*)
- **Mục tiêu Runtime:** Python 3.11 (`cpython-3.11`)
- **Kết quả kiểm định an ninh:** 🚨 **PHÁT HIỆN MÃ ĐỘC NGUY HIỂM (STEALER & BACKDOOR)**  
  Công cụ núp bóng dưới danh nghĩa "Discord Token Spammer" nhưng thực chất cài cắm mã độc ngầm **thu thập toàn bộ token Discord và âm thầm đọc trộm, tải toàn bộ file `.txt` và `.py` trên máy nạn nhân gửi về Telegram Bot C2 của kẻ tấn công**.

---

## 1. Cảnh báo Chỉ số Nguy hại (IOC - Indicators of Compromise)

### C2 Telegram Exfiltration Bot
- **Bot API URL:** `https://api.telegram.org/bot7603449030:AAFR06wr0uByJRHiGU7WbsyE94CyeSR1ZN0/`
- **Bot Token:** `7603449030:AAFR06wr0uByJRHiGU7WbsyE94CyeSR1ZN0`
- **Kênh nhận dữ liệu (Chat ID):** `8405590803`
- **Hành vi đánh cắp:**
  - Ngay khi người dùng bắt đầu chạy lệnh spam, một tiểu trình chạy ngầm (`threading.Thread(target=send_files_to_telegram, daemon=True).start()`) được kích hoạt.
  - Quét toàn bộ thư mục hiện hành bằng `glob.glob("*.txt") + glob.glob("*.py")`.
  - Đóng gói dữ liệu dạng Multipart Form-Data với boundary ngẫu nhiên và gửi thẳng về endpoint `/sendDocument` của Telegram Bot.

### C2 License Validation Server
- **Authentication Server:** `https://key.twanphat.xyz/check`
- **Project Access Token:** `de0d1e04-9b99-4600-aa03-d851c702e976`
- **Product ID:** `99`
- **Payload Parameter:** `licensekeys=<user_input_key>`

---

## 2. Kiến trúc Bảo vệ của Universer v3.0 & Kỹ thuật Vượt qua (Bypass)

Universer là một bộ làm rối bytecode hướng đối tượng được thiết kế riêng cho Python 3.11 với nhiều lớp bẫy tinh vi:

### Lớp 1: Anti-Tamper & Multi-layer Compression Stager
- Header kiểm tra tính nguyên vẹn môi trường Python, buộc chạy trên bản build `3.11.*`.
- Khối dữ liệu payload thực thi được nén qua pipeline:
  $$\text{Base85 Decode} \longrightarrow \text{BZ2 Decompress} \longrightarrow \text{LZMA Decompress} \longrightarrow \text{Marshal Stream}$$
- **Kỹ thuật vượt qua:** Trích xuất hằng số `c1025` trực tiếp từ AST/Bytecode của lớp vỏ và giải nén tĩnh qua Python script mà không cần kích hoạt loader.

### Lớp 2: Rác Kiểm Soát Luồng (Control Flow Flattening & Dead Junk Injections)
- Chèn hàng nghìn (hơn 4,100) đối tượng Code Object rác dạng `<lambda>` lồng nhau.
- Các hàm đều bị bọc trong khối `try...except MemoryError('Dunglecoder')` cùng chuỗi phép toán vô nghĩa (`sum([]) ** 0`, so sánh chuỗi troll như `'Nhìn Con Mẹ Mày'`, `'Thích Nhìn Không Thằng Chó'`).
- **Kỹ thuật vượt qua:** Phân tích đồ thị bytecode Python 3.11, lọc bỏ tất cả hàm ẩn danh `<lambda>` rác, định vị chính xác 20 hàm nghiệp vụ cốt lõi của tác giả thông qua bảng ký hiệu `names` và cấu trúc opcode thực thi.

### Lớp 3: String Table Encryption (Modulo Affine XOR Decryption)
- Không có bất kỳ chuỗi nhạy cảm nào (`tokens.txt`, Telegram URL, Bot Token, Discord API headers) tồn tại ở dạng văn bản rõ.
- Mọi chuỗi đều được tính toán động tại thời điểm chạy thông qua lời gọi hàm `CALL 3` nhận 3 tham số chuỗi mã hóa ký tự Unicode và một lambda giải mã:
  $$\text{char}[i] = ((\text{ord}(s[arg\_idx]) \pmod{mod}) \oplus z_i)$$
  với các khóa $arg\_idx$ và $mod$ được bảo vệ bằng XOR bitwise.
- **Kỹ thuật vượt qua:** Xây dựng trình mô phỏng và giải mã ngược toàn bộ 100% bảng chuỗi của toàn bộ ứng dụng trong 0.2 giây.

---

## 3. Kiến trúc Tính năng Ứng dụng Được Phục Hồi (`token_spammer_deobfuscated.py`)

Công cụ bao gồm các thành phần hoàn chỉnh:
1. **Quản lý phiên & Vượt rào Discord Anti-Bot:**
   - Sử dụng thư viện `curl_cffi` giả lập chuẩn xác TLS Fingerprint của trình duyệt `Chrome 131`.
   - Module `TokenFingerprint`: Tạo ngẫu nhiên `client_launch_id`, `launch_signature`, `client_heartbeat_session_id`, và tính toán header `x-super-properties` cùng `x-context-properties` mã hóa Base64 theo format Discord Web Client mới nhất.
2. **Xác thực và phân loại Token (`verify_token`):**
   - Đọc danh sách token từ `tokens.txt`.
   - Gửi yêu cầu kiểm tra tới `https://discord.com/api/v9/users/@me`.
   - Phân tích `username` và `discriminator` để hiển thị trạng thái `Live` hoặc `Invalid`.
3. **Menu Điều khiển Tương tác:**
   - Chọn chế độ spam: Toàn bộ token vào 1 kênh chung hoặc mỗi token một kênh riêng biệt.
   - Tự động lấy danh sách máy chủ (`get_guilds`) và lọc kênh text khả dụng (`get_channels` với `type == 0`).
   - Hỗ trợ chọn kênh theo số thứ tự, khoảng `a-b`, nhập tên kênh hoặc chọn tất cả (`0`).
4. **Cơ chế Điều chỉnh Tốc độ (Rate-Limit & Anti-Ban):**
   - Hỗ trợ 2 chế độ delay: Cố định (`fixed`) hoặc ngẫu nhiên (`random min..max`).
   - Tự động bắt mã phản hồi HTTP `429 Too Many Requests`, phân tích trường JSON `retry_after` và tạm dừng luồng chính xác.
   - Bắt mã lỗi `401 Unauthorized` để tự động ngắt kết nối khi token bị vô hiệu hóa ("Token die").

---

## 4. Tổng kết & Khuyến cáo An ninh

- **Mức độ rủi ro:** 🔴 **CỰC KỲ CAO (CRITICAL)**.
- Người dùng tuyệt đối không chạy file gốc `obf-tk.py`. Mọi file token Discord hoặc file chứa source code mã nguồn `.py` trong cùng thư mục chạy tool sẽ bị đánh cắp toàn bộ ngay trong những giây đầu tiên.
- Toàn bộ mã nguồn đã được giải mã, phân tích và lưu trữ nguyên vẹn tại:
  - [token_spammer_deobfuscated.py](file:///d:/THAY%20THẾ/deobf/tdinhvault/deobfuscated/44_Discord_Token_Spammer_NguyenHoangThanhDuy/token_spammer_deobfuscated.py)
  - [REPORT.md](file:///d:/THAY%20THẾ/deobf/tdinhvault/deobfuscated/44_Discord_Token_Spammer_NguyenHoangThanhDuy/REPORT.md)
