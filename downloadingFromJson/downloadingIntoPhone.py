import json
import subprocess
import os
import json
from youtubesearchpython import Playlist
from datetime import datetime, timedelta
import sys
import subprocess

""" 
main pl:
playlist_url = "https://www.youtube.com/playlist?list=PLia5vPs9sr0s6c2SDvCU8D_8BzDMh4N4B"
test pl:
playlist_url = "https://www.youtube.com/playlist?list=PLia5vPs9sr0vcXT795-gzPJCpFTQsBlSw"

"""

"""
-format of each song from youtubesearchpython Playlist.videos list:
    {'id': '9NdJRtPqCR0', 'thumbnails': 
    [{'url': 'https://i.ytimg.com/vi/9NdJRtPqCR0/hqdefault.jpg?sqp=-oaymwEbCKgBEF5IVfKriqkDDggBFQAAiEIYAXABwAEG&rs=AOn4CLAfH0CDufm6L3AsfabAzroMBR5MaA', 'width': 168, 'height': 94}, 
    {'url': 'https://i.ytimg.com/vi/9NdJRtPqCR0/hqdefault.jpg?sqp=-oaymwEbCMQBEG5IVfKriqkDDggBFQAAiEIYAXABwAEG&rs=AOn4CLDaPa2xooSkeBkWxnybzT4TvyWqfA', 'width': 196, 'height': 110}, 
    {'url': 'https://i.ytimg.com/vi/9NdJRtPqCR0/hqdefault.jpg?sqp=-oaymwEcCPYBEIoBSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLBuQthIKi-buAFezjiwoq2Pk1aA4A', 'width': 246, 'height': 138}, 
    {'url': 'https://i.ytimg.com/vi/9NdJRtPqCR0/hqdefault.jpg?sqp=-oaymwEcCNACELwBSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLCQaE9tdvCEkSR3kYk10IBb8LsSWw', 'width': 336, 'height': 188}], 
    'title': 'Above & Beyond - Always feat. Zoë Johnston (Above & Beyond Club Mix)', 
    'channel': {'name': 'Above & Beyond', 'id': 'UCVE-ybBDg3UHSUylEVdPAsw', 'link': '/channel/UCVE-ybBDg3UHSUylEVdPAsw'}, 
    'duration': '4:35', 
    'accessibility': {'title': 'Above & Beyond - Always feat. Zoë Johnston (Above & Beyond Club Mix) by Above & Beyond 264,810 views 5 years ago 4 minutes, 35 seconds', 'duration': '4 minutes, 35 seconds'}, 
    'link': 'https://www.youtube.com/watch?v=9NdJRtPqCR0&list=PLia5vPs9sr0s6c2SDvCU8D_8BzDMh4N4B&index=1&pp=iAQB', 'isPlayable': True}
id = the unique youtube song id
"""

# Set these in a script; or modify it directly for your playlist and directory you want to dl to
playlist_link = sys.argv[1]
dl_directory = sys.argv[2]


def create_or_update_playlist(pl_link, dl_dir):
    yt_create_playlist_json(pl_link)
    download_songs_in_dir()

def yt_create_playlist_json(yt_playlist_url, save_path='yt_playlist.json'):
    """
    creates the json dict of videos. ids are the keys
    :param yt_playlist_url: url to the yt playlist
    :param save_path: where you want to save
    :return: none, makes a json file in the specified save_path
    """
    videos_list = get_yt_playlist(yt_playlist_url)
    playlist_dict = yt_playlist_to_dict(videos_list)
    save_playlist_to_json(playlist_dict, save_path)


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


def save_playlist_to_json(playlist_vids, file_path='playlist.json'):
    """
    saves the yt_playlist_vids dict to a json file to a specified file_path
    :param yt_playlist_vids: a dict of the videos with keys being the ids
    :param file_path: name of file path and json file
    :return: creates/updates a json file of the videos on local specified path
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(playlist_vids, file, ensure_ascii=False, indent=4)


def download_video(pl_path, url):
    try:
        command = f'youtube-dl -o "{pl_path}/%(title)s=%(id)s=.%(ext)s" --audio-format m4a --extract-audio --add-metadata --embed-thumbnail "{url}"'
        subprocess.run(command, check=True)
        print("Download completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


def make_phone_dir_songs_json(pl_path):
    songs_dict = {}
    files = os.listdir(pl_path)
    for num, file in enumerate(files):
        if file.split('=')[-1] == '.m4a':
            pl_id = file.split('=')[-2]
            songs_dict[pl_id] = num
    save_playlist_to_json(songs_dict, 'phoneSongs.json')


make_phone_dir_songs_json(dl_directory)


def download_songs_in_dir(yt_pl_json, phone_pl_json):
    with open(phone_pl_json, 'r') as pl_file:
        phone_playlist_data = json.load(pl_file)
        with open(yt_pl_json, 'r') as yt_file:
            yt_playlist_data = json.load(yt_file)
            ppl = len(phone_playlist_data)
            ytpl = len(yt_playlist_data)
            if ppl == ytpl:
                print('Up to Date')
                return
            if ppl == 0:
                download_video(dl_directory, playlist_link)
                return
            files = os.listdir(dl_directory)
            for vid_id, i in phone_playlist_data.items():
                if vid_id not in yt_playlist_data:
                    os.remove(os.path.join(dl_directory, files[i]))
            for vid_id in yt_playlist_data:
                if vid_id not in phone_playlist_data:
                    download_video(dl_directory, vid_id)
