from fastapi import HTTPException
from utils.logger import get_logger
logger = get_logger(__name__)
from models.user_model import User
from supabase_tools.supabase_utils import SUPABASE_CLIENT
# ==========================================================================
#                             handle user db related operations
# ==========================================================================



def delete_user_from_supabase(user_to_be_deleted_id: str):
    try:
        response, delete_error = SUPABASE_CLIENT.table('users').delete().eq('user_id', user_to_be_deleted_id).execute()

        # Assuming that a successful delete operation returns a non-empty response and count > 0
        if delete_error and delete_error[0] == 'count' and delete_error[1] is not None:
            raise HTTPException(status_code=400, detail=f"Error deleting user:{user_to_be_deleted_id} from Supabase: {delete_error}")

        print(f"Deleted user with ID: {user_to_be_deleted_id}")

    except ValueError as e:
        # Handle known errors, such as deletion failure due to the user not existing
        print("Deletion error:", str(e))
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        # Handle unexpected errors
        print("Unexpected error:", str(e))
        raise HTTPException(status_code=500, detail="An unexpected error occurred while deleting data from Supabase")
def add_user_to_supabase(user: User):
    try:
        print("Adding user to supabase")
        user_data = {
            "user_id": user.user_id,
            "email": user.email,
            "orders_array": user.orders_array,
            "gender": user.gender,
            "credits": user.credits,
            "test_mode":user.test_mode
        }
        response, insert_error = SUPABASE_CLIENT.table('users').upsert(user_data).execute()
        print("response: {}".format(response))
        print("insert_error: {}".format(insert_error))
        # Check if the response indicates success, assuming a successful insert returns a specific status or key
        if insert_error and insert_error[0] == 'count' and insert_error[1] is not None:
            raise HTTPException(status_code=400, detail=f"Error inserting data into Supabase: {insert_error}")

        print("User added successfully:", response)

    except ValueError as e:
        # Handle known errors (e.g., insertion failure)
        print("Insertion error:", str(e))
        raise HTTPException(status_code=400, detail=f"Error inserting data into Supabase: {str(e)}")

    except Exception as e:
        # Handle unexpected errors
        print("Unexpected error:", str(e))
        raise HTTPException(status_code=500, detail="An unexpected error occurred while inserting data into Supabase")


def get_user_email_from_user_id():
    pass

## Credits section

async def get_user_current_credits(user_id) -> int:
    try:
        response = SUPABASE_CLIENT.table('users').select('credits').eq('user_id', user_id).execute()
        credits = int(response.data[0]['credits'])
        return credits
    except Exception as e:
        raise Exception(f"Failed to check user credits: {e}")

async def reduce_user_credits(user_id):
    try:
        current_credits = await get_user_current_credits(user_id)

        if current_credits > 0:
            new_credits = current_credits - 1
            response = SUPABASE_CLIENT.table('users').update({'credits': new_credits}).eq('user_id', user_id).execute()
        else:
            raise Exception("Can't reduce credits below 0.")
    except Exception as e:
        raise Exception(f"Failed to reduce image generation credits: {e}")