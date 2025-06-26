# from .router_certificate import router as router_certificate
# from .user_routes import router as user_router

from fastapi import FastAPI
from .router_certificate import router as router_certificate
from .user_routes import router as user_router

def include_routers(app: FastAPI):
    app.include_router(router_certificate)
    app.include_router(user_router)