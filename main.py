import time
import random
from fastapi import FastAPI, Request
from data import Data
from sqlmodel import Field, Session, SQLModel, create_engine, select
import psycopg2
from pydantic import BaseModel


import jwt
# https://pyjwt.readthedocs.io/en/stable/

from config import database_config, secret_key

connection = psycopg2.connect(
    database=database_config["database"],
    user=database_config["user"],
    password=database_config["password"],
    host=database_config["host"],
    port=database_config["port"])

cursor = connection.cursor()

print('__name__', __name__)
data = Data()
app = FastAPI()

# toStart uvicorn main:app --reload --port 8000

def get_data() -> None:
    cursor.execute(""" SELECT id, slug, title, description, body, "tagList", "favoritesCount" FROM public.articles; """)
    data = cursor.fetchall()
    # data = cursor.fetchone()
    return data

def encode_user_token() -> str:
    token = jwt.encode({"some": "test_payload"}, secret_key, algorithm="HS256")
    return token

def decode_user_token(token) -> str:
    print(token)
    return jwt.decode(token, secret_key, algorithms="HS256")


@app.get("/")
async def root():
    return {"message": data.get_fruits()}

@app.get("/data")
async def items():

    # random_timeout = random.randint(1, 4)
    # print('random_timeout', random_timeout)
    # time.sleep(random_timeout)

    token = encode_user_token()
    return {"token": token, "data": data.get_items_with_offset(5), "articles": get_data()}

class Item(BaseModel):
    token: str

@app.post("/token")
async def ecode(req: Item):
    print('item', req.token)
    token = req.token
    decoded = decode_user_token(token)
    return decoded


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["New-header"] = "test"
    return response
