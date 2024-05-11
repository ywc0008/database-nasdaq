import sqlite3
import csv


# CSV 파일에서 데이터 읽기
def read_csv(file_path):
    with open(file_path, newline="") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # 첫 번째 행을 읽지 않음
        data = [row for row in reader]
    return data


# SQLite 데이터베이스 연결
conn = sqlite3.connect("chart.db")

# 커서 생성
c = conn.cursor()

# CSV 파일에서 데이터 읽기
csv_data = read_csv("나스닥 100.csv")

# 테이블 생성 (예시)
c.execute(
    """CREATE TABLE IF NOT EXISTS stocks
             (date datetime, stock_closing_price int, stock_high_price int, stock_low_price int, stock_market_price int, volume int, change int)"""
)

# 데이터 삽입 예시
for row in csv_data:
    c.execute("INSERT INTO stocks VALUES (?, ?, ?, ?, ?, ?, ?)", row)

# 변경사항 저장
conn.commit()

# 연결 종료
conn.close()
