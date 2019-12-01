from flask import Flask
from flask import request, Response, jsonify
import bcrypt
import json
import torch
import numpy as np
import cv2
import os
from flask_sqlalchemy import SQLAlchemy
from PIL import Image

from brain_tumor_detector import Net
from token_handler import TokenHandler

PATH = 'net.pth'
CLASSES = ['No Tumor', 'Tumor']
IMAGE_PATH = 'image.jpg'

net = Net()
net.load_state_dict(torch.load(PATH))
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['POSTGRES_URI']
SQLALCHEMY_TRACK_MODIFICATIONS = False
db = SQLAlchemy(app)

class User(db.Model):

    __tablename__ = 'users'

    salt = db.Column(db.String(255), primary_key=True, nullable=False)
    email = db.Column(db.String(255), primary_key=True, nullable=False)
    password = db.Column(db.String(255), primary_key=True, nullable=False)
    
    def __init__(self, email, password):
        self.email = email
        self.salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(password=password, salt=self.salt).decode('utf8')
        self.salt = self.salt.decode('utf8')

    def save(self):
        db.session.add(self)
        db.session.commit()


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
        email = data.get('email')
        password = data.get('password')

        # We query to see if the user exists, else we should create a new user
        users = db.session.query(User).filter_by(email=email).all()
        
        for user in users:
            hashed_password = bcrypt.hashpw(password=password.encode('utf8'), salt=user.salt.encode('utf8'))
            # if the hashed password exists, then we know that the user exists
            if hashed_password == password:
                return jsonify({
                    'accessToken': str(TokenHandler.get_encoded_token(user_id=user.email, secret_key=app.config.get('SECRET_KEY')), 'utf8')
                })

        # Otherwise... we have to create an account
        new_user = User(email=email, password=password.encode('utf8'))
        db.session.add(new_user)
        db.session.commit()

        new_user = db.session.query(User).filter_by(email=email).first()

        return jsonify({
            'accessToken': str(TokenHandler.get_encoded_token(user_id=new_user.email, secret_key=app.config.get('SECRET_KEY')), 'utf8')
        })

    except Exception as ex:
        return jsonify_error(str(ex), 500)

@app.route('/detect', methods=['POST'])
def detect():

    auth_token = request.headers.get('auth-token')
    if auth_token is None:
        return jsonify_error('No authentication token provided.', 401)

    decoded_token_obj = 'Pre-decoded-token'

    try:
        decoded_token_obj = TokenHandler.decode_token(token=auth_token, secret_key=app.config['SECRET_KEY'])
    except Exception as ex:
        return jsonify_error(str(ex), 404)

    sub_user_id = decoded_token_obj.get('sub')

    # Do a query for if the user_id exists in DB, then proceed. 
    user_ids = db.session.query(User.email).all()

    for user_id in user_ids:
        user_id = user_id[0]
        
        if user_id == sub_user_id:

            file = request.files.get('File', '')
            result = classify_image(file)

            return jsonify({
                'result': result
            })

    return jsonify_error('Invalid access token', 401)


def jsonify_error(reason, code):
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
    app.run(debug=True, host='0.0.0.0', port=8080)