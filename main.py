from fastapi import FastAPI

from api import router as api_router

app = FastAPI()
app.include_router(router=api_router, prefix="/api")
