D=research/positioning/w4/parts/cc-3
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
for off in 1700 1800 1900 2000 2100 2200 2300; do
 ok=0
 for b in 10 20 40 40; do code=$(curl -s -A "$UA" -o $D/raw/ss_lcb_o$off.json -w "%{http_code}" "https://api.semanticscholar.org/graph/v1/paper/arXiv:2403.07974/citations?fields=title,year,externalIds,abstract&limit=100&offset=$off"); echo "off=$off status=$code"; [ "$code" = 200 ] && ok=1 && break; sleep $b; done
 [ $ok = 0 ] && break
 n=$(python3 -I -c "import json;d=json.load(open('$D/raw/ss_lcb_o$off.json'));print(len(d.get('data',[])), d.get('next','END'))"); echo "  $n"
 case "$n" in *END) break;; esac
 sleep 4
done
