from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from app.core.config import settings
from app.db.database import init_db
from app.routes.pages import router as pages_router
from app.routes.auth import router as auth_router
from app.routes.planners import router as planners_router
from app.routes.history import router as history_router
from app.routes.system import router as system_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="PocketSmart AI - budget-aware recommendations for home, parties and jewelry.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(pages_router)
app.include_router(auth_router, prefix="/api")
app.include_router(planners_router, prefix="/api")
app.include_router(history_router, prefix="/api")
app.include_router(system_router, prefix="/api")
