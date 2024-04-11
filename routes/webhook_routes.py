from models.orders_model import OrderData, Status
from models.webhook_model import WebhookPayload
from payments.lemon_squeezy_webhook_handler import validate_and_process_request_lemon_squeezy
from models.orders_model import PaymentPlatform
from payments.razor_pay_webhook_handler import validate_and_process_request_razorpay
from fastapi import Request, HTTPException
from utils.logger import get_logger
logger = get_logger(__name__)
import json
from fastapi import APIRouter
from utils.config import settings
from models.clerk_webhook_model import ClerkWebhookPayload
from database.handle_user_db_updates import add_user_to_supabase, delete_user_from_supabase
from models.user_model import User


webhook_router = APIRouter()
@webhook_router.post("/webhook/razorpay")
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

@webhook_router.post("/webhook/lemonsqueezy")
async def lemonsqueezy_webhook(request: Request, payload: WebhookPayload):
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


@webhook_router.post("/webhook/clerk")
async def clerk_webhook(request: Request, test_mode: bool = True):
    try:
        # Set the test mode based on the endpoint hit
        settings.IS_TEST_MODE = test_mode

        data = await request.json()
        payload = ClerkWebhookPayload(**data)

        # Check if the event is user.created
        if payload.type == 'user.created':
            # Extract required information
            user = User(
                user_id=payload.data.id,
                email=payload.data.email_addresses[0].email_address if payload.data.email_addresses else None,
                user_image_link=payload.data.profile_image_url,
                # The following fields are just placeholders as I don't have the actual payload structure for them
                credits=1,  # You would replace None with the actual credits info from payload
                orders_array=[],  # Replace None with the actual orders info from payload
                gender=None,  # Replace None with the actual gender info from payload
                test_mode=settings.IS_TEST_MODE
            )
            # Process the extracted information as needed
            print(user)
            add_user_to_supabase(user)
            return {"success": "User created event processed.", "user_info": user}

        if payload.type == 'user.deleted':
            user_to_be_deleted_id: str = payload.data.id
            delete_user_from_supabase(user_to_be_deleted_id)
            print(user_to_be_deleted_id)

        return {"success": "Webhook received, but no action taken for this event type."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing webhook data: {e}")

@webhook_router.post("/webhook/clerk/prod")
async def clerk_webhook_prod(request: Request):
    return await clerk_webhook(request, test_mode=False)