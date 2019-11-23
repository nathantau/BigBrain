import datetime
import jwt

class TokenHandler():
    '''
    This is a helper class with the sole purpose of handling the authorization for this API
    '''

    @staticmethod
    def get_encoded_token(user_id, secret_key):

        payload = {
            'expiry_date': str(datetime.datetime.utcnow() + datetime.timedelta(0, seconds=60)),
            'generated_date': str(datetime.datetime.utcnow()),
            'subject': user_id
        }

        return jwt.encode(
            payload,
            secret_key,
            algorithm='HS256'
        )

print(TokenHandler.get_encoded_token('user', 'secret'))
