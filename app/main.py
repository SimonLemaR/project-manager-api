from fastapi import FastAPI
from app.routers.user import user_router

app = FastAPI()


@app.get("/")
def root():
    return {"message": "API running"}

app.include_router(user_router, prefix="/api/v1/users", tags=["Users"])