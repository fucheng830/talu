from dotenv import load_dotenv
import os

env_name = '.env' 
dotenv_path = os.path.join(os.path.dirname(__file__), env_name)
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path, override=True)

from app import api
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from typing import Optional
import os
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import structlog
from app import initialize_db


logger = structlog.get_logger(__name__)

app = FastAPI()

# Get root of app, used to point to directory containing static files
ROOT = Path(__file__).parent.parent

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api.chat_router)
app.include_router(api.user_router)
app.include_router(api.image_router)
app.include_router(api.agent_router)
app.include_router(api.auth_router)
app.include_router(api.knowledge_router)
app.include_router(api.order_router)
app.include_router(api.chatbot_router)

@app.get("/hello_world")
async def wechat(request: Request):
    # 尝试从X-Forwarded-For头部获取真实IP
    x_forwarded_for: Optional[str] = request.headers.get("x-forwarded-for")
    if x_forwarded_for:
        # X-Forwarded-For可能包含多个IP地址，取第一个作为客户端IP
        client_ip = x_forwarded_for.split(",")[0]
    else:
        # 如果没有X-Forwarded-For头部，直接从连接信息获取IP
        client_ip = request.client.host
    return "请关注微信公众号：Aibot机器人对话，获取更多信息！"

ui_dir = str(ROOT / "frontend/dist")
print(ui_dir)
# 检查路径 ui_dir 是否存在
if os.path.exists(ui_dir):
    # 如果存在，则将其挂载为静态文件目录，根路径为 ""，支持 HTML 文件
    app.mount("", StaticFiles(directory=ui_dir, html=True), name="ui")
else:
    # 如果不存在，则记录一条警告信息，表示仅提供 API 服务
    logger.warn("No UI directory found, serving API only.")

initialize_db.auto_create_data()

if __name__=="__main__":
    # 读取环境变量
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)





