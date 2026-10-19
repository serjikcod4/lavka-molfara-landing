"""Збирає index.html + img/ + fonts/ в один самодостатній HTML-файл.

Використання:  python3 scripts/build_standalone.py  ->  dist/lavka-molfara-landing.html
Файл відкривається без інтернету і без сервера (зручно надіслати в Telegram).
"""
import base64, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
MIME = {'.webp': 'image/webp', '.png': 'image/png', '.jpg': 'image/jpeg', '.woff2': 'font/woff2'}

html = (ROOT / 'index.html').read_text(encoding='utf-8')
# прелоади з crossorigin не потрібні у вбудованому файлі
html = re.sub(r'\s*<link rel="preload"[^>]*>', '', html)

cache = {}
def data_uri(rel):
    if rel not in cache:
        p = ROOT / rel
        cache[rel] = f"data:{MIME[p.suffix]};base64," + base64.b64encode(p.read_bytes()).decode()
    return cache[rel]

html = re.sub(r'(?<![\w/.-])((?:img|fonts)/[\w.-]+\.(?:webp|png|jpg|woff2))', lambda m: data_uri(m.group(1)), html)

out = ROOT / 'dist' / 'lavka-molfara-landing.html'
out.parent.mkdir(exist_ok=True)
out.write_text(html, encoding='utf-8')
print(out, round(out.stat().st_size / 1024 / 1024, 2), 'MB,', len(cache), 'files inlined')
