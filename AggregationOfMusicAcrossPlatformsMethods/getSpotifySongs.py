import spotipy
import sys
from ytPlaylistToJsonAndLinks import addVideoLinksToList, saveVideoInfoToFile
from spotipy.oauth2 import SpotifyClientCredentials
from config import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, PLAYLIST_ID

client_credentials_manager = SpotifyClientCredentials(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET
)
sys.stdout.reconfigure(encoding='utf-8')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def getSpotifyTracksInBatches(playlistId, batch_size=100):
    spotify_songs_list = []
    offset = 0
    track_count = 0

    while True:
        # Retrieve a batch of tracks (up to batch_size at a time)
        playlist_info = sp.playlist_tracks(playlistId, offset=offset, limit=batch_size)
        tracks = playlist_info['items']

        if not tracks:
            break  # No more tracks to retrieve

        for track in tracks:
            track_count += 1
            track_name = track['track']['name']
            artists = ', '.join([artist['name'] for artist in track['track']['artists']])
            print(f'Track: {track_name} | Artists: {artists}')
            spotify_songs_list.append({
                "title": track_name,
                "channel": artists
            })

        offset += batch_size
    print(track_count)
    spotify_songs_list = addVideoLinksToList(spotify_songs_list)
    return spotify_songs_list

# Call the function to retrieve tracks in batches
batched_spotify_track_list = getSpotifyTracksInBatches(PLAYLIST_ID)

# Save the batched tracks info to a JSON file
saveVideoInfoToFile(batched_spotify_track_list, 'spotify_tracks_info.json')

