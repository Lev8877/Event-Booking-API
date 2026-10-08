import jwt

import os 
from dotenv import load_dotenv

from datetime import datetime, timedelta, timezone

load_dotenv() 

secret_key = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")
access_token_expire_minutes = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
refresh_token_expire_days = os.getenv("REFRESH_TOKEN_EXPIRE_DAYS")


def create_access_token(user_id):
    payload = {
        'sub': str(user_id),
        'exp': datetime.now(timezone.utc) + timedelta(minutes=int(access_token_expire_minutes)),
        'type': 'access'
    }

    token = jwt.encode(payload, secret_key, algorithm=algorithm)

    return token 

def create_refresh_token(user_id, refresh_token_version):
    payload = {
        'sub': str(user_id),
        'exp': datetime.now(timezone.utc) + timedelta(days=int(refresh_token_expire_days)),
        'type': 'refresh',
        'version': int(refresh_token_version)
    }

    token = jwt.encode(payload,secret_key,algorithm=algorithm)

    return token 