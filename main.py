import uvicorn
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.controllers.health_controller import router as health_router
from app.controllers.user_controller import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="NFC-e Backend",
    description="Backend do projeto da disciplina de Programação 3",
    version="1.0.0",
    lifespan=lifespan
)

static_dir = Path("static")
static_dir.mkdir(exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api/v1")
app.include_router(user_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "NFC-e Reader Backend API is running!"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )