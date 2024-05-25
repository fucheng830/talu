# init_db.py
import load_env
import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from models import Base, User  # Import your models here
import uuid
import datetime
from utils import md5

from database import SessionLocal, engine

def create_tables():
    # Create tables defined in your models
    Base.metadata.drop_all(bind=engine)  # Drops all tables
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")

def create_admin_user():
    # Create a session
    db = SessionLocal()
    
    # Define the admin user data
    admin_data = {
        "user_id": uuid.uuid4(),
        "union_id": "admin_union_id",
        "openid": "admin_openid",
        "name": "Admin User",
        "avatar": "http://example.com/admin_avatar.jpg",
        "subscribe_scene": "Admin Scene",
        "password": md5("123456"),
        "phone_num": "1234567890",
        "session_key": "admin_session_key",
        "vip_end_time": datetime.datetime.utcnow()+datetime.timedelta(days=3650),
        "status": 9,
        "register_time": datetime.datetime.utcnow(),
        "email": "admin@example.com",
        "referee": uuid.uuid4(),
        "ip": "127.0.0.1"
    }

    # Create an admin user instance
    admin_user = User(**admin_data)
    
    # Add to the session and commit
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    print("Admin user created successfully. User ID:", admin_user.user_id)

# 执行sql语句创建初始化数据


if __name__ == "__main__":
    create_tables()
    create_admin_user()
