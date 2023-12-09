from curses.panel import new_panel
from inspect import getsource
from pathlib import Path
import glob
import vlc



mp3_files = [
    "/Users/macmini2023/Dropbox/03_WORKSPACE/01_Codes/231209_utaoi_radio/utaoi-radio/src/cache/【鈴木翼】ハブラシ電車.m4a"
]
player = vlc.MediaListPlayer()
mediaList = vlc.MediaList(mp3_files)
player.set_media_list(mediaList)
player.set_playback_mode(vlc.PlaybackMode.loop)
player.play()


player.stop()

mp3_files = [
    "/Users/macmini2023/Dropbox/03_WORKSPACE/01_Codes/231209_utaoi_radio/utaoi-radio/src/cache/はみがきじょうずかな ⧸ おかあさんといっしょ (Coverd byうたスタ) 【楽しく歯磨き習慣！】.m4a"
]
mediaList = vlc.MediaList(mp3_files)
player.set_media_list(mediaList)
player.set_playback_mode(vlc.PlaybackMode.loop)
player.play()

while True:
    pass