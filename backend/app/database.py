# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import redis 


# SQLALCHEMY_DATABASE_URL should be in the format:
# dialect+driver://username:password@host:port/database
# For a simple PostgreSQL connection, it might look like this:
SQLALCHEMY_DATABASE_URL = os.environ["SQLALCHEMY_DATABASE_URL"]

# Create an engine
# echo=True will print all the SQL statements, which is useful for debugging.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    echo=False,
)

# Each instance of the SessionLocal class will be a database session. 
# The class itself is not a database session yet.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for your models to inherit
Base = declarative_base()

# Dependency to get the DB session
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
    socket_timeout=20,  # Socket超时时间，单位：秒
    socket_connect_timeout=10  # 连接超时时间，单位：秒
)
  # 创建一个 Redis 对象，代表一个连接池

# 使用yield的方式创建一个依赖项
def get_redis_conn():
    try:
        # 在这里，我们直接返回连接池对象
        yield redis_conn
    finally:
        # 如果有需要在请求结束后执行的清理代码，可以放在这里
        # 对于Redis连接池来说，通常不需要关闭，所以这里可以留空
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