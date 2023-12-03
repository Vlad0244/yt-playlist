import json
from ytPlaylistToJsonAndLinks import saveVideoInfoToFile
"""
Finds any duplicate links and deletes duplicates. 
Links are the only sure-fire way of uniquely identifying YT videos/songs.
"""

def duplicateSearch(videoInfoJson):
    """
    input: videoInfoJson(string): path to json file. 
    checks if there are existing duplicate links in the json file.
    YT links are an easy to work with unique identifier for every video.
    returns indexes of duplicates.
    """
    with open(videoInfoJson, 'r', encoding='utf-8') as file:
        video_info_list = json.load(file)

        unique_links = set()

        duplicatesIndices = []

        for i, vidInfo in enumerate(video_info_list):
            link = vidInfo.get("link")

            if link in unique_links:
                duplicatesIndices.append(i)
            else:
                unique_links.add(link)
        
        return duplicatesIndices
        # for index in reversed(duplicatesIndices):
        #     del video_info_list[index]
        # saveVideoInfoToFile(video_info_list, videoInfoJson)

duplicates = duplicateSearch('test_playlist.json')
with open('test_playlist.json', 'r', encoding='utf-8') as file:
    video_info_list = json.load(file)
    for i in duplicates:
        print(video_info_list[i])
print(duplicates, len(duplicates))

# duplicateSearch('full_playlist.json')