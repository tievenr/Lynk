from app.routes import router
from prometheus_fastapi_instrumentator import Instrumentator
from fastapi import FastApi

app=FastAPI()
app.include_router(router)

Instrumentator().instrument(app).expose(app)