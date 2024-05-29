import sqlite3
from sqlite3 import Error

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# 데이터베이스 테이블 이름
Tname = "stocks"


# SQLite 데이터베이스 연결 함수
def connect_db():
    try:
        con = sqlite3.connect("back/chart.db")
        return con
    except Error:
        print(Error)


# 데이터 베이스로 부터 정보를 읽어옴
def read_db(con):
    try:
        cursor_db = con.cursor()
        cursor_db.execute(f"SELECT * FROM {Tname} ORDER BY date ASC")
        data = cursor_db.fetchall()
        return data
    except Error:
        print(Error)


# 피어슨 유사도 계산기
def pearson_similarity(x, y):
    return np.corrcoef(x, y)[0, 1]


# 데이터베이스 연결 후 data에 테이블 데이터 저장
db_con = connect_db()
data = read_db(db_con)

df = pd.DataFrame(
    data,
    columns=[
        "datetime",
        "stock_closing_price",
        "stock_market_price",
        "stock_high_price",
        "stock_low_price",
        "volume",
        "change",
    ],
)
df["datetime"] = df["datetime"].str.replace(" ", "")

# datetime을 인덱스 번호로 설정
df.set_index("datetime", inplace=True)

# 종가 데이터 실수화
df["stock_closing_price"] = pd.to_numeric(
    df["stock_closing_price"].str.replace(",", ""), errors="coerce"
)

# 설정한 입력 날짜의 범위
startdate = "2021-09-01"
enddate = "2021-09-20"

# 범위만큼 추출
df_ = df.loc[startdate:enddate]

# 기간 내 종가 데이터 추출
close = df_["stock_closing_price"]

# 데이터 정규화
base = (close - close.min()) / (close.max() - close.min())

# 윈도우 사이즈
window_size = len(base)

# 예측 기간 (유사도가 가장 높았던 패턴의 향후 5일 주가 추이)
next_date = 5

# 검색 횟수
mv_cnt = len(df) - window_size - next_date - 1

# 피어슨 유사도를 담을 리스트
sim_list = []

for i in range(mv_cnt):
    # i 번째 인덱스 부터 i+window_size 만큼의 범위를 가져와 target 변수에 대입
    target = df["stock_closing_price"].iloc[i : i + window_size]

    # base와 마찬가지로 정규화를 적용
    target = (target - target.min()) / (target.max() - target.min())

    # 유사도 계산
    pearson_sim = pearson_similarity(base, target)

    # 리스트에 추가
    sim_list.append(pearson_sim)



#리스트 오름차순 정렬
sorted_list=pd.Series(sim_list).sort_values(ascending=False).head(20)

#두번째로 높은 값의 인덱스 번호 추출
second_value=sorted_list.index[1]

print(second_value)


# 가장 높은 유사도를 갖는 값 그래프로 출력

# 높은 유사도를 기록한 인덱스 대입
idx = second_value

# target 변수에 종가 데이터의 [기준 인덱스] 부터 [기준 인덱스 + window_size + 예측(5일)] 데이터를 추출합니다
target = df["stock_closing_price"].iloc[idx : idx + window_size + 5]

# 정규화를 적용합니다
target = (target - target.min()) / (target.max() - target.min())

# 결과를 시각화합니다
plt.plot(base.values, label="base", color="grey")
plt.plot(target.values, label="target", color="orangered")
plt.xticks(
    np.arange(len(target)),
    pd.to_datetime(target.index.values).strftime("%Y-%m-%d"),
    rotation=45,
)
plt.axvline(x=len(base) - 1, c="grey", linestyle="--")
plt.axvspan(len(base.values) - 1, len(target.values) - 1, facecolor="ivory", alpha=0.7)
plt.legend()

plt.savefig('back/pearson_graph.png')
