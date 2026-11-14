# Author: tdinh cute
# TDinh Antidetect Extension Generator

import os
import json

def generate_stealth_extension(ext_dir: str, canvas_seed: int = 12345, audio_seed: int = 54321):
    os.makedirs(ext_dir, exist_ok=True)
    
    manifest = {
        "version": "1.0.0",
        "manifest_version": 3,
        "name": "TDinh Antidetect Shield",
        "description": "Stealth fingerprint protector by tdinh cute",
        "content_scripts": [
            {
                "matches": ["<all_urls>"],
                "js": ["content.js"],
                "run_at": "document_start",
                "world": "MAIN"
            }
        ]
    }
    
    # JavaScript that injects subtle noise into Canvas, Audio and WebGL
    content_js = f"""// TDinh Stealth Shield - Antidetect Engine
(function() {{
    const CANVAS_SEED = {canvas_seed};
    const AUDIO_SEED = {audio_seed};
    
    // 1. Remove navigator.webdriver
    try {{
        Object.defineProperty(navigator, 'webdriver', {{
            get: () => undefined,
            configurable: true
        }});
    }} catch (e) {{}}

    // 2. Canvas Noise Injection
    try {{
        const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
        HTMLCanvasElement.prototype.toDataURL = function(type) {{
            const ctx = this.getContext('2d');
            if (ctx && this.width > 0 && this.height > 0) {{
                try {{
                    const imgData = ctx.getImageData(0, 0, Math.min(10, this.width), Math.min(10, this.height));
                    for (let i = 0; i < imgData.data.length; i += 4) {{
                        imgData.data[i] = (imgData.data[i] ^ (CANVAS_SEED & 0x03));
                    }}
                    ctx.putImageData(imgData, 0, 0);
                }} catch (err) {{}}
            }}
            return originalToDataURL.apply(this, arguments);
        }};

        const originalGetImageData = CanvasRenderingContext2D.prototype.getImageData;
        CanvasRenderingContext2D.prototype.getImageData = function() {{
            const res = originalGetImageData.apply(this, arguments);
            for (let i = 0; i < Math.min(res.data.length, 32); i += 4) {{
                res.data[i] = (res.data[i] ^ (CANVAS_SEED & 0x01));
            }}
            return res;
        }};
    }} catch (e) {{}}

    // 3. AudioContext Noise
    try {{
        const originalGetChannelData = AudioBuffer.prototype.getChannelData;
        AudioBuffer.prototype.getChannelData = function() {{
            const buffer = originalGetChannelData.apply(this, arguments);
            for (let i = 0; i < Math.min(buffer.length, 64); i += 8) {{
                buffer[i] += (AUDIO_SEED % 5) * 0.0000001;
            }}
            return buffer;
        }};
    }} catch (e) {{}}

    // 4. WebGL Vendor & Renderer spoofing
    try {{
        const getParameter = WebGLRenderingContext.prototype.getParameter;
        WebGLRenderingContext.prototype.getParameter = function(param) {{
            // UNMASKED_VENDOR_WEBGL
            if (param === 37445) return 'Google Inc. (NVIDIA)';
            // UNMASKED_RENDERER_WEBGL
            if (param === 37446) return 'ANGLE (NVIDIA, NVIDIA GeForce RTX 3060 Direct3D11 vs_5_0 ps_5_0, D3D11)';
            return getParameter.apply(this, arguments);
        }};
    }} catch (e) {{}}
}})();
"""
    
    with open(os.path.join(ext_dir, 'manifest.json'), 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)
        
    with open(os.path.join(ext_dir, 'content.js'), 'w', encoding='utf-8') as f:
        f.write(content_js)
