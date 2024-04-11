from fastapi import Request, HTTPException

from utils.logger import get_logger

from payments.process_payments_helper import get_current_payment_mode_from_order_id
logger = get_logger(__name__)
import razorpay
import os
from urllib.parse import urlparse
# ==========================================================================
#                             setup the payments
# ==========================================================================

from fastapi import APIRouter
from pydantic import BaseModel
payments_router = APIRouter()


from payments.lemon_squeezy_helpers import generate_lemonsqueezy_payment_link
from payments.razory_pay_helpers import create_razor_pay_order
from utils.config import settings
@payments_router.post("/payments/generate_payment_link")
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
        
        settings.lemonsqueezy_frontend_redirect_url = f"{origin}/my_orders"
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


## Razorpay routes
@payments_router.get("/payments/razorpay/get_razorpay_key")
async def get_razorpay_key():
    return {"razorpay_key": settings.RAZOR_PAY_ID}


class RazorPayValidationRequest(BaseModel):
    razorpay_payment_id: str
    razorpay_order_id: str
    razorpay_signature: str

@payments_router.post("/payments/razorpay/validate")
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




if __name__ == "__main__":
   mode = get_current_payment_mode_from_order_id("2312270")
   print("mode:", mode)