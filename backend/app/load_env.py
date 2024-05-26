# 读取环境变量
from dotenv import load_dotenv
import os

env_name = '.env' 
dotenv_path = os.path.join(os.path.dirname(__file__), env_name)
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path, override=True)