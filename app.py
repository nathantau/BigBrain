from flask import Flask
from flask import request, Response, jsonify
import json
import torch
import numpy as np
import cv2
from PIL import Image

from brain_tumor_detector import Net

PATH = 'net.pth'
CLASSES = ['No Tumor', 'Tumor']
IMAGE_PATH = 'image.jpg'

net = Net()
net.load_state_dict(torch.load(PATH))
app = Flask(__name__)


@app.route('/')
def home():
    return jsonify({
        'message': 'this is home!'
    })

@app.route('/authorization', methods=['POST'])
def authorize():

    data = request.json

    username = data.get('username')
    password = data.get('password')

    

    # we should get the username and password here
    return data



@app.route('/detect', methods=['POST'])
def detect():

    file = request.files.get('File', '')
    file.save(IMAGE_PATH)

    image = cv2.imread(IMAGE_PATH, 0)
    image = cv2.resize(image, (128, 128))

    print('type', type(image))
    print('size', image.shape)

    # preprocess image and make it into the dimensions the network is accepting
    image = torch.from_numpy(image)
    image = image.view(1, 1, 128, 128).float()

    output = net(image)
    index = torch.argmax(output)

    return jsonify({
        'result': CLASSES[index]
    })















if __name__ == '__main__':
    app.run(debug=True)