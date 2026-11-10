import json,glob,re,sys
kw=re.compile(r'(calibrat|uncertaint|confidence|overconfiden|hidden.state|probe)',re.I)
code=re.compile(r'(code|program|software)',re.I)
seen={}
for f in sorted(glob.glob(sys.argv[1]+'/ss_*_o*.json')):
    try:d=json.load(open(f))
    except: continue
    for r in d.get('data',[]):
        p=r['citingPaper']; t=p.get('title') or ''; a=p.get('abstract') or ''
        if kw.search(t+a) and code.search(t+a) and (kw.search(t) or len(kw.findall(a))>=2):
            seen[p['paperId']]=(p.get('year'),(p.get('externalIds') or {}).get('ArXiv'),t)
for k,v in sorted(seen.items(),key=lambda x:str(x[1][0]),reverse=True): print(v)
print(len(seen))
