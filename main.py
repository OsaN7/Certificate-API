from certificateservice.api.routers.process_template_routes import router as process_template_router
from fastapi import FastAPI

from certificateservice.api.routers import certificate_routes, user_routes, template_routes, process_data_routes
from certificateservice.settings import Settings

app = FastAPI(title="Certificate Service API")

app.include_router(certificate_routes.router)
app.include_router(user_routes.router)
app.include_router(template_routes.router)
app.include_router(process_data_routes.router)


@app.get("/")
async def hc():
    return {"error": False, "msg": "Ok", "result": {"status": "SERVING"}}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=Settings.API_PORT, log_level="info")
