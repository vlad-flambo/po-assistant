# Slice 5 drill, 2026-11-06

Scratch SQLite database (not the host, not Neon), four jobs, `conversation.set_places` then `matching.refilter` and `matching.rescore` run directly. Script: the drill in the session scratchpad (guard: refuses any database whose name is not drill.db).

```

== 0 start (the default: Paris only)   filters: cities=['paris'] remote_france=False remote_cities=['london'] remote_only=False
   Head of Operations Hong Kong       hidden: {"code":"location","places":"Paris"}
   Head of Operations Paris           VISIBLE, scored=True
   Head of Operations Remote France   hidden: {"code":"remote_outside","places":"Paris, London"}
   Head of Operations Singapore       hidden: {"code":"location","places":"Paris"}

== 1 only Hong Kong ticked   filters: cities=['hong_kong'] remote_france=False remote_cities=[] remote_only=False
   Head of Operations Hong Kong       VISIBLE, scored=True
   Head of Operations Paris           hidden: {"code":"location","places":"Hong Kong"}
   Head of Operations Remote France   hidden: {"code":"remote_outside","places":"Hong Kong"}
   Head of Operations Singapore       hidden: {"code":"location","places":"Hong Kong"}

== 2 Paris + remote anywhere in France   filters: cities=['paris'] remote_france=True remote_cities=[] remote_only=False
   Head of Operations Hong Kong       hidden: {"code":"location","places":"Paris"}
   Head of Operations Paris           VISIBLE, scored=True
   Head of Operations Remote France   VISIBLE, scored=True
   Head of Operations Singapore       hidden: {"code":"location","places":"Paris"}

== 3 + Remote only   filters: cities=['paris'] remote_france=True remote_cities=[] remote_only=True
   Head of Operations Hong Kong       hidden: {"code":"location","places":"Paris"}
   Head of Operations Paris           hidden: {"code":"not_remote"}
   Head of Operations Remote France   VISIBLE, scored=True
   Head of Operations Singapore       hidden: {"code":"location","places":"Paris"}

== 4 Remote only off again   filters: cities=['paris'] remote_france=True remote_cities=[] remote_only=False
   Head of Operations Hong Kong       hidden: {"code":"location","places":"Paris"}
   Head of Operations Paris           VISIBLE, scored=True
   Head of Operations Remote France   VISIBLE, scored=True
   Head of Operations Singapore       hidden: {"code":"location","places":"Paris"}

== 5 nothing ticked (no limit)   filters: cities=[] remote_france=False remote_cities=[] remote_only=False
   Head of Operations Hong Kong       VISIBLE, scored=True
   Head of Operations Paris           VISIBLE, scored=True
   Head of Operations Remote France   VISIBLE, scored=True
   Head of Operations Singapore       VISIBLE, scored=True
```
