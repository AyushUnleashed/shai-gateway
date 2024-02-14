from models import WebhookPayload
from supabase_utils import SUPABASE_CLIENT, Client
from fastapi import HTTPException
import hashlib
from typing import Tuple, Dict, Any

from config import settings
import hmac
from typing import Tuple
from logger import get_logger

logger = get_logger(__name__)


def verify_signature(body: bytes, signature: str) -> bool:
    secret = settings.LEMONSQUEEZY_WEBHOOK_SECRET.encode()
    digest = hmac.new(secret, body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(digest, signature)


def check_existing_order(supabase_client: Client, order_id: str) -> Tuple[bool, Dict[str, Any]]:
    """
    Check if an order already exists in the database.

    Args:
        supabase_client (Client): Initialized Supabase client.
        order_id (str): The ID of the order to check.

    Returns:
        Tuple[bool, Dict[str, Any]]: Returns True and the order data if exists, otherwise False.
    """
    response_tuple  = supabase_client.table('orders').select("*").eq('order_id', order_id).execute()
    response_data, response_error = response_tuple

    # Check for response error based on the count of error messages
    if response_error and response_error[0] == 'count' and response_error[1] is None:
        # No error
        error = None
    else:
        # Error exists
        error = response_error

    if error:
        raise HTTPException(status_code=400, detail=f"Unexpected error querying Supabase: {error}")

    exists = len(response_data[1]) > 0
    return exists, response_data[0] if exists else {}

async def insert_new_order( order_data: Dict[str, Any]) -> None:
    """
    Inserts a new order into the database.

    Args:
        supabase_client (Client): Initialized Supabase client.
        order_data (Dict[str, Any]): The order data to insert.

    Raises:
        HTTPException: If there's an error inserting the data into Supabase.
    """
    response, insert_error = SUPABASE_CLIENT.table('orders').insert(order_data).execute()

    if insert_error and insert_error[0] == 'count' and insert_error[1] is not None:
        raise HTTPException(status_code=400, detail=f"Error inserting data into Supabase: {insert_error}")

async def process_webhook(payload: WebhookPayload) -> str:
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

    order_data = {
        "order_id": first_order_item['order_id'],
        "created_at": first_order_item['created_at'],
        "email": custom_data.get('email', ''),
        "user_name": custom_data.get('user_name', ''),
        "gender": custom_data.get('gender', ''),
        "user_image_link": custom_data.get('user_image_link', ''),
        "status": "NOT_PROCESSED",
        "product_name": first_order_item['product_name'],
        "webhook_object": payload.json(),  # Adjusted to use .json() method for serialization
        "test_mode": first_order_item['test_mode']
    }

    exists, _ = check_existing_order(SUPABASE_CLIENT, order_data['order_id'])
    if exists:
        return "Order already exists. No action taken."

    await insert_new_order(order_data)
    return "Webhook received and data processed successfully."

async def validate_and_process_request(body: bytes, signature: str, payload: WebhookPayload) -> Tuple[bool, str]:
    if not verify_signature(body, signature):
        logger.error("Invalid signature.")
        raise HTTPException(status_code=400, detail="Invalid signature.")

    # Await the async process_webhook function and store its result
    message = await process_webhook(payload)  # process_webhook is now awaited

    # Assuming process_webhook returns a string message, success flag is not needed
    # since you're raising HTTPException directly in case of failures.
    logger.info(message)
    return True, message  # Assuming the process is successful if no exception was raised
