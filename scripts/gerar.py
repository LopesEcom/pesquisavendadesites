import sys, json, glob, datetime, html, collections, os
sys.path.insert(0, 'scripts')
from grupos import *
from PIL import Image

base = '01-pesquisa/dados/'
H = html.escape
hoje = datetime.date(2026, 11, 21)
ads = {}
for f in [base + 'todos.json'] + glob.glob(base + 'paginas*/mineracao-*.json') + glob.glob(base + 'leva3/mineracao-*.json'):
    for r in json.load(open(f, encoding='utf-8')):
        ads.setdefault(r['adArchiveId'], r)
idx = json.load(open(base + 'indice-folhas.json'))
an = json.load(open(base + 'analise.json', encoding='utf-8'))
temas = json.load(open(base + 'temas.json', encoding='utf-8'))
trans = json.load(open(base + 'transcricoes.json', encoding='utf-8'))
css = open('01-pesquisa/estilo-base.css', encoding='utf-8').read()
G = an['grupos']

def dias(r): return (hoje - datetime.date.fromisoformat(r['startDate'])).days
def lib(i): return f'https://www.facebook.com/ads/library/?id={i}'
def libpg(p): return f'https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=BR&view_all_page_id={p}'
def pct(a, b): return f'{round(100 * a / b)}%' if b else '0%'

def barras(itens, total):
    mx = max(v for _, v in itens) if itens else 1
    out = []
    for rot, v in itens:
        out.append(f'<div class="barra" title="{H(rot)}: {v} de {total} ({pct(v,total)})"><span class="b-rot">{H(rot)}</span>'
                   f'<span class="b-trilho"><i style="width:{100*v/mx:.1f}%"></i></span><span class="b-val"><b>{pct(v,total)}</b> {v}</span></div>')
    return '<div class="barras">' + ''.join(out) + '</div>'

QN = {'P': 'Pessoa falando', 'M': 'Mockup do site no celular ou notebook', 'A': 'Arte de oferta com preço ou lista',
      'D': 'Arte com a dor ou uma pergunta', 'T': 'Tela gravada ou bastidor', 'V': 'Prova de cliente', 'O': 'Marca, fundo ou outro'}
def quadro_bar(g):
    q = G[g]['quadro']; t = G[g]['q_total']
    return barras([(QN[k], v) for k, v in q], t)

def fmt_bar(g):
    t = G[g]['ads']
    m = {'MULTI_IMAGES': 'Várias imagens'}
    return barras([(m.get(k, k), v) for k, v in G[g]['fmt']], t)

def dest_pag(g):
    c = collections.Counter(x['dest'] for x in an['paginas'] if x['g'] == g)
    n = sum(c.values())
    return barras(c.most_common(), n), n

TEMAS_OK = ['Cliente pesquisa no Google antes', 'Depender só do Instagram ou link na bio', 'Concorrente aparece no lugar',
            'Cita confiança ou credibilidade', 'Botão ou integração com WhatsApp', 'Prazo de entrega na promessa',
            'Mostra preço no texto', 'Mensalidade ou assinatura', 'Sem mensalidade ou pagamento único',
            'Regras do conselho (OAB, CFP, CFM, CRO)', 'Black Friday ou desconto com data', 'Prévia ou diagnóstico grátis',
            'Site grátis (cobra depois)', 'Garantia ou risco zero', 'Aparecer em resposta de IA (ChatGPT)']
def temas_tab():
    nN, nG = temas['N']['n'], temas['G']['n']
    linhas = ''
    for k in TEMAS_OK:
        a, b = temas['N']['temas'][k], temas['G']['temas'][k]
        linhas += f'<tr><td>{H(k)}</td><td class="num"><b>{pct(a,nN)}</b> <span style="color:#6B6B6B">{a}</span></td><td class="num"><b>{pct(b,nG)}</b> <span style="color:#6B6B6B">{b}</span></td></tr>'
    return (f'<div class="tab"><table><thead><tr><th>Tema no texto do anúncio</th><th class="num">Nichados ({nN})</th>'
            f'<th class="num">Genéricos ({nG})</th></tr></thead><tbody>{linhas}</tbody></table></div>')

# ---------- miniaturas recortadas das folhas
os.makedirs('01-pesquisa/criativos/quadros', exist_ok=True)
def recorte(n):
    dst = f'01-pesquisa/criativos/quadros/{n}.jpg'
    if not os.path.exists(dst):
        f = (n - 1) // 20 + 1; j = (n - 1) % 20
        im = Image.open(f'01-pesquisa/criativos/folha-{f:02d}.jpg')
        x, y = (j % 5) * 250 + 5, (j // 5) * 330 + 25
        c = im.crop((x, y, x + 240, y + 300))
        # corta a sobra branca de miniaturas menores
        bg = Image.new(c.mode, c.size, (255, 255, 255))
        from PIL import ImageChops
        bbox = ImageChops.difference(c, bg).getbbox()
        if bbox: c = c.crop(bbox)
        c.save(dst, quality=82)
    return f'01-pesquisa/criativos/quadros/{n}.jpg'

GAL = [  # (número na folha, rótulo do padrão)
    (14, 'Concorrente aparece no Google'), (15, 'Instagram não basta'), (16, 'Concorrente aparece no Google'),
    (28, 'Um nicho só'), (39, 'Preço na cara'), (81, 'Dor com número do nicho'), (84, 'Cena do WhatsApp'),
    (107, 'Um nicho só'), (134, 'Prazo curto'), (142, 'Cena do clique'), (143, 'Preço na cara'),
    (158, 'Preço na cara'), (162, 'Prazo curto'), (176, 'Um nicho só'), (178, 'Pergunta ao nicho'),
    (216, 'Nicho e bairro'), (226, 'Bastidor'), (228, 'Mensalidade'), (229, 'Preço na cara'),
    (230, 'Diagnóstico grátis'), (240, 'Molde multinicho'), (244, 'Molde multinicho'), (245, 'Molde multinicho'),
    (251, 'Preço na cara'), (264, 'Diagnóstico grátis'), (280, 'Um nicho só'), (294, 'Bastidor'),
    (298, 'Molde multinicho'), (305, 'Molde multinicho'), (307, 'Molde multinicho'), (308, 'Molde multinicho'),
    (302, 'Molde multinicho'), (311, 'Molde multinicho'), (312, 'Molde multinicho'),
    (5, 'Quebra de objeção'), (31, 'Prova de cliente'), (53, 'Ancoragem de preço'), (100, 'Paga na entrega'),
    (113, 'Preço na cara'), (174, 'Três pacotes'), (197, 'Três pacotes'), (36, 'Mensalidade'), (236, 'Preço na cara'),
    (256, 'Preço na cara'), (272, 'Quebra de objeção'), (276, 'Quebra de objeção'), (299, 'Ancoragem de preço'),
    (310, 'Ancoragem de preço'), (232, 'Ensina a vender sites'), (82, 'Ensina a vender sites'), (223, 'Ensina a vender sites'),
]
def grupo_nome(p):
    if p in NICHO: return 'Nichado: ' + NICHO[p]
    if p in SAAS: return 'Plataforma: ' + SAAS[p]
    if p in ENSINA: return 'Ensina a vender'
    return 'Genérico'
def galeria():
    itens = []
    for n, rot in GAL:
        r = ads[idx[str(n)]]
        t = (r.get('bodyText') or r.get('title') or '').strip()
        tr = trans.get(r['adArchiveId'], {}).get('t', '')
        cat = grupo_nome(r['pageId'])
        filtro = 'n' if r['pageId'] in NICHO else 'g' if r['pageId'] in GENERICO else 'e'
        itens.append(
            f'<button class="item" data-f="{filtro}" data-txt="{H(t)}" data-tr="{H(tr)}" data-lib="{lib(r["adArchiveId"])}" '
            f'data-tit="{H(r["pageName"])}" data-sub="{H(cat)} · {dias(r)} dias no ar · {H(rot)}" data-img="{recorte(n)}">'
            f'<img loading="lazy" src="{recorte(n)}" alt="Primeiro quadro do anúncio de {H(r["pageName"])}">'
            f'<b>{H(r["pageName"])}</b><span>{H(rot)} · {dias(r)} dias</span></button>')
    return '<div class="grade" id="grade">' + ''.join(itens) + '</div>'

def gancho(titulo, desc, exemplos):
    li = ''
    for frase, aid in exemplos:
        r = ads[aid]
        li += (f'<li>"{H(frase)}"<br><span style="color:#6B6B6B;font-size:13px">{H(r["pageName"])}, {dias(r)} dias no ar · '
               f'{H(grupo_nome(r["pageId"]))} · <a href="{lib(aid)}" target="_blank" rel="noopener">Ver na Biblioteca</a></span></li>')
    return f'<div class="gancho"><h3>{H(titulo)}</h3><p class="sub" style="margin:0 0 8px">{H(desc)}</p><ul class="lista">{li}</ul></div>'

def players():
    linhas = ''
    for x in sorted([x for x in an['paginas'] if x['g'] in 'NS'], key=lambda x: (-x['diasMax'])):
        tipo = 'Vende site para o nicho' if x['g'] == 'N' else 'Plataforma do nicho com site'
        linhas += (f'<tr><td><a href="{libpg(x["pid"])}" target="_blank" rel="noopener">{H(x["nome"])}</a></td><td>{H(x["nicho"])}</td>'
                   f'<td>{tipo}</td><td class="num">{x["ads"]}</td><td class="num">{x["diasMax"]}</td><td>{H(x["dest"])}</td></tr>')
    return ('<div class="tab"><table id="tabela"><thead><tr><th data-k="0">Player</th><th data-k="1">Nicho</th><th data-k="2">Tipo</th>'
            '<th data-k="3" class="num">Anúncios ativos</th><th data-k="4" class="num">Mais antigo (dias)</th><th data-k="5">Destino principal</th>'
            f'</tr></thead><tbody>{linhas}</tbody></table></div>')

N, Gn, S_, E = G['N'], G['G'], G['S'], G['E']
nN_pag = N['paginas']; nS_pag = S_['paginas']
bar_dest_N, nDN = dest_pag('N'); bar_dest_G, nDG = dest_pag('G')
total_lidos = len(ads)
qN = dict(N['quadro']); qG = dict(Gn['quadro'])

PRECOS = [
    ('R$ 97 a R$ 197, pago uma vez', 'Site de uma página feito rápido para um nicho só',
     'Elismael Santos, psicólogos, R$ 97 em 48 h · JJ company, landing para advogados, R$ 147 · Mago Digital, barbearias, R$ 197 em 60 min'),
    ('R$ 297 a R$ 599, pago uma vez', 'A faixa mais comum. Quase sempre com "sem mensalidade" e 1º ano de hospedagem',
     'Publys Tech, mesmo anúncio para advogados, psicólogos e dentistas, R$ 297 · Clinarte, saúde, a partir de R$ 429 · Advogar Digital, a partir de R$ 450 · Cliente em 3 Passos, R$ 497 em 3x · Vytron, R$ 599,90'),
    ('R$ 997 a R$ 3.997, em pacotes', 'Agência de nicho com 3 níveis e sinal de 50%',
     'LPVende, a partir de R$ 1.890 com prévia antes do 2º pagamento · Clinarte na página: R$ 997, R$ 2.497 e R$ 3.997 · Sabrina, cerimonialistas, R$ 997 e R$ 1.597'),
    ('R$ 49,90 a R$ 99 por mês', 'A criação entra na mensalidade',
     'Fantilabs, dentistas, R$ 99/mês · Byte a Byte, clínicas, R$ 59,90/mês · Brain, "site caro é coisa do passado", R$ 90/mês · OPS Empresas, "website por assinatura", R$ 60/mês sem taxa de adesão'),
    ('Grátis, cobrando depois', 'Cria sem custo e ganha na hospedagem ou no plano',
     'Notus Studio, psicólogos, com quiz de 1 minuto para filtrar · Rivor e Tony Zimo, empresas em geral'),
    ('Plataforma do nicho', 'O site vem dentro de um sistema que o profissional já paga',
     'Jusfy, advogados, com convênio da OAB, 58 anúncios · WebPsi, psicólogos, 12x R$ 35 · Imóvel Guide, corretores, R$ 89,90/mês · Brovia, R$ 49,90/mês · ImoTools, imobiliárias, 52 anúncios'),
]
def precos():
    li = ''.join(f'<tr><td><b>{H(a)}</b></td><td>{H(b)}</td><td>{H(c)}</td></tr>' for a, b, c in PRECOS)
    return f'<div class="tab"><table><thead><tr><th>Faixa</th><th>Modelo</th><th>Quem usa (exemplos)</th></tr></thead><tbody>{li}</tbody></table></div>'

pag = f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Venda de sites nichada</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>{css}
.item img{{object-fit:contain;background:#F2F2F2}}
.chips{{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0 0}}.chip{{font-size:12px;border:1px solid var(--borda);border-radius:999px;padding:3px 9px;background:var(--suave)}}
</style></head><body>
<aside class="lado"><div class="marca">Venda de sites nichada<small>Pesquisa de 21/11/2026</small></div>
<nav><a class="ativo" href="#resumo">Resumo</a><a href="#quem">Quem está nichando</a><a href="#criativos">Criativos</a><a href="#ganchos">Ganchos</a><a href="#galeria">Galeria</a><a href="#ofertas">Ofertas e preços</a><a href="#funil">Para onde leva</a><a href="#ensina">Quem ensina a vender</a><a href="#testar">O que testar</a><a href="#players">Players</a><a href="#metodo">Limites e fontes</a></nav></aside>
<main>
<section id="resumo">
<h1>Quem nicha não vende o site, vende o que o cliente do nicho encontra no Google</h1>
<p class="lead">O anúncio nichado chama a profissão pelo nome ("Advogado,", "Psicólogo(a),", "Dentista,") e abre com uma pergunta: quando o paciente ou o cliente pesquisa você, o que ele encontra? O preço quase sempre está entre R$ 297 e R$ 599, pago uma vez, e o clique vai para o WhatsApp.</p>
<div class="tiles">
<div class="tile"><b>{total_lidos:,}</b><span>anúncios ativos no Brasil lidos</span></div>
<div class="tile"><b>{nN_pag}</b><span>vendedores de site nichados</span></div>
<div class="tile"><b>{nS_pag}</b><span>plataformas de nicho que já vêm com site</span></div>
<div class="tile"><b>30 de 42</b><span>nichados atendem advogados ou saúde</span></div>
<div class="tile"><b>{pct(qN.get("D",0),N["q_total"])}</b><span>dos criativos nichados abrem com a dor, contra {pct(qG.get("D",0),Gn["q_total"])} nos genéricos</span></div>
<div class="tile"><b>{pct(temas["N"]["temas"]["Regras do conselho (OAB, CFP, CFM, CRO)"],temas["N"]["n"])}</b><span>dos textos nichados citam as regras do conselho, contra 0% nos genéricos</span></div>
</div>
<div class="card"><h3>O molde que mais se repete no anúncio nichado</h3><p class="sub">Observado nos anúncios. Descreve o que fazem, não prova que funciona melhor.</p>
<ol class="molde">
<li><b>Chamar o nicho:</b> "Advogado,", "Psicólogo(a), tenha um site à altura do seu trabalho", "Atenção, donos de clínicas".</li>
<li><b>A cena da pesquisa:</b> o cliente pesquisa seu nome ou "dentista perto de mim" e acha o concorrente, ou só um link na bio.</li>
<li><b>O que entrega, em lista:</b> site com sua foto, especialidades, botão de WhatsApp, aparecer no Google, e, no nicho regulado, textos dentro das regras da OAB, do CFP ou do CFM.</li>
<li><b>Preço e prazo na arte:</b> R$ 297 "pagamento único, sem mensalidade", pronto em 24 h, 48 h ou 3 dias.</li>
<li><b>Fechamento:</b> "Quero meu site" e WhatsApp.</li>
</ol></div>
<div class="aviso">Período da coleta: semana da Black Friday, então há muito anúncio novo. Só 23 dos {N["ads"]} anúncios nichados passam de 60 dias no ar. Os limites estão em <a href="#metodo">Limites e fontes</a>.</div>
</section>

<section id="quem">
<h2>Quem está nichando, e como</h2>
<p class="sub">Separei à mão as 207 páginas que apareceram vendendo site. Sobraram {nN_pag} nichadas, {nS_pag} plataformas de nicho, 73 genéricas e 13 que ensinam a vender sites.</p>
<div class="duas">
<div class="card"><h3>Nichos atacados pelos {nN_pag} vendedores</h3><p class="sub">Um vendedor conta uma vez, pelo nicho principal</p>
{barras([("Advogados",14),("Psicólogos",5),("Saúde em geral",5),("Clínicas",3),("Dentistas",2),("Imobiliárias e corretores",3),("Nutricionistas",1),("Outros (pet, cerimonial, barbearia, arquitetos, esquadrias)",5),("Por cidade ou região",2),("Vários nichos na mesma peça",2)],42)}</div>
<div class="card"><h3>Cinco jeitos de nichar</h3>
<ol class="passos">
<li><b>Um nicho só, com conselho profissional.</b> Advogar Digital, Oxo e Kromma para advogados; Sites Modernos, Elismael e Notus Studio para psicólogos; Fonseca Web Studio para nutricionistas. O argumento extra é "dentro das regras da OAB / do CFP".</li>
<li><b>Molde multinicho.</b> A mesma arte com a profissão trocada: Publys Tech (advogados, psicólogos e dentistas, R$ 297), Vytron (advogados, psicólogos, dentistas e estética), LPVende (psicólogos, advogados e médicos), Flux (clínicas e fisioterapeutas).</li>
<li><b>Site dentro de um sistema do nicho.</b> Jusfy (58 anúncios, convênio OAB), WebPsi, ImoTools (52 anúncios), Imóvel Guide, Brovia, FREEL e Ritmo (personal).</li>
<li><b>Agência de marketing do nicho com site no pacote.</b> Talismã e TCO (advogados), PHLM (nutricionistas), Aprimora (advogados, manutenção do site).</li>
<li><b>Nicho por lugar.</b> "Seu negócio em São Roque", "pequenas empresas de MG", "clínica veterinária em Moema", Blumenau, Aracaju.</li>
</ol></div>
</div>
<div class="aviso">Na busca, os termos com mais anúncios ativos foram "site para médicos" (1.800), "site para clínicas" (1.600) e "site para restaurantes" (1.100). Mas esse número conta todo anúncio que tem as palavras, não só quem vende site. Para restaurantes, salões, oficinas e igrejas não achei nenhum vendedor de site nichado, só genéricos. Personal trainer só aparece dentro de uma plataforma (Ritmo).</div>
</section>

<section id="criativos">
<h2>Como são os criativos</h2>
<p class="sub">A maior diferença está no primeiro quadro: o nichado abre com a dor do nicho, o genérico abre com o preço.</p>
<div class="duas">
<div class="card"><h3>Primeiro quadro, nichados</h3><p class="sub">{N["q_total"]} criativos únicos, classificados olhando um a um</p>{quadro_bar("N")}</div>
<div class="card"><h3>Primeiro quadro, genéricos</h3><p class="sub">{Gn["q_total"]} criativos únicos</p>{quadro_bar("G")}</div>
<div class="card"><h3>Formato, nichados</h3><p class="sub">{N["ads"]} anúncios</p>{fmt_bar("N")}</div>
<div class="card"><h3>Formato, genéricos</h3><p class="sub">{Gn["ads"]} anúncios</p>{fmt_bar("G")}</div>
</div>
<div class="card" style="margin-top:16px"><h3>O que dizem os textos</h3><p class="sub">Busca por palavras nos textos únicos. Medida aproximada.</p>{temas_tab()}</div>
<p class="sub">"Dinâmico da Meta" é o anúncio em que a Meta combina várias artes e textos sozinha. É muito usado pelos nichados mais novos (Clinarte, Flux, Publys), que sobem 3 ou 4 versões da mesma oferta.</p>
</section>

<section id="ganchos">
<h2>Ganchos que se repetem</h2>
<p class="sub">Frases do texto do anúncio ou da arte. Sem ordem de importância.</p>
{gancho("O que ele encontra quando pesquisa você", "O gancho mais usado pelos nichados. Põe o profissional no lugar do cliente dele.", [("Seu paciente pesquisou o seu nome. O que ele encontrou?","4696471010674229"),("Advogado, quando um cliente pesquisa o seu nome antes de ligar, o que ele encontra?","1145063474637306"),("Seu paciente procura você no Google e encontra só um link na bio?","1470701981696007")])}
{gancho("O concorrente aparece no seu lugar", "Usa uma busca local do nicho como cena.", [("Dentista, sua cadeira vazia tem um motivo: quem pesquisa “lente de contato dental perto de mim” agenda com quem aparece primeiro","1492370412828226"),("Doutor(a), quando alguém pesquisa “advogado perto de mim” no Google, quem aparece: você ou o concorrente?","1181365747561261"),("Todos os dias pessoas pesquisam por nutricionistas no Google","958827420309237")])}
{gancho("O Instagram não é seu", "Medo de perder o perfil ou de depender do algoritmo. O primeiro exemplo roda há 166 dias.", [("Algoritmos mudam, contas podem ser bloqueadas e o alcance pode desaparecer","990996693530281"),("Você é psicólogo(a) e ainda depende apenas das redes sociais para apresentar o seu trabalho?","1359237459732909"),("Se o seu Instagram for bloqueado hoje, quantos clientes você perde amanhã?","1550994653519919")])}
{gancho("Cena do WhatsApp ou do atendimento", "Mostra a conversa que o profissional perde.", [("O paciente chamou às 22h perguntando se tem horário amanhã. Quem respondeu?","1835779044290366"),("Já pensou em mandar o link do seu cerimonial e a noiva sentir, só pelo site, o cuidado que você tem","1155579730324375")])}
{gancho("Quebrar as desculpas", "Lista as objeções e responde cada uma. A Talismã roda esse formato há 230 dias.", [("Ah, mas eu só consigo clientes por indicação (fala no vídeo)","944953507944691"),("“Depois eu faço.” “Já tenho Instagram.” “Minha empresa é pequena.”","2564537490735348")])}
{gancho("Preço e prazo como gancho", "Mais comum nos genéricos, mas os nichados de preço baixo também usam.", [("Site profissional para psicólogos, terapeutas e psicanalistas. Pronto em até 48 horas","2047205416723911"),("Eu faço a sua landing page e você só paga depois de ver pronta. R$ 99","1882788939827463"),("Seu site profissional de R$597 por apenas R$99!","1470324754429948")])}
{gancho("Depoimento do cliente do nicho", "Pouco usado: 3 criativos de prova no recorte.", [("Simplesmente não tem palavras para descrever quanto eu amei (advogada, no vídeo)","1453864926502225")])}
</section>

<section id="galeria">
<h2>Galeria dos criativos</h2>
<p class="sub">Uma seleção de {len(GAL)} criativos que mostram os padrões. Clique para ver o texto, a transcrição e o link da Biblioteca de Anúncios.</p>
<div class="filtros"><button class="on" data-f="todos">Todos</button><button data-f="n">Nichados</button><button data-f="g">Genéricos</button><button data-f="e">Ensinam a vender</button></div>
{galeria()}
</section>

<section id="ofertas">
<h2>Ofertas e preços</h2>
<p class="sub">Preços vistos nos anúncios e nas páginas de destino.</p>
{precos()}
<div class="card" style="margin-top:16px"><h3>Mecânicas de oferta que aparecem</h3>
<ul class="lista">
<li><b>Sem mensalidade</b> como diferencial do preço único (Douglas Business, 250 dias no ar: "você paga uma só vez") e <b>1º ano de hospedagem incluso</b> (Publys).</li>
<li><b>Prazo curto:</b> 60 minutos (barbearia), 24 h, 48 h, 3 dias, 7 dias. Insites roda "a partir de R$ 299, em até 7 dias" há 267 dias, o mais antigo entre quem vende site.</li>
<li><b>Prévia antes de pagar:</b> Flux ("quer ver o site novo da sua clínica antes de pagar?"), LPVende (2ª metade só depois da prévia), Cruzetta ("só paga depois de ver pronta", R$ 99) e Conexão Total ("pague somente na entrega", R$ 99).</li>
<li><b>Diagnóstico grátis</b> como porta de entrada: LPVende (20 a 30 min no WhatsApp), Flux (por escrito em 48 h), Aprimora (check-up do site atual).</li>
<li><b>Três pacotes</b> lado a lado: Flash Sites R$ 697, R$ 1.497 e R$ 2.197; Clinarte R$ 997, R$ 2.497 e R$ 3.997.</li>
<li><b>Ancoragem:</b> "site caro é coisa do passado, R$ 3.000" contra R$ 90/mês; "de R$ 597 por R$ 99" na Black Friday.</li>
<li><b>Itens de nicho somados ao site:</b> Google Meu Negócio, identidade visual de advogado (Ilimitte), cartão com QR Code, logo e mascote por R$ 99 (Escolha seu Site).</li>
<li><b>Escassez com regra:</b> LPVende limita a 8 projetos ao mesmo tempo, com 25% até 30/11.</li>
</ul></div>
</section>

<section id="funil">
<h2>Para onde o clique leva</h2>
<p class="sub">Contando cada vendedor uma vez, pelo destino da maioria dos anúncios.</p>
<div class="duas">
<div class="card"><h3>Nichados</h3><p class="sub">{nDN} vendedores</p>{bar_dest_N}</div>
<div class="card"><h3>Genéricos</h3><p class="sub">{nDG} vendedores</p>{bar_dest_G}</div>
</div>
<div class="card" style="margin-top:16px"><h3>O que as páginas de destino mostram</h3>
<ul class="lista">
<li><b>LPVende (psicólogos):</b> diagnóstico grátis em formulário de 4 passos, depois WhatsApp. Sinal de 50%, prévia em 7 a 15 dias úteis, hospedagem opcional de R$ 49 ou R$ 89 por mês. É a única com prova em número (1º lugar no Google para "cardiologista salvador", pelo Search Console).</li>
<li><b>Clinarte (saúde):</b> três pacotes, 50% na aprovação e 50% na entrega ou 6x, cinco cases com nome do profissional.</li>
<li><b>Advogar Digital:</b> "landing page pronta em até 3 dias", formulário de briefing (landing, site ou refazer; tem logo ou não). Sem preço na página.</li>
<li><b>Fonseca Web Studio (nutricionistas):</b> página feita no Lovable, só botões de WhatsApp com mensagem pronta, "pronto em até 7 dias úteis".</li>
<li><b>Notus Studio (psicólogos, grátis) e Kromma (advogados, quiz):</b> as páginas carregam por código e não abriram na leitura automática.</li>
</ul></div>
</section>

<section id="ensina">
<h2>Quem ensina a vender sites</h2>
<p class="sub">13 páginas vendem ferramenta ou curso para quem quer vender site. Isso mostra quantas pessoas novas estão entrando nesse mercado, e com IA.</p>
<ul class="lista">
<li><b>Valy OS:</b> acha negócios sem site por ramo e cidade no Google Maps, gera o site em 1 minuto e manda o script de abordagem. R$ 697 a R$ 3.497 por ano, garantia de 7 dias. Criativo: "Mandei o site pra dona do salão. Ela respondeu: Quanto custa?".</li>
<li><b>Prompts prontos e cursos rápidos:</b> "Site pronto em 1 hora", "3 sites que eu criei com IA em menos de 10 minutos", prompts do Integra Sites, imersão Acelera IA, Lovable ilimitado.</li>
<li><b>Claude Code para advogados:</b> R$ 148,50 na Black Friday, para o próprio advogado montar o site.</li>
</ul>
<div class="aviso">Leitura: site genérico está virando produto barato feito por IA (R$ 90 a R$ 299). Nichar, com texto dentro das regras do conselho e a cena do cliente daquele nicho, é o jeito que os vendedores estão usando para não brigar só por preço.</div>
</section>

<section id="testar">
<h2>O que parece pouco explorado</h2>
<p class="sub">Raro no recorte indica espaço para testar, mas não prova que funciona: alguém pode ter tentado e parado.</p>
<ul class="lista">
<li><b>Garantia:</b> só 1 texto nichado fala em garantia ou risco zero. A Fade&amp;Co (genérica) usa "7 dias de garantia, ou você ama o seu site ou não paga".</li>
<li><b>Prova com número:</b> só a LPVende mostra resultado medido. Depoimento aparece em 3 de {N["q_total"]} criativos nichados.</li>
<li><b>Prévia antes de pagar:</b> 8% dos textos nichados. É a resposta direta ao medo de pagar e não gostar.</li>
<li><b>Aparecer nas respostas de IA (ChatGPT, Gemini):</b> nenhum nichado fala nisso; só a W2 Websites (genérica).</li>
<li><b>Nichos sem vendedor nichado:</b> restaurantes, salões, oficinas e igrejas. Para eventos, só 1 (cerimonialistas, R$ 997 e R$ 1.597).</li>
<li><b>Ateliês de noiva e debutante:</b> nenhum vendedor de site para eles. A pesquisa da Lennys mostrou que 59% dos anúncios desses ateliês levam ao WhatsApp e só 3% a um site ou quiz, e o site da Lennys já é um caso pronto para mostrar.</li>
</ul>
<div class="card" style="margin-top:16px"><h3>Como seria um teste modelado no que já roda</h3>
<ol class="passos">
<li><b>Um nicho só</b> e o nome dele no primeiro segundo ("Ateliê de noivas,", "Psicólogo(a),").</li>
<li><b>Arte de dor</b> com a busca do cliente do nicho (o que a noiva encontra quando pesquisa o ateliê) e <b>arte de mockup</b> com um site real do nicho.</li>
<li><b>Preço único na faixa de R$ 297 a R$ 597</b>, sem mensalidade no anúncio, e hospedagem cobrada à parte depois.</li>
<li><b>Prévia antes de pagar ou garantia</b>, que quase ninguém usa.</li>
<li><b>WhatsApp como destino</b>, igual à maioria, com uma pergunta de filtro antes do preço.</li>
</ol></div>
</section>

<section id="players">
<h2>Os players nichados</h2>
<p class="sub">Clique no cabeçalho para ordenar. O nome abre todos os anúncios ativos da página na Biblioteca.</p>
{players()}
</section>

<section id="metodo">
<h2>Limites e fontes</h2>
<div class="card"><h3>Como foi feito</h3>
<ul class="lista">
<li>{total_lidos:,} anúncios ativos no Brasil, em 41 buscas na Biblioteca de Anúncios da Meta, em 21/11/2026 (até 120 anúncios por busca), mais todos os anúncios ativos de {nN_pag + nS_pag} páginas nichadas (até 60 por página).</li>
<li>Filtrei por palavras de quem vende site e li as 207 páginas que sobraram, uma a uma, para separar nichado, genérico, plataforma e quem ensina.</li>
<li>Vi o primeiro quadro de 313 criativos únicos e transcrevi os 40 vídeos mais antigos (33 têm fala). Li 10 páginas de destino.</li>
</ul></div>
<div class="card"><h3>O que não foi obtido</h3>
<ul class="lista">
<li><b>Gasto e vendas:</b> a Meta não mostra para anúncio comercial. Tempo no ar é só um indício.</li>
<li><b>Época:</b> semana da Black Friday. Muita coisa tem menos de 10 dias no ar e pode sumir.</li>
<li><b>Busca por palavra:</b> quem vende site sem usar essas palavras no texto ficou de fora.</li>
<li><b>Conversa no WhatsApp:</b> não contatei nenhum vendedor. Preço e fechamento de quem leva direto ao WhatsApp ficaram sem ver.</li>
<li><b>Transcrição automática:</b> tem erros. As frases de vídeo são aproximadas.</li>
</ul></div>
<p class="sub">Dados brutos em <code>01-pesquisa/dados</code>, folhas de criativos em <code>01-pesquisa/criativos</code>, scripts em <code>scripts</code>.</p>
</section>
</main>
<dialog id="dl"><div class="dl"><div class="dl-top"><div><h3 id="dl-tit"></h3><p class="sub" id="dl-sub" style="margin:0"></p></div><button class="fechar" onclick="dl.close()">Fechar</button></div>
<div style="display:grid;grid-template-columns:180px 1fr;gap:16px;margin-top:14px" id="dl-corpo"><img id="dl-img" style="width:100%;border-radius:8px" alt=""><div>
<h4>Texto do anúncio</h4><p id="dl-txt"></p><h4 id="dl-trh">Transcrição automática, com erros</h4><p id="dl-tr"></p>
<a class="botao" id="dl-lib" target="_blank" rel="noopener">Ver na Biblioteca de Anúncios</a></div></div></div></dialog>
<script>
const dl=document.getElementById('dl');
document.querySelectorAll('.item').forEach(b=>b.addEventListener('click',()=>{{
 const d=b.dataset;document.getElementById('dl-tit').textContent=d.tit;document.getElementById('dl-sub').textContent=d.sub;
 document.getElementById('dl-img').src=d.img;document.getElementById('dl-txt').textContent=d.txt||'(sem texto)';
 document.getElementById('dl-tr').textContent=d.tr;document.getElementById('dl-trh').style.display=d.tr?'':'none';
 document.getElementById('dl-lib').href=d.lib;dl.showModal();}}));
document.querySelectorAll('.filtros button').forEach(b=>b.addEventListener('click',()=>{{
 document.querySelectorAll('.filtros button').forEach(x=>x.classList.toggle('on',x===b));
 document.querySelectorAll('#grade .item').forEach(i=>i.style.display=(b.dataset.f==='todos'||i.dataset.f===b.dataset.f)?'':'none');}}));
document.querySelectorAll('#tabela th').forEach(th=>th.addEventListener('click',()=>{{
 const k=+th.dataset.k,tb=th.closest('table').tBodies[0],rs=[...tb.rows],num=th.classList.contains('num');
 const asc=th.dataset.o!=='a';th.dataset.o=asc?'a':'d';
 rs.sort((a,b)=>{{let x=a.cells[k].textContent,y=b.cells[k].textContent;if(num){{x=+x;y=+y;return asc?x-y:y-x}}return asc?x.localeCompare(y,'pt'):y.localeCompare(x,'pt')}});
 rs.forEach(r=>tb.appendChild(r));}}));
const links=[...document.querySelectorAll('.lado nav a')],secs=links.map(a=>document.querySelector(a.getAttribute('href')));
addEventListener('scroll',()=>{{let i=0;secs.forEach((s,j)=>{{if(s.getBoundingClientRect().top<120)i=j}});links.forEach((a,j)=>a.classList.toggle('ativo',j===i))}});
if(matchMedia('(max-width:860px)').matches)document.getElementById('dl-corpo').style.gridTemplateColumns='1fr';
</script></body></html>'''
pag = pag.replace('· 1 dias', '· 1 dia').replace(', 1 dias no ar', ', 1 dia no ar').replace('· 1 dias no ar', '· 1 dia no ar')
pag = pag.replace(f'{total_lidos:,}', f'{total_lidos:,}'.replace(',', '.'))
import re as _re
for _m in _re.finditer('[—–]', pag):
    print('TRAV', repr(pag[max(0, _m.start() - 90):_m.start() + 10]))
open('index.html', 'w', encoding='utf-8').write(pag)
print('ok', len(pag))
