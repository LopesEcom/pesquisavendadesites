import sys,json,re; sys.path.insert(0,'scripts'); from grupos import *
d=json.load(open('01-pesquisa/dados/candidatos.json',encoding='utf-8'))
vist=set()
for r in d:
  p=r['pageId']; g='N' if p in NICHO else 'S' if p in SAAS else 'E' if p in ENSINA else 'G' if p in GENERICO else None
  if not g: continue
  t=(r.get('bodyText') or '')+' '+(r.get('title') or '')
  pr=re.findall(r'(?:\d+\s?x\s(?:de\s)?)?R\$\s?[\d\.,]+',t)
  k=(r['pageName'],tuple(pr))
  if pr and k not in vist: vist.add(k); print(g,'|',r['pageName'][:30],'|',pr[:5])
