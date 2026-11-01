"""Assemble 02-deliverable-1-rocketlane-architecture.md from the source template.
Inlines Mermaid diagrams from diagrams/*.mmd, a grade count table from the ledger,
and the verification summary from report-src/verification-section.md.
Run: python3 -I build_report.py
"""
import csv, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
src = open(os.path.join(HERE, 'd1-report.src.md')).read()

rows = list(csv.DictReader(open(os.path.join(ROOT, 'ledger', 'd1-evidence-ledger.csv'))))
order = ['CONFIRMED', 'DOCUMENTED BEHAVIOUR', 'VENDOR CLAIM', 'INFERRED', 'UNKNOWN']
counts = {g: sum(1 for r in rows if r['grade'] == g) for g in order}
table = '| Grade | Ledger rows |\n|---|---|\n' + ''.join(f'| {g} | {counts[g]} |\n' for g in order) + f'| **Total** | **{len(rows)}** |\n'
src = src.replace('{{GRADE_TABLE}}', table)

def diagram(m):
    name = m.group(1)
    body = open(os.path.join(ROOT, 'diagrams', name + '.mmd')).read().rstrip()
    return f'```mermaid\n{body}\n```\n\n*Source: `diagrams/{name}.mmd` · rendered: `diagrams/rendered/{name}.svg`*'
src = re.sub(r'\{\{DIAGRAM:([\w-]+)\}\}', diagram, src)

vpath = os.path.join(HERE, 'verification-section.md')
src = src.replace('{{VERIFICATION}}', open(vpath).read().strip() if os.path.exists(vpath) else '_Pending._')
assert not re.search(r'\{\{(DIAGRAM:|GRADE_TABLE|VERIFICATION)', src), 'unresolved placeholder'
out = os.path.join(ROOT, '02-deliverable-1-rocketlane-architecture.md')
open(out, 'w').write(src)
print('wrote', out, len(src.split()), 'words')
