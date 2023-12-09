
import vlc

player = vlc.MediaListPlayer()
mediaList = vlc.MediaList(["https://www.youtube.com/watch?v=yXQViqx6GMY"])
player.set_media_list(mediaList)
player.set_playback_mode(vlc.PlaybackMode.loop)
player.play()