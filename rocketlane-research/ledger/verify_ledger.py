"""Evidence verification pass for the Deliverable 1 ledger.

For every ledger row this checks:
  1. The grade is one of the five allowed grades.
  2. Rows graded CONFIRMED or DOCUMENTED BEHAVIOUR or VENDOR CLAIM cite a source URL
     that exists in sources/manifest.csv (i.e. a saved copy with retrieval date + hash).
  3. Their verbatim quote(s) appear in the saved text of that source
     (whitespace- and quote-character-normalised). Multiple quotes are separated by ' || '.
  4. VENDOR CLAIM rows cite a marketing source (blog / marketing page), and
     CONFIRMED / DOCUMENTED BEHAVIOUR rows cite official documentation (help centre / developer docs).
  5. INFERRED rows carry reasoning; UNKNOWN rows carry a note saying what was searched.

Usage: python3 -I verify_ledger.py   (run from anywhere)
Writes ledger/d1-verification-report.md and exits non-zero if any row fails.
"""
import csv, os, re, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LEDGER = os.path.join(HERE, 'd1-evidence-ledger.csv')
MANIFEST = os.path.join(ROOT, 'sources', 'manifest.csv')
REPORT = os.path.join(HERE, 'd1-verification-report.md')
GRADES = {'CONFIRMED', 'DOCUMENTED BEHAVIOUR', 'VENDOR CLAIM', 'INFERRED', 'UNKNOWN'}
OFFICIAL = ('https://help.rocketlane.com/', 'https://developer.rocketlane.com/')
MARKETING = ('https://www.rocketlane.com/',)


def norm(s):
    s = unicodedata.normalize('NFKC', s)
    s = s.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')
    s = s.replace('–', '-').replace('—', '-')
    return re.sub(r'\s+', ' ', s).strip().lower()


def load_sources():
    src = {}
    for r in csv.DictReader(open(MANIFEST)):
        p = os.path.join(ROOT, 'sources', r['text_file'])
        if os.path.exists(p):
            src[r['url']] = (norm(open(p, errors='replace').read()), r['retrieved_utc'])
    return src


def main():
    src = load_sources()
    rows = list(csv.DictReader(open(LEDGER)))
    fails, notes = [], []
    counts = {}
    for r in rows:
        rid, grade = r['id'], r['grade'].strip()
        counts[grade] = counts.get(grade, 0) + 1
        problems = []
        if grade not in GRADES:
            problems.append(f'invalid grade "{grade}"')
        if grade in ('CONFIRMED', 'DOCUMENTED BEHAVIOUR', 'VENDOR CLAIM'):
            urls = [u.strip() for u in r['source_url'].split(' || ') if u.strip()]
            quotes = [q.strip() for q in r['verbatim_quote'].split(' || ') if q.strip()]
            if not urls:
                problems.append('no source URL')
            if not quotes:
                problems.append('no verbatim quote')
            for u in urls:
                if u not in src:
                    problems.append(f'source not saved in manifest: {u}')
            if grade == 'VENDOR CLAIM' and urls and not all(u.startswith(MARKETING) and not u.startswith(OFFICIAL) for u in urls):
                problems.append('VENDOR CLAIM should cite marketing material')
            if grade in ('CONFIRMED', 'DOCUMENTED BEHAVIOUR') and urls and not all(u.startswith(OFFICIAL) for u in urls):
                problems.append(f'{grade} must cite official documentation')
            texts = [src[u][0] for u in urls if u in src]
            for q in quotes:
                if not any(norm(q) in t for t in texts):
                    problems.append(f'quote not found in cited source(s): "{q[:80]}..."')
        elif grade == 'INFERRED':
            if len(r['reasoning_or_notes'].strip()) < 40:
                problems.append('INFERRED row lacks written reasoning')
        elif grade == 'UNKNOWN':
            if len(r['reasoning_or_notes'].strip()) < 20:
                problems.append('UNKNOWN row lacks a note on what was searched')
        if problems:
            fails.append((rid, r['finding'][:90], problems))
    with open(REPORT, 'w') as fh:
        fh.write('# Deliverable 1 evidence verification report\n\n')
        fh.write(f'Rows checked: {len(rows)}\n\n')
        fh.write('| Grade | Rows |\n|---|---|\n')
        for g in ['CONFIRMED', 'DOCUMENTED BEHAVIOUR', 'VENDOR CLAIM', 'INFERRED', 'UNKNOWN']:
            fh.write(f'| {g} | {counts.get(g, 0)} |\n')
        fh.write(f'\nRows passing all checks: {len(rows) - len(fails)}\n\nRows failing: {len(fails)}\n\n')
        fh.write('Checks: valid grade; cited source saved with retrieval date and hash; every verbatim quote found in the saved '
                 'source text; vendor claims cite marketing, documented findings cite official docs; inferred rows show '
                 'reasoning; unknown rows say what was searched.\n\n')
        if fails:
            fh.write('## Failures\n\n')
            for rid, f, p in fails:
                fh.write(f'- **{rid}** ({f}): ' + '; '.join(p) + '\n')
    print(f'{len(rows)} rows, {len(fails)} failing')
    for rid, f, p in fails:
        print(rid, '|', '; '.join(p))
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()
