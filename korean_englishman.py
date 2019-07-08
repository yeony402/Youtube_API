# 동영상 ID 별 동영상 나열

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')


# 빌드할 youtube 정보
DEVELOPER_KEY = "AIzaSyATMl5xc68esF93TBeRVVR1hRpQj50loig" # API_KEY
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# creating youtube resource
# object for interacting with API
youtube = build(YOUTUBE_API_SERVICE_NAME,
                YOUTUBE_API_VERSION,
                developerKey=DEVELOPER_KEY)


def multiple_video_details():
    # https://developers.google.com/youtube/v3/docs/videos/list?hl=ko
    list_videos_byid = youtube.videos().list(
        id='QMaRjUS4Jtw, ceUBtZE5ZTw', # 영국남자 동영상 id
        part="id, snippet, contentDetails, statistics",).execute()

    # 검색결과
    results = list_videos_byid.get("items", [])

    videos = []
    n = 1
    for result in results:
        videos.append("% s (% s) (% s) (% s) (% s) (% s) (% s)"
                      % (n, result["snippet"]["title"], #제목
                         result["snippet"]["tags"], # 영상 관련 태그
                         result['snippet']['description'], # description
                         result["snippet"]["publishedAt"], # datetime
                         result['contentDetails'], # 동영상의 길이 및 비 등 콘텑츠에 관한 정보
                         result["statistics"])) # 조회수, 좋아요수, 댓글수 등
        # https://developers.google.com/youtube/v3/docs/videos?hl=ko
        n = n + 1

    print("Videos:\n", "\n".join(videos), "\n") # .join() 리스트에서 문자열로 변환


if __name__ == "__main__":
    multiple_video_details()
