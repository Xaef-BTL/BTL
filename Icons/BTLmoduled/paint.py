# ------------------ FILE: paint.py ------------------
"""
open_paint_app (trimmed but functional)
"""
import tkinter as tk
from tkinter import Toplevel, messagebox, filedialog, simpledialog, colorchooser
try:
    from PIL import Image, ImageDraw, ImageTk, ImageOps
    PIL_OK = True
except Exception:
    PIL_OK = False


def open_paint_app(parent=None):
    root = parent or tk._default_root
    if root is None:
        raise RuntimeError("open_paint_app: root bulunamadı")
    win = Toplevel(root)
    win.title("BTL Paint — Düzeltilmiş")
    win.geometry("1000x700")
    canvas = tk.Canvas(win, bg="#ffffff", cursor="cross")
    canvas.pack(expand=True, fill="both")
    status = tk.Label(win, text="Hazır", anchor="w")
    status.pack(side="bottom", fill="x")
    # very small subset: free draw
    last = {'x': None, 'y': None}
    def start(e):
        last['x'], last['y'] = e.x, e.y
    def draw(e):
        x,y = e.x,e.y
        if last['x'] is not None:
            canvas.create_line(last['x'], last['y'], x, y, width=4, capstyle=tk.ROUND, smooth=True)
        last['x'], last['y'] = x,y
    def stop(e):
        last['x'] = last['y'] = None
    canvas.bind('<ButtonPress-1>', start)
    canvas.bind('<B1-Motion>', draw)
    canvas.bind('<ButtonRelease-1>', stop)
    return win
