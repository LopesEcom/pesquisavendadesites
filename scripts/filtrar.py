import json,re,sys,collections
base=r'C:/Users/Familia/Desktop/Pesquisa de Mercado/Raio-X Venda de Sites BR/01-pesquisa/dados/'
d=json.load(open(base+'mineracao-2026-11-21-01-43-21.json',encoding='utf-8'))
def txt(r): return ' '.join(str(r.get(k) or '') for k in ('bodyText','title','linkDescription','linkCaption')).lower()
VENDE=[r'cria[çc][ãa]o de (sites?|landing|p[áa]ginas?|lojas? virtu)',r'(criamos|fazemos|desenvolvemos|montamos|constru[íi]mos|fa[çc]o|crio|entregamos)\b.{0,50}\b(sites?|landing ?pages?|p[áa]ginas?)',
 r'(tenha|ter|quer|precisa de|garanta)\b.{0,25}\b(seu |um |o seu |sua )?(pr[óo]prio )?(site|landing ?page)\b',r'site profissional',r'sites? (para|pra) (advog|dentist|psic|cl[íi]nic|m[ée]dic|nutri|restaur|imobili|corretor|sal[ãa]o|arquitet|igreja|oficina|fisio|empresa|neg[óo]cio|profission|pequen|aut[ôo]nom)',
 r'desenvolvimento (de|web)',r'web ?design',r'seu site (pronto|profissional|em|no ar|de alta)',r'landing ?pages? (profission|de alta|que convert|para)',r'site (pronto|em \d+ (dias|horas))',r'(seu|sua) (neg[óo]cio|empresa|cl[íi]nica|escrit[óo]rio|consult[óo]rio)\b.{0,40}\b(site|internet|google)']
NAO=[r'(acesse|visite|confira|veja|entre|acessar|visitar) (o |no |nosso |em nosso )?site',r'link (na|da) bio']
def classifica(r):
    t=txt(r); h=sum(bool(re.search(p,t)) for p in VENDE)
    return h,t
rows=[]
for r in d:
    h,t=classifica(r)
    if h>=1: rows.append((h,r))
print('candidatos',len(rows),'paginas',len({r['pageId'] for h,r in rows}))
if len(sys.argv)>1:
    import random; random.seed(1)
    for h,r in random.sample(rows,min(40,len(rows))):
        print('---',h,r['pageName'],'|',(r.get('pageCategories') or [''])[0],'|',r.get('linkDomain'),'|',(r.get('bodyText') or '')[:220].replace('\n',' '))
json.dump([r for h,r in rows],open(base+'candidatos.json','w',encoding='utf-8'),ensure_ascii=False)
