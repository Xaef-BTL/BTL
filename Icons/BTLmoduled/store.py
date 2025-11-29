# ------------------ FILE: store.py ------------------
"""
BTL Store basit sürümü
"""
import tkinter as tk
from tkinter import Toplevel, messagebox, ttk, StringVar
import random
from core import ICONS_DIR
from desktop import add_icon


def btl_store(parent=None):
    root = parent or tk._default_root
    win = Toplevel(root)
    win.title("BTL Store — Mini Sürüm")
    win.geometry("520x520")
    # basitleştirilmiş: mini oyunlar / uygulamalar
    def get_callable(name, fallback_type="app"):
        from globals import safe_get
        return safe_get(name)

    mini_games = {"Yılan Oyunu": lambda: get_callable('open_snake_game')(),
                  "Top Yakalama": lambda: get_callable('open_ball_game')()}
    mini_apps = {"Not Defteri": lambda: get_callable('open_notepad')()}

    def install_app(name, func):
        add_icon(random.randint(50, 700), random.randint(100, 500), os.path.join(ICONS_DIR, "game.png"), name, func, deletable=True)
        messagebox.showinfo("BTL Store", f"{name} indirildi ve masaüstüne eklendi!")

    # UI basit: liste + install
    left = tk.LabelFrame(win, text="Mini Oyunlar")
    left.pack(side="left", fill="both", expand=True, padx=4, pady=4)
    right = tk.LabelFrame(win, text="Mini Uygulamalar")
    right.pack(side="left", fill="both", expand=True, padx=4, pady=4)

    for name, func in mini_games.items():
        frm = tk.Frame(left)
        frm.pack(fill="x", pady=3, padx=4)
        tk.Label(frm, text=name).pack(side="left", anchor="w")
        tk.Button(frm, text="📥 İndir", command=lambda n=name, f=func: install_app(n, f)).pack(side="right")

    for name, func in mini_apps.items():
        frm = tk.Frame(right)
        frm.pack(fill="x", pady=3, padx=4)
        tk.Label(frm, text=name).pack(side="left", anchor="w")
        tk.Button(frm, text="📥 İndir", command=lambda n=name, f=func: install_app(n, f)).pack(side="right")

    return win
