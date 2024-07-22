FROM node:20 AS builder

COPY ./frontend /frontend

WORKDIR /frontend

RUN npm install -g pnpm

ENV FETCH_TIMEOUT=120000

RUN pnpm install

RUN rm -rf .env

RUN pnpm run build-only

# 使用miniconda作为基础镜像
FROM continuumio/miniconda3

# 打包前端资源
WORKDIR /backend
# 使用pip安装剩余的Python依赖
COPY ./backend /backend

RUN apt-get update && \
    apt-get install -y build-essential gcc
    
# 设置channels，优先使用清华大学镜像
RUN conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
RUN conda config --add channels defaults
# 设置 pip 使用清华大学镜像源
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

RUN pip install -r requirements.txt
RUN pip install uvicorn gunicorn

# 将前端资源复制到后端 static 目录
COPY --from=builder /frontend/dist /frontend/dist

WORKDIR /backend

# 设置容器启动时执行的命令，使用uvicorn运行FastAPI应用
CMD ["uvicorn", "main:app", "--port", "8080", "--host", "0.0.0.0"]
