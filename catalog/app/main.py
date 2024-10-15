from fastapi import FastAPI

from app.api import router as api_router

app = FastAPI(root_path="/api")
app.include_router(router=api_router)
