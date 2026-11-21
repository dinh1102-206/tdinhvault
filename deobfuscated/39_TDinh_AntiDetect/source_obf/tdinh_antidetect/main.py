# Author: tdinh cute
# TDinh Antidetect Browser Launcher v1.0
# Free, Offline & Unlimited Browser Profile Manager

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random

# Add local path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from core.db import ProfileDB, DEFAULT_UAS
from core.launcher import BrowserLauncher

class AntidetectApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TDinh Antidetect Launcher v1.0 — by tdinh cute")
        self.root.geometry("980x600")
        self.root.minsize(800, 500)
        self.root.configure(bg="#1e1e24")

        # Database & Launcher
        db_file = os.path.join(BASE_DIR, "data", "profiles.json")
        self.db = ProfileDB(db_file)
        self.launcher = BrowserLauncher(BASE_DIR)

        self._setup_style()
        self._build_ui()
        self._load_profiles()

    def _setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Configure Dark Table
        style.configure("Treeview",
            background="#25252d",
            foreground="#e0e0e0",
            rowheight=32,
            fieldbackground="#25252d",
            font=("Segoe UI", 10)
        )
        style.map("Treeview", background=[("selected", "#3d5afe")], foreground=[("selected", "#ffffff")])

        style.configure("Treeview.Heading",
            background="#18181f",
            foreground="#61afef",
            font=("Segoe UI", 10, "bold")
        )

    def _build_ui(self):
        # 1. Header Frame
        hdr = tk.Frame(self.root, bg="#18181f", height=65)
        hdr.pack(fill="x", side="top")
        
        lbl_title = tk.Label(hdr, text="⚡ TDinh Antidetect Browser Manager", font=("Segoe UI", 15, "bold"), fg="#61afef", bg="#18181f")
        lbl_title.pack(side="left", padx=20, pady=12)

        lbl_author = tk.Label(hdr, text="Free & Offline • Author: tdinh cute", font=("Segoe UI", 9), fg="#98c379", bg="#18181f")
        lbl_author.pack(side="right", padx=20, pady=15)

        # 2. Main Container
        main_frame = tk.Frame(self.root, bg="#1e1e24")
        main_frame.pack(fill="both", expand=True, padx=20, pady=15)

        # Toolbar
        toolbar = tk.Frame(main_frame, bg="#1e1e24")
        toolbar.pack(fill="x", side="top", pady=(0, 10))

        btn_launch = tk.Button(toolbar, text="🚀 KHỞI CHẠY (LAUNCH)", font=("Segoe UI", 10, "bold"), bg="#3d5afe", fg="#ffffff", activebackground="#536dfe", relief="flat", padx=15, pady=6, cursor="hand2", command=self.on_launch)
        btn_launch.pack(side="left", padx=(0, 8))

        btn_add = tk.Button(toolbar, text="➕ Tạo Profile mới", font=("Segoe UI", 10), bg="#2c313a", fg="#98c379", activebackground="#3e4451", relief="flat", padx=12, pady=6, cursor="hand2", command=self.on_add_dialog)
        btn_add.pack(side="left", padx=4)

        btn_del = tk.Button(toolbar, text="🗑️ Xóa", font=("Segoe UI", 10), bg="#2c313a", fg="#e06c75", activebackground="#3e4451", relief="flat", padx=12, pady=6, cursor="hand2", command=self.on_delete)
        btn_del.pack(side="left", padx=4)

        btn_open = tk.Button(toolbar, text="📂 Mở thư mục", font=("Segoe UI", 10), bg="#2c313a", fg="#abb2bf", activebackground="#3e4451", relief="flat", padx=12, pady=6, cursor="hand2", command=self.on_open_folder)
        btn_open.pack(side="left", padx=4)

        # Table
        columns = ("id", "name", "browser", "proxy", "canvas", "created_at")
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings", selectmode="browse")
        
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Tên Profile")
        self.tree.heading("browser", text="Trình duyệt")
        self.tree.heading("proxy", text="Proxy")
        self.tree.heading("canvas", text="Stealth Shield")
        self.tree.heading("created_at", text="Ngày tạo")

        self.tree.column("id", width=90, anchor="center")
        self.tree.column("name", width=220, anchor="w")
        self.tree.column("browser", width=110, anchor="center")
        self.tree.column("proxy", width=200, anchor="w")
        self.tree.column("canvas", width=120, anchor="center")
        self.tree.column("created_at", width=160, anchor="center")

        # Scrollbar
        scroll = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        # Double click to launch
        self.tree.bind("<Double-1>", lambda e: self.on_launch())

        # Status Bar
        self.status_bar = tk.Label(self.root, text="Sẵn sàng • Quản lý profile trình duyệt hoàn toàn miễn phí, độc lập.", font=("Segoe UI", 9), fg="#abb2bf", bg="#18181f", anchor="w", padx=15, pady=6)
        self.status_bar.pack(fill="x", side="bottom")

    def _load_profiles(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for p in self.db.get_all():
            proxy_display = p.get("proxy") or "Không dùng (IP gốc)"
            stealth = "🛡️ Đang bật" if p.get("canvas_noise", True) else "Tắt"
            self.tree.insert("", "end", values=(
                p["id"],
                p["name"],
                p.get("browser", "Chrome"),
                proxy_display,
                stealth,
                p.get("created_at", "")
            ))

    def on_launch(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Thông báo", "Vui lòng chọn 1 profile trong danh sách để khởi chạy!")
            return
        vals = self.tree.item(selected[0], "values")
        pid = vals[0]
        profile = next((p for p in self.db.get_all() if p["id"] == pid), None)
        if not profile:
            return
        
        try:
            self.launcher.launch(profile)
            self.status_bar.config(text=f"🚀 Đã khởi chạy Profile: {profile['name']} (ID: {pid})")
        except Exception as e:
            messagebox.showerror("Lỗi khởi chạy", str(e))

    def on_delete(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Thông báo", "Vui lòng chọn profile cần xóa!")
            return
        vals = self.tree.item(selected[0], "values")
        pid = vals[0]
        p_name = vals[1]
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa Profile: {p_name}?"):
            self.db.delete(pid)
            self._load_profiles()
            self.status_bar.config(text=f"🗑️ Đã xóa Profile: {p_name}")

    def on_open_folder(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Thông báo", "Vui lòng chọn profile để mở thư mục lưu trữ!")
            return
        pid = self.tree.item(selected[0], "values")[0]
        path = os.path.join(BASE_DIR, "profiles", pid)
        os.makedirs(path, exist_ok=True)
        os.system(f'explorer "{path}"')

    def on_add_dialog(self):
        dlg = tk.Toplevel(self.root)
        dlg.title("Tạo Profile mới — TDinh Antidetect")
        dlg.geometry("500x380")
        dlg.configure(bg="#21252b")
        dlg.transient(self.root)
        dlg.grab_set()

        tk.Label(dlg, text="Tên Profile:", font=("Segoe UI", 10), fg="#e0e0e0", bg="#21252b").pack(anchor="w", padx=30, pady=(15, 2))
        ent_name = tk.Entry(dlg, font=("Segoe UI", 10), bg="#282c34", fg="#ffffff", insertbackground="white")
        ent_name.insert(0, f"Profile {len(self.db.get_all()) + 1:02d}")
        ent_name.pack(fill="x", padx=30, pady=(0, 10))

        tk.Label(dlg, text="Trình duyệt lõi:", font=("Segoe UI", 10), fg="#e0e0e0", bg="#21252b").pack(anchor="w", padx=30, pady=(5, 2))
        cb_browser = ttk.Combobox(dlg, values=["Chrome", "Edge"], state="readonly")
        cb_browser.set("Chrome")
        cb_browser.pack(fill="x", padx=30, pady=(0, 10))

        tk.Label(dlg, text="Proxy (IP:Port hoặc IP:Port:User:Pass - để trống nếu dùng IP gốc):", font=("Segoe UI", 10), fg="#e0e0e0", bg="#21252b").pack(anchor="w", padx=30, pady=(5, 2))
        ent_proxy = tk.Entry(dlg, font=("Segoe UI", 10), bg="#282c34", fg="#ffffff", insertbackground="white")
        ent_proxy.pack(fill="x", padx=30, pady=(0, 10))

        var_stealth = tk.BooleanVar(value=True)
        chk_stealth = tk.Checkbutton(dlg, text="Kích hoạt Stealth Shield (Chống phát hiện Canvas/WebGL/WebRTC)", variable=var_stealth, font=("Segoe UI", 9), fg="#61afef", bg="#21252b", selectcolor="#282c34", activebackground="#21252b")
        chk_stealth.pack(anchor="w", padx=30, pady=(5, 15))

        def save():
            name = ent_name.get().strip() or "Unnamed Profile"
            b = cb_browser.get()
            proxy = ent_proxy.get().strip()
            stealth = var_stealth.get()
            self.db.add(name=name, browser=b, proxy=proxy, canvas_noise=stealth)
            self._load_profiles()
            dlg.destroy()
            self.status_bar.config(text=f"✔ Đã tạo mới Profile: {name}")

        btn_save = tk.Button(dlg, text="Lưu & Tạo Profile", font=("Segoe UI", 10, "bold"), bg="#98c379", fg="#21252b", activebackground="#7eb365", relief="flat", pady=6, cursor="hand2", command=save)
        btn_save.pack(fill="x", padx=30, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = AntidetectApp(root)
    root.mainloop()
