from pathlib import Path
try:
    from PyPDF2 import PdfReader
except Exception as e:
    print('PyPDF2 import failed', e)
    raise

path = Path(r"C:\Users\Administrator\.openclaw\media\inbound\3c18a9de-0435-4557-a3d6-d8fe37daeac1.pdf")
reader = PdfReader(str(path))
print('pages', len(reader.pages))
for i, p in enumerate(reader.pages):
    text = p.extract_text()
    print('--- page', i+1, '---')
    print(text)
