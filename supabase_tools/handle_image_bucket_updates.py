from supabase_tools.supabase_utils import SUPABASE_CLIENT
from supabase import StorageException
import asyncio

async def handle_supabase_upload(bucket_name, file_path, path_on_supastorage):
    with open(file_path, 'rb') as f:
        try:
            print("Try uploading the file")
            SUPABASE_CLIENT.storage.from_(bucket_name).upload(
                path=path_on_supastorage,
                file=f,
                file_options={"content-type": "image/*"}
            )
        except StorageException as e:
            if e.args[0].get('statusCode') == 400 and e.args[0].get('error') == 'Duplicate':
                print("File already exists, trying to update it")
                try:
                    SUPABASE_CLIENT.storage.from_(bucket_name).update(
                        path=path_on_supastorage,
                        file=f,
                        file_options={"content-type": "image/*"}
                    )
                except Exception as update_error:
                    print(f"Error updating file: {update_error}")
            else:
                print(f"Error uploading file: {e}")

async def get_bucket_image_url(bucket_name, supabase_image_path):
    try:
        image_url = SUPABASE_CLIENT.storage.from_(bucket_name).get_public_url(supabase_image_path)
        return image_url
    except Exception as e:
        print(f"Failed to get final image url from Supabase, Exception is: {e}")

if __name__ == '__main__':
    user_id = "123_1"
    asyncio.run(handle_supabase_upload('free-user-images',f'image_generator/user_content/image_id_{user_id}/face_swap_{user_id}/fs_{user_id}.png',f'user_{user_id}/user_image.png'))