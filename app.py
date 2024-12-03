from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import time
from helpers import file_upload


app = Flask(__name__)
CORS(app)


IMAGE_DIR = 'static/uploaded_images'
os.makedirs(IMAGE_DIR, exist_ok=True)


import routes


@app.post('/upload')
def upload():
    base64_string = request.json['image']
    image_path = os.path.join(IMAGE_DIR)
    return (image_path)
    name = f"{time.time()}.png"
    file = file_upload.upload(base64_string, image_path, name)
    return file


if __name__ == '__main__':
    app.run()
