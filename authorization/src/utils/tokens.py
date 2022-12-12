from datetime import datetime, timedelta

import jwt
from models.user import UserModel
from schemas import UserData


def _gen_access(user: UserModel, secret_key: str, time_out: int = 600) -> str:
    time_now = datetime.now()
    payload = UserData().dump(user)
    payload.update(
        {
            'exp': time_now + timedelta(seconds=time_out),
            'iat': time_now,
        }
    )
    return jwt.encode(
        payload,
        secret_key,
        algorithm='HS256',
    )


def _gen_refresh(user: UserModel, secret_key: str) -> str:
    return _gen_access(user, secret_key, time_out=604800)


def gen_tokens(user: UserModel, secret_key: str) -> dict:
    return {
        'access': _gen_access(user, secret_key),
        'refresh': _gen_refresh(user, secret_key),
    }
