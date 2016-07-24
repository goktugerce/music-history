#!/usr/bin/python

from googleapiclient.discovery import build

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyCgcDnt01hNG1mfVHrkxY6-GXZmdQsYWsc"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(q):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
        q=q,
        part="id,snippet",
        maxResults=1
    ).execute()

    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            id = search_result["id"]["videoId"]
            video_response = youtube.videos().list(part="contentDetails", id=id).execute()
            for video_result in video_response.get("items", []):
                duration = video_result["contentDetails"]["duration"]
        else:
            return

    if "S" not in duration:
        mins = int(duration[2:-1])
        duration = 1000 * mins * 60
    elif "M" not in duration:
        secs = int(duration[2:-1])
        duration = 1000 * secs
    else:
        mins, secs = duration[2:-1].split("M")
        mins = int(mins)
        secs = int(secs)
        duration = 1000 * (mins * 60 + secs)

    return duration
