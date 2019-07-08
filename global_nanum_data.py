import sys
import io
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
import sqlite3
import time
from datetime import timedelta, date
# from oauth2client.tools import argparser


sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')


# 빌드할 youtube 정보
DEVELOPER_KEY = "AIzaSyBQejQHKXBPeSy4veIPisCjT9jmcfoxN04"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# creating youtube resource
# object for interacting with API
youtube = build(YOUTUBE_API_SERVICE_NAME,
                YOUTUBE_API_VERSION,
                developerKey=DEVELOPER_KEY)

token = None

def nanum_event_videos(token, date_string):
    print(date_string, '=============================================')
    search_response = youtube.search().list(
        q = 'giveaway',
        part = 'snippet',
        maxResults = 50,
        pageToken = token,
        type = 'video',
        order = 'date',
        publishedAfter = str(date_string) +'T00:00:00.000Z',
        publishedBefore = str(date_string) +'T23:59:59.000Z'
        ).execute()

    for search_result in search_response.get("items", []):
        channelTitle = search_result["snippet"]["channelTitle"]
        videoId = search_result['id']['videoId']
        print(channelTitle)
        if channelTitle == "Disney":
            continue

        # 영상 업로드 시간, 영상 조회 수, 카테고리id
        video_response = youtube.videos().list(
            id = search_result['id']['videoId'], #영상 ID
            part="snippet, statistics"
            ).execute()

        for video_result in video_response.get("items", []):
            datetime = video_result["snippet"]["publishedAt"] #datetime
            categoryId = video_result["snippet"]["categoryId"]
            viewcount = video_result["statistics"]["viewCount"]# 값이 비어있는 데이터가 존재할 때 keyerror가 남

        # 채널의 구독자 수
        channel_response = youtube.channels().list(
            id = search_result['snippet']['channelId'],
            part="snippet, statistics" #, brandingSettings
            ).execute()
        for channel_result in channel_response.get("items", []):
            subscriberCount = channel_result["statistics"]["subscriberCount"]
            channel_thumbnails = channel_result['snippet']["thumbnails"]["medium"]["url"]

        con = sqlite3.connect('youtube.db')
        cursor = con.cursor()

        table = '''create table if not exists global_nanum_data(channelTitle varchar(100) not null, datetime varchar(100) not null, categoryId varchar(100) not null, viewcount int(100) default 0, subscriberCount int(100) default 0, channel_thumbnails varchar(500))'''
        cursor.execute(table)

        # unique index를 설정하여 insert 할 떄 중복데이터를 제거한다.
        # https://dba.stackexchange.com/questions/189058/how-do-i-insert-record-only-if-the-record-doesnt-exist
        unique_index = 'CREATE UNIQUE INDEX IF NOT EXISTS my_unique_index ON global_nanum_data (channelTitle, datetime, categoryId)'
        cursor.execute(unique_index)

        sql = "insert or ignore into global_nanum_data(channelTitle, datetime, categoryId, viewcount, subscriberCount, channel_thumbnails)VALUES(?,?,?,?,?,?)"
        cursor.execute(sql, (channelTitle, datetime, categoryId, viewcount, subscriberCount, channel_thumbnails))
        con.commit()

    # 변수의 존재 여부
    # locals() globals()
    if search_response['nextPageToken'] in locals():
        tokens = []
        tokens.append(search_response['nextPageToken'])
        for i in tokens:
            nanum_event_videos(i, date_string)
    else:
        pass



if __name__=="__main__":
    # Input start and end date
    start_date = date(2016, 12, 31)
    end_date = date(2019, 1, 1)
    def daterange(start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)

    try:
        for single_date in daterange(start_date, end_date):
            date_string = single_date.strftime("%Y-%m-%d")
            nanum_event_videos(token, date_string)
    except HttpError as e:
        print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
