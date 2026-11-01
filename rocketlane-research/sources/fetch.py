"""Fetch a source, save raw bytes + extracted text, append to manifest. Usage: python3 -I fetch.py URL [URL...]"""
import sys, os, re, html, hashlib, subprocess, datetime, csv
BASE = os.path.dirname(os.path.abspath(__file__))
MAN = os.path.join(BASE, 'manifest.csv')
UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0 Safari/537.36'

def slug(u):
    s = re.sub(r'^https?://', '', u).rstrip('/')
    return re.sub(r'[^A-Za-z0-9._-]+', '_', s)[:180]

def extract(raw, url):
    s = raw
    if url.endswith('.md') or url.endswith('.txt'):
        return s
    # Freshdesk article body
    m = re.search(r'<div[^>]*(?:id="article-body"|class="[^"]*article-body[^"]*")[^>]*>(.*?)</article>', s, re.S) or \
        re.search(r'<article[^>]*>(.*?)</article>', s, re.S)
    body = m.group(1) if m else s
    t = re.search(r'<title>(.*?)</title>', s, re.S)
    title = html.unescape(t.group(1).strip()) if t else ''
    body = re.sub(r'(?s)<(script|style|noscript|svg)[^>]*>.*?</\1>', ' ', body)
    body = re.sub(r'(?i)<(br|/p|/li|/h[1-6]|/tr|/div|li|h[1-6])[^>]*>', '\n', body)
    body = re.sub(r'(?i)<img[^>]*alt="([^"]*)"[^>]*>', r' [image: \1] ', body)
    body = re.sub(r'<[^>]+>', ' ', body)
    body = html.unescape(body)
    body = '\n'.join(re.sub(r'[ \t\xa0]+', ' ', l).strip() for l in body.splitlines())
    body = re.sub(r'\n{3,}', '\n\n', body).strip()
    return f'TITLE: {title}\nURL: {url}\n\n{body}\n'

def main(urls):
    new = not os.path.exists(MAN)
    with open(MAN, 'a', newline='') as fh:
        w = csv.writer(fh)
        if new: w.writerow(['source_id','url','retrieved_utc','http_status','raw_sha256','raw_file','text_file','text_words'])
        for u in urls:
            sid = slug(u)
            rawp = os.path.join(BASE, 'raw', sid + ('.md' if u.endswith('.md') else '.html'))
            r = subprocess.run(['curl','-sS','-L','-m','60','-A',UA,'-o',rawp,'-w','%{http_code}',u], capture_output=True, text=True)
            code = r.stdout.strip()
            data = open(rawp,'rb').read() if os.path.exists(rawp) else b''
            txt = extract(data.decode('utf-8','replace'), u)
            tp = os.path.join(BASE, 'text', sid + '.txt'); open(tp,'w').write(txt)
            import time; time.sleep(0.3)
            ts = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
            w.writerow([sid,u,ts,code,hashlib.sha256(data).hexdigest(),os.path.relpath(rawp,BASE),os.path.relpath(tp,BASE),len(txt.split())])
            print(code, len(txt.split()), 'words', u)
main(sys.argv[1:])
