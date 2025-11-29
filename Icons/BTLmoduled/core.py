# ------------------ FILE: core.py ------------------
"""
core.py
Temel yardımcı fonksiyonlar, feature-detection, güvenli image loader
"""
import os
import sys
import time
import subprocess
import getpass
import platform
import threading
from pathlib import Path
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except Exception:
    Image = ImageTk = None
    PIL_AVAILABLE = False
try:
    import pygame
    PYGAME_AVAILABLE = True
except Exception:
    pygame = None
    PYGAME_AVAILABLE = False
try:
    import psutil
    PSUTIL_AVAILABLE = True
except Exception:
    psutil = None
    PSUTIL_AVAILABLE = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICONS_DIR = os.path.join(BASE_DIR, "Icons")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
os.makedirs(ICONS_DIR, exist_ok=True)
os.makedirs(ASSETS_DIR, exist_ok=True)

_image_refs = []


def load_image_as_tk(path, size=(64,64)):
    """Güvenli image yükleyici: Pillow varsa kullan, yoksa tkinter.PhotoImage ile dene."""
    if not path:
        return None
    try:
        if PIL_AVAILABLE and os.path.isfile(path):
            img = Image.open(path).convert("RGBA")
            img.thumbnail(size)
            tkimg = ImageTk.PhotoImage(img)
            _image_refs.append(tkimg)
            return tkimg
        else:
            if os.path.isfile(path):
                import tkinter as tk
                tkimg = tk.PhotoImage(file=path)
                _image_refs.append(tkimg)
                return tkimg
    except Exception:
        pass
    return None


def safe_start(path):
    try:
        if sys.platform.startswith("win"):
            os.startfile(path)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])
    except Exception:
        try:
            import tkinter as tk
            from tkinter import messagebox
            messagebox.showerror("Hata", f"Açma başarısız: {path}")
        except Exception:
            print("Açma başarısız:", path)


def _safe_run_and_decode(cmd_list):
    try:
        proc = subprocess.run(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False)
        out_bytes = proc.stdout or b""
    except Exception:
        return ""
    encodings = ('utf-8', 'cp1254', 'cp850', 'cp437', 'latin1')
    for enc in encodings:
        try:
            return out_bytes.decode(enc)
        except Exception:
            continue
    return out_bytes.decode('utf-8', errors='replace')


def is_admin():
    try:
        if os.name == 'nt':
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        else:
            return os.geteuid() == 0
    except Exception:
        return False


def detect_password_status(username):
    try:
        system = platform.system().lower()
        if system == 'windows':
            out = _safe_run_and_decode(['net', 'user', username]).lower()
            if not out.strip():
                return None
            return 'var'
        else:
            out = _safe_run_and_decode(['passwd', '-s', username]).lower() or _safe_run_and_decode(['passwd', '-S', username]).lower()
            if not out.strip():
                return None
            parts = out.split()
            if len(parts) > 1 and 'np' in parts[1]:
                return 'yok'
            return 'var'
    except Exception:
        return None


def get_user_info():
    info = {}
    try:
        username = getpass.getuser()
    except Exception:
        username = 'Bilinmiyor'
    current_user = username
    if PSUTIL_AVAILABLE:
        try:
            users_list = psutil.users()
            if users_list:
                current_user = users_list[0].name or username
        except Exception:
            current_user = username
    info['username'] = current_user or 'Bilinmiyor'
    info['is_admin'] = is_admin()
    info['password_status'] = detect_password_status(info['username'])
    return info
