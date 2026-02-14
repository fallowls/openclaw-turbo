import os, json
from pathlib import Path

base = Path(os.environ.get('LOCALAPPDATA','')) / 'Google' / 'Chrome' / 'User Data' / 'Default' / 'Extensions'
print('BASE', base)
if not base.exists():
    raise SystemExit('Extensions path not found')

hits = []
for manifest in base.rglob('manifest.json'):
    try:
        j = json.loads(manifest.read_text(encoding='utf-8'))
    except Exception:
        continue
    name = str(j.get('name',''))
    desc = str(j.get('description',''))
    blob = (name + ' ' + desc).lower()
    if any(k in blob for k in ['openclaw','claw','relay']):
        hits.append((name, desc, str(manifest)))

for name, desc, path in sorted(hits):
    print(name)
    print('  desc:', desc)
    print('  manifest:', path)
