from youtubesearchpython import Playlist
import sys
def jsonFromYtPlaylist(playlist):
    yt_playlist = Playlist(playlist)
    prints = 0
    while yt_playlist.hasMoreVideos:
        yt_playlist.getNextVideos()
        print(f'Videos Retrieved: {len(yt_playlist.videos)}')
        # add code to create json file from playlist
    print(yt_playlist)
jsonFromYtPlaylist('https://www.youtube.com/playlist?list=PLia5vPs9sr0s6c2SDvCU8D_8BzDMh4N4B')