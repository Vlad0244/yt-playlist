import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Read the contents of the first JSON file
with open('spotify_tracks_info.json', 'r', encoding='utf-8') as file1:
    data1 = json.load(file1)

# Read the contents of the second JSON file
with open('video_info.json', 'r', encoding='utf-8') as file2:
    data2 = json.load(file2)

# Merge the lists from both files
merged_data = data1 + data2

# Write the merged data to a new JSON file
with open('test_playlist.json', 'w', encoding='utf-8') as merged_file:
    json.dump(merged_data, merged_file, indent=4)
