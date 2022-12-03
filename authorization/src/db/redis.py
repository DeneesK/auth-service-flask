import os

import redis

redis_connection = redis.Redis(
    os.environ.get('REDIS_HOST', 'localhost'),
    os.environ.get('REDIS_PORT', 6379),
)
