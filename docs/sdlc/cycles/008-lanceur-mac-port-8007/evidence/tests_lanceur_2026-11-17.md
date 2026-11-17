# Tests du lanceur sous Linux (2026-11-17)

Script : 4 scénarios, `open` simulé par un script qui note l'URL reçue.

```
=== A. Démarrage normal
A: l'application répond sur 8007
A: navigateur ouvert sur : http://localhost:8007
=== B. Déjà lancé
B: code de sortie 0 ; 1 message 'tourne déjà' ; navigateur : http://localhost:8007
=== C. Port pris par un autre programme
C: code de sortie 1 ; 1 message 'autre programme' ; navigateur : '' ; streamlit lancé : 0
=== D. uv introuvable
D: code de sortie 1 ; 1 message 'uv introuvable' ; 1 commande d'installation
```

Lancement manuel `uv run streamlit run app.py` (sans option de port) : `/_stcore/health` répond « ok » sur 8007.

Mode git : `100755 PO Assist.command`. `bash -n` : syntaxe correcte ; aucune syntaxe bash 4 (mapfile, readarray, declare -A, ${x,,}).

## Sortie du scénario C (port pris)
```
PO Assist · lancement sur http://localhost:8007

Le port 8007 est déjà utilisé par un autre programme :

COMMAND PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
python3 451 root    3u  IPv4    370      0t0  TCP 127.0.0.1:8007 (LISTEN)

Fermez ce programme, puis relancez ce fichier.

```
