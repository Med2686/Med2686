#!/usr/bin/env bash
# Voix off gratuite -> WAV calé sur une durée cible, puis (option) mixé sur la vidéo.
# Usage : voix_off.sh "texte" sortie.wav [duree_s] [video.mp4 video_sortie.mp4]
# Moteurs, dans l'ordre : edge-tts (voix naturelle, en ligne, non officiel) ->
#   piper (si PIPER_MODEL=chemin/vers/voix.onnx) -> espeak-ng (hors ligne, robotique, toujours dispo après apt install).
set -euo pipefail
TXT="${1:?texte}"; OUT="${2:?sortie.wav}"; DUR="${3:-}"; VID="${4:-}"; VOUT="${5:-}"
VOICE="${VOIX:-fr-FR-DeniseNeural}"; TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
moteur=""
if command -v edge-tts >/dev/null && timeout 20 edge-tts --voice "$VOICE" --text "$TXT" --write-media "$TMP/v.mp3" 2>/dev/null && [ -s "$TMP/v.mp3" ]; then
  ffmpeg -y -loglevel error -i "$TMP/v.mp3" "$TMP/v.wav"; moteur=edge-tts
elif [ -n "${PIPER_MODEL:-}" ] && command -v piper >/dev/null; then
  echo "$TXT" | piper --model "$PIPER_MODEL" --output_file "$TMP/v.wav" >/dev/null 2>&1; moteur=piper
elif command -v espeak-ng >/dev/null; then
  espeak-ng -v "${ESPEAK_VOIX:-fr}" -s "${ESPEAK_VITESSE:-150}" "$TXT" -w "$TMP/v.wav"; moteur=espeak-ng
else
  echo "Aucun moteur de voix : apt-get install -y espeak-ng  (ou pip install edge-tts)" >&2; exit 1
fi
# caler la durée : accélérer (jusqu'à x1,35) si trop long ; sinon laisser tel quel + silence
cur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$TMP/v.wav")
if [ -n "$DUR" ] && awk "BEGIN{exit !($cur > $DUR)}"; then
  r=$(awk "BEGIN{r=$cur/($DUR-0.15); if(r>1.35)r=1.35; printf \"%.3f\", r}")
  ffmpeg -y -loglevel error -i "$TMP/v.wav" -filter:a "atempo=$r" "$TMP/f.wav"; mv "$TMP/f.wav" "$TMP/v.wav"
  cur2=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$TMP/v.wav")
  awk "BEGIN{exit !($cur2 > $DUR)}" && echo "ATTENTION : voix ($cur2 s) plus longue que la cible ($DUR s) même à x1,35 : raccourcir le texte." >&2
fi
cp "$TMP/v.wav" "$OUT"; echo "voix ($moteur) -> $OUT  [$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT") s]"
if [ -n "$VID" ] && [ -n "$VOUT" ]; then
  ffmpeg -y -loglevel error -i "$VID" -i "$OUT" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 160k -af "apad" -shortest "$VOUT"
  echo "vidéo + voix -> $VOUT"
fi
