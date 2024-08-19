from mem0 import Memory
from ...config import config

m = Memory.from_config(config)
m.handle_query("你好", user_id="123")