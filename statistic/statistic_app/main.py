from fastapi import FastAPI

from .subscribe import note_request_router

app = FastAPI(root_path="/statistic")
app.include_router(note_request_router)


@app.get("/health-check/")
async def health_check() -> bool:
    return True
