
from dotenv import load_dotenv
load_dotenv()
from database.supabase_utils import SUPABASE_CLIENT
from fastapi import  HTTPException
from utils.logger import get_logger
logger = get_logger(__name__)


def get_current_payment_mode_from_order_id(order_id: str):
    try:
        response_tuple = SUPABASE_CLIENT.table('orders').select("test_mode").eq('order_id', order_id).execute()
        print("response_tuple:", response_tuple)

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

        print("response_data:", response_data)
        test_mode = response_data[1][0].get("test_mode")
        curr_mode = "TEST" if test_mode else "PROD"

    except Exception as e:
        logger.error(f"Error determining payment platform mode: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while determining payment mode.")
    return curr_mode
