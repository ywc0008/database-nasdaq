from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.middleware.cors import CORSMiddleware

import sqlite3
from cosine import compute_cosine_similarity
import base64

import os

from fastapi.responses import JSONResponse
from pydantic import BaseModel


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
    try:
        # 경로 수정
        db_path = os.path.abspath("chart.db")
        print(f"Connecting to database at: {db_path}")  # 디버깅 출력
        con = sqlite3.connect(db_path)
        return con
    except Error as e:
        print(f"Database connection error: {e}")
        return None


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/nasdaq_chart")
async def get_nasdaq_chart():
    try:
        conn = connect_db()
        if conn is None:
            raise HTTPException(status_code=500, detail="Database connection failed")

        c = conn.cursor()
        c.execute("SELECT * FROM stocks ORDER BY date DESC")
        rows = c.fetchall()

        if not rows:
            raise HTTPException(status_code=404, detail="Chart data not found")

        column_names = [
            "date",
            "stock_closing_price",
            "stock_high_price",
            "stock_low_price",
            "stock_market_price",
            "volume",
            "change",
        ]
        chart_data = []
        for row in rows:
            chart_data.append({column_names[i]: row[i] for i in range(len(row))})

        return chart_data
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()


@app.post("/submit")
async def submit_item(request: Request):
    data = await request.json()
    firstDate = data.get("firstDate")
    secondDate = data.get("secondDate")

    if not firstDate or not secondDate:
        raise HTTPException(status_code=400, detail="Invalid date range provided")

    similarity = compute_cosine_similarity(firstDate, secondDate)
    return {"firstDate": firstDate, "secondDate": secondDate, "similarity": similarity}


@app.get("/cosine_similarity")
async def get_cosine_similarity(
    firstDate: str = Query(...), secondDate: str = Query(...)
):
    try:
        if not firstDate or not secondDate:
            raise HTTPException(status_code=400, detail="Invalid date range provided")

        similarity = compute_cosine_similarity(firstDate, secondDate)
        if not similarity:
            raise HTTPException(status_code=404, detail="Chart data not found")
        return JSONResponse(content={"similarity": similarity})  # JSON 응답 반환
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.get("/cosine_graph")
async def get_cosine_graph():
    try:
        conn = connect_db()
        if conn is None:
            raise HTTPException(status_code=500, detail="Database connection failed")

        c = conn.cursor()
        c.execute("SELECT image FROM cosine")
        rows = c.fetchall()

        if not rows:
            raise HTTPException(status_code=404, detail="Chart data not found")
        
        strings=[]
        for row in rows:
            image_binary = row[0]
            strings.append(base64.b64encode(image_binary).decode("utf-8"))
        return strings

    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()