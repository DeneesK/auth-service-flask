import os

import redis
from utils.r_calbacks import decode_resp

redis_connection = redis.Redis(
    os.environ.get('REDIS_HOST', 'localhost'),
    os.environ.get('REDIS_PORT', 6379),
)

redis_connection.set_response_callback('GET', decode_resp)
