from youtubesearchpython import Playlist
from datetime import datetime, timedelta
import sys
print((111*60+45)*60)
def jsonFromYtPlaylist(playlist):
    yt_playlist = Playlist(playlist)
    prints = 0
    while yt_playlist.hasMoreVideos:
        yt_playlist.getNextVideos()
        #print(f'Videos Retrieved: {len(yt_playlist.videos)}')
        # add code to create json file from playlist
    #print(yt_playlist.videos)
    durations_list = []
    index = 0
    for yt_vid in yt_playlist.videos:
        durations_list.append(yt_vid['duration'])
        index += 1
    print(durations_list)
    print(index)
    total_time = timedelta()  # Initialize total_time to zero
    total_seconds = 0
    for length in durations_list:
        components = length.split(':')
        if len(components) == 2:
            # Minutes and seconds
            time_delta = timedelta(minutes=int(components[0]), seconds=int(components[1]))
        elif len(components) == 3:
            # Hours, minutes, and seconds
            time_delta = timedelta(hours=int(components[0]), minutes=int(components[1]), seconds=int(components[2]))
        else:
            raise ValueError(f"Invalid time format: {length}")

        total_seconds += time_delta.total_seconds()

    print("Total Duration of Playlist (seconds):", total_seconds)





jsonFromYtPlaylist('https://www.youtube.com/playlist?list=PLia5vPs9sr0s6c2SDvCU8D_8BzDMh4N4B')

import subprocess


def download_video(url, output_path="."):
    try:
        #command = ["youtube-dl", "--no-warnings", "--verbose", "-o", f"{output_path}/%(title)s.%(ext)s", url]
        command = "youtube-dl -k --audio-format wav --extract-audio 9NdJRtPqCR0 "
        playlist_url = "https://www.youtube.com/playlist?list=PLia5vPs9sr0s6c2SDvCU8D_8BzDMh4N4B"




        subprocess.run(command, check=True)
        print("Download completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


# Example usage
id = "9NdJRtPqCR0"
# video_url = id
video_url = "https://www.youtube.com/watch?v=" + id

# download_video(video_url)
"""
{'id': '9NdJRtPqCR0', 'thumbnails': [{'url': 'https://i.ytimg.com/vi/9NdJRtPqCR0/hqdefault.jpg?sqp=-oaymwEbCKgBEF5IVfKriqkDDggBFQAAiEIYAXABwAEG&rs=AOn4CLAfH0CDufm6L3AsfabAzroMBR5MaA', 'width': 168, 'height': 94}, {'url': 'https://i.ytimg.com/vi/9NdJRtPqCR0/hqdefault.jpg?sqp=-oaymwEbCMQBEG5IVfKriqkDDggBFQAAiEIYAXABwAEG&rs=AOn4CLDaPa2xooSkeBkWxnybzT4TvyWqfA', 'width': 196, 'height': 110}, {'url': 'https://i.ytimg.com/vi/9NdJRtPqCR0/hqdefault.jpg?sqp=-oaymwEcCPYBEIoBSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLBuQthIKi-buAFezjiwoq2Pk1aA4A', 'width': 246, 'height': 138}, {'url': 'https://i.ytimg.com/vi/9NdJRtPqCR0/hqdefault.jpg?sqp=-oaymwEcCNACELwBSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLCQaE9tdvCEkSR3kYk10IBb8LsSWw', 'width': 336, 'height': 188}], 'title': 'Above & Beyond - Always feat. Zoë Johnston (Above & Beyond Club Mix)', 'channel': {'name': 'Above & Beyond', 'id': 'UCVE-ybBDg3UHSUylEVdPAsw', 'link': '/channel/UCVE-ybBDg3UHSUylEVdPAsw'}, 'duration': '4:35', 'accessibility': {'title': 'Above & Beyond - Always feat. Zoë Johnston (Above & Beyond Club Mix) by Above & Beyond 264,810 views 5 years ago 4 minutes, 35 seconds', 'duration': '4 minutes, 35 seconds'}, 'link': 'https://www.youtube.com/watch?v=9NdJRtPqCR0&list=PLia5vPs9sr0s6c2SDvCU8D_8BzDMh4N4B&index=1&pp=iAQB', 'isPlayable': True}

"""
