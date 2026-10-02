#!/usr/bin/env bash
# Two-pass x264 encode of both formats with the shared audio mix.
# The video bitrate is worked out from the duration so each file lands near 27 MB (under the 30 MB rule), capped at 2600k.
# usage: bash encode.sh kd-hot-topic_2026-10-02      -> <name>_16x9.mp4 and <name>_9x16.mp4
set -e
NAME=${1:?name}
NULL=/dev/null; [ "$OS" = "Windows_NT" ] && NULL=NUL
for f in out:16x9 out-916:9x16; do
  dir=${f%%:*}; tag=${f##*:}
  [ -f "$dir/video_silent.mp4" ] || { echo "skip $tag (no $dir/video_silent.mp4)"; continue; }
  DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$dir/video_silent.mp4")
  BR=$(awk -v d="$DUR" 'BEGIN{b=int(27*8*1024/d-140); if(b>2600)b=2600; print b}')
  echo "$tag: ${DUR}s -> ${BR}k"
  (cd "$dir" && ffmpeg -v error -y -i video_silent.mp4 -c:v libx264 -preset slow -tune animation -b:v ${BR}k -maxrate 5000k -bufsize 10000k -pass 1 -passlogfile x264 -an -f mp4 $NULL)
  ffmpeg -v error -y -i "$dir/video_silent.mp4" -i out/audio_final.wav -c:v libx264 -preset slow -tune animation -b:v ${BR}k -maxrate 5000k -bufsize 10000k \
    -pass 2 -passlogfile "$dir/x264" -pix_fmt yuv420p -c:a aac -b:a 128k -movflags +faststart -shortest "${NAME}_${tag}.mp4"
  ls -la "${NAME}_${tag}.mp4"
done
