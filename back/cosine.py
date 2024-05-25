import sqlite3
from sqlite3 import Error
import numpy as np
import pandas as pd

# SQLite 데이터베이스 연결 함수
def connect_db():
    try:
        con=sqlite3.connect("chart.db")
        return con
    except  Error:
        print(Error)

def read_db(con):
    cursor_db=con.cursor()
    cursor_db.execute('SELECT * FROM ')
    data=cursor_db.fetchall()
    return data
