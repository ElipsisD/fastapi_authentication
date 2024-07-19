from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from core.models import db_manager, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_manager.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def hello_world() -> dict[str, str]:
    return {
        "data": "Hello World",
    }


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
