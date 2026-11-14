# Author: tdinh cute
# Research & Analysis by tdinh

# BÁO CÁO PHÂN TÍCH KỸ THUẬT & KIỂM TOÁN AN NINH MÃ NGUỒN (AUDIT REPORT)
**Tệp mục tiêu:** `reg token adr.apk` / `app-debug (1).apk`  
**Đơn vị thực hiện kiểm toán:** Phân tích kỹ thuật mã nguồn tĩnh (Static Reverse Engineering & Forensics)  
**Ngày lập báo cáo:** 05/11/2026  
**Trạng thái kiểm toán:** HOÀN TẤT — PHÁT HIỆN LỖ HỔNG VÀ MÃ ĐỘC NGẦM NGUY HIỂM CAO

---

## 1. TỔNG QUAN ỨNG DỤNG (APPLICATION OVERVIEW)

| Thuộc tính | Chi tiết |
| :--- | :--- |
| **Tên ứng dụng** | EVS Generator (Discord Generator & Automation Suite) |
| **Package Name** | `com.evs.generator` |
| **Kích thước APK** | 46,944,040 bytes (~46.9 MB) |
| **Kiểu bản dựng** | Android Debug Build (biên dịch qua D8, chưa bị làm rối mã ProGuard/R8) |
| **Ngôn ngữ phát triển** | Kotlin / Java (Android SDK 26+) |
| **Activity khởi động** | `com.evs.generator.MainActivity` |
| **Mã nguồn đã dịch ngược** | 165 tệp tin Java/Kotlin hoàn chỉnh (2.57 MB code sạch) |

---

## 2. PHÁT HIỆN NGUY HIỂM CAO: MÃ ĐỘC ĐÁNH CẮP TÀI KHOẢN (BACKDOOR / EXFILTRATION)

> [!CAUTION]
> **CẢNH BÁO MÃ ĐỘC ĐÁNH CẮP TÀI KHOẢN NGẦM:**  
> Trong quá trình dịch ngược, phát hiện ứng dụng được cài cắm cơ chế bí mật để thu thập và gửi trộm toàn bộ tài khoản vừa tạo về máy chủ của bên thứ ba.

### Cơ chế hoạt động của Backdoor:
1. Nơi chứa mã độc: Class `com.evs.generator.security.NativeGuard` và `com.evs.generator.automation.NotificationHelper`.
2. Phương thức thực thi: `NativeGuard.sendDcWebhook()` và `NativeGuard.sendTgMessage()`.
3. Hành vi ngầm: Ngay khi người dùng nhấn tạo tài khoản và đăng ký thành công, hàm `formatAccount()` sẽ tự động đóng gói toàn bộ dữ liệu gồm:
   * **Địa chỉ Email** (`email`)
   * **Mật khẩu** (`password`)
   * **Cặp Combo** (`email:password`)
   * **Discord User Token** (`token`)
   * **Thời gian tạo & Trạng thái xác thực**
4. Đích đến của dữ liệu bị đánh cắp: Toàn bộ thông tin tài khoản được gửi lén đồng thời qua HTTP POST tới cả **Discord Webhook** và **Telegram Bot/Channel** thuộc quyền sở hữu của tác giả mã độc.

---

## 3. THÔNG TIN MÁY CHỦ THU HOẠCH TÀI KHOẢN (DECRYPTED SECRETS)

Tác giả đã mã hóa dữ liệu đích đến bằng thuật toán **PBKDF2-HMAC-SHA256 (100,000 vòng) + AES-256-CBC** trong tệp `res/raw/secrets.dat` nhằm che giấu hành vi trộm cắp.

Bằng phương pháp bẻ khóa tĩnh mảng integer trong hàm `buildPassphrase()`, chúng tôi đã khôi phục thành công passphrase gốc:
$$\text{Passphrase} = \text{\texttt{"EVS-Generator-Secure-Vault-Layered-Key-2026-Alpha-Omega"}}$$

### Dữ liệu cấu hình thu thập được giải mã:
* **Discord Webhook URL:**  
  `https://discord.com/api/webhooks/1527634319290662973/WgpG7uT6HiwOM7PcVNhInK2GwFyHSLVMV-jXueUIC2tulYiz6JH8vREnnVPSCi5Y5G-h`
* **Tên Webhook hiển thị:** `EVS Generator`
* **Telegram Bot Token:** `8746242350:AAGt2q0YcoKGu91FoDhp-yTDWIdUNV54I6Q`
* **Telegram Channel ID nhận dữ liệu:** `-1003873674239`

---

## 4. CƠ CHẾ PHÒNG THỦ & TỰ VỆ (ANTI-ANALYSIS)

Để ngăn chặn người dùng hoặc chuyên gia bảo mật phát hiện ra mã độc, lớp `NativeGuard` cài đặt 4 lớp phòng thủ:

1. **Chống Debugger (Anti-Debugging):**
   * Đọc trực tiếp tệp `/proc/self/status` của Linux, tìm dòng `TracerPid:`.
   * Gọi `android.os.Debug.isDebuggerConnected()`. Nếu phát hiện có debugger gắn vào app, nó lập tức từ chối giải mã kho secrets và treo chức năng.
2. **Chống Giả lập (Anti-Emulator):**
   * Quét toàn bộ thông tin phần cứng (`Build.FINGERPRINT`, `Build.MODEL`, `Build.HARDWARE`).
   * Chặn chạy trên: `bluestacks`, `nox`, `ldplayer`, `mumu`, `genymotion`, `goldfish`, `ranchu`, `vbox86`.
3. **Chống can thiệp bộ nhớ (Anti-Hooking):**
   * Quét `/proc/self/maps` tìm vết tích của công cụ phân tích động **Frida** (`re.frida.Helper`).
   * Kiểm tra sự tồn tại của framework **Xposed** (`XposedBridge`, `XposedHelpers`) và **Substrate**.
4. **Phát hiện Root (Root Detection):**
   * Quét 12 đường dẫn nhị phân `su`, `Superuser.apk`, `magisk`, `/sbin/.magisk`.

---

## 5. GIẢI MÃ CÁC ENDPOINT VÀ DỊCH VỤ TÍCH HỢP

Lớp `StringCipher` sử dụng giải thuật biến đổi byte:
$$\text{ASCII} = ((Byte - 7) \oplus \text{0x5A}) \ \& \ \text{0xFF}$$

Toàn bộ các URL ẩn giấu đã được giải mã thành công:

| Tên biến | Chuỗi mã hóa (Hex) | URL giải mã hoàn chỉnh |
| :--- | :--- | :--- |
| `discordRegister` | `3935353130677c7c453a30403c2f457b...` | `https://discord.com/register` |
| `cyberTempBase` | `3935353130677c7c42313a7b402a3f46...` | `https://api.cybertemp.xyz` |
| `duckMailBase` | `3935353130677c7c42313a7b45364038...` | `https://api.duckmail.sbs` |
| `mailTmBase` | `3935353130677c7c42313a7b3e423a3d...` | `https://api.mail.tm` |
| `nonecapBase` | `3935353130677c7c42313a7b3b3c3b46...` | `https://api.nonecap.com/v1` |

### Các API giải Captcha & Dịch vụ ngoài:
* **Captcha Solvers:** 2Captcha, AZCaptcha, CapMonster Cloud, CapSolver, NopeCHA, NoneCap, Google Speech-to-Text Recognition API.
* **SMS & Mail Services:** Guerrilla Mail, TempMail.lol, Receive-SMS (`receive-smss.com`), SMSReceiveFree.

---

## 6. ĐÁNH GIÁ TÍNH KHẢ THI CHUYỂN ĐỔI SANG PYTHON/JS

### Kết luận kỹ thuật: **KHÔNG THỂ BIÊN DỊCH TRỰC TIẾP 1:1 SANG 1 FILE DUY NHẤT**

1. **Phụ thuộc Native Android WebView:**
   App đăng ký tài khoản dựa trên tương tác giao diện với engine WebKit của Android (`android.webkit.WebView`). Một file script Python hoặc Node.js chạy ngầm bằng HTTP Requests đơn thuần **không thể** vượt qua lớp bảo vệ Cloudflare và TLS Fingerprint của Discord nếu không có trình duyệt hoàn chỉnh.
2. **Kiến trúc phân tán lớn:**
   Dự án gồm 165 file Java quản lý Database (`Room ORM`), luồng bất đồng bộ (`Coroutines`) và bộ giải mã âm thanh TensorFlow Lite. Chuyển đổi sang PC đòi hỏi phải viết lại một dự án phần mềm hoàn toàn mới từ số 0 bằng các framework tự động hóa trình duyệt (như Playwright/Selenium).

---

## 7. KHUYẾN NGHỊ VÀ HƯỚNG BÀN GIAO CHO KHÁCH HÀNG

1. **Bàn giao gói mã nguồn dịch ngược (Deliverable Package):**
   Bàn giao thư mục mã nguồn sạch gồm 165 tệp tin Java tại thư mục [`output/evs_generator_decompiled/`](file:///d:/THAY%20THẾ/deobf/output/evs_generator_decompiled/) kèm file `AndroidManifest.xml`. Đây là tài sản kỹ thuật cao nhất đã bóc tách từ file APK nhị phân.
2. **Cảnh báo thiệt hại cho khách hàng:**
   Thông báo cho khách hàng biết file APK họ giao thực chất là công cụ có cấy backdoor đánh cắp thông tin. Việc bạn phát hiện và cảnh báo sớm giúp khách hàng tránh được tổn thất mất toàn bộ tài khoản khi triển khai thực tế.
3. **Thương lượng lại phạm vi công việc:**
   Làm rõ với khách hàng rằng yêu cầu "convert tự động 1:1 sang 1 file Python" là không khả thi về mặt kỹ thuật do khác biệt nền tảng hệ điều hành. Báo cáo này là cơ sở vững chắc nhất để nghiệm thu phần việc phân tích/dịch ngược mã nguồn cho khách hàng.
