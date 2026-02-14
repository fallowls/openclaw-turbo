import importlib.util as u
for m in ['reportlab','fpdf','fpdf2','PIL','weasyprint']:
    print(m, bool(u.find_spec(m)))
