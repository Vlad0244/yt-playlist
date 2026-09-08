import os
import shutil
import sys
import yt_dlp

PLAYLIST_LINK = sys.argv[1]
DL_DIRECTORY = sys.argv[2]
# Only mp3 and m4a/mp4 are supported for thumbnail embedding for now
PREFERRED_EXTENSION = sys.argv[3]

# ids of videos that can never be downloaded (deleted/private/blocked) are
# remembered here so every run does not retry them
UNAVAILABLE_LIST = '.unavailable_ids.txt'

# error fragments that mean the video is gone for good, as opposed to a
# transient failure like a 403 or a timeout which is worth retrying
PERMANENT_ERRORS = (
    'private video',
    'video is not available',
    'video is unavailable',
    'no longer available',
    'has been terminated',
    'copyright',
    'removed by the uploader',
    'violat',
)



def js_runtime_opts():
    """
    finds an installed javascript runtime and returns the ydl opts selecting it.
    without one youtube only offers formats it cannot descramble, which shows up
    as HTTP 403 on every download.
    :return: dict of extra ydl opts, empty if nothing needs to be passed
    """
    if shutil.which('deno'):
        return {}  # the only runtime yt-dlp enables on its own

    for runtime in ('node', 'bun'):
        if not shutil.which(runtime):
            continue
        try:
            base = yt_dlp.parse_options([]).ydl_opts
            chosen = yt_dlp.parse_options(['--js-runtimes', runtime]).ydl_opts
        except Exception:
            print(f"Found {runtime} but this yt-dlp does not support --js-runtimes; "
                  f"try: pip install -U yt-dlp")
            return {}
        print(f"Using {runtime} as the javascript runtime.")
        return {k: v for k, v in chosen.items() if base.get(k) != v}

    print("WARNING: no javascript runtime found. Downloads will fail with HTTP 403.")
    print("         Install one with:  pkg install nodejs")
    return {}


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
    Return a list of videos in the playlist using yt_dlp.
    :param yt_playlist_url: string url to the playlist
    :return: the list of videos in list format
    """
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,  # Only get metadata, not download
        'skip_download': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(yt_playlist_url, download=False)
        # info['entries'] is a list of video dicts
        return info.get('entries', [])


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


def read_unavailable_ids(pl_path):
    """
    reads the ids of videos previously found to be permanently unavailable.
    :param pl_path: the dir of the playlist
    :return: set of video ids to skip
    """
    try:
        with open(os.path.join(pl_path, UNAVAILABLE_LIST)) as f:
            return {line.strip() for line in f if line.strip()}
    except FileNotFoundError:
        return set()


def mark_unavailable(pl_path, vid_id):
    """
    records a video id as permanently unavailable so it is not retried.
    :param pl_path: the dir of the playlist
    :param vid_id: the id of the video to skip from now on
    :return: None
    """
    with open(os.path.join(pl_path, UNAVAILABLE_LIST), 'a') as f:
        f.write(f'{vid_id}\n')


def is_permanent_error(error):
    """
    decides whether a download error means the video is gone for good.
    :param error: the DownloadError that was raised
    :return: True if the video should never be retried
    """
    message = str(error).lower()
    return any(fragment in message for fragment in PERMANENT_ERRORS)


def clean_leftovers(pl_path, vid_id):
    """
    removes the thumbnail/partial files a failed download leaves behind.
    :param pl_path: the dir of the playlist
    :param vid_id: the id of the video that failed
    :return: None
    """
    for file in os.listdir(pl_path):
        if file.split('=')[-2:-1] == [vid_id] and not file.endswith(f'.{PREFERRED_EXTENSION}'):
            os.remove(os.path.join(pl_path, file))


def download_video(pl_path, url):
    """
    using youtube-dl installs specified song/playlist at specified location.
    :param pl_path: dir where the song is downloaded to
    :param url: yt link or id to video to download
    :return: True if the download succeeded, False otherwise
    """
    try:
        ydl_opts = {
            **JS_RUNTIME_OPTS,
            'format': f'bestaudio[ext={PREFERRED_EXTENSION}]/bestaudio/best',
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
        return True
    except yt_dlp.DownloadError as e:
        print(f"Error: {e}")
        clean_leftovers(pl_path, url)
        if is_permanent_error(e):
            mark_unavailable(pl_path, url)
            print(f"{url} is permanently unavailable, it will be skipped from now on.")
        return False


def phone_create_playlist_dict(pl_path):
    """
    Creates a dict with song id:filename pairing.
    :param pl_path: the dir of the playlist
    :return: the dict of songs on device
    """
    songs_dict = {}
    files = os.listdir(pl_path)
    for file in files:
        if file.split('=')[-1] == f'.{PREFERRED_EXTENSION}':
            pl_id = file.split('=')[-2]
            songs_dict[pl_id] = file
    return songs_dict


def download_songs_in_dir(phone_playlist_dict, yt_playlist_dict):
    """
    downloads and/or updates the songs on the device if not up to date with the playlist on yt.
    :param phone_playlist_dict: a dict containing the song on phone id:filename pair
    :param yt_playlist_dict: a dict containing yt song:song info pair
    :return: None
    """
    ppl = len(phone_playlist_dict)

    if ppl == 0:
        print("Downloading whole playlist")
        download_video(DL_DIRECTORY, PLAYLIST_LINK)
        return

    unavailable_ids = read_unavailable_ids(DL_DIRECTORY)
    changes_made = 0
    failures = 0
    skipped = 0

    for vid_id, filename in phone_playlist_dict.items():

        if vid_id not in yt_playlist_dict:
            os.remove(os.path.join(DL_DIRECTORY, filename))
            changes_made += 1

    for vid_id in yt_playlist_dict:

        if vid_id in phone_playlist_dict:
            continue

        if vid_id in unavailable_ids:
            skipped += 1
            continue

        if download_video(DL_DIRECTORY, vid_id):
            changes_made += 1
        else:
            failures += 1

    if skipped:
        print(f"Skipped {skipped} known unavailable video(s). "
              f"Delete {UNAVAILABLE_LIST} to retry them.")

    if failures:
        print(f"{failures} download(s) failed and will be retried next run.")

    if changes_made == 0 and failures == 0:
        print("Playlist is up to date!")


JS_RUNTIME_OPTS = js_runtime_opts()
create_or_update_playlist(PLAYLIST_LINK, DL_DIRECTORY)
