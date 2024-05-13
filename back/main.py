from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 클라이언트의 주소
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


# SQLite 데이터베이스 연결 함수
def connect_db():
    return sqlite3.connect("chart.db")


# API 엔드포인트 작성
@app.get("/nasdaq_chart")
async def get_nasdaq_chart():
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT * FROM stocks ORDER BY date DESC LIMIT 10")
    rows = c.fetchall()
    conn.close()
    if not rows:
        raise HTTPException(status_code=404, detail="Chart data not found")

    column_names = [description[0] for description in c.description]  # 컬럼명 가져오기

    # 데이터를 JSON 형식으로 변환
    chart_data = []
    for row in rows:
        chart_data.append({column_names[i]: row[i] for i in range(len(row))})

    return chart_data
