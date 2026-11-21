# Author: tdinh cute
# Research & Analysis by tdinh

# 📊 BÁO CÁO PHÂN TÍCH KIẾN TRÚC KỸ THUẬT: GPM LOGIN GLOBAL (v5.1.6-STABLE)

## 1. Thông tin tổng quan (Software Overview)
- **Tên phần mềm**: GPMLoginGlobal Setup (GPM-Login)
- **Phiên bản**: `5.1.6-stable`
- **Nhà phát triển**: `gpmsoftwares.com` / `gpmloginapp.com`
- **Tập tin nguồn**: `input/GPMLoginGlobal_setup_latest.exe` (596,648,032 bytes ~ 596.6 MB)
- **Bộ đóng gói cài đặt**: Inno Setup 7.0.0 Unicode (`Inno Setup Setup Data 7.0.0.3`)
- **Mật khẩu giải mã gói cài đặt**: `gpmsoftwares.com` (Được nhúng trong Pascal Script `CompiledCode.bin`)
- **Thư mục trích xuất**: [`output/gpmlogin_extracted/app/{app}`](file:///d:/THAY%20THẾ/deobf/output/gpmlogin_extracted/app/{app})

---

## 2. Kiến trúc ứng dụng (Application Architecture)

### 2.1. Nền tảng cốt lõi (.NET 8 Native AOT)
- **File thực thi chính**: `GPMLoginGlobal.exe` (100,859,696 bytes ~ 100.8 MB).
- **Công nghệ biên dịch**: **.NET Native AOT (Ahead-of-Time compilation)** trên kiến trúc `x86_64` Windows.
  - Mã nguồn C# được biên dịch trực tiếp sang mã máy (Machine code) trong section `.text` (28.2 MB).
  - Không sử dụng máy ảo CLR runtime truyền thống (`IMAGE_DIRECTORY_ENTRY_COM_DESCRIPTOR = 0`), giúp tối ưu hóa hiệu năng khởi động và tăng cường khả năng bảo vệ mã nguồn trước các công cụ decompiler thông thường (như dnSpy, ILSpy).
- **Framework giao diện (UI Framework)**:
  - Sử dụng **Avalonia UI** kết hợp thư viện đồ họa **SkiaSharp** (`libSkiaSharp.dll`), **HarfBuzzSharp** (`libHarfBuzzSharp.dll`) và OpenGL ES (`av_libglesv2.dll`).

### 2.2. Cơ sở dữ liệu cục bộ & Mã hóa
- **Thư viện SQLite**: `e_sqlite3.dll` quản lý dữ liệu profile, cookie, extension và lịch sử proxy.
- **Thư viện mật mã học**: `libsodium.dll` cung cấp các thuật toán mã hóa hiện đại (ChaCha20-Poly1305, Ed25519) để bảo vệ thông tin tài khoản người dùng lưu trên máy.

---

## 3. Các thành phần bổ trợ (Auxiliary Tools)

1. **`Tools/GPMLogin.Tools.Win.exe` (Bộ đồng bộ thao tác đa luồng)**:
   - Viết bằng C# .NET Framework (CLR 4.0), sử dụng file native `SyncHook.dll`.
   - Cài đặt các hook hệ thống: `SetWindowsHookEx`, `SetWinEventHook` để bắt sự kiện chuột và bàn phím.
   - Nhân bản (mirror) thao tác của người dùng sang hàng loạt cửa sổ trình duyệt đang chạy cùng lúc (`- GPM-Browser`).

2. **`Plugins/IpV6Creator/Ipv6Service.exe`**:
   - Dịch vụ nền hỗ trợ tạo, gán và quản lý mạng proxy IPv6 cho các phiên duyệt web độc lập.

3. **`Elevator.exe` & `Restarter.exe`**:
   - Quản lý nâng quyền UAC (Administrator elevation) và cơ chế tự khởi động lại phần mềm khi cập nhật phiên bản mới.

---

## 4. Hệ sinh thái Proxy & Antidetect Fingerprint

### 4.1. Tích hợp mạng lưới Proxy đối tác
GPM-Login tích hợp sẵn cấu hình kết nối API của hơn 20 nhà cung cấp dịch vụ proxy tại Việt Nam và quốc tế:
- `tinproxy.com`, `vnproxy.com`, `suiproxy.com`, `rotaproxy.com`, `m2proxy.com`
- `kiotproxy.com`, `proxyxoay.org`, `proxyxoay.shop`, `tmproxy.com`, `wwproxy.com`
- `ipgeo.gologin.com` (Định vị Geolocation theo cơ sở dữ liệu GoLogin)

### 4.2. Cơ chế giả lập dấu vân tay trình duyệt (Fingerprint Emulation)
Hệ thống sử dụng các thuật toán giả lập sâu vào nhân Chromium:
- **Canvas & WebGL**: Thêm nhiễu ngẫu nhiên (`noise_global_alpha`, `noise_shadow_blur`, `noise_shadow_offset`).
- **WebRTC**: Hỗ trợ 4 chế độ xử lý IP (Real IP, Disabled, Proxy IP, Fixed Public IP).
- **Timezone & Geolocation**: Tự động tính toán IANA Timezone và kinh độ/vĩ độ theo địa chỉ IP của proxy được gán.
- **System Fonts**: Tích hợp sẵn bộ hơn 400 font chữ (Windows & MacOS) trong thư mục `Assets/Data/Fonts` để tùy biến font fingerprint theo từng hệ điều hành.

---
*Báo cáo phân tích kỹ thuật hoàn thành bởi tdinh cute.*
