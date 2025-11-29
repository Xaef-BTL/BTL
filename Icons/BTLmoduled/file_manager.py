# ------------------ FILE: file_manager.py ------------------
"""
Open-source extracted version of open_file_manager (trimmed for clarity)
"""
import tkinter as tk
from tkinter import Toplevel, ttk, messagebox, Scrollbar, Label, Text, END
import datetime, copy


def open_file_manager(parent=None):
    root = parent or tk._default_root
    if root is None:
        raise RuntimeError("open_file_manager: root bulunamadı")
    win = Toplevel(root)
    win.title("Gelişmiş Dosya Yöneticisi (Düzeltilmiş)")
    win.geometry("900x560")

    FS = {
        "root": {
            "type": "folder",
            "children": {
                "Windows": {"type":"folder","children":{"System32":{"type":"folder","children":{f"SYSTEM_FILE_{i}.sys": {"type":"file","content":"","size":4,"modified":datetime.datetime.now()} for i in range(1,21)}}},
                "Belgelerim": {"type":"folder","children":{"notlar.txt":{"type":"file","content":"Bu bir önizleme dosyası.\nMerhaba.","size":12,"modified":datetime.datetime.now()}}}
            }
        }
    }

    clipboard = {"node": None, "mode": None}

    top_frame = tk.Frame(win)
    top_frame.pack(fill="x", padx=6, pady=6)

    search_var = tk.StringVar()
    search_entry = tk.Entry(top_frame, textvariable=search_var)
    search_entry.pack(side="left", fill="x", expand=True)

    btn_search = tk.Button(top_frame, text="Ara", command=lambda: refresh_tree(filter_text=search_var.get()))
    btn_search.pack(side="left", padx=4)

    btn_new_folder = tk.Button(top_frame, text="Yeni Klasör", command=lambda: new_folder())
    btn_new_folder.pack(side="left", padx=4)

    btn_new_file = tk.Button(top_frame, text="Yeni Dosya", command=lambda: new_file())
    btn_new_file.pack(side="left", padx=4)

    main_pane = tk.PanedWindow(win, orient="horizontal", sashrelief="raised")
    main_pane.pack(fill="both", expand=True, padx=6, pady=(0,6))

    tree_frame = tk.Frame(main_pane)
    tree = ttk.Treeview(tree_frame)
    tree.pack(fill="both", expand=True, side="left")
    tree_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=tree_scroll.set)
    tree_scroll.pack(side="right", fill="y")

    right_frame = tk.Frame(main_pane)
    preview_label = tk.Label(right_frame, text="Önizleme", anchor="w")
    preview_label.pack(fill="x")
    preview_text = tk.Text(right_frame, height=18)
    preview_text.pack(fill="both", expand=True)

    status = tk.Label(win, text="Hazır", anchor="w")
    status.pack(fill="x", side="bottom")

    main_pane.add(tree_frame, width=360)
    main_pane.add(right_frame)

    # --- helper inner functions (get_node_by_tree_id, populate_tree, etc.)
    def get_node_by_tree_id(tree_id):
        parts = []
        cur = tree_id
        while cur:
            parts.append(tree.item(cur, "text"))
            cur = tree.parent(cur)
        if not parts:
            return None, []
        parts.reverse()
        node = FS["root"]
        for p in parts[1:]:
            if "children" in node and p in node["children"]:
                node = node["children"][p]
            else:
                return None, parts
        return node, parts

    def populate_tree():
        tree.delete(*tree.get_children())
        def _insert(parent, node_dict):
            for name, meta in sorted(node_dict.items()):
                iid = tree.insert(parent, "end", text=name, open=False)
                if meta["type"] == "folder":
                    tree.insert(iid, "end", text="__placeholder__")
        root_iid = tree.insert("", "end", text="root", open=True)
        _insert(root_iid, FS["root"]["children"])

    populate_tree()

    def expand_real_children(event):
        iid = tree.focus()
        if not iid:
            return
        children = tree.get_children(iid)
        if len(children) == 1 and tree.item(children[0], "text") == "__placeholder__":
            tree.delete(children[0])
            node, parts = get_node_by_tree_id(iid)
            if not node:
                return
            for name, meta in sorted(node.get("children", {}).items()):
                child_iid = tree.insert(iid, "end", text=name, open=False)
                if meta["type"] == "folder":
                    tree.insert(child_iid, "end", text="__placeholder__")

    tree.bind("<<TreeviewOpen>>", expand_real_children)

    def get_path_str(tree_iid):
        if not tree_iid:
            return ""
        parts = []
        cur = tree_iid
        while cur:
            parts.append(tree.item(cur, "text"))
            cur = tree.parent(cur)
        parts.reverse()
        return "/".join(parts)

    def refresh_tree(filter_text=""):
        expanded = set()
        def collect_open(iid):
            if tree.item(iid, "open"):
                expanded.add(get_path_str(iid))
                for c in tree.get_children(iid):
                    collect_open(c)
        for iid in tree.get_children():
            collect_open(iid)
        tree.delete(*tree.get_children())
        def _insert(parent, node_dict):
            for name, meta in sorted(node_dict.items()):
                if filter_text and filter_text.lower() not in name.lower():
                    if meta["type"] == "folder" and any(filter_text.lower() in k.lower() for k in meta.get("children", {})):
                        pass
                    else:
                        continue
                open_state = (get_path_str(parent)+"/"+name) in expanded
                iid = tree.insert(parent, "end", text=name, open=open_state)
                if meta["type"] == "folder":
                    if meta.get("children"):
                        tree.insert(iid, "end", text="__placeholder__")
        root_iid = tree.insert("", "end", text="root", open=True)
        _insert(root_iid, FS["root"]["children"])

    def show_properties(node, parts):
        if not node:
            return
        typ = node["type"]
        if typ == "folder":
            size = sum(child.get("size",0) for child in node.get("children", {}).values())
        else:
            size = node.get("size", 0)
        modified = node.get("modified", "")
        messagebox.showinfo("Özellikler", f"Ad: {parts[-1]}\nTür: {typ}\nBoyut: {size} KB\nSon Değişiklik: {modified}")

    def on_select(event):
        iid = tree.focus()
        node, parts = get_node_by_tree_id(iid)
        if not parts:
            preview_text.delete("1.0", END)
            status.config(text="Seçim yok")
            return
        name = parts[-1]
        if node is None:
            preview_text.delete("1.0", END)
            preview_text.insert(END, f"'{name}' seçildi — öğe ağaçta var ama simüle edilmiş FS'de bulunamadı.")
            status.config(text=f"Seçili: {'/'.join(parts)} (bulunamadı)")
            return
        if node["type"] == "file":
            preview_text.delete("1.0", END)
            preview_text.insert(END, node.get("content", ""))
        else:
            preview_text.delete("1.0", END)
            preview_text.insert(END, f"{name} klasörü, {len(node.get('children',{}))} öğe")
        status.config(text=f"Seçili: {'/'.join(parts)}")

    tree.bind("<<TreeviewSelect>>", on_select)

    # context menu and actions (delete/rename/copy/paste) omitted for brevity — keep from original if needed

    # Initial selection
    root_items = tree.get_children()
    if root_items:
        tree.selection_set(root_items[0])
        tree.focus(root_items[0])

    status.config(text="Kısayollar: Delete=Sil, F2=Yeniden adlandır, Ctrl+C/Ctrl+V=Kopyala/Yapıştır")
