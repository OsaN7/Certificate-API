from fastapi import FastAPI
from certificateservice.api.Routers.router_certificate import router as router_certificate
from certificateservice.api.Routers.user_routes import router as user_router
from certificateservice.api.Routers.process_template_routes import router as process_template_router
from certificateservice.api.Routers.process_data_routes import router as process_data_router
import os

app = FastAPI(title="Certificate Service API")

app.include_router(router_certificate)
app.include_router(user_router)
app.include_router(process_template_router)
app.include_router(process_data_router)

# Print the DATABASE_URL from environment variables
print("DATABASE_URL:", os.getenv("DATABASE_URL"))

# Health check endpoint
@app.get("/")
async def hc():
    return {"error": False, "msg": "Ok", "result": {"status": "SERVING"}}