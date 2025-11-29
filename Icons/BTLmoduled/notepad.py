# ------------------ FILE: notepad.py ------------------
"""
open_notepad fonksiyonu
"""
import tkinter as tk
from tkinter import Toplevel, Text, Scrollbar, END, messagebox, simpledialog, filedialog
import tkinter.font as tkfont


def open_notepad(parent=None):
    root = parent or tk._default_root
    if root is None:
        raise RuntimeError("open_notepad: root bulunamadı")
    win = Toplevel(root)
    win.title("Not Defteri — Sarma Edition")
    win.geometry("700x500")
    state = {"filepath": None, "saved": True}
    text = Text(win, wrap="word", undo=True)
    text.pack(expand=True, fill="both")
    current_font = tkfont.Font(font=text['font'])
    status = tk.Label(win, text="Satır: 1  Kolon: 0  |  Kelime: 0", anchor="w")
    status.pack(side="bottom", fill="x")

    def update_status(event=None):
        idx = text.index("insert")
        line, col = idx.split(".")
        content = text.get("1.0", "end-1c")
        words = len(content.split())
        status.configure(text=f"Satır: {line}  Kolon: {col}  |  Kelime: {words}")
    text.bind("<<Modified>>", lambda e: (update_status(), text.edit_modified(False)))

    def maybe_save():
        if not state['saved']:
            answer = messagebox.askyesnocancel("Kaydedilsin mi?", "Değişiklikler kaydedilsin mi?")
            if answer:
                return save_file()
            if answer is None:
                return False
        return True

    def new_file():
        if not maybe_save():
            return
        text.delete("1.0", "end")
        state['filepath'] = None
        state['saved'] = True
        win.title("Not Defteri — Yeni Belge")
        update_status()

    def open_file():
        if not maybe_save():
            return
        fp = filedialog.askopenfilename(filetypes=[("Text files", "*.txt;*.py;*.md;*.log"), ("All files", "*.*")])
        if not fp:
            return
        try:
            with open(fp, "r", encoding="utf-8") as f:
                data = f.read()
        except Exception as e:
            messagebox.showerror("Hata", f"Dosya açılamadı: {e}")
            return
        text.delete("1.0", "end")
        text.insert("1.0", data)
        state['filepath'] = fp
        state['saved'] = True
        win.title(f"Not Defteri — {os.path.basename(fp)}")

    def save_file():
        fp = state['filepath']
        if not fp:
            return save_as()
        try:
            with open(fp, "w", encoding="utf-8") as f:
                f.write(text.get("1.0", "end-1c"))
        except Exception as e:
            messagebox.showerror("Hata", f"Kaydedilemedi: {e}")
            return False
        state['saved'] = True
        win.title(f"Not Defteri — {os.path.basename(fp)}")
        return True

    def save_as():
        fp = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if not fp:
            return False
        try:
            with open(fp, "w", encoding="utf-8") as f:
                f.write(text.get("1.0", "end-1c"))
        except Exception as e:
            messagebox.showerror("Hata", f"Kaydedilemedi: {e}")
            return False
        state['filepath'] = fp
        state['saved'] = True
        win.title(f"Not Defteri — {os.path.basename(fp)}")
        return True

    def on_edit(event=None):
        state['saved'] = False
    text.bind("<<Modified>>", lambda e: (on_edit(), text.edit_modified(False)))

    # Menüler ve kısa yollar basitçe eklenebilir - kullanım için main app'te ekleme tavsiye edilir
    win.protocol("WM_DELETE_WINDOW", lambda: (maybe_save() and win.destroy()))
    text.focus_set()
    update_status()
    return win
