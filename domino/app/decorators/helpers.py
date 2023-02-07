import os, base64, jwt

def get_secret():
    secret_b64 = os.environ['JWT_TOKEN_SECRET']
    secret_bytes = secret_b64.encode('ascii')
    secret_b64_bytes = base64.b64decode(secret_bytes)
    secret = secret_b64_bytes.decode('ascii')
    return secret

def validate_token(auth_token, secret):
    success = True
    try:
        payload = jwt.decode(auth_token, secret)
    except jwt.ExpiredSignatureError:
        success = False
        return 'Signature expired', success
    except jwt.InvalidTokenError:
        success = False
        return 'Invalid token', success
    else:
        return payload['sub'], success
