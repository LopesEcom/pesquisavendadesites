import sys,json,glob,re,collections
sys.path.insert(0,'scripts'); from grupos import *
base='01-pesquisa/dados/'
ads={}
for f in [base+'todos.json']+glob.glob(base+'paginas*/mineracao-*.json')+glob.glob(base+'leva3/mineracao-*.json'):
  for r in json.load(open(f,encoding='utf-8')): ads.setdefault(r['adArchiveId'],r)
T={
 'Cliente pesquisa no Google antes':r'pesquis|procura (você|sua|seu|pelo)|google',
 'Concorrente aparece no lugar':r'concorr',
 'Depender só do Instagram ou link na bio':r'instagram|link na bio|rede(s)? socia',
 'Cita confiança ou credibilidade':r'confian|credibilid|autoridade|profissionalismo',
 'Botão ou integração com WhatsApp':r'whatsapp',
 'Prazo de entrega na promessa':r'(em|até) \d+ ?(h|horas?|dias?|minutos?)|pronto hoje|24 ?h',
 'Mostra preço no texto':r'r\$ ?\d',
 'Sem mensalidade ou pagamento único':r'sem mensalidade|pagamento único|paga uma (só )?vez|sem taxa',
 'Mensalidade ou assinatura':r'/m[êe]s|mensa(l|is)|assinatura|por m[êe]s',
 'Parcelamento':r'\d+ ?x ',
 'Regras do conselho (OAB, CFP, CFM, CRO)':r'\boab\b|\bcfp\b|\bcfm\b|\bcro\b|conselho|ética|etica|normas',
 'Aparecer em resposta de IA (ChatGPT)':r'chatgpt|\bias?\b recomend|respostas da ia|gemini',
 'Garantia ou risco zero':r'garantia|devolv|só paga depois|paga somente|pague somente|sem risco|após ver|depois de ver',
 'Prévia ou diagnóstico grátis':r'prévia|previa|diagnóstico|diagnostico|avaliação gratuita|check-?up',
 'Black Friday ou desconto com data':r'black|até \d+/\d+|só hoje|vagas limitadas|últimas vagas',
 'Site grátis (cobra depois)':r'site.{0,30}gr[áa]tis|sem pagar (nada )?pela cria|gratuit',
 'Portfólio ou case de cliente':r'portf[óo]lio|projetos reais|sites que criamos|cliente|case',
}
res={}
for g,S in [('N',NICHO),('G',GENERICO)]:
  vist=set(); txts=[]
  for r in ads.values():
    if r['pageId'] in S:
      t=((r.get('bodyText') or '')+' '+(r.get('title') or '')).lower()
      k=t[:120]
      if k in vist or len(t)<15: continue
      vist.add(k); txts.append(t)
  n=len(txts)
  res[g]={'n':n,'temas':{k:sum(bool(re.search(p,t)) for t in txts) for k,p in T.items()}}
  print(g,n); [print('  ',k,v,f'{v/n:.0%}') for k,v in sorted(res[g]['temas'].items(),key=lambda x:-x[1])]
json.dump(res,open(base+'temas.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
