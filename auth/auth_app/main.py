from fastapi import FastAPI

from .api import router as api_router

app = FastAPI(root_path="/auth")
app.include_router(router=api_router)
