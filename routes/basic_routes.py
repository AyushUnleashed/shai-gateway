from fastapi import APIRouter
# webhook_router = APIRouter()
#
basic_router = APIRouter()
@basic_router.get("/")
async def read_root():
    return {"message": "Welcome to the superhero ai backend gateway. This is the root endpoint."}
