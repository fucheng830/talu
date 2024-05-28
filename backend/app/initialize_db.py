# init_db.py
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from app.models import Base, User  # Import your models here
import uuid
import datetime
from app.utils import md5
from sqlalchemy import inspect
from sqlalchemy import text
import sqlalchemy

from app.database import SessionLocal, engine

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


def create_vector_extension() -> None:
    try:
        with SessionLocal() as session:  # type: ignore[arg-type]
            # The advisor lock fixes issue arising from concurrent
            # creation of the vector extension.
            # https://github.com/langchain-ai/langchain/issues/12933
            # For more information see:
            # https://www.postgresql.org/docs/16/explicit-locking.html#ADVISORY-LOCKS
            statement = sqlalchemy.text(
                """BEGIN;
                SELECT pg_advisory_xact_lock(1573678846307946496);
                CREATE EXTENSION IF NOT EXISTS vector;
                CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
                COMMIT;
                """
            )
            session.execute(statement)
            session.commit()
    except Exception as e:
        raise Exception(f"Failed to create vector extension: {e}") from e


# 执行sql语句创建初始化数据
def auto_create_data():
    # Create a session
    db = SessionLocal()

    # Create an inspector and get table names
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    if not tables:
        create_vector_extension()
        create_tables()
        create_admin_user()
    else:
        print("Tables already exist. Skipping creation.")

if __name__ == "__main__":
    auto_create_data()
    
