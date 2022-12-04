from datetime import datetime, timedelta

import jwt
from models.user import UserModel
from schemas.user import user_data

#  Would it be better to use an environment variable?
SECRET_KEY = 'MQ1JbT6uwNzyb2pdFa6tI5No4cope2cT48DR3rhp2V7elM6StWG1qsMVjNupTTP'

def _gen_access(user: UserModel, time_out: int = 600) -> (str, int):
    time_now = datetime.now()
    payload = user_data.dump(user)
    payload.update(
        {
            'exp': time_now + timedelta(seconds=time_out),
            'iat': time_now,
        }
    )
    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm='HS256',
    )


def _gen_refresh(user: UserModel):
    return _gen_access(user=user, time_out=604800)


def gen_tokens(user: UserModel):
    return {'access': _gen_access(user), 'refresh': _gen_refresh(user)}
