
from config import API_KEY


import json
import google.oauth2.credentials
from googleapiclient.discovery import build
import time
# Read your JSON file containing song data
with open('full_playlist.json', 'r', encoding='utf-8') as file:
    songs_data = json.load(file)
print(len(songs_data))
# Authenticate with the YouTube Data API
credentials = google.oauth2.credentials.Credentials.from_authorized_user_file('user_credentials.json')
youtube = build('youtube', 'v3', credentials=credentials)

# Define the ID of your YouTube playlist
playlist_id = ''

# Prepare the playlist items for all songs
playlist_items = []
for song in songs_data:
    video_id = song['link']
    link_id = video_id.split('v=')[1]
    playlist_items.append({
        'snippet': {
            'playlistId': playlist_id,
            'resourceId': {
                'kind': 'youtube#video',
                'videoId': link_id
            }
        }
    })

# Add all playlist items with a delay between requests
# for index in range(1000, len(playlist_items)):
#     playlist_item = playlist_items[index]
#     request = youtube.playlistItems().insert(
#         part='snippet',
#         body=playlist_item
#     )
#     print(index)
#     response = request.execute()

print('All videos added to the playlist.')
