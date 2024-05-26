import sqlite3
from sqlite3 import Error
import numpy as np
import pandas as pd

# 데이터베이스 테이블 이름
Tname = "stocks"

# SQLite 데이터베이스 연결 함수
def connect_db():
    try:
        con=sqlite3.connect("back/chart.db")
        return con
    except  Error:
        print(Error)

# 데이터 베이스로 부터 정보를 읽어옴
def read_db(con):
    try:
         cursor_db=con.cursor()
         cursor_db.execute(f"SELECT * FROM {Tname} ")
         data=cursor_db.fetchall()
         return data
    except Error:
         print(Error)

# 데이터베이스 연결 후 data에 테이블 데이터 저장
db_con= connect_db()
data=read_db(db_con)

df=pd.DataFrame(data, columns=["datetime",
                               "stock_closing_price",
                               "stock_market_price",
                               "stock_high_price",
                               "stock_low_price",
                               "volume","change"])
df["datetime"]=df["datetime"].str.replace(" ","")
#datetime을 인덱스 번호로 설정
df.set_index("datetime", inplace=True)

startdate = '2021-09-01'
enddate = '2021-09-20'
data_ = df.loc[startdate:enddate]
print(df)