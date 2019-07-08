import sys
import io
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
import sqlite3
import datetime
import time
from datetime import timedelta, date
#
#
# sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
# sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')


# 빌드할 youtube 정보
DEVELOPER_KEY = "AIzaSyDg1b0m38hjwPGtdOYLOL7WOHCoF6wTmyE"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# creating youtube resource
# object for interacting with API
youtube = build(YOUTUBE_API_SERVICE_NAME,
                YOUTUBE_API_VERSION,
                developerKey=DEVELOPER_KEY)

# results = []
#
# channel_box = []
# date_box = []
# category_box = []
# viewcount_box = []
# subscriber_box = []
# channel_thumbnails_box = []

token = None

def nanum_event_videos(token, date_string):
    print(date_string, '=============================================')
    search_response = youtube.search().list(
        q = '나눔이벤트',
        part = 'snippet',
        maxResults = 50,
        pageToken = token,
        order = 'date',
        publishedAfter = str(date_string) +'T00:00:00.000Z',
        publishedBefore = str(date_string) +'T23:59:59.000Z'
    ).execute()

    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            channelTitle = search_result["snippet"]["channelTitle"]
            print(channelTitle)

            # 영상 업로드 시간, 영상 조회 수, 카테고리id
            video_response = youtube.videos().list(
                id = search_result['id']['videoId'], #영상 ID
                part="snippet, statistics"
            ).execute()
            for video_result in video_response.get("items", []):
                datetime = video_result["snippet"]["publishedAt"] #datetime
                categoryId = video_result["snippet"]["categoryId"]
                viewcount = video_result["statistics"]["viewCount"]# 값이 비어있는 데이터가 존재할 때 keyerror가 남
            # channel_box.append(channelTitle) # 채널 명
            # date_box.append(datetime)
            # category_box.append(categoryId)
            # viewcount_box.append(viewcount)

            # 채널의 구독자 수
            channel_response = youtube.channels().list(
                id = search_result['snippet']['channelId'],
                part="snippet, statistics" #, brandingSettings
            ).execute()
            for channel_result in channel_response.get("items", []):
                subscriberCount = channel_result["statistics"]["subscriberCount"]
                channel_thumbnails = channel_result['snippet']["thumbnails"]["medium"]["url"] # 모바일 어플용 배너 중간해상도 이미지
            # subscriber_box.append(subscriberCount) # 값이 비어있는 속성이 존재할 때 keyerror가 남
            # channel_thumbnails_box.append(channel_thumbnails)
            #
            # channelTitle_ = channel_box[sum]
            # datetime_ = date_box[sum]
            # categoryId_ = category_box[sum]
            # viewcount_ = viewcount_box[sum]
            # subscriberCount_ = subscriber_box[sum]
            # channel_thumbnails_ = channel_thumbnails_box[sum]
            # sum = sum + 1

            # results.append("(%s,%s,%s,%s,%s,%s)" % (channelTitle_, datetime_, categoryId_, viewcount_, subscriberCount_, channel_thumbnails_))

            con = sqlite3.connect('youtube.db')
            cursor = con.cursor()

            table = '''create table if not exists kr_nanum_data(channelTitle varchar(100) not null, datetime varchar(100) not null, categoryId varchar(100) not null, viewcount int(100) not null, subscriberCount int(100) not null, channel_thumbnails varchar(500) not null)'''
            cursor.execute(table)

            unique_index = 'CREATE UNIQUE INDEX IF NOT EXISTS my_unique_index ON kr_nanum_data (channelTitle, datetime, categoryId, channel_thumbnails)'
            cursor.execute(unique_index)

            sql = "insert or ignore into kr_nanum_data(channelTitle, datetime, categoryId, viewcount, subscriberCount, channel_thumbnails) VALUES(?,?,?,?,?,?)"
            cursor.execute(sql, (channelTitle, datetime, categoryId, viewcount, subscriberCount, channel_thumbnails))
            con.commit()
            con.close()

    # 변수의 존재 여부
    # locals() globals()
    if search_response['nextPageToken'] in locals():
        tokens = []
        tokens.append(search_response['nextPageToken'])
        for i in tokens:
            nanum_event_videos(i, date_string)
    else:
        pass


    # print(results)
    # return token


if __name__=="__main__":
    # Input start and end date
    start_date = date(2016, 12, 31)
    end_date = date(2019, 1, 1)
    def daterange(start_date, end_date):
        for n in range(int((end_date - start_date).days)): #일 별로 계산
            yield start_date + timedelta(n)
    try:
        for single_date in daterange(start_date, end_date):
            date_string = single_date.strftime("%Y-%m-%d")
            nanum_event_videos(token, date_string)
    except HttpError as e:
        print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
    # except keyerror as e:
    #     print("keyError: %s" % str(e))
