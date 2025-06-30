# from .router_certificate import router as router_certificate
# from .user_routes import router as user_router

from fastapi import FastAPI
from .certificate_routes import router as certificate_routes
from .user_routes import router as user_routes
from .process_template_routes import router as template_routes
from .process_data_routes import router as process_data_routes

def include_routers(app: FastAPI):
    app.include_router(certificate_routes)
    app.include_router(user_routes)
    app.include_router(template_routes)
    app.include_router(process_data_routes)