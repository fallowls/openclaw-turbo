from PIL import Image
import os
base=r"C:\Users\Administrator\.openclaw\workspace\brand_dacreation"
files=[
  ("work_mirchandani.webp","work_mirchandani.png"),
  ("work_png_ls1.webp","work_png_ls1.png"),
]
for src,dst in files:
    inp=os.path.join(base,src)
    out=os.path.join(base,dst)
    img=Image.open(inp).convert('RGB')
    img.save(out, format='PNG')
    print('wrote',out,img.size)
