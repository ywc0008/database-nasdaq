import sqlite3
import os
import pandas as pd

try:
    # SQLite 데이터베이스 연결
    conn = sqlite3.connect("back/chart.db")

    # 커서 생성
    c = conn.cursor()

    print("현재 작업디렉토리: " + os.getcwd())

    # 판다스 사용 데이터 읽기
    # 파일이 들어있는 디렉토리 경로
    directory = "back/"

    csv_data=pd.DataFrame()
    # 디렉토리 내의 파일들을 확인하고, "나스닥"으로 시작하는 파일을 찾음
    for filename in os.listdir(directory):
        if filename.startswith("나스닥"):
            file_path = os.path.join(directory, filename)
            temp = pd.read_csv(file_path)
            csv_data = pd.concat([csv_data, temp], ignore_index=True)

    # 데이터프레임이 비어 있는 경우 처리
    if csv_data.empty:
        raise ValueError("CSV 파일에 데이터가 없습니다.")

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

    # 테이블 생성
    c.execute(
        """CREATE TABLE IF NOT EXISTS stocks
                (
                date datetime, 
                stock_closing_price int,
                stock_market_price int, 
                stock_high_price int, 
                stock_low_price int, 
                volume int, 
                change int
                )"""
    )
    Tname = "stocks"

    # 데이터프레임을 SQLite 테이블에 삽입
    csv_data.to_sql(Tname, conn, if_exists="replace", index=False)

    # 변경사항 저장
    conn.commit()
    
    # PRAGMA 문을 사용하여 테이블의 구조 확인
    c.execute(f"PRAGMA table_info({Tname})")

    table_info = c.fetchall()

    for column in table_info:
        print(column)

    #2024-04의 데이터확인
    c.execute(f"SELECT * FROM {Tname} WHERE date LIKE '%2024%'")
    table_data = c.fetchmany(6)

    # 내부 데이터 출력
    for row in table_data:
        print(row)
except Exception as e:
    print("오류 발생:", e)

finally:
    # 연결 종료
    conn.close()
