import sys
import io
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
import sqlite3
# from oauth2client.tools import argparser


sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')


# 빌드할 youtube 정보
DEVELOPER_KEY = "AIzaSyAEOuhQN1wltLVHJtWoXMxZd1Kx4oJF4_A"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# creating youtube resource
# object for interacting with API
youtube = build(YOUTUBE_API_SERVICE_NAME,
                YOUTUBE_API_VERSION,
                developerKey=DEVELOPER_KEY)

videos = []

channel_box = []
date_box = []
category_box = []
viewcount_box = []
subscriber_box = []
channel_thumbnails_box = []

token = None

def nanum_event_videos(token):
    sum = 0 #sum = 0이 함수 밖으로 나가있을 때 함수밖의 sum은 전역변수, 함수내의 sum은 지역변수로 인지하여 같은 범위내에서 사용되면 안된다고 판단함
    while True:
        try:
            search_response = youtube.search().list(
                q = 'giveaway',
                part = 'snippet',
                maxResults = 50,
                pageToken = token,
                order = 'date',
                publishedAfter = '2017-02-09T00:00:00Z',
                publishedBefore = '2017-02-09T20:59:49.000Z'
                ).execute()

            for search_result in search_response.get("items", []):
                if search_result["id"]["kind"] == "youtube#video":
                    channelTitle = search_result["snippet"]["channelTitle"]
                    videoId = search_result['id']['videoId']
                    print(channelTitle)
                    if channelTitle == "Disney":
                        continue
                elif search_result["id"]["kind"] == "youtube#channel":
                    continue
                elif search_result["id"]["kind"] == "youtube#playlist":
                    continue
                channel_box.append(channelTitle) # 채널 명

                # 영상 업로드 시간, 영상 조회 수, 카테고리id
                video_response = youtube.videos().list(
                    id = videoId, #영상 ID
                    part="snippet, statistics"
                    ).execute()
                print(videoId)

                for video_result in video_response.get("items", []):
                    datetime = video_result["snippet"]["publishedAt"] #datetime
                    categoryId = video_result["snippet"]["categoryId"]
                    viewcount = video_result["statistics"]["viewCount"]# 값이 비어있는 데이터가 존재할 때 keyerror가 남
                date_box.append(datetime)
                category_box.append(categoryId)
                viewcount_box.append(viewcount)


                # 채널의 구독자 수
                channel_response = youtube.channels().list(
                    id = search_result['snippet']['channelId'],
                    part="snippet, statistics" #, brandingSettings
                    ).execute()
                for channel_result in channel_response.get("items", []):
                    subscriberCount = channel_result["statistics"]["subscriberCount"]
                    channel_thumbnails = channel_result['snippet']["thumbnails"]["medium"]["url"]
                    print(subscriber_box)
                subscriber_box.append(subscriberCount) # 값이 비어있는 속성이 존재할 때 keyerror가 남
                channel_thumbnails_box.append(channel_thumbnails)

                token = search_response['nextPageToken']
                print(token)

                global channelTitle_, datetime_, categoryId_, viewcount_, subscriberCount_,channel_thumbnails_
                channelTitle_ = channel_box[sum]
                datetime_ = date_box[sum]
                categoryId_ = category_box[sum]
                viewcount_ = viewcount_box[sum]
                subscriberCount_ = subscriber_box[sum]
                channel_thumbnails_ = channel_thumbnails_box[sum]
                sum = sum + 1


                videos.append("(%s,%s,%s,%s,%s,%s)" % (channelTitle_, datetime_, categoryId_, viewcount_, subscriberCount_, channel_thumbnails_))


                con = sqlite3.connect('youtube.db')
                cursor = con.cursor()

                table = '''create table if not exists global_info(channelTitle varchar(100) not null, datetime varchar(100) not null, categoryId varchar(100) not null, viewcount int(100) default 0, subscriberCount int(100) default 0, channel_thumbnails varchar(500))'''
                cursor.execute(table)

                # unique index를 설정하여 insert 할 떄 중복데이터를 제거한다.
                # https://dba.stackexchange.com/questions/189058/how-do-i-insert-record-only-if-the-record-doesnt-exist
                unique_index = 'CREATE UNIQUE INDEX IF NOT EXISTS my_unique_index ON global_info (channelTitle, datetime, categoryId)'
                cursor.execute(unique_index)

                sql = "insert or ignore into global_info(channelTitle, datetime, categoryId, viewcount, subscriberCount, channel_thumbnails)VALUES(?,?,?,?,?,?)"
                cursor.execute(sql, (channelTitle_, datetime_, categoryId_, viewcount_, subscriberCount_, channel_thumbnails_))
                con.commit()

            if token=="" or token==None:
                print('not nextPageToken')
                break

        except HttpError as e:
            print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
            break
        except keyerror as e:
            print("keyError: %s" % str(e))
            break

    print(videos)




if __name__=="__main__":
    nanum_event_videos(token)
