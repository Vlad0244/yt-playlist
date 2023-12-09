# YouTube Playlist Installer/Updater

This Python script allows you to install a playlist of your choice from YouTube. Re-running the script will update your playlist to match the content of the specified YouTube playlist.

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

2. change the following variables either via bash script or directly:
    ```
    PLAYLIST_LINK = sys.argv[1]
    DL_DIRECTORY = sys.argv[2]
    PREFERRED_EXTENSION = sys.argv[3]
3. Run the file 
