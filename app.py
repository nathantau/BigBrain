from flask import Flask
from flask import request, Response, jsonify
import json
import torch
import numpy as np
import cv2
import os
from PIL import Image

from brain_tumor_detector import Net
from token_handler import TokenHandler

PATH = 'net.pth'
CLASSES = ['No Tumor', 'Tumor']
IMAGE_PATH = 'image.jpg'

net = Net()
net.load_state_dict(torch.load(PATH))
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

MOCK_DB = {
    'subs': ['nathan']
}

@app.route('/')
def home():
    return jsonify({
        'message': 'This is home!'
    })

@app.route('/authorization', methods=['POST'])
def authorize():
    try: 
        data = request.json

        username = data.get('username')
        password = data.get('password') # Unused right now

        return jsonify({
            'accessToken': str(TokenHandler.get_encoded_token(user_id=username, secret_key=app.config.get('SECRET_KEY')))
        })

    except Exception as ex:
        return jsonify(ex)

@app.route('/detect', methods=['POST'])
def detect():

    auth_token = request.headers.get('auth-token')
    if auth_token is None:
        return get_error('No authentication token provided.', 401)

    decoded_token_obj = 'Pre-decoded-token'

    try:
        decoded_token_obj = TokenHandler.decode_token(token=auth_token, secret_key=app.config['SECRET_KEY'])
    except Exception as ex:
        return get_error(str(ex), 401)

    user_id = decoded_token_obj.get('sub')

    # Do a query for if the user_id exists in DB, then proceed. 
    # For now, we will mock a daetabase with a dictionary
    if user_id not in MOCK_DB['subs']:
        return get_error('Invalid access token', 401)

    file = request.files.get('File', '')
    result = classify_image(file)

    return jsonify({
        'result': result
    })


def get_error(reason, code):
    return jsonify({'Reason for failure': reason}), code

def classify_image(file):
    file.save(IMAGE_PATH)

    image = cv2.imread(IMAGE_PATH, 0)
    image = cv2.resize(image, (128, 128))

    # preprocess image and make it into the dimensions the network is accepting
    image = torch.from_numpy(image)
    image = image.view(1, 1, 128, 128).float()

    output = net(image)
    index = torch.argmax(output)

    return CLASSES[index]

if __name__ == '__main__':
    app.run(debug=True)