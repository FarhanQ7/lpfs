from flask import Flask, request, make_response,jsonify, render_template
from werkzeug.utils import secure_filename
from config import config
import random
import string
import os
import subprocess
import shutil
from PIL import Image
from io import BytesIO
import base64
from flask import send_file
import numpy as np
import cv2
from io import BytesIO
from ini import doer
import imghdr


app = Flask(__name__, template_folder='/home/farhanq7/mysite/templates', static_url_path='/home/farhanq7/mysite/static')
app.config.from_object(config)




def deprocess_image(encoded_image):
    # Decode the base64 encoded string
    decoded_image = base64.b64decode(encoded_image)

    return decoded_image

def process_image_in_memory(image):
    # Convert the FileStorage object to a bytes object
    image_bytes = image.read()
    # Use the BytesIO object to create a file-like object in memory
    image_file = BytesIO(image_bytes)
    # Load the image from the memory buffer
    img = cv2.imdecode(np.frombuffer(image_file.getvalue(), np.uint8), -1)
    # Perform your image processing here
    # ...
    # Return the processed image
    return img

def generate_hash():
    # generate a random 7 character hash
    hash = ''.join(random.choices(string.ascii_letters + string.digits, k=7))
    return hash

def add_elements(string):
    html_data = {'new_element': f'<p class="subtitle">{string}</p>'}
    return jsonify(html_data)

@app.route('/')
def hello():
    try:
        return render_template('home.html')
    except FileNotFoundError:
        return "Image not found", 404


@app.route('/upload', methods=['POST'])
def upload_image():
    print("OOOOOOOOOOOOOOVERRRRRR HEREEEEEEEEEEEEEEEEEEEEEEEEEE")
    if 'image' in request.files:
        image = request.files['image']
        filename = str(generate_hash()) + secure_filename(image.filename)
        image_type = image.content_type
        print("PRINTING IMAGEEEEEE")
        print(image)
        # print(f"request received: {image}")
        # filename = str(generate_hash()) + secure_filename(image.filename)
        # image.save(f'/home/farhanq7/mysite/inputs/{filename}')
        # add_elements("Image uploaded")
        # add_elements("processing image")
        try:
            #return send_file(deprocess_image(process_image_in_memory(image)), mimetype=image_type, attachment_filename= f'{filename}', as_attachment=True)
            response = make_response(deprocess_image(doer(process_image_in_memory(image))))
            response.headers['Content-Disposition'] = f'attachment; filename={filename}'
            response.mimetype = image_type
            return response
        except FileNotFoundError:
            return "Image not found", 404



if __name__ == '__main__':
    app.run()
