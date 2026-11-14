"""Cycle 029: compare candidate 1 keywords of the 28 Oct dump (jobs_config rows exported with pg_restore -t jobs_config --data-only -f cfg28.sql) with the 29 Oct scratch copy (psql -At -c "select keywords::text, keyword_weight, profile_version, md5(profile_text) from jobs_config where candidate_id=1" > cfg29.txt).
    uv run python config_diff.py <folder holding cfg28.sql and cfg29.txt>"""
import json,sys
sp=sys.argv[1]
lines=open(sp+"/cfg28.sql",encoding="utf-8",errors="replace").read().split("\n")
i=[k for k,l in enumerate(lines) if l.startswith("COPY")][0]+1
rows=[]
for l in lines[i:]:
    if l.startswith("\."): break
    rows.append(l.split("\t"))
row=[r for r in rows if r[-1]=="1"][0]
old=json.loads(row[3]); print("28 Oct c1 pv",row[2],"kw_weight",row[6])
new=open(sp+"/cfg29.txt",encoding="utf-8",errors="replace").read().strip().split("|")
nk=json.loads("|".join(new[:-3])); print("29 Oct c1 pv",new[-2],"kw_weight",new[-3])
for side in ("include","exclude"):
    o=old.get(side,{}); n=nk.get(side,{})
    print(side,len(o),"->",len(n))
    print(" added",{k:v for k,v in n.items() if k not in o})
    print(" removed",{k:v for k,v in o.items() if k not in n})
    print(" reweighted",{k:(o[k],n[k]) for k in n if k in o and o[k]!=n[k]})
