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


# 创建一个新的conda环境并激活
RUN conda create -n quchat python=3.10
SHELL ["conda", "run", "-n", "quchat", "/bin/bash", "-c"]

# 设置channels，优先使用清华大学镜像
RUN conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
RUN conda config --add channels defaults

# 安装依赖包
RUN conda install \
    _libgcc_mutex=0.1=main \
    _openmp_mutex=5.1=1_gnu \
    bzip2=1.0.8=h7b6447c_0 \
    ca-certificates=2023.12.12=h06a4308_0 \
    ld_impl_linux-64=2.38=h1181459_1 \
    libffi=3.4.4=h6a678d5_0 \
    libgcc-ng=11.2.0=h1234567_1 \
    libgomp=11.2.0=h1234567_1 \
    libstdcxx-ng=11.2.0=h1234567_1 \
    libuuid=1.41.5=h5eee18b_0 \
    ncurses=6.4=h6a678d5_0 \
    openssl=3.0.12=h7f8727e_0 \
    pip=23.3.1=py310h06a4308_0 \
    python=3.10.13=h955ad1f_0 \
    readline=8.2=h5eee18b_0 \
    setuptools=68.2.2=py310h06a4308_0 \
    sqlite=3.41.2=h5eee18b_0 \
    tk=8.6.12=h1ccaba5_0 \
    wheel=0.41.2=py310h06a4308_0 \
    xz=5.4.5=h5eee18b_0 \
    zlib=1.2.13=h5eee18b_0


RUN pip install -r requirements.txt
RUN pip install uvicorn gunicorn

# 将前端资源复制到后端 static 目录
COPY --from=builder /frontend/dist /frontend/dist

WORKDIR /backend

# 设置容器启动时执行的命令，使用uvicorn运行FastAPI应用
CMD ["conda", "run", "-n", "quchat", "uvicorn", "main:app", "--port", "8002", "--host", "0.0.0.0"]
