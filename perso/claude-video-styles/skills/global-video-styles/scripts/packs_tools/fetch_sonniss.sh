#!/usr/bin/env bash
# Download + extract Sonniss #GameAudioGDC bundles part by part (resume-safe), deleting each zip only after a clean extraction.
# usage: bash fetch_sonniss.sh 2026 2024     (then: python ../sfx_packs.py scan && python ../sfx_packs.py index)
# Sizes (2026-11-14): GDC2026 = 5 zips, 6.9 GB download, 7.5 GiB extracted, 301 WAV; GDC2024 = 9 zips, 23.5 GB download, 28 GiB extracted.
# Disk guard: refuses to start a part unless C: keeps >= MINFREE_GB free after the part is downloaded AND extracted.
set -u
PACKS="~/.claude/skills/global-video-styles/sfx/packs"
DL="$PACKS/_downloads"; mkdir -p "$DL"
SEVENZ="/c/Program Files/7-Zip/7z.exe"
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
MINFREE_GB=${MINFREE_GB:-46}
free_gb() { df -BG --output=avail /c | tail -1 | tr -dc '0-9'; }
for YEAR in "$@"; do
  case $YEAR in 2026) N=5;; 2024) N=9;; *) echo "unknown year $YEAR"; continue;; esac
  OUT="$PACKS/sonniss-gdc$YEAR"; mkdir -p "$OUT"
  for i in $(seq 1 $N); do
    NAME="Sonniss.com-GDC${YEAR}-GameAudioBundle${i}of${N}.zip"
    DONE="$OUT/.part${i}.done"
    [ -f "$DONE" ] && { echo "[$YEAR $i/$N] already extracted"; continue; }
    URL="https://downloads.sonniss.com/$NAME"
    SIZE=$(curl -sIL -A "$UA" "$URL" | grep -i '^content-length' | tail -1 | tr -dc '0-9')
    NEED=$(( SIZE * 2 / 1000000000 + 1 ))
    F=$(free_gb)
    if [ $(( F - NEED )) -lt $MINFREE_GB ]; then echo "[$YEAR $i/$N] STOP: free ${F}G, part needs ${NEED}G, floor ${MINFREE_GB}G"; exit 2; fi
    echo "[$YEAR $i/$N] $(date +%H:%M:%S) downloading $NAME ($((SIZE/1000000)) MB), free ${F}G"
    for try in 1 2 3 4 5 6; do
      curl -sS -L -A "$UA" --retry 5 --retry-delay 10 -C - -o "$DL/$NAME" "$URL" && break
      echo "  retry $try"; sleep 15
    done
    GOT=$(stat -c %s "$DL/$NAME" 2>/dev/null || echo 0)
    if [ "$GOT" != "$SIZE" ]; then echo "[$YEAR $i/$N] size mismatch $GOT != $SIZE"; exit 3; fi
    echo "[$YEAR $i/$N] $(date +%H:%M:%S) extracting"
    WIN_ZIP=$(cygpath -w "$DL/$NAME"); WIN_OUT=$(cygpath -w "$OUT")
    cmd.exe //c start "\"\"" //belownormal //b //wait "C:\Program Files\7-Zip\7z.exe" x -y -bd -mmt=2 "-o$WIN_OUT" "$WIN_ZIP" > "$DL/$NAME.log" 2>&1
    RC=$?
    if [ $RC -eq 0 ] && grep -q "Everything is Ok" "$DL/$NAME.log"; then
      rm -f "$DL/$NAME"; touch "$DONE"; echo "[$YEAR $i/$N] $(date +%H:%M:%S) ok, zip deleted, free $(free_gb)G"
    else
      echo "[$YEAR $i/$N] extraction failed rc=$RC (zip kept)"; tail -5 "$DL/$NAME.log"; exit 4
    fi
  done
done
# keep every path under 240 chars (Python / ffmpeg / Explorer MAX_PATH); originals listed in <pack>/_renamed.json
for YEAR in "$@"; do
  "$HOME/.venvs/claude-video/Scripts/python.exe" "$(dirname "$0")/../sfx_packs.py" shorten "$PACKS/sonniss-gdc$YEAR"
done
echo SONNISS_DONE
