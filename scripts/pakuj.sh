#!/usr/bin/env bash
# Buduje paczki do wgrania: dist/<nazwa>.zip (folder <nazwa>/ z SKILL.md).
# Użycie: scripts/pakuj.sh [nazwa ...]   (bez argumentów = wszystkie z skills/)
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p dist
names=("$@"); [ ${#names[@]} -eq 0 ] && names=($(ls skills))
for n in "${names[@]}"; do
  [ -f "skills/$n/SKILL.md" ] || { echo "brak skills/$n/SKILL.md" >&2; exit 1; }
  rm -f "dist/$n.zip" "dist/$n.skill"
  (cd skills && zip -qr "../dist/$n.zip" "$n" -x '*/__pycache__/*' '*.pyc')
  echo "dist/$n.zip"
done
