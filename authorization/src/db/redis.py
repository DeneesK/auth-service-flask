import os

import redis

from utils.redis_callback import decode_resp

redis_connection = redis.Redis(
    os.environ.get('REDIS_HOST', 'localhost'),
    os.environ.get('REDIS_PORT', 6379),
)

redis_connection.set_response_callback('GET', decode_resp)
