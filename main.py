import time
import random
from typing import Any
from fastapi import FastAPI, Request, HTTPException
from data import Data
from sqlmodel import Field, Session, SQLModel, create_engine, select
import psycopg2
from pydantic import BaseModel
import bcrypt
import jwt

from config import database_config, jwt_key, salt_key
# https://pyjwt.readthedocs.io/en/stable/

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

# toStart:
# uvicorn main:app --reload --port 8000

def get_data() -> list[tuple[Any, ...]]:
    cursor.execute(""" SELECT id, slug, title, description, body, "tagList", "favoritesCount" FROM public.articles; """)
    data = cursor.fetchall()
    # data = cursor.fetchone()
    return data

def encode_user_token(user, password) -> str:
    return jwt.encode({'user' : user, 'password': password}, jwt_key, algorithm="HS256")

def decode_user_token(token) -> dict[str, Any]:
    decoded = jwt.decode(token, jwt_key, algorithms="HS256")
    return {'user': decoded['user']}

class Token(BaseModel):
    token: str

class User(BaseModel):
    user: str
    password: str

@app.get("/")
async def root():
    return {"message": data.get_fruits()}

@app.post("/login")
async def items(req: User):

    # random_timeout = random.randint(1, 4)
    # print('random_timeout', random_timeout)
    # time.sleep(random_timeout)

    # TODO: create database
    user = 'test'
    password = 'test'
    hashed_password = b'$2a$12$w40nlebw3XyoZ5Cqke14M./ar4P1Fgf7WqZADId2xZEJpq0MvmcJW'

    print(req)

    if req.user != user:
         return HTTPException(status_code=400, detail="Unknown user")


    hashed_password = bcrypt.hashpw(bytes(password, encoding='utf8'), salt_key)
    print('hashed_password:', hashed_password)

    hashed_req_password = bcrypt.hashpw(bytes(req.password, encoding='utf8'), salt_key)

    if hashed_password != hashed_req_password:
        return HTTPException(status_code=401, detail="Password Incorrect")

    token = encode_user_token('test', 'test')
    return {"token": token}


@app.post("/check-token")
async def ecode(req: Token):
    print('item', req.token)
    token = req.token
    try:
        return decode_user_token(token)
    except:
        return HTTPException(status_code=401, detail="Token Incorrect")

@app.post("/decode")
async def decode(req: Token):
    return ''


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["New-header"] = "test"
    return response
