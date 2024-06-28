import uvicorn

from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from v1.config import settings
from v1.resources.routes import (
    router as categories_router,
    dev_router as dev_categories_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="lucamatei.dev API",
    lifespan=lifespan,
)

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(categories_router)

if settings.ENVIRONMENT in ("dev", "local"):
    v1_router.include_router(dev_categories_router)

app.include_router(v1_router)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
