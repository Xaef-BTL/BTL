# ------------------ FILE: system.py ------------------
"""
open_cmd_panel, trash, task manager, settings
"""
import tkinter as tk
from tkinter import Toplevel, Text, Scrollbar, Button, END, messagebox
import shutil, os

RECYCLEBIN_DIR = os.path.join(os.path.expanduser("~"), ".my_app_recyclebin")
os.makedirs(RECYCLEBIN_DIR, exist_ok=True)


def open_cmd_panel(parent=None):
    root = parent or tk._default_root
    win = Toplevel(root)
    win.title("BTLshell")
    win.geometry("600x400")
    output_text = Text(win, bg="black", fg="lime", font=("Consolas", 10))
    output_text.pack(expand=True, fill="both", padx=10, pady=10)
    entry = tk.Entry(win)
    entry.pack(fill='x', padx=10)
    def run():
        cmd = entry.get().strip()
        if not cmd:
            return
        output_text.insert(END, f"> {cmd}\n")
        def task():
            try:
                proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                for line in proc.stdout:
                    output_text.insert(END, line)
            except Exception as e:
                output_text.insert(END, f"Hata: {e}\n")
        threading.Thread(target=task, daemon=True).start()
        entry.delete(0, END)
    Button = tk.Button
    tk.Button(win, text="Çalıştır", command=run).pack(pady=4)
    return win


def move_to_trash(app_name, frame=None):
    try:
        if frame is not None:
            try:
                if hasattr(frame, "place_forget"):
                    frame.place_forget()
                elif hasattr(frame, "destroy"):
                    frame.destroy()
            except Exception:
                pass
        try:
            # desktop_icons global may exist in desktop.py
            from desktop import desktop_icons
            desktop_icons.pop(app_name, None)
        except Exception:
            pass
        safe_name = "".join(c for c in app_name if c not in r'\\/:*?"<>|')
        filename = safe_name + ".txt"
        path = os.path.join(RECYCLEBIN_DIR, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"name:{app_name}\n")
            f.write(f"deleted_at:{time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        return True
    except Exception as e:
        print("move_to_trash hata:", e)
        return False


def open_trash(parent=None):
    root = parent or tk._default_root
    win = Toplevel(root)
    win.title("Çöp Kutusu")
    win.geometry("300x400")
    files = [f for f in os.listdir(RECYCLEBIN_DIR) if f.endswith('.txt')]
    lb = tk.Listbox(win)
    lb.pack(expand=True, fill='both')
    for f in files:
        lb.insert(END, f.replace('.txt',''))
    def restore():
        try:
            sel = lb.get(tk.ACTIVE)
        except Exception:
            return
        if sel:
            path = os.path.join(RECYCLEBIN_DIR, sel + '.txt')
            if os.path.exists(path):
                try:
                    os.remove(path)
                except Exception:
                    pass
                try:
                    from desktop import add_icon
                    add_icon(100, 100, None, sel, lambda: messagebox.showinfo('Uygulama', f"{sel} açıldı!"), deletable=True)
                except Exception:
                    pass
                lb.delete(tk.ACTIVE)
    tk.Button(win, text='Geri Yükle', command=restore).pack()
    tk.Button(win, text='Çöp Kutusunu Boşalt', command=lambda: [os.remove(os.path.join(RECYCLEBIN_DIR,f)) for f in os.listdir(RECYCLEBIN_DIR)] and lb.delete(0, 'end')).pack()
    return win
