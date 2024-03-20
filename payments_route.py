from fastapi import FastAPI, Request, HTTPException, APIRouter
from models.webhook_model import WebhookPayload
from lemon_squeezy_hanlder import validate_and_process_request_lemon_squeezy
from logger import get_logger
from models.orders_model import OrderData, Status
from slackbot import SHAI_Slack_Bot
from process_payments_helper import get_current_payment_mode
logger = get_logger(__name__)
import json
import razorpay
import os
from urllib.parse import urlparse
# ==========================================================================
#                             setup the payments
# ==========================================================================

from fastapi import APIRouter
payments_webhook_router = APIRouter()
from config import settings
from routers import basic_router

from models.orders_model import PaymentPlatform
from razor_pay_handler import validate_and_process_request_razorpay
@payments_webhook_router.post("/webhook/razorpay")
async def razorpay_webhook(request: Request):
    payload = await request.json()
    print("REQUEST data received:", payload)
    # Extract major information
    event_type = payload["event"]
    from utils.utils import convert_unix_to_datetime
    if event_type == "order.paid":
        payment_entity = payload['payload']['payment']['entity']
        order_data = OrderData(
            order_id=payment_entity['order_id'],
            created_at=convert_unix_to_datetime(payment_entity['created_at']),
            email=payment_entity['notes'].get('email', ''),
            payment_platform=PaymentPlatform.RAZOR_PAY.value,
            user_id=payment_entity['notes'].get('user_id', ''),
            gender=None,
            user_name=payment_entity['notes'].get('user_name', ''),
            user_image_link=None,
            status= Status.NOT_GENERATED.value,
            pack_type=payment_entity['notes'].get('pack_type', '').upper(),
            webhook_object=json.dumps(payload),
            test_mode=settings.is_razor_pay_test_mode,
            custom_data=json.dumps(payment_entity['notes']),
        )
        try:
            await validate_and_process_request_razorpay(order_data)
        except HTTPException as e:
            raise e

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


# from pydantic import BaseModel
#
# class RazorPayOrderRequest(BaseModel):
#     name: str
#     email: str
#     user_id: str
#     pack_type: str
#
# @basic_router.post("/payments/razorpay/create_order")
# async def generate_razorpay_order(order_request: RazorPayOrderRequest):
#     from process_payments_helper import create_razor_pay_order
#     order = create_razor_pay_order(
#         order_request.name,
#         order_request.email,
#         order_request.user_id,
#         order_request.pack_type
#     )
#     return order


from process_payments_helper import generate_lemonsqueezy_payment_link, create_razor_pay_order
from configuration import CONFIG
@basic_router.post("/payments/generate_payment_link")
async def process_payments(request: Request):
    try:
        # Extract 'Origin' header from the request
        origin = request.headers.get("origin")
        
        # If 'Origin' is not present, try to extract the base URL from the 'Referer' header
        if not origin:
            referer = request.headers.get("referer")
            if referer:
                parsed_referer = urlparse(referer)
                origin = f"{parsed_referer.scheme}://{parsed_referer.netloc}"
            else:
                # If neither 'Origin' nor 'Referer' header is present, raise an error
                raise HTTPException(status_code=400, detail="Origin is missing and Referer header cannot be used.")
        
        CONFIG.lemonsqueezy_frontend_redirect_url = f"{origin}/my_orders"
        payload = await request.json()
        print("REQUEST data received:", payload)

        payment_platform = payload.get("payment_platform")
        pack_type = payload.get("pack_type")
        user_id = payload.get("user_id")
        name = payload.get("name")
        email = payload.get("email")

        if not all([payment_platform, pack_type, user_id, name, email]):
            raise HTTPException(status_code=400, detail="Missing payment information in the request.")

        if payment_platform == "RAZORPAY":
            try:
                order_details = create_razor_pay_order(name, email, user_id, pack_type)
                return order_details
            except Exception as e:
                logger.error(f"Failed to create Razorpay order: {e}")
                raise HTTPException(status_code=500, detail="Failed to create Razorpay order.")
        elif payment_platform == "LEMONSQUEEZY":
            try:
                payment_link = generate_lemonsqueezy_payment_link(name, email, user_id, pack_type)
                return {"payment_link": payment_link}
            except Exception as e:
                logger.error(f"Failed to generate LemonSqueezy payment link: {e}")
                raise HTTPException(status_code=500, detail="Failed to generate LemonSqueezy payment link.")
        else:
            raise HTTPException(status_code=400, detail="Invalid payment platform specified.")
    except HTTPException as http_exc:
        logger.error(f"An unexpected http error occurred: {http_exc}")
        raise http_exc
    except Exception as exc:
        logger.error(f"An unexpected error occurred: {exc}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")

from pydantic import BaseModel

class RazorPayValidationRequest(BaseModel):
    razorpay_payment_id: str
    razorpay_order_id: str
    razorpay_signature: str

@basic_router.post("/payments/razorpay/validate")
async def validate_razorpay_payment(validation_request: RazorPayValidationRequest):

    RAZOR_PAY_ID = os.getenv('RAZOR_PAY_ID')
    RAZOR_PAY_SECRET = os.getenv('RAZOR_PAY_SECRET')
    client = razorpay.Client(auth=(RAZOR_PAY_ID, RAZOR_PAY_SECRET))

    try:
        client.utility.verify_payment_signature({
            'razorpay_order_id': validation_request.razorpay_order_id,
            'razorpay_payment_id': validation_request.razorpay_payment_id,
            'razorpay_signature': validation_request.razorpay_signature
        })
        logger.info("Payment signature verified successfully.")
        return {"message": "Payment signature verified successfully."}
    except razorpay.errors.SignatureVerificationError as e:
        logger.error(f"Signature verification failed: {e}")
        raise HTTPException(status_code=400, detail="Signature verification failed.")


from supabase_utils import SUPABASE_CLIENT
supabase = SUPABASE_CLIENT

@basic_router.post("/update_paid_user_db")
async def update_paid_user_db(request: Request):
    payload = await request.json()
    logger.info(payload)
    order_id = payload.get("order_id")
    user_id = payload.get("user_id")
    gender = payload.get("gender")

    # Get image link from Supabase Storage
    image_path = f"{user_id}/{order_id}.png"
    curr_mode = get_current_payment_mode(order_id)

    if curr_mode == "PROD":
        image_link = supabase.storage.from_('paid-user-images').get_public_url(image_path)
    elif curr_mode == "TEST":
        image_link = supabase.storage.from_('test-paid-user-images').get_public_url(image_path)

    # Update orders table with image link and gender
    orders_table = supabase.table('orders')
    update_response = orders_table.update({
        'user_image_link': image_link,
        'gender': gender,
        'status': 'GENERATING'
    }).eq('order_id', order_id).eq('user_id', user_id).execute()
    
    await SHAI_Slack_Bot.send_message(f"{curr_mode}: \n Update Successful: \n User ID: {user_id},\n Order ID: {order_id},\n Image Link: {image_link},\n Gender: {gender},\n Status: 'GENERATING'")
    return {"message": "Order updated successfully", "image_link": image_link}

@basic_router.get("/payments/razorpay/get_razorpay_key")
async def get_razorpay_key():
    return {"razorpay_key": settings.RAZOR_PAY_ID}

if __name__ == "__main__":
   mode = get_current_payment_mode("2312270")
   print("mode:", mode)