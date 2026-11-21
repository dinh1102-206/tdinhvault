# Author: tdinh
# Decoded by: tdinh cute
"""
Automated Extractor & Deobfuscator for 29A PE-Infector & VBA Hybrid Virus
Target: input/file 9app by tipi.exe
Extracts:
1. Stage 1 Polymorphic Decryption (14-byte arithmetic sequence)
2. Stage 2 Key Extraction & XOR Decryption (32-byte dynamic key)
3. Stage 3 Native LZNT1 Decompression (ntdll!RtlDecompressBuffer)
4. Stage 4 Restored PE DLL payload (x64.dll) and embedded VBA macro
"""

import os
import struct
import ctypes

def extract_29a_payload(target_exe_path, output_dll_path, output_vba_path):
    print(f"[*] Processing infected executable: {target_exe_path}")
    if not os.path.exists(target_exe_path):
        raise FileNotFoundError(f"Target not found: {target_exe_path}")

    # Stage 1: Read encrypted carrier body from offset 370176 (0x5A600)
    with open(target_exe_path, 'rb') as f:
        f.seek(370176)
        data = bytearray(f.read(0xbd000)) # 774,144 bytes

    print("[*] Stage 1: Reversing 14-byte arithmetic poly-cipher...")
    for i in range(0, len(data), 14):
        w0 = (struct.unpack('<H', data[i:i+2])[0] + 0xf083) & 0xffff
        data[i:i+2] = struct.pack('<H', w0)
        dw1 = (struct.unpack('<I', data[i+2:i+6])[0] - 0x14eca804) & 0xffffffff
        data[i+2:i+6] = struct.pack('<I', dw1)
        data[i+6] = (data[i+6] + 0x45) & 0xff
        data[i+7] = (data[i+7] + 0xed) & 0xff
        w4 = (struct.unpack('<H', data[i+8:i+10])[0] + 0xb8b1) & 0xffff
        data[i+8:i+10] = struct.pack('<H', w4)
        dw5 = (struct.unpack('<I', data[i+10:i+14])[0] + 0x5008130e) & 0xffffffff
        data[i+10:i+14] = struct.pack('<I', dw5)

    # Stage 2: Extract 32-byte dynamic XOR key and decrypt payload
    print("[*] Stage 2: Extracting 32-byte key & XOR decrypting payload...")
    key32 = bytes(data[0x1c : 0x3c])
    raw_payload = data[0x61b88 : 0x61b88 + 0x56dfc]
    decrypted_payload = bytearray(len(raw_payload))
    for i in range(len(raw_payload)):
        decrypted_payload[i] = raw_payload[i] ^ key32[i % 32]

    # Stage 3: LZNT1 Decompression via ntdll!RtlDecompressBuffer
    print("[*] Stage 3: Decompressing LZNT1 payload buffer...")
    ntdll = ctypes.windll.ntdll
    fmt = 0x0102 # COMPRESSION_FORMAT_LZNT1 | COMPRESSION_ENGINE_MAXIMUM
    uncmprsd_size = len(raw_payload) * 3
    uncmprsd_buf = ctypes.create_string_buffer(uncmprsd_size)
    final_size = ctypes.c_ulong(0)

    status = ntdll.RtlDecompressBuffer(
        ctypes.c_ushort(fmt),
        uncmprsd_buf,
        ctypes.c_ulong(uncmprsd_size),
        (ctypes.c_char * len(decrypted_payload)).from_buffer(decrypted_payload),
        ctypes.c_ulong(len(decrypted_payload)),
        ctypes.byref(final_size)
    )

    if status != 0:
        raise RuntimeError(f"RtlDecompressBuffer failed with status: {hex(status & 0xffffffff)}")

    decomp = bytearray(uncmprsd_buf[:final_size.value])
    print(f"[+] Decompressed {final_size.value} bytes successfully!")

    # Stage 4: Reconstruct PE DOS stub (replace fake PNG header)
    print("[*] Stage 4: Reconstructing PE headers for hidden x64.dll...")
    decomp[0:2] = b'MZ'
    decomp[0x3c:0x40] = struct.pack('<I', 0x110)
    decomp[0x110:0x114] = b'PE\x00\x00'

    os.makedirs(os.path.dirname(output_dll_path), exist_ok=True)
    with open(output_dll_path, 'wb') as f:
        f.write(decomp)
    print(f"[+] Restored x64.dll saved to: {output_dll_path}")

    # Extract embedded VBA macro source
    print("[*] Extracting embedded VBA macro source...")
    vba_marker = b'#If Win64 Then'
    pos = decomp.find(vba_marker)
    if pos != -1:
        end_pos = decomp.find(b'End Sub', pos) + 7
        vba_code = decomp[pos:end_pos].decode('latin1', errors='ignore')
        with open(output_vba_path, 'w', encoding='utf-8') as f:
            f.write("' Author: tdinh\n' Decoded by: tdinh cute\n\n" + vba_code)
        print(f"[+] Clean VBA macro runner saved to: {output_vba_path}")

if __name__ == '__main__':
    extract_29a_payload(
        'output/chua_file_co_ma_doc/file 9app by tipi.exe',
        'output/tools_sach/restored_x64_virus.dll',
        'output/tools_sach/extracted_vba_runner.vba'
    )
