import time
import random
from fastapi import FastAPI, Request
from data import Data
from sqlmodel import Field, Session, SQLModel, create_engine, select
import psycopg2

connection = psycopg2.connect(database="streamway", user="", password="pass", host="localhost", port=5432)


print('__name__', __name__)
data = Data()
app = FastAPI()

# toStart uvicorn main:app --reload --port 8000

@app.get("/")
async def root():
    return {"message": data.get_fruits()}

@app.get("/data")
async def items():
    random_timeout = random.randint(1, 4)
    print('random_timeout', random_timeout)
    # time.sleep(random_timeout)
    return {"timeout": random_timeout, "data": data.get_items_with_offset(random_timeout)}

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
