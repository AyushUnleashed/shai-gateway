from supabase_tools.supabase_utils import SUPABASE_CLIENT, Client
from fastapi import HTTPException
from typing import Dict, Any

from typing import Tuple
from utils.logger import get_logger

logger = get_logger(__name__)


# ==========================================================================
#                             handle orders db related operations
# ==========================================================================



def check_existing_order(supabase_client: Client, order_id: str) -> Tuple[bool, Dict[str, Any]]:
    """
    Check if an order already exists in the supabase_tools.

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
    Inserts a new order into the supabase_tools.

    Args:
        supabase_client (Client): Initialized Supabase client.
        order_data (Dict[str, Any]): The order data to insert.

    Raises:
        HTTPException: If there's an error inserting the data into Supabase.
    """
    response, insert_error = SUPABASE_CLIENT.table('orders').insert(order_data).execute()

    if insert_error and insert_error[0] == 'count' and insert_error[1] is not None:
        raise HTTPException(status_code=400, detail=f"Error inserting data into Supabase: {insert_error}")
