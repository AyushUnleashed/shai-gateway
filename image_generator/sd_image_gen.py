from dotenv import load_dotenv
import os

load_dotenv()
import asyncio
import httpx
from image_generator.utils.prompts import MALE_SUPERHERO_PROMPTS, FEMALE_SUPERHERO_PROMPTS
from image_generator.utils.constants import PROMPT_SUFFIX
from supabase_tools.handle_image_tb_updates import make_image_db_entry


def get_prompt(gender, style_id):
    try:
        if gender == "MALE":
            prompt = MALE_SUPERHERO_PROMPTS[int(style_id)]
        elif gender == "FEMALE":
            prompt = FEMALE_SUPERHERO_PROMPTS[int(style_id)]  # Fixed to use FEMALE_SUPERHERO_PROMPTS for female gender
        else:
            raise ValueError(f"Invalid gender: {gender}")
    except Exception as e:
        raise ValueError(f"Error in getting prompt: {e}")
    return prompt

async def handle_sd_image_generation(user_id, style_id, gender, user_image_link):
    prompt = f"{get_prompt(gender, style_id)}, {PROMPT_SUFFIX}"
    prediction_id = await call_sd_api_replicate(prompt, user_image_link, user_image_link)
    image_id = await make_image_db_entry(prediction_id=prediction_id, user_id=user_id)
    return prediction_id, image_id


async def call_sd_api_replicate(prompt, user_image_link, pose_image_link):
    # httpx
    print(os.getenv('REPLICATE_API_TOKEN'))
    sd_replicate_backend_url = "https://api.replicate.com/v1/predictions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Token {os.getenv('REPLICATE_API_TOKEN')}"
    }
    payload = {
        "version": "1dddf6ccc0961b68e4660a1d2b159e05a2975931ce89fc0c6cef255c95114ffd",
        "input": {
            "ip_image": user_image_link,
            "control_net_image": pose_image_link,
            "width": 768,
            "height": 768,
            "prompt": prompt,
            "guidance_scale": 7.5,
            "num_inference_steps": 40,
            "controlnet_conditioning_scale": 0
        },
        "webhook": "https://brave-happily-wahoo.ngrok-free.app/webhook/replicate",
        "webhook_events_filter": ["completed"]
    }

    # Send the POST request to start the prediction
    async with httpx.AsyncClient() as client:
        response = await client.post(sd_replicate_backend_url, headers=headers, json=payload)
        print(response.json())
        # Handle the response
        if response.status_code == 201:
            data = response.json()
            print(data)
            print(f"Prediction started successfully, ID: {data['id']}")
            return data['id']  # Return the ID of the prediction task
        else:
            print("Failed to start prediction")
            return None


if __name__ == "__main__":
    user_image_link = "https://mvlmexldvleywcfmvzwt.supabase.co/storage/v1/object/public/paid-user-images/user_2dn0xb5utBAiH2r7f4Pm7929L7f/order_NohiIjMu5GJKHT.png"
    prediction_id, image_id = asyncio.run(handle_sd_image_generation("user_123",9,"MALE", user_image_link))
    print("Prediction id: ", prediction_id)
    print("Image id:", image_id)
