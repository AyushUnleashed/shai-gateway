from pydantic import FilePath, AnyHttpUrl
from dotenv import load_dotenv
import replicate
import asyncio
import os
import requests
load_dotenv()
REPLICATE_API_TOKEN =os.getenv('REPLICATE_API_TOKEN') # Ensure your API key is correctly set in your environment variables

from image_generator.utils.constants import USER_CONTENT_DIRECTORY_PATH


async def perform_face_swap_and_save_simple(target_image_url, source_image_url, user_id:str, image_id: str):
    

    try:
        print(f"Sourced image URL: {source_image_url}")
        if(target_image_url is None or source_image_url is None):
            raise Exception("Error | either target or source image url is None.")

        input = {
            "swap_image":source_image_url,
            "target_image": target_image_url
        }

        output = replicate.run(
            "omniedgeio/face-swap:c2d783366e8d32e6e82c40682fab6b4c23b9c6eff2692c0cf7585fc16c238cfe",
            input=input
        )

        # Assuming the API responds with a direct link to the output image in its immediate response
        output_image_url: AnyHttpUrl =output
        if not output_image_url:
            print("Output image URL not found in response.")
            return

        # Download the output image
        image_response = requests.get(output_image_url)
        image_response.raise_for_status()  # Check if the download was successful
        
        # Save the image
        face_swap_directory = f"{USER_CONTENT_DIRECTORY_PATH}/user_{user_id}"
        os.makedirs(face_swap_directory, exist_ok=True)  # Create the directory if it doesn't exist
        
        image_path = f"{face_swap_directory}/fs_{image_id}.png"
        with open(image_path, 'wb') as file:
            file.write(image_response.content)
        print(f"Face Swap image saved successfully: {image_path}")
        
        return output_image_url, image_path
        
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An unexpected error occurred: {err}")

# Ensure USER_CONTENT_DIRECTORY_PATH is defined in your environment
# Example: USER_CONTENT_DIRECTORY_PATH = "/path/to/your/directory"
# To use this function, simply call it with the appropriate arguments
import os

async def main():
    # Define the source and target image paths


    target_image_path="https://replicate.delivery/pbxt/ReQbRvR2YeoGcUrY6qI6zayY9gP1qyLwzLYn8Q9dkybTt2NSA/out-0.png"
    source_image_path= "https://upcdn.io/W142hJk/thumbnail/demo/4ktGbixgKx.jpg"
    
    # Define a user ID and count for the example
    user_id = '123'
    count = '1'
    
    # Call the face swap function with the provided images and user information
    await perform_face_swap_and_save_simple(
        target_image_url=target_image_path,
        source_image_url=source_image_path,
        image_id="123_1"
    )

# Check if the script is being run directly (not imported)
if __name__ == "__main__":
    asyncio.run(main())

