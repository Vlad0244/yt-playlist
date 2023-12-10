# YouTube Playlist Installer/Updater

This Python script allows you to install a playlist of your choice from YouTube. Re-running the script will update your playlist to match the content of the specified YouTube playlist.

AggregationOfMusicAcrossPlatformsMethods/ contains code I used to pool together songs from spotify/other yt playlists into one playlist.
## Dependencies

Make sure you have the following dependencies installed on your system:

- [youtube-dl](https://github.com/ytdl-org/youtube-dl)
- [ffmpeg](https://ffmpeg.org/)
- [atomicparsley](https://github.com/wez/atomicparsley)
- [youtubesearchpython](https://github.com/alexmercerind/youtube-search-python)

## Instructions

1. download the script to your local machine:

   ```bash
   curl -O https://raw.githubusercontent.com/Vlad0244/yt-playlist/main/downloadingFromYTplaylist/download_yt_playlist.py

2. modify the following variables either via bash script or directly:
   https://github.com/Vlad0244/yt-playlist/blob/b1a6648958f014f21d95bce42e80b67b8801d7ed/downloadingFromYTplaylist/download_yt_playlist.py#L7-L9
    ```
    # youtube link to a playlist
    PLAYLIST_LINK = sys.argv[1]
   
    # directory to where you want to install the songs eg: '/data/storage/music'
    DL_DIRECTORY = sys.argv[2]
   
    # Only mp3 and m4a/mp4 are supported for thumbnail embedding for now
    # do not include the period . before the extension
    PREFERRED_EXTENSION = sys.argv[3]
3. Run the file 
