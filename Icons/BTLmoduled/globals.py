# ------------------ FILE: globals.py ------------------
"""
Küçük yardımcı: güvenli şekilde global isimleri çekmek için
"""
import importlib

def safe_get(name):
    # aranan fonksiyonu bulmak için modüller arasında dolaş
    for mod in ('btl_all','oyunlar','notepad','file_manager','desktop','store','paint','media','system'):
        try:
            m = importlib.import_module(mod)
            if hasattr(m, name):
                return getattr(m, name)
        except Exception:
            pass
    # fallback: raise so caller knows
    raise RuntimeError(f"Fonksiyon bulunamadı: {name}")

