import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware




app = FastAPI(
    title="shai-gateway",
    description="This is backend gateway for superhero ai",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# List your frontend domain(s) here
origins = [
    "http://localhost:3000",
    "https://superheroai.pro",
    "https://superheroai-git-dev-ayushyadavcodes-gmailcoms-projects.vercel.app",
    "https://superheroai-git-main-ayushyadavcodes-gmailcoms-projects.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # This allows all methods, including OPTIONS
    allow_headers=["*"],
)

# from routers import webhook_router, basic_router
from clerk_routes import webhook_router
from payments_route import payments_webhook_router
from routers import basic_router
app.include_router(webhook_router)
app.include_router(basic_router)
app.include_router(payments_webhook_router)
if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=5151)