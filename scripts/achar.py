import sys,json,glob,datetime
base='01-pesquisa/dados/'
ads={}
for f in [base+'todos.json']+glob.glob(base+'paginas*/mineracao-*.json')+glob.glob(base+'leva3/mineracao-*.json'):
  for r in json.load(open(f,encoding='utf-8')): ads.setdefault(r['adArchiveId'],r)
hoje=datetime.date(2026,11,21)
for q in sys.argv[1:]:
  best=None
  for r in ads.values():
    t=(r.get('bodyText') or '')+' '+(r.get('title') or '')
    if q.lower() in t.lower() or q.lower() in r['pageName'].lower():
      d=(hoje-datetime.date.fromisoformat(r['startDate'])).days
      if not best or d>best[0]: best=(d,r)
  if best: d,r=best; print(f"{q!r} || {r['pageName']} || {d} || {r['adArchiveId']} || {r['displayFormat']} || {(r.get('bodyText') or '')[:160]}".replace('\n',' '))
  else: print(q,'NAO ACHEI')
