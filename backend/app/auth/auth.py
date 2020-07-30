import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen
from app.auth import bp

AUTH0_DOMAIN = 'dev-c.eu.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'casting-agency'

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Get Token from Auth Header
def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    # is there an Auth Header?
    auth_header = request.headers.get('Authorization', None)
    if not auth_header:
        raise AuthError({
            'success': False,
            'status': 401,
            'description': 'Authorization header is expected.'
        }, 401)

    header_parts = auth_header.split(' ')

    # check for right format: 2 parts separated by space, first is *bearer*
    if len(header_parts) != 2:
        raise AuthError({
            'success': False,
            'status': 401,
            'description': 'Authorization header is not in right format.'
        }, 401)

    elif header_parts[0].lower() != 'bearer':
        raise AuthError({
            'success': False,
            'status': 401,
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    token = header_parts[1]
    return token



# Check if specific permission is granted
def check_permissions(payload, permission = ''):
    "Check if user has permission to perform requested action"
    # print(payload)
    "is there permission in JWT?"
    if 'permissions' not in payload:
        raise AuthError({
            'success': False,
            'status': 400,
            'description': 'Permissions not included in JWT'
            }, 400)

    "is specific permission granted?"
    if permission not in payload['permissions']:
        raise AuthError({
            'success': False,
            'status': 403,
            'description': "No Permission"
            }, 403)

    return True



# verify if token is valid
'''
    !!NOTE urlopen has a common certificate error described here: https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''
def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'success': False,
            'status': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'success': False,
                'status': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'success': False,
                'status': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'success': False,
                'status': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'success': False,
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)



# decorator for authentication process
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(payload, permission)
            return f(*args, **kwargs)

        return wrapper
    return requires_auth_decorator