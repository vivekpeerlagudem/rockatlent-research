"""Parse the OpenAPI blocks embedded in saved developer.rocketlane.com reference pages.
Outputs api-endpoints.csv and api-entity-fields.csv into ../analysis/."""
import json, re, os, glob, csv
BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(BASE), 'analysis'); os.makedirs(OUT, exist_ok=True)
eps, fields = [], {}
def resolve(s, comps, depth=0):
    if depth > 6 or not isinstance(s, dict): return s
    if '$ref' in s: return resolve(comps.get(s['$ref'].split('/')[-1], {}), comps, depth + 1)
    return s
for p in sorted(glob.glob(os.path.join(BASE, 'text', 'developer.rocketlane.com_reference_*.md.txt'))):
    t = open(p).read()
    m = re.search(r'```json\n(.*?)\n```', t, re.S)
    if not m: continue
    try: spec = json.loads(m.group(1))
    except Exception: continue
    comps = spec.get('components', {}).get('schemas', {})
    page = 'https://developer.rocketlane.com/reference/' + os.path.basename(p).split('reference_')[1].replace('.md.txt', '')
    for path, ops in spec.get('paths', {}).items():
        for verb, op in ops.items():
            if not isinstance(op, dict): continue
            eps.append([verb.upper(), path, op.get('summary', ''), ','.join(op.get('tags', [])), page])
            for code, resp in op.get('responses', {}).items():
                if not code.startswith('2'): continue
                sch = resolve(resp.get('content', {}).get('application/json', {}).get('schema', {}), comps)
                if sch.get('type') == 'object' and 'data' in sch.get('properties', {}):
                    d = resolve(sch['properties']['data'], comps)
                    sch = resolve(d.get('items', d), comps)
                tag = ','.join(op.get('tags', []))
                for k, v in (sch.get('properties') or {}).items():
                    v2 = resolve(v, comps)
                    typ = v2.get('type', 'object')
                    sub = ''
                    if typ == 'object': sub = ' '.join(list((v2.get('properties') or {}).keys())[:8])
                    if typ == 'array':
                        it = resolve(v2.get('items', {}), comps); sub = 'items: ' + ' '.join(list((it.get('properties') or {}).keys())[:8])
                    fields.setdefault((tag, k), [typ, sub, page])
with open(os.path.join(OUT, 'api-endpoints.csv'), 'w', newline='') as fh:
    w = csv.writer(fh); w.writerow(['method', 'path', 'summary', 'resource', 'source_page'])
    seen = set()
    for e in eps:
        if (e[0], e[1]) in seen: continue
        seen.add((e[0], e[1])); w.writerow(e)
with open(os.path.join(OUT, 'api-entity-fields.csv'), 'w', newline='') as fh:
    w = csv.writer(fh); w.writerow(['resource', 'field', 'type', 'nested_keys', 'source_page'])
    for (tag, k), (typ, sub, page) in sorted(fields.items()): w.writerow([tag, k, typ, sub, page])
print(len(seen), 'endpoints;', len(fields), 'resource fields')
