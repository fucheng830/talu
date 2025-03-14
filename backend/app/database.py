# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import redis 

SQLALCHEMY_DATABASE_URL = os.environ["SQLALCHEMY_DATABASE_URL"]

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise 
    finally:
        db.close()

REDIS_URL = os.environ.get("REDIS_URL") or "redis://localhost:6379/0"

redis_conn = redis.from_url(
    REDIS_URL,
    socket_timeout=20,
    socket_connect_timeout=10
)

def get_redis_conn():
    try:
        yield redis_conn
    finally:
        pass

def set_key(key, value, **kwargs): 
    return redis_conn.set(key, value, **kwargs)
 
def get_key(key): 
    value_bytes = redis_conn.get(key)
    if value_bytes is not None:
        value_str = value_bytes.decode('utf-8')
        return value_str
    else:
        return None