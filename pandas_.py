import pandas as pd
import matplotlib
import numpy as np
from pylab import *
import matplotlib.pyplot as plt
# from pandas.plotting import scatter_matrix
# import matplotlib.pyplot as plt
%matplotlib inline
import sqlite3


con = sqlite3.connect('youtube.db')
df = pd.read_sql_query("SELECT * FROM global_nanum_data group by channelTitle, datetime", con)

# 출력 포맷팅 설정
# https://financedata.github.io/posts/pandas-display-format.html
pd.options.display.float_format = '{:.3f}'.format
# df

# datetime필드를 날짜로 인식하도록 변환
df['datetime'] = pd.to_datetime(df['datetime'])
df.set_index('datetime', inplace=True)
data_mean = df.resample('MS').mean()

# 조회수, 구독자수 평균
data_mean
# 월별 조회수, 구독자수 line 그래프
data_mean.plot()
