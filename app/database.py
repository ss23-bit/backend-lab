from dotenv import load_dotenv
import os
import psycopg

load_dotenv()

conn = psycopg.connect(
    host=os.getenv("DB_HOST"),
    name=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

print(os.getenv("DB_HOST"))

cursor = conn.cursor()
