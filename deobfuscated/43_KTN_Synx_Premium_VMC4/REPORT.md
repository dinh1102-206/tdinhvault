# BÁO CÁO GIẢI MÃ & KIỂM ĐỊNH MÃ ĐỘC: FETCH_OBF.PY (KTN SYNX-PREMIUM v3.0)

- **Target File:** `input/fetch_obf.py` (Kích thước: 2,431,253 bytes)
- **Tên gốc xác định:** `test_obf_5kb.py - obfuscator test` (Benchmark / Kiểm thử Obfuscator ~5KB)
- **Công cụ Obfuscate:** **KTN VANISH CLUB - SYNX-PREMIUM v3.0** (`t.me/Synx_obf`, `synxpremium.asia`)
- **Chế độ bảo vệ:** `VMC4 · Tier-D VMP` (Custom Virtual Machine trong C Native DLL x64)
- **Kết quả kiểm định mã độc:** **SẠCH 100% (CLEAN)** - Không có Webhook Discord, không Stealer, không Mining, không Backdoor, không Persistence.

---

## 1. Cấu trúc các lớp bảo vệ (Architecture Analysis)

### Lớp 1: Anti-Tamper & Multi-stage Compression (Python Wrapper)
- Header kiểm tra SHA-256 toàn vẹn file.
- Payload chính được lưu trong biến unicode `按飍飩['Σ']` (717,386 bytes Base85).
- Pipeline giải nén:
  $$\text{Base85 Decode (573,950 B)} \longrightarrow \text{BZ2 Decompress (570,885 B)} \longrightarrow \text{Zlib Decompress (864,992 B)} \longrightarrow \text{marshal.loads}$$
- Kết quả thu được Code Object Python 3.12 chứa 845 constants (`co_consts`) và 78 hàm/tên biến bị làm rối.

### Lớp 2: Embedded Native C Extension (`_core.pyd`)
- Tại `co.co_consts[475]`: Chứa 1 file Windows PE x64 DLL nguyên vẹn kích thước 263,680 bytes.
- Module CPython Native tên `_core` (`cpython|3.12|64|le|win|x86_64|1`).
- Các hàm native export:
  - `vmp_run`: Điểm thực thi chính của Virtual Machine (nhận buffer payload đã giải mã và globals dict).
  - `vm_run`: Thực thi VMC4 boot program.
  - `harden`, `selfdebug`: Kiểm tra anti-debug (NtQueryInformationProcess, CheckRemoteDebuggerPresent, IsDebuggerPresent).
  - `tripwire_tag`, `tripwire_scan`: Kiểm tra anti-dumping bộ nhớ.

### Lớp 3: VMC4 Virtual Machine Engine & Bytecode Payload
- Tại `co.co_consts[844]`: Chứa VMC4 payload string mã hóa (464,185 ký tự).
- Hàm Python `deccaiditmemay_87` giải mã payload và cấu trúc bảng VMP (`itab`, `htab`, `lane_a`, `lane_b`, `btab`, `macros`, `code`).
- Bảng chuỗi (String Table) được mã hóa bằng phép biến đổi affine:
  $$\text{char} = ((v - k_{248}) \times k_{249} \pmod{65536}) \oplus ((i \times k_{250}) \pmod{65536})$$
  Với các khóa: $k_{248} = 30352$, $k_{249} = 56813$, $k_{250} = 49614$.

---

## 2. Toàn bộ logic mã nguồn gốc được phục hồi

Nội dung mã nguồn gốc là một bộ benchmark tính năng Python tổng hợp (được dùng để stress-test độ tương thích của VM):
1. **PRNG (LCG Algorithm):** Generator sinh số ngẫu nhiên tuyến tính ($state = (1103515245 \times state + 12345) \pmod{2^{31}-1}$).
2. **Quicksort:** Thuật toán phân hoạch chia để trị 3 nhánh sắp xếp mảng 12 phần tử.
3. **Memoization & Fibonacci:** Closure decorator lưu cache đệ quy tính $fib(20) = 6765$.
4. **Caesar Cipher:** Dịch chuyển ký tự Caesar text `'Obfuscator Test 2026!'` với bước nhảy 7.
5. **Hệ thống Hình học Hướng đối tượng (OOP Shapes):**
   - Lớp cơ sở `Shape` và các lớp kế thừa `Circle`, `Rectangle`, `Triangle` tính diện tích và chu vi theo công thức Heron.
   - Hàm `shape_report` thống kê tổng diện tích và hình lớn nhất.
6. **Máy trạng thái hữu hạn (FSM):** Quản lý chu trình trạng thái `idle` $\to$ `run` $\to$ `paused` $\to$ `stop`.
7. **Thống kê văn bản (Word Stats):** Đếm tần suất từ vựng, top 3 từ xuất hiện nhiều nhất và từ dài nhất.
8. **Dãy Collatz:** Đếm số bước hội tụ về 1 cho $n = 27$ (kết quả: 111 bước).
9. **Sàng số nguyên tố Eratosthenes:** Tìm các số nguyên tố $< 50$.
10. **XOR Cipher Roundtrip:** Kiểm tra tính toàn vẹn mã hóa/giải mã XOR đối xứng.

---

## 3. Kết luận kiểm tra an toàn
- **Mã độc:** Không phát hiện bất kỳ đoạn mã độc hại, token grabber, webhook, reverse shell hay persistence nào.
- **Tính toàn vẹn mã nguồn:** File deobfuscated chạy độc lập 100% trên Python 3.x chuẩn, không cần bất kỳ dependency bên ngoài hay native DLL nào.
