import sys,json,glob,re,datetime,collections,statistics
sys.path.insert(0,'scripts'); from grupos import *
exec(open('scripts/quadros.py').read())
base='01-pesquisa/dados/'
ads={}
for f in [base+'todos.json']+glob.glob(base+'paginas*/mineracao-*.json')+glob.glob(base+'leva3/mineracao-*.json'):
  for r in json.load(open(f,encoding='utf-8')): ads.setdefault(r['adArchiveId'],r)
hoje=datetime.date(2026,11,21)
def grp(p): return 'N' if p in NICHO else 'S' if p in SAAS else 'E' if p in ENSINA else 'G' if p in GENERICO else None
for r in ads.values():
  r['_g']=grp(r['pageId']); r['_dias']=(hoje-datetime.date.fromisoformat(r['startDate'])).days
sel=[r for r in ads.values() if r['_g']]
idx=json.load(open(base+'indice-folhas.json'))
quadro={idx[str(i+1)]:S[i] for i in range(len(S))}
def dest(r):
  d=(r.get('linkDomain') or '').lower(); c=(r.get('ctaType') or '')
  if 'whatsapp' in d or 'WHATSAPP' in c: return 'WhatsApp'
  if 'instagram' in d or 'INSTAGRAM' in c: return 'Instagram'
  if 'MESSAGE' in c or 'messenger' in d or d in('fb.me','m.me'): return 'Direct ou Messenger'
  if not d or d=='facebook.com': return 'Facebook ou sem destino'
  return 'Site ou página'
FMT={'VIDEO':'Vídeo','IMAGE':'Imagem','CAROUSEL':'Carrossel','DCO':'Dinâmico da Meta','DPA':'Catálogo'}
out={}
for g in 'NGSE':
  rs=[r for r in sel if r['_g']==g]
  pg={r['pageId'] for r in rs}
  q=collections.Counter(quadro[r['adArchiveId']] for r in rs if r['adArchiveId'] in quadro)
  out[g]={'ads':len(rs),'paginas':len(pg),
   'fmt':collections.Counter(FMT.get(r['displayFormat'],r['displayFormat']) for r in rs).most_common(),
   'dest':collections.Counter(dest(r) for r in rs).most_common(),
   'dias_med':statistics.median([r['_dias'] for r in rs]) if rs else 0,
   'mais60':sum(r['_dias']>=60 for r in rs),
   'quadro':q.most_common(),'q_total':sum(q.values())}
  print(g,json.dumps(out[g],ensure_ascii=False))
# por página (nicho e genérico): ads, dias max, variações
lin=[]
for p in set(NICHO)|GENERICO|set(SAAS):
  rs=[r for r in sel if r['pageId']==p]
  if not rs: continue
  lin.append({'pid':p,'nome':rs[0]['pageName'],'g':rs[0]['_g'],'nicho':NICHO.get(p) or SAAS.get(p) or 'Genérico','ads':len(rs),
   'diasMax':max(r['_dias'] for r in rs),'var':sum(r.get('collationCount') or 1 for r in rs),
   'dest':collections.Counter(dest(r) for r in rs).most_common(1)[0][0],'ig':rs[0]['pageUrl'],'likes':rs[0].get('pageLikeCount')})
lin.sort(key=lambda x:(-x['diasMax']))
json.dump({'grupos':out,'paginas':lin},open(base+'analise.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
for x in lin[:40]: print(x['g'],x['diasMax'],x['ads'],x['var'],x['nicho'],'|',x['nome'],'|',x['dest'])
