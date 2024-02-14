from fastapi import FastAPI, Request, HTTPException
from models import WebhookPayload
from webhook_handler import validate_and_process_request
from logger import get_logger

app = FastAPI()
logger = get_logger(__name__)


@app.post("/webhook/")
async def receive_webhook(request: Request, payload: WebhookPayload):
    signature = request.headers.get('x-signature')
    if not signature:
        logger.error("Missing signature header.")
        raise HTTPException(status_code=400, detail="Missing signature header.")

    body = await request.body()
    try:
        await validate_and_process_request(body, signature, payload)
    except HTTPException as e:
        raise e

    return {"message": "Webhook received and data processed successfully."}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5151)
