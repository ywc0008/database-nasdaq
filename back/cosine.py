import sqlite3
from sqlite3 import Error
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import io

# 데이터베이스 테이블 이름
Tname = "stocks"


# SQLite 데이터베이스 연결 함수
def connect_db():
    try:
        # 경로 수정
        db_path = os.path.abspath("chart.db")
        print(f"Connecting to database at: {db_path}")  # 디버깅 출력
        con = sqlite3.connect(db_path)
        return con
    except Error as e:
        print(f"Database connection error: {e}")
        return None


# 데이터베이스로부터 정보를 읽어옴
def read_db(con):
    try:
        cursor_db = con.cursor()
        cursor_db.execute(f"SELECT * FROM {Tname} ORDER BY date ASC")
        data = cursor_db.fetchall()
        return data
    except Error as e:
        print(f"Read database error: {e}")
        return None


# 코사인 유사도 계산기
def cosine_similarity(x, y):
    return np.dot(x, y) / (np.sqrt(np.dot(x, x)) * np.sqrt(np.dot(y, y)))


# 메인 함수
def compute_cosine_similarity(startdate, enddate):
    db_con = connect_db()
    if db_con is None:
        return "Database connection failed"

    data = read_db(db_con)
    if data is None:
        return "Failed to read data from database"

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
    df.set_index("datetime", inplace=True)
    df["stock_closing_price"] = pd.to_numeric(
        df["stock_closing_price"].str.replace(",", ""), errors="coerce"
    )

    df_ = df.loc[startdate:enddate]
    close = df_["stock_closing_price"]
    base = (close - close.min()) / (close.max() - close.min())
    window_size = len(base)
    next_date = 5
    mv_cnt = len(df) - window_size - next_date - 1

    sim_list = []
    for i in range(mv_cnt):
        target = df["stock_closing_price"].iloc[i : i + window_size]
        target = (target - target.min()) / (target.max() - target.min())
        cosine_sim = cosine_similarity(base, target)
        sim_list.append(cosine_sim)

    sorted_list = pd.Series(sim_list).sort_values(ascending=False).head(10)
    similarity = pd.Series(sim_list).sort_values(ascending=False).head(10).to_dict()

    # 유사도를 내림차순으로 정렬
    sorted_similarity = dict(
        sorted(similarity.items(), key=lambda item: item[1], reverse=True)
    )

    print(sorted_similarity)

    #유사도를 받아 이미지 제작
    def make_image(idx):
        target = df["stock_closing_price"].iloc[idx : idx + window_size]
        target = (target - target.min()) / (target.max() - target.min())

        plt.plot(base.values, label="base", color="grey")
        plt.plot(target.values, label="target", color="orangered")
        plt.xticks(
            np.arange(len(target)),
            pd.to_datetime(target.index.values).strftime("%Y-%m-%d"),
            rotation=25,
        )
        plt.axvline(x=len(base) - 1, c="grey", linestyle="--")
        plt.axvspan(
            len(base.values) - 1, len(target.values) - 1, facecolor="ivory", alpha=0.7
        )
        plt.legend()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        return buf.getvalue()
    
    # 기존의 cosine 테이블을 삭제하고 새로운 테이블을 생성
    db_con.execute("DROP TABLE IF EXISTS cosine")

    db_con.execute(
        """CREATE TABLE IF NOT EXISTS cosine
                (
                idx int, 
                similarity float,
                image BLOB
                )"""
    )

    db_con.commit()


    for idx, sim in sorted_list.items():
        image=make_image(idx)
        db_con.execute(
            "INSERT OR REPLACE INTO cosine (idx, similarity, image) VALUES (?, ?, ?)",
            (int(idx), sim, image),
        )

    db_con.commit()

    plt.close()
    db_con.close()

    return sorted_similarity  # 정렬된 Dict 형태로 반환

compute_cosine_similarity("2014-05-06","2014-06-06")