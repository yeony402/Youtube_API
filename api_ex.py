import sys
import io
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
# from oauth2client.tools import argparser


sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')


# 빌드할 youtube 정보
DEVELOPER_KEY = "AIzaSyDg1b0m38hjwPGtdOYLOL7WOHCoF6wTmyE" # API_KEY
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# creating youtube resource
# object for interacting with API
youtube = build(YOUTUBE_API_SERVICE_NAME,
                YOUTUBE_API_VERSION,
                developerKey=DEVELOPER_KEY)

def nanum_event_videos():
    search_response = youtube.search().list(
        q = '나눔이벤트',
        part = 'snippet',
        maxResults = 50
    ).execute()


    videos = []
    channels = []
    playlists = []

    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get("items", []):
      if search_result["id"]["kind"] == "youtube#video":
        videos.append("%s (%s) (%s) (%s)" % (search_result["snippet"]["title"],
                                   search_result["id"]["videoId"],
                                   search_result["snippet"]["channelTitle"],
                                   search_result["snippet"]["thumbnails"]["high"]["url"]))
      elif search_result["id"]["kind"] == "youtube#channel":
        channels.append("%s (%s) (%s) (%s)" % (search_result["snippet"]["title"],
                                     search_result["id"]["channelId"],
                                     search_result["snippet"]["channelTitle"],
                                     search_result["snippet"]["thumbnails"]["high"]["url"]))
      elif search_result["id"]["kind"] == "youtube#playlist":
        playlists.append("%s (%s) (%s) (%s)" % (search_result["snippet"]["title"],
                                      search_result["id"]["playlistId"],
                                      search_result["snippet"]["channelTitle"],
                                      search_result["snippet"]["thumbnails"]["high"]["url"]))

    print("Videos:\n", "\n".join(videos), "\n")
    print("Channels:\n", "\n".join(channels), "\n")
    print("Playlists:\n", "\n".join(playlists), "\n")

    # print(results)

if __name__=="__main__":
    try:
        nanum_event_videos()
    except HttpError as e:
        print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
