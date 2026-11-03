from fastapi import FastAPI
from app.routes import health, auth

app = FastAPI(title="API Biblioteca Segura")

app.include_router(health.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")