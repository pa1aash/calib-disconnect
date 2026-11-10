import json,sys,re
code=re.compile(r'HumanEval|MBPP|LiveCodeBench|EvalPlus|code generation|program|APPS|BigCodeBench|CodeContests|pass@',re.I)
cal=re.compile(r'ECE|calibrat|Brier|AUROC|confidence|uncertaint',re.I)
for f in sys.argv[1:]:
    d=json.load(open(f));print('==',d['tag'],d['query'],d['total'],len(d['hits']))
    for h in d['hits']:
        s=h['snip']; flag=('C' if code.search(s) else '-')+('K' if cal.search(s) else '-')
        if flag=='CK': print(h['id'],flag,'|',s[:300])
