import uvicorn
from fastapi import FastAPI





app = FastAPI(
    title="shai-gateway",
    description="This is backend gateway for superhero ai",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

from clerk_routes import webhook_router


app.include_router(webhook_router)
if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=5151)