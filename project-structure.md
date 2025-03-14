# Talu Project Structure

```
talu/
├── frontend/                  # Vue.js frontend application
│   ├── src/
│   │   ├── assets/           # Static assets
│   │   ├── components/       # Reusable Vue components
│   │   │   ├── agents/      
│   │   │   ├── workflows/
│   │   │   └── knowledge/
│   │   ├── views/           # Page components
│   │   ├── store/           # Vuex store modules
│   │   └── services/        # API services
│   └── tests/               # Frontend tests
│
├── backend/                  # FastAPI backend application
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   │   ├── agents/
│   │   │   ├── auth/
│   │   │   └── workflows/
│   │   ├── core/          # Core business logic
│   │   ├── models/        # Database models
│   │   ├── schemas/       # Pydantic schemas
│   │   └── services/      # Business services
│   ├── tests/            # Backend tests
│   └── alembic/          # Database migrations
│
├── plugins/               # Plugin system
│   ├── wechat/
│   ├── douyin/
│   └── email/
│
├── docs/                 # Documentation
│   ├── api/
│   ├── deployment/
│   └── development/
│
└── docker/              # Docker configuration
    ├── frontend/
    ├── backend/
    └── nginx/
```

## Key Improvements

1. **Modular Architecture**
   - Separated frontend and backend
   - Clear separation of concerns
   - Plugin-based architecture for extensions

2. **Development Workflow**
   - Consistent directory structure
   - Easy to locate components
   - Clear separation of tests

3. **Documentation**
   - Centralized documentation
   - API documentation
   - Deployment guides

4. **Containerization**
   - Docker support for all components
   - Easy deployment
   - Environment consistency
