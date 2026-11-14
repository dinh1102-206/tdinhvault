# Author: tdinh cute
# Research & Analysis by tdinh

# BÁO CÁO PHÂN TÍCH VÀ DỊCH NGƯỢC (REVERSE ENGINEERING AUDIT REPORT)
## MỤC TIÊU: QuasarTool (11).rar & QuasarTuner.exe
> **Author:** tdinh | **Decoded by:** tdinh cute  
> **Thời gian phân tích:** 14/11/2026  
> **Đối tượng:** `Quasar Loader.exe` (PyInstaller) & `QuasarTuner.exe` (Nuitka Onefile C-compiled)

---

### 1. TỔNG QUAN VÀ PHÂN LOẠI MỤC TIÊU

Người dùng cung cấp 2 file mới trong thư mục `input\`:
1. **`QuasarTool (11).rar`** (8.8 MB):
   - Bên trong chứa file **`Quasar Loader.exe`** (8.99 MB).
   - Đóng gói bằng: **PyInstaller (Python 3.14)**.
2. **`QuasarTuner.exe`** (9.31 MB):
   - Đóng gói bằng: **Nuitka Onefile (C-compiled Python 3.12 + Zstandard Compressed Payload)**.
   - Bên trong chứa payload chính **`QuasarCT.dll`** (9.44 MB) và môi trường runtime đồ họa **Tkinter/Tcl**.

---

### 2. KẾT QUẢ DỊCH NGƯỢC: QUASAR LOADER (`QL.py`)

- **Bản chất**: Trình tải giao diện dòng lệnh (CLI/TUI) giúp người dùng chọn tải bản TUI hoặc GUI của bộ công cụ Quasar.
- **Tác giả / Dev**: `vhs8 + f1eq`
- **Phiên bản**: `1.0.0`
- **Cộng đồng Discord**: `discord.gg/quas`
- **Đường dẫn tải nguồn (Releases)**:
  - TUI Version: `https://github.com/quasartool/QuasarToolTUI/releases/download/QuasarTool/QuasarTool.rar`
  - GUI Version: `https://github.com/quasartool/QuasarToolGUI/releases/download/QuasarTool/QuasarTool.rar`
- **Mã nguồn gốc đã được phục hồi 100%**: Đã lưu tại [`d:\THAY THẾ\deobf\output\tools_sach\QL_decompiled.py`](file:///d:/THAY%20THẾ/deobf/output/tools_sach/QL_decompiled.py).

---

### 3. KẾT QUẢ DỊCH NGƯỢC: QUASAR TUNER (`QuasarTuner.exe` / `QuasarCT.dll`)

#### A. Kiến trúc Đóng gói (Packaging & Decompression)
- `QuasarTuner.exe` sử dụng bộ nén **Zstandard (ZSTD)** với signature header `'KAY'` tại offset `0x20650`.
- Đã giải nén thành công archive dung lượng **32,798,059 bytes** (~32.8 MB) chứa **947 files** tại [`d:\THAY THẾ\deobf\output\quasartuner_unpacked`](file:///d:/THAY%20THẾ/deobf/output/quasartuner_unpacked).
- Trọng tâm xử lý logic nằm ở thư viện nhị phân C-Python: **`QuasarCT.dll`** (9.44 MB).

#### B. Cơ chế Xác thực Bản quyền & HWID (License Gate)
- **Máy chủ xác thực (Auth Server)**: `https://duz0.pythonanywhere.com`
- **Cửa hàng License**: `https://quasarshop.base44.app`
- **Khóa bí mật / Hash Salt**: `90f78cca449189e5c6f4eddb7cf7e1f631ea02becd89b1ae`
- **File lưu license cục bộ**: `_license.json`
- **Các gói bản quyền**:
  - `Week`: 7 ngày
  - `Month`: 30 ngày
  - `Lifetime`: Vĩnh viễn
- **Thuật toán sinh HWID (`get_hwid`)**:
  - Đọc `MachineGuid` từ Registry: `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Cryptography`.
  - Kết hợp thông tin phần cứng ổ đĩa (Disk Serial), CPU ID, và trạng thái pin (`Win32_Battery`).
  - Đóng gói dạng JSON nén rồi băm SHA-256 đối chiếu với server.

#### C. Các tính năng Tối ưu hóa Game & Hệ thống (Tweaks & Features)
1. **FPS Overlay (HUD hiển thị FPS trong game)**:
   - Module `FpsHud`: Tạo cửa sổ click-through đè lên game.
   - Tích hợp **Intel PresentMon** (tải tự động từ `https://api.github.com/repos/GameTechDev/PresentMon/releases/latest`). Đo frame time qua Event Tracing for Windows (ETW) nên không can thiệp bộ nhớ game (an toàn, không bị Anticheat ban).
2. **Tối ưu hóa Windows Registry**:
   - Vô hiệu hóa tính năng bóp hiệu năng nguồn điện CPU: `SYSTEM\CurrentControlSet\Control\Power\PowerThrottling`.
   - Tối ưu hóa độ ưu tiên luồng xử lý CPU (Win32PrioritySeparation): `SYSTEM\CurrentControlSet\Control\PriorityControl`.
   - Tắt thu thập dữ liệu / Telemetry ngầm: `SOFTWARE\Policies\Microsoft\Windows\DataCollection`.
   - Vô hiệu hóa các Windows Services không cần thiết để giảm độ trễ (latency).

---

### 4. DANH MỤC FILE KẾT QUẢ ĐÃ TRÍCH XUẤT

| File / Thư mục | Mô tả |
| :--- | :--- |
| [`QL_decompiled.py`](file:///d:/THAY%20THẾ/deobf/output/tools_sach/QL_decompiled.py) | Toàn bộ mã nguồn Python gốc của `Quasar Loader.exe` (100% sạch, chạy độc lập). |
| [`quasartuner_unpacked\`](file:///d:/THAY%20THẾ/deobf/output/quasartuner_unpacked) | 947 file payload giải nén hoàn chỉnh từ Nuitka Onefile của `QuasarTuner.exe`. |
| [`QuasarCT.dll`](file:///d:/THAY%20THẾ/deobf/output/quasartuner_unpacked/QuasarCT.dll) | Core C-extension DLL chứa toàn bộ thuật toán tối ưu và kiểm tra bản quyền. |
| [`QUASAR_TOOL_AUDIT_REPORT.md`](file:///d:/THAY%20THẾ/deobf/output/reports/QUASAR_TOOL_AUDIT_REPORT.md) | Báo cáo chi tiết kỹ thuật này. |
