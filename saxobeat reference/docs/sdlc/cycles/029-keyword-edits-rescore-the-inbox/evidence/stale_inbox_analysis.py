"""Cycle 029: read the replay JSON that cycle 021 replay_harness.py --save writes (glossary off) and count how far the inbox rows are from their stored scores.
    uv run python stale_inbox_analysis.py replay.json     (read only, no database)"""
import json,sys,statistics as st
d=json.load(open(sys.argv[1],encoding="utf-8")); rows=d["rows"] if isinstance(d,dict) else d
print(list(d.keys()) if isinstance(d,dict) else "list", list(rows[0].keys()))
inbox=[r for r in rows if r["status"]=="new" and r["stored_version"]==5]
print("inbox v5 rows",len(inbox))
dl=[r["det"]-r["stored_det"] for r in inbox]
print("det delta mean %.2f median %.2f max %.1f min %.1f"%(st.mean(dl),st.median(dl),max(dl),min(dl)))
up=[x for x in dl if x>=1]; dn=[x for x in dl if x<=-1]
print("rise>=1:",len(up),"fall<=-1:",len(dn),"within1:",len(dl)-len(up)-len(dn))
print("rise>=5:",sum(x>=5 for x in dl),"rise>=10:",sum(x>=10 for x in dl))
floor=35
a=sum(1 for r in inbox if r["stored_det"]<floor<=r["det"]); b=sum(1 for r in inbox if r["stored_det"]>=floor>r["det"])
print("cross up (under->at/above floor):",a,"cross down:",b)
# top-50 by stored vs replay
top=lambda k:set(r["job"] for r in sorted(inbox,key=lambda r:-r[k])[:50])
print("top50 overlap stored vs replay:",len(top("stored_det")&top("det")))
top=lambda k:set(r["job"] for r in sorted(inbox,key=lambda r:-r[k])[:100])
print("top100 overlap:",len(top("stored_det")&top("det")))
