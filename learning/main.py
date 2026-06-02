from fastapi import FastAPI
from sqlalchemy import create_engine, text
import os
import redis

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")
REDIS_URL = os.getenv("REDIS_URL")

engine = create_engine(DATABASE_URL)
r = redis.Redis.from_url(REDIS_URL, decode_responses=True)

@app.get("/")
def home():

    cached = r.get("postgres_version")

    if cached:
        return {
            "source": "redis-cache",
            "postgres_version": cached
        }

    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        version = result.fetchone()[0]

    r.set("postgres_version", version, ex=60)
    
    return {
        "source": "postgres-db",
        "postgresql_version": version 
    }

    