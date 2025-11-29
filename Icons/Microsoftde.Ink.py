from PIL import Image

# Girdi ve çıktı dosyaları
input_file = r"C:\Users\Yiğit Aslan\Desktop\BTL_setups.exe\Icons\mouse.png"
output_file = r"C:\Users\Yiğit Aslan\Desktop\BTL_setups.exe\Icons\mouse.ico"

# PNG'yi aç
img = Image.open(input_file)

# ICO olarak kaydet (boyutlar)
img.save(output_file, format='ICO', sizes=[(32,32),(64,64),(128,128)])

print("mouse.ico oluşturuldu!")
