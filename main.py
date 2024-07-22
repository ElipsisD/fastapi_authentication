from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from core.models import db_manager, Base
from api import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=api_router, prefix="/api")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
