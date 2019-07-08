import sys
import io
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
import sqlite3
# from oauth2client.tools import argparser


sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')


# 빌드할 youtube 정보
DEVELOPER_KEY = "AIzaSyBYXqdhXJfDhMM1G9xUXhp5N0_HBeO9ecM"
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
                q = '나눔이벤트',
                part = 'snippet',
                maxResults = 50,
                pageToken = token,
                order = 'date',
                publishedAfter = '2017-01-01T00:00:00Z',
                publishedBefore = '2017-01-31T00:00:00Z'
                ).execute()

            # videos.append("%s\n" % (search_response["pageInfo"]["resultsPerPage"]))

            for search_result in search_response.get("items", []):
                if search_result["id"]["kind"] == "youtube#video":
                    channelTitle = search_result["snippet"]["channelTitle"]
                    # video_title = search_result["snippet"]["title"], # 나눔이벤트 영상 제목
                    # thumbnails = earch_result["snippet"]["thumbnails"]["high"]["url"]))

                    # 영상 업로드 시간, 영상 조회 수, 카테고리id
                    video_response = youtube.videos().list(
                        id = search_result['id']['videoId'], #영상 ID
                        part="snippet, statistics"
                        ).execute()
                    for video_result in video_response.get("items", []):
                        datetime = video_result["snippet"]["publishedAt"] #datetime
                        categoryId = video_result["snippet"]["categoryId"]
                        viewcount = video_result["statistics"]["viewCount"]# 값이 비어있는 데이터가 존재할 때 keyerror가 남
                    channel_box.append(channelTitle) # 채널 명
                    date_box.append(datetime)
                    category_box.append(categoryId)
                    viewcount_box.append(viewcount)
                    print(date_box)

                    # 채널의 구독자 수
                    channel_response = youtube.channels().list(
                        id = search_result['snippet']['channelId'],
                        part="snippet, statistics" #, brandingSettings
                        ).execute()
                    print(search_result['snippet']['channelId'])
                    for channel_result in channel_response.get("items", []):
                        subscriberCount = channel_result["statistics"]["subscriberCount"]
                        print(subscriberCount)
                        channel_thumbnails = channel_result['snippet']["thumbnails"]["medium"]["url"] # 모바일 어플용 배너 중간해상도 이미지
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

                    table = '''create table if not exists kr_info(channelTitle varchar(100) not null, datetime varchar(100) not null, categoryId varchar(100) not null, viewcount int(100) not null, subscriberCount int(100) not null, channel_thumbnails varchar(500) not null)'''
                    cursor.execute(table)

                    unique_index = 'CREATE UNIQUE INDEX IF NOT EXISTS my_unique_index ON kr_info (channelTitle, datetime, categoryId, channel_thumbnails)'
                    cursor.execute(unique_index)

                    sql = "insert or ignore into kr_info(channelTitle, datetime, categoryId, viewcount, subscriberCount, channel_thumbnails) VALUES(?,?,?,?,?,?)"
                    cursor.execute(sql, (channelTitle_, datetime_, categoryId_, viewcount_, subscriberCount_, channel_thumbnails_))
                    con.commit()

            if not token:
                print('not nextPageToken')
                break

        except HttpError as e:
            print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
            break
        except KeyError as e:
            print('keyerror: %s' % str(e))
            break


    print(videos)
    # con.close()



if __name__=="__main__":
    nanum_event_videos(token)
