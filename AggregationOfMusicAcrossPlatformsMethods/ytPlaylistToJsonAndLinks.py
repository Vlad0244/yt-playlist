import os
from youtubesearchpython import VideosSearch
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')
import time
#provide the path to your text file
file_path = "ytPlaylistTestCopy.txt"
"""
Goal of this progrm is to read a txt file in the following format
that is copy pasted text from a youtube playlist:

3:15
NOW PLAYING
Hide and Seek
she
•
14K views • 3 years ago


2:45
NOW PLAYING
Hareton Salvanini - Quarto de Hotel
Ricardo Maraña
•
2.4M views • 6 years ago

then get the link to this video using VideosSearch from youtubesearchpython and 
store the info in a JSON file. 

Not really useful considering there are tools online that can downlaod 
a playlist given a youtube link. Just an excercise in reading a file given
some information and using Python API for Youtube. This JSON file will be used
as input to install songs based on the link.
"""
#define a function to extract video information from the text file
def extract_video_info(file_path):
    '''
    input: file_path (string): directory of the txt file in the format above.
    will only work when formatted in that way. To get this copy and paste out of a 
    youtube playlist.
    '''
    video_info_list = []

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        i = 0
        song_count = 0

        while i < len(lines):
            #check if the line contains the title and channel information
            if "NOW PLAYING" in lines[i] and "views" in lines[i + 4]:
                song_count += 1
                # Extract video title and channel
                video_title = lines[i + 1].strip()
                channel_name = lines[i + 2].strip()

                #append the extracted information to the list as a dict
                video_info_list.append({
                    "title": video_title,
                    "channel": channel_name
                })

            i += 1
        print('Now Playing Count: ', song_count)
        print('Number of Lines:', len(lines))
    return video_info_list

def addVideoLinksToList(vidInfoList):
    """
    input: vidInfoList (list of dictionaries): Takes in the output from above function. Will be in this format:
    [
    {
        "title": "SONG TITLE 1",
        "channel": "NAME OF UPLOADER 1"
    },
    {
        "title": "SONG TITLE 2",
        "channel": "NAME OF UPLOADER 2"
    },
    ........
    ]
    
    Uses VideosSearch from the Python API youtubesearchpython that allows you to make Youtube searches and get
    various details. We search for the first option given the title and channel. If found it adds a link key
    to the given songs dictionary. The output is then the list with a link:
    [
    {
        "title": "SONG TITLE 1",
        "channel": "NAME OF UPLOADER 1"
        "link": "https://www.youtube.com/watch?v=vidId"
    },
    ...........

    If there is no result found, then "link" is given the value 0
    """
    for vidInfo in vidInfoList:
        try:
            # use VideosSearch to find the song. Search is limited to 1. The assumption is the correct song is found given title and channel
            videosSearch = VideosSearch(f"{vidInfo['title']} {vidInfo['channel']}", limit = 1)
            video_info = videosSearch.result()['result'][0]
            video_link = video_info['link']
            # adds link key to a given list entry
            vidInfo.update({"link": video_link})
        # IndexError implies the song was not found given the title+channel, sets link to 0 in this case.
        # Somewhat rare case; I believe it'll only happen when there are some odd symbols in the title
        except IndexError:
            vidInfo.update({"link": 0})
    return vidInfoList

def saveVideoInfoToFile(videoInfoList, file_path):
    """
    input: videoInfoList (list of dicts): takes in the above methods list as input.
    input: file_path (string): takes in a string of the file path/name you want a file to be created/modified.
    ensure this is a JSON file

    Creates a JSON file with the list info. 
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(videoInfoList, file, ensure_ascii=False, indent=4)

# function calls and tracking runtime. Adding links takes a long time.
# start_time = time.time()
# video_info_list = extract_video_info(file_path)

# end_time = time.time()
# elapsed_time = end_time - start_time
# print(f"Elapsed Time for Extract Video Info: {elapsed_time:.4f} seconds")


# start_time = time.time()
# video_info_list = addVideoLinksToList(video_info_list)

# end_time = time.time()
# elapsed_time = end_time - start_time
# print(f"Elapsed Time for Adding Links: {elapsed_time:.4f} seconds")


# start_time = time.time()
# saveVideoInfoToFile(video_info_list, 'video_info.json')

# end_time = time.time()
# elapsed_time = end_time - start_time
# print(f"Elapsed Time for Creating JSON file: {elapsed_time:.4f} seconds")

