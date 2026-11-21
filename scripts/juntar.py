import json,re,glob,collections,sys
sys.path.insert(0,'scripts')
base='01-pesquisa/dados/'
todos={}
for f in glob.glob(base+'mineracao-*.json')+glob.glob(base+'leva2/mineracao-*.json'):
    for r in json.load(open(f,encoding='utf-8')):
        todos.setdefault(r['adArchiveId'],r)
print('anuncios unicos',len(todos))
src=open('scripts/filtrar.py',encoding='utf-8').read()
ns={"re":re}
exec(src[src.find('def txt'):src.find('rows=[]')],ns)
cand=[r for r in todos.values() if ns['classifica'](r)[0]>=1]
json.dump(list(todos.values()),open(base+'todos.json','w',encoding='utf-8'),ensure_ascii=False)
json.dump(cand,open(base+'candidatos.json','w',encoding='utf-8'),ensure_ascii=False)
pg=collections.defaultdict(list)
for r in cand: pg[r['pageId']].append(r)
print('candidatos',len(cand),'paginas',len(pg))
out=[]
for pid,rs in sorted(pg.items(),key=lambda x:-len(x[1])):
    r=max(rs,key=lambda r:len(r.get('bodyText') or ''))
    out.append(f"{pid} | {rs[0]['pageName']} | {len(rs)} ads | {(r.get('pageCategories') or [''])[0]} | {r.get('linkDomain')} | {(r.get('bodyText') or r.get('title') or '')[:170]}".replace('\n',' '))
open(base+'paginas-candidatas.txt','w',encoding='utf-8').write('\n'.join(out))
