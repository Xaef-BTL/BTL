
# ------------------ FILE: main.py ------------------
"""
Ana giriş dosyası: root oluşturur, temel ikonları yerleştirir ve modülleri çağırır.
Kullanım: her FILE bloğunu ayrı dosya olarak kaydedin ve main.py'yi çalıştırın.
"""
import tkinter as tk
from pathlib import Path
BASE_DIR = Path(__file__).parent
ICONS_DIR = BASE_DIR / 'Icons'
ICONS_DIR.mkdir(exist_ok=True)

# dynamic import: eğer btl_all.py varsa onu kullan
try:
    import btl_all as btl
except Exception:
    btl = None

# import helper functions from modules
from core import load_image_as_tk
from desktop import add_icon

root = tk.Tk()
root.title('BTL OS')
root.geometry('1280x720')

# place some icons (safe)
try:
    add_icon(50,50, str(ICONS_DIR / 'notepad.png'), 'Not Defteri', lambda: __import__('notepad').open_notepad())
    add_icon(150,50, str(ICONS_DIR / 'snake.png'), 'Yılan Oyunu', lambda: __import__('oyunlar').open_snake_game())
except Exception:
    pass

if __name__ == '__main__':
    root.mainloop()
