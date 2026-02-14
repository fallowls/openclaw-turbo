from PIL import Image
in_path=r"C:\Users\Administrator\.openclaw\workspace\brand_dacreation\icon-white.webp"
out_path=r"C:\Users\Administrator\.openclaw\workspace\brand_dacreation\icon-white.png"
img=Image.open(in_path).convert('RGBA')
img.save(out_path, format='PNG')
print('wrote', out_path, img.size)
