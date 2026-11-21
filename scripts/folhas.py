import sys,json,glob,io,urllib.request,datetime
sys.path.insert(0,'scripts'); from grupos import *
from PIL import Image,ImageDraw
base='01-pesquisa/dados/'
ads={}
for f in [base+'todos.json']+glob.glob(base+'paginas*/mineracao-*.json')+glob.glob(base+'leva3/mineracao-*.json'):
  for r in json.load(open(f,encoding='utf-8')): ads.setdefault(r['adArchiveId'],r)
hoje=datetime.date(2026,11,21)
sel=[r for r in ads.values() if r['pageId'] in NICHO or r['pageId'] in GENERICO or r['pageId'] in SAAS or r['pageId'] in ENSINA]
# criativo único: página + início do texto + formato
uni={}
for r in sorted(sel,key=lambda r:r['startDate']):
  k=(r['pageId'],(r.get('bodyText') or '')[:60],r['displayFormat'])
  uni.setdefault(k,r)
lst=list(uni.values())
lst.sort(key=lambda r:r['startDate'])
print('criativos unicos',len(lst))
idx={}
def thumb(r):
  u=(r.get('videoPreviewUrls') or [])[:1] or (r.get('imageUrls') or [])[:1]
  if not u: return None
  try:
    b=urllib.request.urlopen(urllib.request.Request(u[0],headers={'User-Agent':'Mozilla/5.0'}),timeout=20).read()
    im=Image.open(io.BytesIO(b)).convert('RGB'); im.thumbnail((240,300)); return im
  except Exception: return None
cel=(250,330); por=20
folha=0; i=0; buf=[]
for r in lst:
  im=thumb(r)
  if im is None: continue
  i+=1; idx[i]=r['adArchiveId']; buf.append((i,im))
  if len(buf)==por:
    folha+=1; W=Image.new('RGB',(cel[0]*5,cel[1]*4),'white'); d=ImageDraw.Draw(W)
    for j,(n,m) in enumerate(buf):
      x,y=(j%5)*cel[0],(j//5)*cel[1]; W.paste(m,(x+5,y+25)); d.rectangle([x,y,x+60,y+22],fill='black'); d.text((x+6,y+5),str(n),fill='yellow')
    W.save(f'01-pesquisa/criativos/folha-{folha:02d}.jpg',quality=70); buf=[]
if buf:
  folha+=1; W=Image.new('RGB',(cel[0]*5,cel[1]*4),'white'); d=ImageDraw.Draw(W)
  for j,(n,m) in enumerate(buf):
    x,y=(j%5)*cel[0],(j//5)*cel[1]; W.paste(m,(x+5,y+25)); d.rectangle([x,y,x+60,y+22],fill='black'); d.text((x+6,y+5),str(n),fill='yellow')
  W.save(f'01-pesquisa/criativos/folha-{folha:02d}.jpg',quality=70)
json.dump(idx,open(base+'indice-folhas.json','w'),indent=0)
print('miniaturas',i,'folhas',folha)
