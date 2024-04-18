from supabase_tools.supabase_utils import SUPABASE_CLIENT
import asyncio

async def make_image_db_entry(prediction_id, user_id):
    try:
        # Create a new row in the 'images' table with the specified data
        response = SUPABASE_CLIENT.table('images').insert({
            'prediction_id': prediction_id,
            'user_id': user_id,
            'status': 'SD_IMAGE_GEN_STARTED'
        }).execute()

        new_image_id = response.data[0]['id']
        return new_image_id
    except Exception as e:
        raise Exception(f"Failed to create image db entry:  {e}")


async def get_image_id_user_id_from_prediction_id(prediction_id):
    try:
        # Create a new row in the 'images' table with the specified data
        response = (SUPABASE_CLIENT.table('images')
                    .select('id','user_id')
                    .eq('prediction_id',prediction_id)
                    .execute())

        image_id = response.data[0]['id']
        user_id = response.data[0]['user_id']

        return image_id, user_id
    except Exception as e:
        raise Exception(f"Failed to create image db entry:  {e}")

async def update_db_with_final_image_link(image_id, sd_image_url,fs_image_url, final_image_url,status):
    try:
        response = SUPABASE_CLIENT.table('images').update({
            'sd_image_url': sd_image_url,
            'image_url': final_image_url,
            'fs_image_url': fs_image_url,
            'status': status
        }).eq('id', image_id).execute()

    except Exception as e:
        raise Exception(f"Failed to update image db entry: {e}")


if __name__ == "__main__":
    image_id = asyncio.run(get_image_id_user_id_from_prediction_id("123", "https://example.com/sd_image.png"))
    asyncio.run(update_db_with_final_image_link(image_id, "https://example.com/fs_image.png"))
    print("Image db entry: ", image_id)