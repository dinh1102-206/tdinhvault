# Author: tdinh cute
# Profile Database Management

import os
import json
import uuid
import time
import random

DEFAULT_UAS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
]

class ProfileDB:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.profiles = []
        self._load()

    def _load(self):
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, 'r', encoding='utf-8') as f:
                    self.profiles = json.load(f)
            except Exception:
                self.profiles = []
        else:
            # Seed 2 sample profiles
            self.profiles = [
                {
                    "id": str(uuid.uuid4())[:8],
                    "name": "Profile 01 (Clean)",
                    "browser": "Chrome",
                    "proxy": "",
                    "user_agent": DEFAULT_UAS[0],
                    "canvas_noise": True,
                    "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
                },
                {
                    "id": str(uuid.uuid4())[:8],
                    "name": "Profile 02 (Stealth)",
                    "browser": "Chrome",
                    "proxy": "",
                    "user_agent": DEFAULT_UAS[1],
                    "canvas_noise": True,
                    "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
                }
            ]
            self._save()

    def _save(self):
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(self.profiles, f, indent=2, ensure_ascii=False)

    def get_all(self):
        return self.profiles

    def add(self, name: str, browser: str = "Chrome", proxy: str = "", user_agent: str = None, canvas_noise: bool = True):
        pid = str(uuid.uuid4())[:8]
        if not user_agent:
            user_agent = random.choice(DEFAULT_UAS)
        item = {
            "id": pid,
            "name": name,
            "browser": browser,
            "proxy": proxy.strip(),
            "user_agent": user_agent,
            "canvas_noise": canvas_noise,
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.profiles.append(item)
        self._save()
        return item

    def delete(self, pid: str):
        self.profiles = [p for p in self.profiles if p["id"] != pid]
        self._save()

    def update(self, pid: str, data: dict):
        for p in self.profiles:
            if p["id"] == pid:
                p.update(data)
                break
        self._save()
