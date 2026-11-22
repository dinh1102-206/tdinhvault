# BÁO CÁO GIẢI MÃ & KIỂM ĐỊNH MÃ ĐỘC: FETCH_OBF.PY (KTN SYNX-PREMIUM v3.0 VMC4)

- **Target File:** `input/fetch_obf.py` (Kích thước: 2,431,253 bytes)
- **Tên gốc xác định:** `fetch.py` (Discord Guild Member Scraper / Fetcher)
- **Công cụ Obfuscate:** **KTN VANISH CLUB - SYNX-PREMIUM v3.0** (`t.me/Synx_obf`, `synxpremium.asia`)
- **Chế độ bảo vệ:** `VMC4 · Tier-D VMP` (Custom Virtual Machine trong C Native DLL x64 & Python 3.12 Sealed Bytecode)
- **Kết quả kiểm định mã độc:** **SẠCH 100% (CLEAN)** - Công cụ Discord bot cào danh sách thành viên (Member Fetcher) xuất ra file TXT và CSV, không chứa Webhook lén, không Token Stealer, không Mining, không Backdoor.

---

## 1. Cấu trúc các lớp bảo vệ & Lỗ hổng kiến trúc

### Lớp 1: Anti-Tamper & Multi-stage Compression Stager
- Header kiểm tra SHA-256 toàn vẹn file, nếu sai sẽ khởi tạo 4 thread đốt 100% CPU.
- Payload chính được lưu trong biến unicode `按風風['Σ']` (717,386 bytes Base85).
- Pipeline giải nén:
  $$\text{Base85 Decode} \longrightarrow \text{BZ2 Decompress} \longrightarrow \text{Zlib Decompress} \longrightarrow \text{marshal.loads}$$
- Lỗ hổng: Mã băm SHA256 hoàn toàn tách biệt khỏi payload. Giải nén tĩnh bên ngoài không bị ảnh hưởng.

### Lớp 2: Sealed Bytecode CPython 3.12 & Bẫy Anti-Decompiler Out-of-Bounds
- Khối nhị phân chứa 1 root Code Object Python 3.12 chứa 847 constants và 78 hàm/tên biến bị làm rối.
- Cài cắm các lệnh `LOAD_FAST` vào `<module>` cấp cao nhằm kích hoạt lỗi `IndexError: tuple index out of range` trên các decompiler tiêu chuẩn.
- Lỗ hổng: Bẫy `LOAD_FAST` chỉ là dead-code sau lệnh nhảy. Định dạng Marshal Format 4 hoàn toàn nguyên vẹn.

### Lớp 3: String Table Encryption (Affine Modulo $Z_{65536}$)
- Tên module (`sys`, `hashlib`, `discord`, `zlib`), tên hàm hạt nhân đều mã hóa dưới dạng tuple số nguyên 16-bit.
- Giải mã qua hàm `sieusaoktn_68`:
  $$\text{char} = ((v - 30352) \times 56813 \pmod{65536}) \oplus ((i \times 49614) \pmod{65536})$$

### Lớp 4: Máy ảo VMC4 & Lỗ hổng Payload thật sự
- Payload máy ảo Base85 giải mã bằng PRNG Xorshift32 stream cipher với Seed tĩnh nằm ở header container.
- Máy ảo VMC4 27 opcode chạy 10,101 lệnh sinh ra 8 số nguyên bí mật:
  `keys = [824711383, 519189802, 1532045991, 812362389, 2955779481, 4222362540, 2487048097, 464730426]`
- **Lỗ hổng cốt lõi:** Toàn bộ mã nguồn Python gốc **không hề bị dịch sang máy ảo**, mà được mã hóa đối xứng bằng Stream Cipher SHA256 KDF và lưu dưới dạng Code Object CPython chuẩn xác 100% tại `_blob[9]` (`e3`)!
- Các hàm con được gán nhãn tiền tố `b'SYNXC'` được giải mã đối xứng qua `salt_key = SHA256(K + b'|C|' + salt)`.

---

## 2. Toàn bộ logic mã nguồn gốc được phục hồi (`fetch.py`)

File gốc là một công cụ cào danh sách thành viên máy chủ Discord (Member Fetcher/Scraper):
1. **Khởi tạo và cấu hình:**
   - Đọc cấu hình hoặc hỏi người dùng nhập `Bot token`, `Guild (server) ID`, và tùy chọn có bao gồm bot hay không (`include_bot`).
   - Cấu hình Discord Intents (`guilds = True`, `members = True`), prefix `!`.
2. **Thuật toán cào danh sách thành viên (`run`):**
   - Phân trang tuần tự với `BATCH_SIZE = 1000` thông qua generator bất đồng bộ `guild.fetch_members(limit=BATCH_SIZE, after=last)`.
   - Lưu trữ danh sách `all_ids` (tập hợp set ID thành viên duy nhất) và `all_members` (ánh xạ ID -> `(username, tag)`).
   - Đo lường thời gian thực thi bằng `time.perf_counter()`.
   - Cảnh báo độ lệch nếu `approximate_member_count > len(all_ids)` do giới hạn cache Discord.
3. **Xuất báo cáo dữ liệu:**
   - Tạo dấu thời gian `ts = datetime.now().strftime('%Y%m%d_%H%M%S')`.
   - Xuất danh sách ID ra file TXT: `member_ids_{ts}.txt`.
   - Xuất chi tiết `id,username,tag` ra file CSV UTF-8 with BOM: `members_{ts}.csv`.
   - In 5 ID mẫu ra màn hình console và tự động đóng phiên làm việc (`bot.close()`).

---

## 3. Kết luận kiểm tra an toàn
- **Mã độc:** SẠCH 100% (CLEAN).
- Không chứa token grabber, không stealer, không kết nối server ngầm bên ngoài ngoài Discord API chính thức.
- File sạch sau khi deobfuscate hoàn chỉnh:
  `tdinhvault/deobfuscated/43_KTN_Synx_Premium_VMC4/fetch_deobfuscated.py`
