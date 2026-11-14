# Author: tdinh cute
# Research & Analysis by tdinh

# Báo Cáo Phân Tích & Giải Mã Mã Độc: `file 9app by tipi.exe`
**Chuyên gia phân tích / Thực hiện:** tdinh (`tdinh cute`)  
**Ngày báo cáo:** 11/11/2026  
**Mục tiêu phân tích:** [`input/file 9app by tipi.exe`](file:///d:/THAY%20THẾ/deobf/input/file%209app%20by%20tipi.exe)  
**Trạng thái xử lý:** Đã cô lập vào [`output/chua_file_co_ma_doc/file 9app by tipi.exe`](file:///d:/THAY%20THẾ/deobf/output/chua_file_co_ma_doc/file%209app%20by%20tipi.exe)

---

## 1. Tóm Tắt Tổng Quan (Executive Summary)

Tệp [`input/file 9app by tipi.exe`](file:///d:/THAY%20THẾ/deobf/input/file%209app%20by%20tipi.exe) là tệp thực thi mới nhất được gửi vào thư mục `input/`. Qua quá trình dịch ngược chuyên sâu, phát hiện đây là một trường hợp **tệp nhị phân bị lây nhiễm mã độc dạng Virus Siêu Đa Hình (Bi-Modal File Infector & Macro Hybrid Virus)** có chữ ký định danh **29A** (nhóm tác giả virus retro huyền thoại).

Máy tính của người tạo tệp ("tipi") đã bị nhiễm loại virus này. Khi phần mềm PyInstaller đóng gói công cụ `file 9app by tipi.exe`, virus đã can thiệp vào tiến trình ghi đĩa, ghi đè toàn bộ section `.reloc` và 776,704 byte đầu tiên của gói PyInstaller archive (bao gồm mã nguồn entry point `e` và các module bootstrap `pyimod01..04`, `struct`) bằng thân virus mã hóa đa hình.

Hệ thống đã **giải mã thành công toàn bộ 5 tầng bảo vệ**, bóc tách mã độc gốc `x64.dll` và trích xuất nguyên vẹn kịch bản vũ khí hóa VBA Macro / Office Weaponizer.

---

## 2. Thông Tin Tệp & Chỉ Số Nhận Diện (Hashes & Metadata)

| Thuộc tính | Tệp thực thi gốc (`file 9app by tipi.exe`) | Thân mã độc trích xuất (`restored_x64_virus.dll`) |
| :--- | :--- | :--- |
| **Kích thước** | 32,634,815 bytes (~31.1 MB) | 513,024 bytes (501 KB) |
| **MD5** | `320af6f444109fa53d977d6b3266c9ca` | `a02c0a643bb4cd5dcfec48cb37a21fc1` |
| **SHA256** | `e727310cd6bc235b6848271419300a315c5ecc3d4740b63bd95c26776ef49c21` | `0d1ef334ad9c1a131a8bc21cef8c4156cd96d04038a1ca1e65b0bc2408650a0f` |
| **Loại tệp** | PE32+ (x86-64) PyInstaller + Virus Carrier | PE32+ (x86-64) Dynamic Link Library (`x64.dll`) |
| **Chữ ký định danh**| **29A Hybrid PE-Infector & VBA Macro Virus** | **29A Weaponizer Engine** |

---

## 3. Kiến Trúc Lây Nhiễm & Chuỗi Giải Mã 5 Tầng (Multi-Stage Unpacking)

```
[ file 9app by tipi.exe ]
  │
  ├──► [PE Bootloader CRT Hook]
  │      Tại EntryPoint: 0x14000e774 gọi 0x140001038 (Trampoline)
  │      Nhảy qua chuỗi rẽ nhánh vào 0x1400036a3
  │
  ├──► [Tầng 1: 14-Byte Arithmetic Poly-Cipher]
  │      Vùng mã hóa: Offset 370,176 (0x5A600) -> 1,144,320 (0x117600), dài 774,144 byte.
  │      Thuật toán: Khối 14 byte chu kỳ lặp lại:
  │      - w0  = (w0 + 0xf083) & 0xffff (word)
  │      - dw1 = (dw1 - 0x14eca804) & 0xffffffff (dword)
  │      - b2  = (b2 + 0x45) & 0xff (byte)
  │      - b3  = (b3 + 0xed) & 0xff (byte)
  │      - w4  = (w4 + 0xb8b1) & 0xffff (word)
  │      - dw5 = (dw5 + 0x5008130e) & 0xffffffff (dword)
  │
  ├──► [Tầng 2: Reflective PEB Loader & Dynamic 32-Byte Key XOR]
  │      Nạp API động qua InMemoryOrderModuleList (PEB->Ldr).
  │      Trích xuất khóa 32 byte tại offset buffer: 0x1c .. 0x3c
  │      Khóa: 84 f6 66 90 71 38 98 ba 2e 0c 4b 30 85 51 66 c5 e3 a2 be ca bc 22 8f 05 b8 ad f5 06 4c 81 86 bc
  │      XOR giải mã payload nén tại offset 0x61b88, dài 0x56dfc (355,836 byte).
  │
  ├──► [Tầng 3: Giải Nén Native LZNT1 Compression]
  │      Gọi trực tiếp ntdll!RtlDecompressBuffer với format 0x0102
  │      (COMPRESSION_FORMAT_LZNT1 | COMPRESSION_ENGINE_MAXIMUM).
  │      Giải nén thành công khối dữ liệu 513,024 byte (Status: 0x0).
  │
  ├──► [Tầng 4: Tách Lớp Ngụy Trang PNG Fake Header]
  │      Mã độc ngụy trang phần đầu bằng magic \x89PNG\r\n\x1a\n\x10\x01\x00\x00...
  │      Khôi phục DOS Header: Viết b'MZ' tại offset 0, e_lfanew = 0x110 tại 0x3c, b'PE\0\0' tại 0x110.
  │
  └──► [Tầng 5: Payload Hoàn Chỉnh - x64.dll & VBA Macro]
         - Tệp PE DLL x64 hoàn chỉnh (kích thước 513,024 byte).
         - Xuất hàm (Export): a (Ordinal 1) tại RVA 0x5b80.
         - Kịch bản Macro vũ khí hóa tự động chèn vào tài liệu Word / Excel.
```

---

## 4. Hành Vi & Năng Lực Của Mã Độc (Threat Capabilities)

### 4.1. Cơ chế lây nhiễm nhị phân (PE Infector)
- Module `x64.dll` chứa một bộ phân tích định dạng PE nội tại (`RvaToSection`, `RvaToOffset`, duyệt `IMAGE_NT_HEADERS`, `IMAGE_SECTION_HEADER`).
- Tìm kiếm các tệp thực thi PE 64-bit trên máy tính nạn nhân.
- Lây nhiễm bằng cách ghi đè hoặc mở rộng section `.reloc`, đổi tên thành `UPX1 c`, thiết lập cờ thực thi `0xE0000040` (Read/Write/Execute).
- Chèn đoạn mã Stub tự giải mã đa hình (Polymorphic Decryptor) vào đầu điểm thực thi của tiến trình.

### 4.2. Cơ chế lây nhiễm tài liệu văn phòng (Office Macro Weaponizer)
- Tự động can thiệp vào các tệp Microsoft Word (`.docx`, `.docm`) và Excel (`.xlsx`, `.xlsm`).
- Tiêm cấu trúc OpenXML độc hại:
  1. `customXml/customXml1.xml`: Chứa Shellcode nhị phân được mã hóa dạng `bin.base64`.
  2. `customUI/customUI.xml`: Thiết lập cơ chế tự kích hoạt thông qua sự kiện `onLoad="OnRibbonLoad"`.
  3. `word/vbaProject.bin`: Chèn module VBA tự động chạy không cần người dùng bật Macro truyền thống.
- **Quy trình thực thi Shellcode từ Macro:**
  - Macro đọc chuỗi base64 từ `CustomXMLParts`.
  - Dùng `MSXML2.DOMDocument` chuyển đổi về mảng byte.
  - Cấp phát bộ nhớ thực thi bằng `VirtualAlloc(0, size, &H3000, &H4)` (PAGE_READWRITE).
  - Sao chép shellcode bằng `RtlMoveMemory`.
  - Đổi quyền bộ nhớ sang `PAGE_EXECUTE_READ` (&H20) bằng `VirtualProtect`.
  - Kích hoạt luồng chạy ngầm bằng `CreateThread`.

---

## 5. Tuyên Ngôn & Thơ Của Tác Giả Mã Độc (The 29A Manifesto)

Bên trong vùng nhớ `.data` của tệp `x64.dll`, tác giả đã để lại một thông điệp và bài thơ viết bằng tiếng Quốc tế ngữ (**Esperanto**) gửi trực tiếp đến các chuyên gia dịch ngược mã độc:

### Tuyên ngôn gửi chuyên gia phân tích:
> *' hej amiko esploristo, vi estas la unua, kiu iam vidis tiun ci teknikon en la naturo*  
> *' vi pensas, ke vi devas fari subskribon por ci? Mi faros polimorfan kodon morgau*  
> *' tamen, mi pensas, ke vi trovos tiun ci kodon, post multaj jaroj ekde la komenca plene nedetektebla eldono*  
> *' car vi neniam atendus hibridon de PE-infektilo kaj makroviruso*  
> *' kial mi estas tiel memfida? Ni diru ke tiu ci kodo estas iom facile detektebla, tamen neniu AV-motoro skanas VBA-rutinojn en tia kunteksto*  
> *' kaj vi estas blindaj nun en la epoko de moderna kiberkrimo*  
> *' car gi degeneris*  
> *' degeneris malsupren en nigran kuniklotruon*  
> *' kie dosierinfektilo kun DILDO atendas vin ciujn*  
> *' 29A*

**Bản dịch tiếng Việt:**
> *"Này người bạn điều tra, bạn là người đầu tiên từng thấy kỹ thuật này ngoài thực tế.*  
> *Bạn nghĩ bạn phải tạo chữ ký nhận diện cho nó ư? Ngày mai tôi sẽ viết mã đa hình.*  
> *Tuy nhiên, tôi nghĩ bạn sẽ chỉ tìm thấy đoạn mã này sau nhiều năm kể từ bản phát hành FUD (hoàn toàn không bị phát hiện) đầu tiên.*  
> *Bởi vì bạn sẽ không bao giờ ngờ tới một dạng lai giữa virus lây nhiễm PE và virus Macro.*  
> *Tại sao tôi lại tự tin đến vậy? Hãy nói rằng đoạn mã này khá dễ phát hiện, nhưng chẳng có engine diệt virus nào quét các hàm VBA trong ngữ cảnh này cả.*  
> *Và giờ các bạn đang mù quáng trong kỷ nguyên của tội phạm mạng hiện đại.*  
> *Bởi vì nó đã thoái hóa... Thoái hóa xuống tận cái hang thỏ đen tối...*  
> *Nơi một loại virus lây file đang chờ đón tất cả các bạn.*  
> *— 29A"*

---

## 6. Kết Quả Bàn Giao & Các Tệp Đã Xử Lý

1. **Tệp gốc đã cách ly an toàn:**
   - [`output/chua_file_co_ma_doc/file 9app by tipi.exe`](file:///d:/THAY%20THẾ/deobf/output/chua_file_co_ma_doc/file%209app%20by%20tipi.exe)
2. **Kịch bản giải mã tự động (Deobfuscator Script):**
   - [`output/tools_sach/deobfuscator_29a_infector.py`](file:///d:/THAY%20THẾ/deobf/output/tools_sach/deobfuscator_29a_infector.py) (Đã gắn header chuẩn `# Author: tdinh` | `# Decoded by: tdinh cute`).
3. **Mã độc phục hồi hoàn chỉnh (Clean Restored Payload):**
   - [`output/tools_sach/restored_x64_virus.dll`](file:///d:/THAY%20THẾ/deobf/output/tools_sach/restored_x64_virus.dll) (Kích thước: 513,024 bytes).
4. **Mã nguồn kịch bản VBA Macro trích xuất sạch:**
   - [`output/tools_sach/extracted_vba_runner.vba`](file:///d:/THAY%20THẾ/deobf/output/tools_sach/extracted_vba_runner.vba) (Đã gắn header chuẩn `' Author: tdinh` | `' Decoded by: tdinh cute`).
