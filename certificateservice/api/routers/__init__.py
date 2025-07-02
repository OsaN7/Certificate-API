# from .router_certificate import router as router_certificate
# from .user_routes import router as user_router

from fastapi import FastAPI
from .process_router import router as process_routes
from .user_router import router as user_routes
from .template_router import router as template_routes
from .process_data_router import router as process_data_routes

def include_routers(app: FastAPI):
    app.include_router(process_routes)
    app.include_router(user_routes)
    app.include_router(template_routes)
    app.include_router(process_data_routes)