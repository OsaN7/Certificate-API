from fastapi import FastAPI

from certificateservice.api.routers import process_data_routes, process_routes, user_routes, template_routes
from certificateservice.settings import Settings

app = FastAPI(title="Certificate Service API")

app.include_router(process_routes)
app.include_router(user_routes)
app.include_router(template_routes)
app.include_router(process_data_routes)


@app.get("/")
async def hc():
    return {"error": False, "msg": "Ok", "result": {"status": "SERVING"}}


if __name__ == '__main__':
    import uvicorn

    print(f"DATABASE_URL: '{Settings.DATABASE_URL}'")
    uvicorn.run(app, host="0.0.0.0", port=Settings.API_PORT, log_level="info")
