#!/usr/bin/env bash
# Turn the maker's screen recordings into 1440x810 JPEG frame sequences at 30 fps,
# already sped up / slowed down, so the page can show them frame-accurately (Chromium can't play H.264).
# usage: edit the lines below, then  bash extract_clips.sh "/path/to/videos"
# ex <name> <file> <start s> <length s> <speed> <crop w:h:x:y (16:9 box around the site content)>
set -e; SRC="$1"; C=clips
ex(){ mkdir -p $C/$1; rm -f $C/$1/*.jpg
  ffmpeg -v error -y -ss $3 -t $4 -i "$SRC/$2" -an -vf "crop=$6,scale=1440:810:flags=lanczos,setpts=(PTS-STARTPTS)/$5,fps=30" -q:v 3 $C/$1/%04d.jpg
  echo "$1: $(ls $C/$1 | wc -l) frames"; }
# EP.01 Arkedia
ex home   "Hompage.mp4"                        0  7.9   0.664 1440:810:290:0
ex hanoi  "Tower of Hanoi (game).mp4"          0  17.07 1.8   1440:810:235:0
ex ttt    "Tic-Tac-Toe.mp4"                    10 12.9  1.11  1600:900:153:180
ex memory "Memory (game).mp4"                  20 30.5  3.5   1600:900:160:70
ex howto  "(It has how to play sections).mp4"  0  10.26 1.49  1280:720:150:0
# stills (for slow Ken Burns moves): ffmpeg -ss 4.25 -i "$SRC/Hompage.mp4" -vf crop=1440:810:290:0 -frames:v 1 -q:v 2 clips/stills/home_4.25.jpg
