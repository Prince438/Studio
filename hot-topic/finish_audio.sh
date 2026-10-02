#!/usr/bin/env bash
# Final loudness for KD Hot Topic: gentle compression, then ONE fixed gain to -14 LUFS integrated, then a peak limiter.
# (Single-pass ffmpeg loudnorm normalises dynamically and lifts quiet parts such as the intro and end card back up,
#  which undoes the subtle music bed set in mix_vo.py. A fixed gain keeps the mix balance exactly as designed.)
set -e
ffmpeg -v error -y -i out/audio_vo.wav -af "acompressor=threshold=-18dB:ratio=2.5:attack=8:release=120" -c:a pcm_f32le out/audio_comp.wav
I=$(ffmpeg -hide_banner -nostats -i out/audio_comp.wav -af ebur128 -f null - 2>&1 | grep -A2 "Integrated loudness" | grep -oE "I: +-?[0-9.]+" | grep -oE -- "-?[0-9.]+")
G=$(awk -v i="$I" 'BEGIN{printf "%.2f", -14 - i}')
ffmpeg -v error -y -i out/audio_comp.wav -af "volume=${G}dB,alimiter=limit=0.7:level=false" -ar 44100 out/audio_final.wav
echo "measured ${I} LUFS -> gain ${G} dB"
ffmpeg -hide_banner -nostats -i out/audio_final.wav -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I|Peak):"
