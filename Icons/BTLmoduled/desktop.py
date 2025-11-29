# ------------------ FILE: desktop.py ------------------
"""
desktop.py
Masaüstü ikon yönetimi: add_icon ve yeni öğe yaratma yardımcıları.
"""
import os
import random
import zipfile
from core import ICONS_DIR, safe_start, load_image_as_tk
import tkinter as tk

desktop_icons = {}


def add_icon(x, y, icon_path, label, command=None, deletable=True, parent=None):
    parent = parent or tk._default_root
    if parent is None:
        raise RuntimeError("add_icon: root (tk._default_root) bulunamadı")
    frame = tk.Frame(parent, bg=parent.cget("bg"))
    frame.place(x=x, y=y)
    tk_img = load_image_as_tk(icon_path)
    if tk_img:
        icon_label = tk.Label(frame, image=tk_img, bg=parent.cget("bg"))
        icon_label.image = tk_img
        icon_label.pack()
    else:
        icon_label = tk.Label(frame, text=label, font=("Arial", 12), bg=parent.cget("bg"))
        icon_label.pack()
    text_label = tk.Label(frame, text=label, font=("Arial", 9), bg=parent.cget("bg"))
    text_label.pack()
    desktop_icons[label] = {"frame": frame, "icon_label": icon_label, "text_label": text_label}

    def call_cmd(event=None):
        if callable(command):
            try:
                command()
            except Exception as e:
                from tkinter import messagebox
                messagebox.showerror("Hata", f"Fonksiyon çalıştırılırken hata: {e}")
        else:
            if isinstance(command, str) and os.path.exists(command):
                safe_start(command)

    for w in (frame, icon_label, text_label):
        w.bind("<Button-1>", call_cmd)

    if deletable:
        def remove(evt=None):
            try:
                frame.destroy()
                desktop_icons.pop(label, None)
            except Exception:
                pass
        for w in (frame, icon_label, text_label):
            w.bind("<Button-3>", remove)


def create_new_file(desktop_dir):
    path = os.path.join(desktop_dir, f"YeniDosya{random.randint(1,100)}.txt")
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write("")
    except Exception:
        pass
    icon_path = os.path.join(ICONS_DIR, "text.png")
    add_icon(200, 200, icon_path, os.path.basename(path), lambda p=path: safe_start(p), deletable=True)


def create_new_folder(desktop_dir):
    folder_path = os.path.join(desktop_dir, f"YeniKlasor{random.randint(1,100)}")
    try:
        os.makedirs(folder_path, exist_ok=True)
    except Exception:
        pass
    icon_path = os.path.join(ICONS_DIR, "clasor.png")
    add_icon(250, 200, icon_path, os.path.basename(folder_path), lambda p=folder_path: safe_start(p), deletable=True)


def create_new_zip(desktop_dir):
    zip_name = f"YeniZip{random.randint(1,100)}.zip"
    zip_path = os.path.join(desktop_dir, zip_name)
    try:
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            pass
    except Exception:
        pass
    icon_path = os.path.join(ICONS_DIR, "zip.png")
    add_icon(300, 200, icon_path, zip_name, lambda p=zip_path: safe_start(p), deletable=True)
