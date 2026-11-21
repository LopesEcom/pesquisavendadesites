import json,subprocess,os,sys,shutil
base='01-pesquisa/dados/'
fila=json.load(open(base+'videos-fila.json',encoding='utf-8'))
N=int(sys.argv[1]) if len(sys.argv)>1 else 30
out_p=base+'transcricoes.json'
res=json.load(open(out_p,encoding='utf-8')) if os.path.exists(out_p) else {}
ff=shutil.which('ffmpeg')
os.chdir(base+'transcricoes')
for v in fila[:N]:
    if v['id'] in res: continue
    dest=v['id']+'.txt'
    af=f"whisper=model=E{chr(92)*2}:/tmp-raiox-atelie/ggml-base.bin:language=pt:queue=10:destination={dest}:format=text"
    try:
        subprocess.run([ff,'-hide_banner','-loglevel','error','-i',v['url'],'-vn','-af',af,'-f','null','-'],timeout=240,capture_output=True)
        t=open(dest,encoding='utf-8',errors='ignore').read().strip() if os.path.exists(dest) else ''
    except Exception as e: t=''
    res[v['id']]={'pagina':v['pagina'],'dias':v['dias'],'t':t}
    print(v['dias'],v['pagina'],len(t),flush=True)
    json.dump(res,open('../transcricoes.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
