# from fastapi import FastAPI
# from certificateservice.api.Routers import router_certificate, user_router

# app = FastAPI(title="Certificate Service API")

# # Register your routers
# app.include_router(router_certificate.router)
# app.include_router(user_router.router)

from fastapi import FastAPI

from certificateservice.api.Routers.router_certificate import router as router_certificate
from certificateservice.api.Routers.user_routes import router as user_router
from certificateservice.api.Routers.folder_upload_routes import router as folder_upload_router

app = FastAPI(title="Certificate Service API")

app.include_router(router_certificate)
app.include_router(user_router)
app.include_router(folder_upload_router)


# Health check endpoint
@app.get("/")
async def hc():
    return {"error": False, "msg": "Ok", "result": {"status": "SERVING"}}

