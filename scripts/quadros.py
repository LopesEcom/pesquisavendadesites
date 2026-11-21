# primeiro quadro, classificado olhando as folhas (uma linha por folha de 20)
# P pessoa falando | M mockup do site | A arte de oferta (preço/lista) | D arte com dor ou pergunta
# T tela gravada ou bastidor | V prova de cliente | O marca, abstrato ou outro
F=['PAOOPPTDPPDDMDDDDMTO','PAOAOOPMMPVPPAPAMOAO','OMMPPPPPPDOPAAMOPMPO','APOODTTPDTODDDOOOAOP',
'DMPDPOOTDODDPPODOMMA','PDAAAPAAPOPOAPTVPAMA','OAOOOOPOAOAPDMPOMAPP','MMAAAOOOOOAAPAPPMAMD',
'PAAOAPPDPOOADAAMDMDP','VOAAMPPDPADDOAPMAAAD','MDMAAAAPPPPDPPAAOMTD','MAPAAMPAADATAATAMPPD',
'OOADDAAOOOAPMOAADOTM','MOMDODAOOODDDDPPPPAM','OPPDODDMMMDPATAMADAP','PAAADODDPAAAT']
assert all(len(x)==20 for x in F[:-1]) and len(F[-1])==13
S=''.join(F)
