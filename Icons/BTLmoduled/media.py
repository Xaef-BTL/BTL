# ------------------ FILE: media.py ------------------
"""
open_media_player (trimmed, keeps playlist features)
"""
import tkinter as tk
from tkinter import Toplevel, filedialog, messagebox, ttk
import json, os
try:
    import pygame
    PYGAME_AVAILABLE = True
except Exception:
    pygame = None
    PYGAME_AVAILABLE = False


def open_media_player(parent=None):
    root = parent or tk._default_root
    win = Toplevel(root)
    win.title("BTL Media Player")
    win.geometry("660x380")
    state = {"playlist": [], "index": None}
    lb = tk.Listbox(win)
    lb.pack(side="left", fill="y")
    def add_files():
        paths = filedialog.askopenfilenames(filetypes=[("Audio Files", "*.mp3 *.wav *.ogg *.flac *.m4a"), ("All files","*.*")])
        if paths:
            state['playlist'].extend(paths)
            lb.delete(0,'end')
            for i,p in enumerate(state['playlist']):
                lb.insert('end', os.path.basename(p))
    tk.Button(win, text="Dosya Ekle", command=add_files).pack()
    return win