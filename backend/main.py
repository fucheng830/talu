from src import load_env
from src import router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from typing import Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router.chat_router)
app.include_router(router.user_router)
app.include_router(router.image_router)
app.include_router(router.agent_router)
app.include_router(router.auth_router)
app.include_router(router.knowledge_router)
app.include_router(router.wechat_router)
app.include_router(router.order_router)

@app.get("/")
async def wechat(request: Request):
    # 尝试从X-Forwarded-For头部获取真实IP
    x_forwarded_for: Optional[str] = request.headers.get("x-forwarded-for")
    if x_forwarded_for:
        # X-Forwarded-For可能包含多个IP地址，取第一个作为客户端IP
        client_ip = x_forwarded_for.split(",")[0]
    else:
        # 如果没有X-Forwarded-For头部，直接从连接信息获取IP
        client_ip = request.client.host
    print(client_ip)
    return "请关注微信公众号：Aibot机器人对话，获取更多信息！"


if __name__=="__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)





