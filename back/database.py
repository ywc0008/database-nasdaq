import sqlite3
import csv
import os
import pandas as pd

# SQLite 데이터베이스 연결
conn = sqlite3.connect("chart.db")


# 커서 생성
c = conn.cursor()

print("현재 작업디렉토리: " + os.getcwd())
# 판다스 사용 데이터 읽기
csv_data = pd.read_csv("back/data1.csv")

# 테이블 연결을 위한 재정의
csv_data = csv_data.rename(
    columns={
        "날짜": "date",
        "종가": "stock_closing_price",
        "시가": "stock_market_price",
        "고가": "stock_high_price",
        "저가": "stock_low_price",
        "거래량": "volume",
        "변동 %": "change",
    }
)
# 테이블 생성 (예시)
c.execute(
    """CREATE TABLE IF NOT EXISTS stocks
            (
            date datetime PRIMARY KEY , 
            stock_closing_price int,
            stock_high_price int, 
            stock_low_price int, 
            stock_market_price int, 
            volume int, 
            change int
            )"""
)
Tname = "stocks"

# 데이터프레임을 SQLite 테이블에 삽입
csv_data.to_sql(Tname, conn, if_exists="append", index=False)

# 조회

# PRAGMA 문을 사용하여 테이블의 구조 확인
c.execute(f"PRAGMA table_info({Tname})")

table_info = c.fetchall()

for column in table_info:
    print(column)


c.execute(f"SELECT * FROM {Tname} WHERE date LIKE '%2024-04%'")
table_data = c.fetchmany(6)

# 내부 데이터 출력
for row in table_data:
    print(row)

# 변경사항 저장
conn.commit()

# 연결 종료
conn.close()
