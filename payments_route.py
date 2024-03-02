from fastapi import FastAPI, Request, HTTPException, APIRouter
from models.webhook_model import WebhookPayload
from lemon_squeezy_hanlder import validate_and_process_request_lemon_squeezy
from logger import get_logger
from models.orders_model import OrderData, Status

logger = get_logger(__name__)
import json

# ==========================================================================
#                             setup the payments
# ==========================================================================

from fastapi import APIRouter
payments_webhook_router = APIRouter()

from routers import basic_router

from models.orders_model import PaymentPlatform

@payments_webhook_router.post("/webhook/razorpay")
async def razorpay_webhook(request: Request):
    payload = await request.json()
    print("REQUEST data received:", payload)
    # Extract major information
    event_type = payload["event"]
    payment_entity = payload['payload']['payment']['entity']

    order_data = OrderData(
        order_id=payment_entity['order_id'],
        created_at=payment_entity['created_at'],
        email=payment_entity['notes'].get('email', ''),
        payment_platform=PaymentPlatform.RAZOR_PAY.value,
        user_id=payment_entity['notes'].get('user_id', ''),
        gender=None,
        user_name=payment_entity['notes'].get('user_name', ''),
        user_image_link=None,
        status= Status.NOT_GENERATED.value,
        pack_type=payment_entity['notes'].get('pack_type', ''),
        webhook_object=json.dumps(payload),
        test_mode=True,
        custom_data=json.dumps(payment_entity['notes']),
    )


    return {"message": "Webhook received and processed successfully"}


@payments_webhook_router.post("/webhook/lemonsqueezy")
async def receive_webhook(request: Request, payload: WebhookPayload):
    signature = request.headers.get('x-signature')
    if not signature:
        logger.error("Missing signature header.")
        raise HTTPException(status_code=400, detail="Missing signature header.")

    body = await request.body()
    try:
        await validate_and_process_request_lemon_squeezy(body, signature, payload)
    except HTTPException as e:
        raise e

    return {"message": "Webhook received and data processed successfully."}


from pydantic import BaseModel

class RazorPayOrderRequest(BaseModel):
    name: str
    email: str
    user_id: str
    pack_type: str

@basic_router.post("/payments/razorpay/create_order")
async def generate_razorpay_order(order_request: RazorPayOrderRequest):
    from generate_payment_link import create_razor_pay_order
    order = create_razor_pay_order(
        order_request.name, 
        order_request.email, 
        order_request.user_id, 
        order_request.pack_type
    )
    return order