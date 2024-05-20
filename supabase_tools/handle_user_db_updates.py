from fastapi import HTTPException
from utils.logger import get_logger
logger = get_logger(__name__)
from models.user_model import User
from supabase_tools.supabase_utils import SUPABASE_CLIENT
# ==========================================================================
#                             handle user db related operations
# ==========================================================================



# def delete_user_from_supabase(user_to_be_deleted_id: str):
#     try:
#         response, delete_error = SUPABASE_CLIENT.table('users').delete().eq('user_id', user_to_be_deleted_id).execute()

#         # Assuming that a successful delete operation returns a non-empty response and count > 0
#         if delete_error and delete_error[0] == 'count' and delete_error[1] is not None:
#             raise HTTPException(status_code=400, detail=f"Error deleting user:{user_to_be_deleted_id} from Supabase: {delete_error}")

#         print(f"Deleted user with ID: {user_to_be_deleted_id}")

#     except ValueError as e:
#         # Handle known errors, such as deletion failure due to the user not existing
#         print("Deletion error:", str(e))
#         raise HTTPException(status_code=404, detail=str(e))

#     except Exception as e:
#         # Handle unexpected errors
#         print("Unexpected error:", str(e))
#         raise HTTPException(status_code=500, detail="An unexpected error occurred while deleting data from Supabase")

        
def add_user_to_supabase(user: User):
    try:
        print("Checking for existing user with same email and test mode in supabase")
        existing_user_response, existing_user_error = SUPABASE_CLIENT.table('users').select('*').eq('email', user.email).eq('test_mode', user.test_mode).execute()

        # Check for error using the specified format
        if existing_user_error and existing_user_error[0] == 'count' and existing_user_error[1] is not None:
            raise HTTPException(status_code=400, detail=f"Error checking for existing user in Supabase: {existing_user_error}")

        if existing_user_response:
            print("Existing user found, updating user_id")
            update_response, update_error = SUPABASE_CLIENT.table('users').update({"user_id": user.user_id}).match({'email': user.email, 'test_mode': user.test_mode}).execute()

            # Check for error using the specified format
            if update_error and update_error[0] == 'count' and update_error[1] is not None:
                raise HTTPException(status_code=400, detail=f"Error updating existing user in Supabase: {update_error}")

            print("Existing user updated successfully:", update_response)
        else:
            print("No existing user found, adding new user to supabase")
            user_data = {
                "user_id": user.user_id,
                "email": user.email,
                "orders_array": user.orders_array,
                "gender": user.gender,
                "credits": user.credits,
                "test_mode": user.test_mode
            }
            insert_response, insert_error = SUPABASE_CLIENT.table('users').insert(user_data).execute()

            # Check for error using the specified format
            if insert_error and insert_error[0] == 'count' and insert_error[1] is not None:
                raise HTTPException(status_code=400, detail=f"Error inserting new user into Supabase: {insert_error}")

            print("New user added successfully:", insert_response)

    except ValueError as e:
        # Handle known errors (e.g., insertion failure)
        print("Error:", str(e))
        raise HTTPException(status_code=400, detail=f"Error processing user in Supabase: {str(e)}")

    except Exception as e:
        # Handle unexpected errors
        print("Unexpected error:", str(e))
        raise HTTPException(status_code=500, detail="An unexpected error occurred while processing user data in Supabase")

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


async def get_user_email_from_user_id(user_id: str) -> str:
    try:
        response = SUPABASE_CLIENT.table('users').select('email').eq('user_id', user_id).execute()
        email = str(response.data[0]['email'])
        return email
    except Exception as e:
        raise Exception(f"Failed to check user credits: {e}")