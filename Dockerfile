# Stage 1: Build the frontend
FROM node:20 AS builder

COPY ./frontend /frontend

WORKDIR /frontend

RUN npm install -g pnpm

ENV FETCH_TIMEOUT=120000

RUN pnpm install

RUN pnpm run build-only

# Stage 2: Set up the backend with Miniconda and Poetry
FROM continuumio/miniconda3

# Install system dependencies
RUN apt-get update && \
    apt-get install -y build-essential gcc curl libpq-dev

# Create a conda environment with Python 3.10
RUN conda create -n myenv python=3.10

# Activate the environment
SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-c"]

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Configure Poetry to use Tsinghua University mirror
RUN poetry config repositories.tuna https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple

# Copy backend code
COPY ./backend /backend

WORKDIR /backend

# Install Python dependencies using Poetry in the conda environment
RUN poetry install --no-root

# Install additional dependencies if needed
RUN poetry add uvicorn gunicorn

# Copy frontend build to the backend static directory
COPY --from=builder /frontend/dist /frontend/dist

# Set the command to run the application using Uvicorn
CMD ["conda", "run", "-n", "myenv", "poetry", "run", "uvicorn", "main:app", "--port", "8080", "--host", "0.0.0.0", "--log-level", "debug"]
