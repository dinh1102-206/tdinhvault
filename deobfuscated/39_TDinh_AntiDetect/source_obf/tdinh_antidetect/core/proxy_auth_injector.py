# Author: tdinh cute
# Proxy Authentication Extension Generator

import os
import json

def generate_proxy_auth_extension(ext_dir: str, username: str, password: str):
    os.makedirs(ext_dir, exist_ok=True)
    manifest = {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "TDinh Proxy Auth",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version": "22.0.0"
    }
    
    background_js = f"""// TDinh Proxy Auth Handler
chrome.webRequest.onAuthRequired.addListener(
    function(details) {{
        return {{
            authCredentials: {{
                username: "{username}",
                password: "{password}"
            }}
        }};
    }},
    {{urls: ["<all_urls>"]}},
    ["blocking"]
);
"""
    with open(os.path.join(ext_dir, 'manifest.json'), 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)
    with open(os.path.join(ext_dir, 'background.js'), 'w', encoding='utf-8') as f:
        f.write(background_js)
