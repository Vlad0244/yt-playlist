from datetime import timedelta


def get_playlist_duration(yt_playlist):
    """
    Helper function
    Used to get the total duration of a playlist in seconds
    :param yt_playlist: link to ytPlaylist
    :return: None. prints total seconds in playlist
    """
    durations_list = []
    for yt_vid in yt_playlist.videos:
        durations_list.append(yt_vid['duration'])
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