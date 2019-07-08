from selenium import webdriver
import time
from bs4 import BeautifulSoup
import mysql.connector
# import sys
# import io
#
#
# sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
# sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

keyword = input("검색어를 입력하세요.")
url = 'https://www.youtube.com/results?search_query='+keyword+'&sp=CAI%253D'

driver = webdriver.Chrome('chromedriver')
time.sleep(2)
driver.get(url)

# video_lists = driver.find_elements_by_xpath('//*[@id="title-wrapper"]/h3')
#
# for i in video_lists:
#     print(i.text.strip())
# html = driver.page_source # 페이지의 elements모두 가져오기
# soup = BeautifulSoup(html, 'html.parser')
# soup.select("body a")

aa = driver.find_elements_by_partial_link_text('/watch?').click()
time.sleep(2)
driver.back()
