#!/bin/bash
# PO Assist : double-cliquer sur ce fichier dans le Finder pour lancer l'application (macOS).
# Elle s'ouvre dans le navigateur sur http://localhost:8007. Fermer cette fenêtre (ou Ctrl+C) l'arrête.
# Compatible avec le bash 3.2 fourni par macOS.

PORT=8007
URL="http://localhost:$PORT"

cd "$(dirname "$0")" || exit 1
HERE="$(pwd -P)"

pause() {
  echo
  read -r -p "Appuyez sur Entrée pour fermer cette fenêtre. " _ || true
}

open_browser() {
  if command -v open >/dev/null 2>&1; then
    open "$URL"
  elif command -v xdg-open >/dev/null 2>&1; then
    xdg-open "$URL" >/dev/null 2>&1
  else
    echo "Ouvrez $URL dans votre navigateur."
  fi
}

echo "PO Assist · lancement sur $URL"
echo

# 1. uv (une fenêtre ouverte depuis le Finder n'a pas toujours le PATH du terminal)
if ! command -v uv >/dev/null 2>&1; then
  for dir in "$HOME/.local/bin" "$HOME/.cargo/bin" /opt/homebrew/bin /usr/local/bin; do
    if [ -x "$dir/uv" ]; then
      PATH="$dir:$PATH"
      export PATH
      break
    fi
  done
fi
if ! command -v uv >/dev/null 2>&1; then
  echo "uv est introuvable : c'est l'outil qui installe Python et les dépendances de PO Assist."
  echo "Installez-le avec l'une de ces commandes, puis relancez ce fichier :"
  echo
  echo "    curl -LsSf https://astral.sh/uv/install.sh | sh"
  echo "    brew install uv"
  pause
  exit 1
fi

# 2. Le port 8007 est-il libre ?
PID=""
if command -v lsof >/dev/null 2>&1; then
  PID="$(lsof -nP -t -iTCP:"$PORT" -sTCP:LISTEN 2>/dev/null | head -n 1)"
fi
if [ -n "$PID" ]; then
  CWD="$(lsof -a -p "$PID" -d cwd -Fn 2>/dev/null | sed -n 's/^n//p' | head -n 1)"
  if [ -n "$CWD" ] && [ "$(cd "$CWD" 2>/dev/null && pwd -P)" = "$HERE" ]; then
    echo "PO Assist tourne déjà sur $URL : ouverture du navigateur."
    open_browser
    exit 0
  fi
  echo "Le port $PORT est déjà utilisé par un autre programme :"
  echo
  lsof -nP -iTCP:"$PORT" -sTCP:LISTEN 2>/dev/null
  echo
  echo "Fermez ce programme, puis relancez ce fichier."
  pause
  exit 1
fi

# 3. Environnement Python (la première fois : une à deux minutes)
echo "Préparation de l'environnement…"
if ! uv sync --quiet; then
  echo "La préparation de l'environnement a échoué (voir le message ci-dessus)."
  pause
  exit 1
fi

# 4. Ouvrir le navigateur dès que l'application répond, puis la lancer
(
  for _ in $(seq 1 90); do
    if curl -fsS "$URL/_stcore/health" >/dev/null 2>&1; then
      open_browser
      exit 0
    fi
    sleep 1
  done
  echo "L'application ne répond pas après 90 secondes : regardez les messages ci-dessus."
) &

echo "PO Assist démarre. Fermez cette fenêtre (ou Ctrl+C) pour l'arrêter."
echo
exec uv run streamlit run app.py --server.port "$PORT" --server.headless true
