# ------------------ FILE: update_center.py ------------------
"""
UpdateCenter sınıfı (orijinalden kırpıldı ama temel işlevleri koruyor)
"""
import tkinter as tk
from tkinter import ttk, messagebox
import threading, queue, time, random, functools

class UpdateCenter(tk.Toplevel):
    def __init__(self, master=None, title="Güncelleme Merkezi"):
        super().__init__(master)
        self.title(title)
        self.q = queue.Queue()
        self.download_threads = {}
        self._build_ui()
        self.after(100, self._process_queue)
    def _build_ui(self):
        self.tree = ttk.Treeview(self, columns=("version","size","status"), show='headings', height=8)
        self.tree.heading("version", text="Versiyon")
        self.tree.heading("size", text="Boyut")
        self.tree.heading("status", text="Durum")
        self.tree.pack()
    def check_updates(self):
        t = threading.Thread(target=self._simulate_check_updates, daemon=True)
        t.start()
    def _simulate_check_updates(self):
        time.sleep(1.0 + random.random()*1.5)
        sample = []
        for i in range(random.randint(2,6)):
            sample.append({"id":f"pkg-{int(time.time()*1000)%100000 + i}","name":f"Paket{random.randint(1,99)}","version":"1.0","size":"5 MB","status":"Bekliyor"})
        self.q.put(("updates_found", sample))
    def _process_queue(self):
        try:
            while True:
                item = self.q.get_nowait()
                typ, data = item
                if typ == 'updates_found':
                    self.tree.delete(*self.tree.get_children())
                    for u in data:
                        self.tree.insert('', 'end', iid=u['id'], values=(u['version'], u['size'], u['status']))
        except Exception:
            pass
        self.after(200, self._process_queue)

def open_update_center(parent=None):
    root = parent or tk._default_root
    if root is None:
        raise RuntimeError('Önce root oluşturun')
    uc = UpdateCenter(root)
    return uc
