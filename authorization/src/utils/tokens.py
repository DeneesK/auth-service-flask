from datetime import datetime, timedelta

import jwt
from models.user import UserModel
from schemas import UserData


def _gen_access(user: UserModel, secret_key: str, ttl: int) -> str:
    time_now = datetime.now()
    payload = UserData().dump(user)
    payload.update(
        {
            'exp': time_now + timedelta(seconds=ttl),
            'iat': time_now,
        }
    )
    return jwt.encode(
        payload,
        secret_key,
        algorithm='HS256',
    )


def _gen_refresh(user: UserModel, secret_key: str, ttl: int) -> str:
    return _gen_access(user, secret_key, ttl)


def gen_tokens(
    user: UserModel, secret_key: str, access_ttl: int, refresh_ttl: int
) -> dict:
    return {
        'access': _gen_access(user, secret_key, access_ttl),
        'refresh': _gen_refresh(user, secret_key, refresh_ttl),
    }
