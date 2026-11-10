import sys, re, html, json, subprocess, urllib.parse, os, time
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
qid_tag, q, outdir = sys.argv[1], sys.argv[2], sys.argv[3]
maxr = int(sys.argv[4]) if len(sys.argv) > 4 else 100
assert len(q) <= 64, "query too long"
hits = []; total = None; statuses = []
for start in range(0, maxr, 10):
    url = "https://search.arxiv.org/?in=&query=" + urllib.parse.quote(q) + (f"&startat={start}" if start else "")
    fn = os.path.join(outdir, f"{qid_tag}_p{start//10}.html")
    r = subprocess.run(["curl", "-s", "-A", UA, "-o", fn + ".body", "-w", "%{http_code}", url], capture_output=True, text=True)
    st = r.stdout.strip(); statuses.append(st)
    body = open(fn + ".body", encoding="utf-8", errors="replace").read()
    os.remove(fn + ".body")
    with open(fn, "w") as f:
        f.write(f"<!-- URL: {url}\n DATE: 2026-11-10\n HTTP: {st} -->\n" + body)
    m = re.search(r"Displaying hits (\d+) to (\d+) of (\d+)", body)
    if not m:
        if total is None: total = 0
        break
    total = int(m.group(3))
    s = re.sub(r"<script.*?</script>|<style.*?</style>", "", body, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", s); t = re.sub(r"\s+", " ", html.unescape(t))
    t = t.split("Reorder by date .", 1)[-1]
    parts = re.split(r"https://arxiv\.org/abs/([0-9]{4}\.[0-9]{4,5}|[a-z\-]+/[0-9]{7})", t)
    for i in range(0, len(parts) - 1, 2):
        hits.append({"id": parts[i + 1], "snip": parts[i].strip()[:600]})
    if int(m.group(2)) >= total: break
    time.sleep(1)
json.dump({"tag": qid_tag, "query": q, "total": total, "statuses": statuses, "hits": hits},
          open(os.path.join(outdir, f"{qid_tag}.json"), "w"), indent=1)
print(f"{qid_tag}\t{q}\ttotal={total}\tread={len(hits)}\tHTTP={','.join(statuses)}")
