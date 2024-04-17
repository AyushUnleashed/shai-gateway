from supabase_tools.supabase_utils import SUPABASE_CLIENT
supabase = SUPABASE_CLIENT
from fastapi import  Request, HTTPException
from utils.logger import get_logger
from slack_bot.slackbot import SHAI_Slack_Bot
from payments.process_payments_helper import get_current_payment_mode_from_order_id
logger = get_logger(__name__)
from supabase_tools.handle_user_db_updates import get_user_current_credits, reduce_user_credits

from fastapi import APIRouter
basic_router = APIRouter()
from image_generator.sd_image_gen import handle_sd_image_generation

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


# user image generation routes for free users
@basic_router.post("/generate_free_image")
async def generate_free_image(request: Request):
    payload = await request.json()
    user_id = payload.get("user_id")
    gender = payload.get("gender")
    style_id = payload.get("style_id")
    user_image_url = payload.get("user_image_url")

    current_credits = await get_user_current_credits(user_id)
    if current_credits > 0:
        await reduce_user_credits(user_id)
        await handle_sd_image_generation(user_id, style_id, gender, user_image_url)
    else:
        raise HTTPException(status_code=400, detail="Insufficient credits to generate image")

@basic_router.post("/get_user_credits")
async def get_user_credits(request: Request):
    payload = await request.json()
    user_id = payload.get("user_id")
    current_credits = await get_user_current_credits(user_id)
    return {"credits":current_credits}