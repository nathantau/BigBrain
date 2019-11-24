import datetime
import jwt

class TokenHandler():
    '''
    This is a helper class with the sole purpose of handling the authorization for this API
    '''

    @staticmethod
    def get_encoded_token(user_id, secret_key):

        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(0, seconds=60),
            'iat': datetime.datetime.utcnow() + datetime.timedelta(0, seconds = 0),
            'sub': user_id
        }

        return jwt.encode(
            payload,
            secret_key,
            algorithm='HS256'
        )

    @staticmethod
    def decode_token(token, secret_key):
        return jwt.decode(token, secret_key)

