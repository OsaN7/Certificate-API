# from fastapi import FastAPI
# from certificateservice.api.Routers import certificate_router

# def include_routers(app: FastAPI):
#     app.include_router(certificate_router.router)
from .router_certificate import router as router_certificate
from .user_routes import router as user_router

