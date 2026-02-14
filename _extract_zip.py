import zipfile, os
zip_path = r"C:\Users\Administrator\Downloads\LTI\lusha.zip"
out_dir = r"C:\Users\Administrator\Downloads\LTI\lusha"
os.makedirs(out_dir, exist_ok=True)
try:
    with zipfile.ZipFile(zip_path) as z:
        z.extractall(out_dir)
    print('ok')
except Exception as e:
    print('err', e)
