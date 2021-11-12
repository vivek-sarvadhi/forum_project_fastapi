from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import setting


SQLALCHEMY_DATABASE_URL = setting.databse_url

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='blogpost', user="postgres", password="vivek", cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("database connection was successfully")
#         break
#     except Exception as error:
#         print("connection to database fail")
#         print("Error  ", error)
#         time.sleep(2)