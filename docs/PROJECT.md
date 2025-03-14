# Talu 项目文档

## 项目概述

Talu 是一个基于 FastAPI 和 Vue.js 的全栈知识库管理系统，支持文档处理、向量检索和 AI 对话等功能。系统采用前后端分离架构，使用 Docker 进行容器化部署。

## 技术栈

### 后端
- FastAPI: Python Web 框架
- SQLAlchemy: ORM 框架
- PostgreSQL + pgvector: 数据库和向量存储
- Redis: 缓存服务
- Langchain: AI 对话和文档处理框架

### 前端
- Vue 3: 前端框架
- Vite: 构建工具
- Naive UI: UI 组件库
- Tailwind CSS: CSS 框架

## 系统架构

### 核心模块

1. **知识库管理**
   - 支持创建和管理知识库
   - 文档上传和处理
   - 文本分割和向量化
   - 内容检索

2. **Agent 系统**
   - 可配置的对话代理
   - 工具集成
   - 对话历史管理

3. **用户系统**
   - 用户认证和授权
   - 会员订阅
   - 积分系统

### 数据模型

主要数据表：
- users: 用户信息
- nodes: 知识节点
- langchain_pg_collection: 知识库集合
- langchain_pg_embedding: 向量存储
- agent: 对话代理配置

## 功能模块

### 1. 文档处理

支持多种文档格式：
- Word (.docx, .doc)
- PDF
- Excel (.xlsx, .xls)
- PowerPoint (.pptx, .ppt)
- 文本文件 (.txt)
- 图片 (.jpg, .png, etc.)
- 音视频文件

处理流程：
1. 文件上传
2. 内容提取
3. 文本分割
4. 向量化存储

### 2. 知识抽取

支持两种主要的知识抽取方式：
- 摘要生成
- 问答对抽取

### 3. 向量检索

使用 pgvector 进行向量相似度检索：
- 支持多种检索策略
- 元数据过滤
- 结果重排序

### 4. 订阅系统

会员计划功能：
- 多种订阅等级
- 使用额度限制
- 支付集成

## 部署说明

### Docker 部署

使用 Docker Compose 进行多容器部署：

```yaml
services:
  backend:
    build: .
    ports: 
      - "8088:8002"
    environment:
      - SQLALCHEMY_DATABASE_URL=postgresql://postgres:password@postgres:5432/quchat
      # ...其他环境变量...
  
  postgres:
    image: ankane/pgvector
    
  redis:
    image: redis:latest
```

### 环境变量配置

关键配置项：
- 数据库连接
- OpenAI API 密钥
- Redis 连接
- 安全密钥

## API 文档

### 知识库接口

主要端点：
```
POST /add_knowledge      # 创建知识库
POST /upload_file       # 上传文件
POST /split_document    # 文档分割
POST /extract_document  # 知识抽取
POST /upload_data      # 保存处理后的数据
POST /search_node      # 知识检索
```

### Agent 接口

```
POST /agent/create     # 创建对话代理
POST /agent/chat      # 对话
GET  /agent/list      # 获取代理列表
```

## 前端架构

### 目录结构
```
frontend/
  ├── src/
  │   ├── api/        # API 调用
  │   ├── components/ # 通用组件
  │   ├── views/      # 页面
  │   ├── store/      # 状态管理
  │   └── utils/      # 工具函数
  ├── public/         # 静态资源
  └── vite.config.ts  # 构建配置
```

### 主要页面

1. 知识库管理
   - 知识库列表
   - 文档上传
   - 文档处理配置
   - 内容检索

2. Agent 配置
   - 代理列表
   - 代理创建和编辑
   - 对话界面

3. 用户中心
   - 个人信息
   - 订阅管理
   - 使用统计

## 安全性考虑

1. 认证和授权
   - JWT token 认证
   - 基于角色的访问控制

2. 数据安全
   - 文件存储安全
   - 敏感信息加密
   - SQL 注入防护

3. API 安全
   - CORS 配置
   - 请求限流
   - 参数验证

## 扩展性设计

1. 模块化架构
   - 插件系统
   - 工具集成接口

2. 性能优化
   - 缓存策略
   - 异步处理
   - 数据分片

## 维护和监控

1. 日志系统
   - 操作日志
   - 错误追踪
   - 性能监控

2. 备份策略
   - 数据库备份
   - 文件备份
   - 恢复流程

## 后续开发计划

1. 功能增强
   - 多语言支持
   - 更多文件格式支持
   - 高级检索功能

2. 性能优化
   - 向量检索优化
   - 缓存策略优化
   - 并发处理改进

3. 用户体验
   - UI/UX 改进
   - 响应式设计
   - 移动端适配
