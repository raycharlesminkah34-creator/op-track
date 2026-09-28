from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.models import opportunity as _models  # noqa: F401
from app.routers import opportunities, dashboard


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="OP-TRACK API",
    description="Opportunity Tracker API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    opportunities.router,
    prefix="/api/v1/opportunities",
    tags=["opportunities"],
)
app.include_router(
    dashboard.router,
    prefix="/api/v1/dashboard",
    tags=["dashboard"],
)


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}
