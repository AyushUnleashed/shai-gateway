from models.webhook_model import WebhookPayload
from models.orders_model import OrderData, Status
from supabase_utils import SUPABASE_CLIENT, Client
from fastapi import HTTPException
import hashlib
from typing import Tuple, Dict, Any
from webhook_supabase_handler import check_existing_order, insert_new_order
from config import settings
import hmac
from typing import Tuple
from logger import get_logger

logger = get_logger(__name__)
import json

from models.orders_model import PaymentPlatform


def verify_signature(body: bytes, signature: str) -> bool:
    secret = settings.LEMONSQUEEZY_WEBHOOK_SECRET.encode()
    digest = hmac.new(secret, body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(digest, signature)


async def process_lemon_squeezy_webhook(payload: WebhookPayload) -> str:
    """
    Processes the incoming webhook payload.

    Args:
        payload (WebhookPayload): The payload of the webhook.
        supabase_client (Client): Initialized Supabase client.

    Returns:
        str: A message indicating the outcome of the operation.
    """
    event_name = payload.meta.get('event_name', 'Unknown')
    custom_data = payload.meta.get('custom_data', {})
    first_order_item = payload.data['attributes']['first_order_item']

    if event_name == "order_created":
        order_data = OrderData(
            order_id=first_order_item['order_id'],
            pack_type= custom_data.get('pack_type', '').upper(),
            created_at=first_order_item['created_at'],
            email=custom_data.get('email', ''),
            user_name=custom_data.get('user_name', ''),
            user_id=custom_data.get('user_id', ''),
            gender=None,
            user_image_link=None,
            status=Status.NOT_GENERATED.value,  # Default status, update based on your logic
            webhook_object=payload.json(),
            test_mode=first_order_item['test_mode'],
            custom_data=json.dumps(custom_data),
            payment_platform=PaymentPlatform.LEMON_SQUEEZY.value
        )

        exists, _ = check_existing_order(SUPABASE_CLIENT, order_data.order_id)
        if exists:
            return "Order already exists. No action taken."
        await insert_new_order(order_data.__dict__)
        return "Webhook received and data processed successfully."

    return "Webhook received and no action taken."


async def validate_and_process_request_lemon_squeezy(body: bytes, signature: str, payload: WebhookPayload) -> Tuple[
    bool, str]:
    if not verify_signature(body, signature):
        logger.error("Invalid signature.")
        raise HTTPException(status_code=400, detail="Invalid signature.")

    # Await the async process_webhook function and store its result
    message = await process_lemon_squeezy_webhook(payload)  # process_webhook is now awaited

    # Assuming process_webhook returns a string message, success flag is not needed
    # since you're raising HTTPException directly in case of failures.
    logger.info(message)
    return True, message  # Assuming the process is successful if no exception was raised
