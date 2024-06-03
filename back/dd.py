from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.middleware.cors import CORSMiddleware

import sqlite3
from cosine import compute_cosine_similarity
import base64

import os

from fastapi.responses import JSONResponse
from pydantic import BaseModel

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
print(strings)