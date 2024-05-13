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
    try:
        conn = connect_db()
        c = conn.cursor()
        c.execute("SELECT * FROM stocks ORDER BY date DESC")
        rows = c.fetchall()

        if not rows:
            raise HTTPException(status_code=404, detail="Chart data not found")

        # 컬럼명 정의
        column_names = [
            "date",
            "stock_closing_price",
            "stock_high_price",
            "stock_low_price",
            "stock_market_price",
            "volume",
            "change",
        ]

        # 데이터를 JSON 형식으로 변환
        chart_data = []
        for row in rows:
            chart_data.append({column_names[i]: row[i] for i in range(len(row))})

        return chart_data
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()
