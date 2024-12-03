import os
import base64
import random


def upload(base64_image, save_path, image_name):
    try:
        # Get the Base64 image from the request
        data = base64_image

        # Separate the header from the base64 data
        header, base64_data = data.split(',')

        # Decode the base64 image data
        image_data = base64.b64decode(base64_data)

        # Define the path to save the image
        image_path = os.path.join(save_path, image_name)

        # Write the image data to a file
        with open(image_path, 'wb') as file:
            file.write(image_data)

        return image_path
    except Exception as e:
        return str(e)
