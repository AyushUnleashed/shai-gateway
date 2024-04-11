from database.supabase_utils import SUPABASE_CLIENT
supabase = SUPABASE_CLIENT
from fastapi import  Request
from utils.logger import get_logger
from slack_bot.slackbot import SHAI_Slack_Bot
from payments.process_payments_helper import get_current_payment_mode_from_order_id
logger = get_logger(__name__)

from fastapi import APIRouter
basic_router = APIRouter()

@basic_router.get("/")
async def read_root():
    return {"message": "Welcome to the superhero ai backend gateway. This is the root endpoint."}

@basic_router.post("/update_paid_user_db")
async def update_paid_user_order_with_details(request: Request):
    payload = await request.json()
    logger.info(payload)
    order_id = payload.get("order_id")
    user_id = payload.get("user_id")
    gender = payload.get("gender")

    # Get image link from Supabase Storage
    image_path = f"{user_id}/{order_id}.png"
    curr_mode = get_current_payment_mode_from_order_id(order_id)

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
