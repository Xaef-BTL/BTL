import os
import shutil

icons_path = r"C:\Users\Yiğit Aslan\Desktop\BTL_setups.exe\Icons"

# Icons klasörü içindeki tüm alt klasörleri tara
for item in os.listdir(icons_path):
    subfolder = os.path.join(icons_path, item)
    if os.path.isdir(subfolder):
        # Alt klasördeki tüm dosyaları Icons'a taşı
        for f in os.listdir(subfolder):
            src = os.path.join(subfolder, f)
            dst = os.path.join(icons_path, f)
            # Eğer hedefte aynı isimde dosya varsa üzerine yazma
            if os.path.exists(dst):
                print(f"{dst} zaten var, atlanıyor")
                continue
            shutil.move(src, dst)
        # Alt klasör artık boşsa sil
        if not os.listdir(subfolder):
            os.rmdir(subfolder)
