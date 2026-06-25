from fastapi import FastAPI
from app.routers.user import user_router
from app.routers.project import project_router
from app.routers.document import document_router


app = FastAPI()


@app.get("/")
def root():
    return {"message": "API running"}


app.include_router(user_router, prefix="/api/v1/users", tags=["Users"])
app.include_router(project_router, prefix="/api/v1/projects", tags=["Projects"])
app.include_router(document_router, prefix="/api/v1/documents", tags=["Documents"])
