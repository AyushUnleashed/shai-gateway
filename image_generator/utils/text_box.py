from PIL import Image, ImageDraw, ImageFont
import os
import asyncio

async def add_text_box(image_path, text="SuperHeroAI.pro", output_path=None):
    try:
        # Open the image
        img = Image.open(image_path)

        # Create a drawing object
        draw = ImageDraw.Draw(img)

        # Set the font size and load a font
        font_size = 24  # Adjust the font size as needed
        # specified font size
        font = ImageFont.truetype(r'image_generator/assets/font/Montserrat/Montserrat-Regular.ttf', font_size)

        # Calculate the position for the text box in the bottom right corner
        box_width = len(text) * font_size * 0.7
        box_height = font_size * 2
        box_position = (10, img.size[1] - box_height - 10)

        # Draw a black box
        draw.rectangle([box_position, (box_position[0] + box_width, box_position[1] + box_height)], fill="black")

        bbox = draw.textbbox((box_position[0], box_position[1]), text, font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_position = (
            box_position[0] + (box_width - text_width) // 2,
            box_position[1] + (box_height - text_height) // 2
        )

        # Add white text inside the black box
        draw.text(text_position, text, fill="white", font=font)

        # Save the modified image
        if output_path is None:
            #output_path = os.path.splitext(image_path)[0] + "_marked.png"
            output_path = image_path
        img.save(output_path)

        print(f"Image with centered text box in the bottom right saved at: {output_path}")
        return output_path

    except Exception as e:
        raise Exception(f"Text addition failed with error: {e}")


def main():
    # Provide the path to your image and the text you want to add
    image_path = "image_generator/user_content/user_user_123/fs_f79dfbad-17ae-46a5-85e8-544fb8506264.png"
    text = "SuperHeroAI.pro"

    # Call the function to add a text box to the image
    asyncio.run(add_text_box(image_path, text))

if __name__ == "__main__":
    main()