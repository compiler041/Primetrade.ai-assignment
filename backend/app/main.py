from fastapi.middleware.cors import CORSMiddleware
from app.db.session import SessionLocal, engine, Base
from app.core import config
from fastapi import FastAPI, Depends
from starlette.requests import Request
import sys

app = FastAPI(
    title=config.PROJECT_NAME,
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    description="Scalable REST API with Authentication & Role-Based Access Control",
)

origins = config.CORS_ORIGINS.split(',') if config.CORS_ORIGINS else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Create all database tables on startup (useful for SQLite dev)."""
    # Import all models so they are registered with Base.metadata
    from app.domains.users.db import user_entity  # noqa
    from app.domains.tasks.db.tasks import task_entity  # noqa
    from app.domains.tasks.db.projects import project_entity  # noqa
    Base.metadata.create_all(bind=engine)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = SessionLocal()
    response = await call_next(request)
    request.state.db.close()
    return response


@app.get("/api/v1")
async def root():
    return {"message": "Hello World", "version": "1.0.0"}


@app.get("/api/health")
async def health():
    return {"status": "ok"}


# Import routers after app creation to avoid circular imports
try:
    from app.domains.auth.api.api_v1.routers.auth import auth_router
    from app.domains.tasks.api.api_v1.routers.tasks import tasks_router
    from app.domains.tasks.api.api_v1.routers.projects import projects_router
    from app.domains.users.api.api_v1.routers.users import users_router
    from app.domains.auth.auth import get_current_active_user

    # Include routers
    app.include_router(auth_router, prefix="/api", tags=["auth"])

    app.include_router(
        tasks_router,
        prefix="/api/v1",
        tags=["tasks"],
        dependencies=[Depends(get_current_active_user)],
    )

    app.include_router(
        projects_router,
        prefix="/api/v1",
        tags=["projects"],
        dependencies=[Depends(get_current_active_user)],
    )

    app.include_router(
        users_router,
        prefix="/api/v1",
        tags=["users"],
        dependencies=[Depends(get_current_active_user)],
    )
except ImportError as e:
    print(f"Warning: Could not import all routers: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
