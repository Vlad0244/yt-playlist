import os
from youtubesearchpython import Playlist
import sys
import yt_dlp

PLAYLIST_LINK = sys.argv[1]
DL_DIRECTORY = sys.argv[2]
# Only mp3 and m4a/mp4 are supported for thumbnail embedding for now
PREFERRED_EXTENSION = sys.argv[3]


def create_or_update_playlist(pl_link, dl_dir):
    """
    creates or updates the playlist based on playlist link and preferred dir.
    :param pl_link: string to the playlist id/link
    :param dl_dir: string to dir you want to dl to
    :return: none
    """
    print("Getting youtube playlist info...")
    yt_songs_dict = yt_create_playlist_dict(pl_link)
    print("Getting local playlist info...")
    phone_songs_dict = phone_create_playlist_dict(dl_dir)
    download_songs_in_dir(phone_songs_dict, yt_songs_dict)


def yt_create_playlist_dict(yt_playlist_url):
    """
    creates the json dict of videos. ids are the keys
    :param yt_playlist_url: url to the yt playlist
    :return: none, makes a json file in the specified save_path
    """
    videos_list = get_yt_playlist(yt_playlist_url)
    playlist_dict = yt_playlist_to_dict(videos_list)
    return playlist_dict


def get_yt_playlist(yt_playlist_url):
    """
    return a list of videos. the videos are a dict of the video's information
    :param yt_playlist_url: string url to the playlist
    :return: the list of videos in list format
    """
    yt_playlist = Playlist(yt_playlist_url)
    while yt_playlist.hasMoreVideos:
        yt_playlist.getNextVideos()
    return yt_playlist.videos


def yt_playlist_to_dict(yt_playlist):
    """
    modifies the videos list to be a dict with ids as keys.
    :param yt_playlist: list of vids
    :return: returns dict of vids with id as key
    """
    video_dict = {}
    for video in yt_playlist:
        video_dict[video['id']] = video
    return video_dict


def download_video(pl_path, url):
    """
    using youtube-dl installs specified song/playlist at specified location.
    :param pl_path: dir where the song is downloaded to
    :param url: yt link or id to video to download
    :return: None
    """
    try:
        ydl_opts = {
            'format': f'{PREFERRED_EXTENSION}/bestaudio/best',
            'outtmpl': f'{pl_path}/%(title)s=%(id)s=.%(ext)s',
            'writethumbnail': True,
            'embedthumbnail': True,
            'postprocessors': [{
                'key': 'FFmpegMetadata',
            },
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': PREFERRED_EXTENSION,
                    'preferredquality': 'best',
                },
                {
                    'key': 'EmbedThumbnail',
                },
            ],

        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        print("Download completed successfully.")
    except yt_dlp.DownloadError as e:
        print(f"Error: {e}")


def phone_create_playlist_dict(pl_path):
    """
    Creates a dict with song id:index pairing.
    :param pl_path: the dir of the playlist
    :return: the dict of songs on device
    """
    songs_dict = {}
    files = os.listdir(pl_path)
    for num, file in enumerate(files):
        if file.split('=')[-1] == '.m4a':
            pl_id = file.split('=')[-2]
            songs_dict[pl_id] = num
    return songs_dict


def download_songs_in_dir(phone_playlist_dict, yt_playlist_dict):
    """
    downloads and/or updates the songs on the device if not up to date with the playlist on yt.
    :param phone_playlist_dict: a dict containing the song on phone id:index in os.listdir pair
    :param yt_playlist_dict: a dict containing yt song:song info pair
    :return: None
    """
    ppl = len(phone_playlist_dict)

    if ppl == 0:
        print("Downloading whole playlist")
        download_video(DL_DIRECTORY, PLAYLIST_LINK)
        return

    changes_made = 0
    files = os.listdir(DL_DIRECTORY)
    for vid_id, i in phone_playlist_dict.items():

        if vid_id not in yt_playlist_dict:
            os.remove(os.path.join(DL_DIRECTORY, files[i]))
            changes_made += 1

    for vid_id in yt_playlist_dict:

        if vid_id not in phone_playlist_dict:
            download_video(DL_DIRECTORY, vid_id)
            changes_made += 1

    if changes_made == 0:
        print("Playlist is up to date!")


create_or_update_playlist(PLAYLIST_LINK, DL_DIRECTORY)
