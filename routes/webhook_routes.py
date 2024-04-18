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
from supabase_tools.handle_user_db_updates import add_user_to_supabase, delete_user_from_supabase, get_user_email_from_user_id
from models.user_model import User
from fastapi import BackgroundTasks

from supabase_tools.handle_image_tb_updates import get_image_id_user_id_from_prediction_id, \
    update_db_with_final_image_link
from supabase_tools.handle_image_bucket_updates import handle_supabase_upload, get_bucket_image_url
from image_generator.replicate_face_swap_api_call import perform_face_swap_and_save_simple
from image_generator.utils.text_box import add_text_box

from notification.slackbot import SHAI_FREE_IMAGE_SLACK_BOT
from notification.gmail_service import send_image_via_gmail
import utils.constants as constants

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
            status=Status.NOT_GENERATED.value,
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


@webhook_router.post("/webhook/replicate")
async def replicate_webhook(request: Request, background_tasks: BackgroundTasks):
    # Asynchronously get JSON data from request
    data = await request.json()
    # # Print the JSON data for debugging purposes
    # print("Received JSON data:", data)
    background_tasks.add_task(process_replicate_webhook, data)
    # Respond to the webhook
    return {"status": "received"}


async def process_replicate_webhook(data):
    # get prediction id, sd image link from the webhook payload

    prediction_id = data.get("id")
    sd_image_url = data.get("output")[0]
    user_image_link = data.get("input")["ip_image"]


    # from prediction id get the image id, user id
    image_id, user_id = await get_image_id_user_id_from_prediction_id(prediction_id)
    try:
        # call face swap with user image link and sd image link
        face_swap_image_url, fs_image_path = await perform_face_swap_and_save_simple(
            target_image_url=sd_image_url,
            source_image_url=user_image_link,
            user_id=user_id,
            image_id=image_id)

        # add text box to face swapped image
        final_image_path = await add_text_box(fs_image_path)
        # upload final image to supabase storage & get it's url
        supabase_final_image_path = f"user_{user_id}/image_{image_id}.png"
        await handle_supabase_upload(constants.FREE_IMAGE_BUCKET_NAME, final_image_path,supabase_final_image_path)
        final_image_url = await get_bucket_image_url(bucket_name=constants.FREE_IMAGE_BUCKET_NAME,
                                                     supabase_image_path=supabase_final_image_path)
        # update the db with the final image link
        await update_db_with_final_image_link(image_id,
                                              sd_image_url=sd_image_url,
                                              fs_image_url=face_swap_image_url,
                                              final_image_url=final_image_url,
                                              status=constants.SUCCESS)

        # send image link to the user via email
        user_email = await get_user_email_from_user_id(user_id)

        await SHAI_FREE_IMAGE_SLACK_BOT.send_message(
            f"Final Image generated and saved successfully for \n user: {user_id} \n user_email: {user_email} \n image_link: {final_image_url}")


        send_image_via_gmail(user_email=user_email,image_url=final_image_url)

    except Exception as e:
        # update the db with failed status
        await update_db_with_final_image_link(image_id,
                                              sd_image_url=sd_image_url,
                                              fs_image_url=None,
                                              final_image_url=None,
                                              status=constants.FAILED)

        raise HTTPException(status_code=400, detail="Error processing replicate webhook data {}".format(e))
