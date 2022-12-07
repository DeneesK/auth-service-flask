import redis


class RedisExtension:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.logger.info(
            'Connecting to redis at %s:%d ...',
            app.config['REDIS_HOST'],
            app.config['REDIS_PORT'],
        )
        conn = redis.Redis(app.config['REDIS_HOST'], app.config['REDIS_PORT'])
        app.logger.info('Connected to redis')
        conn.set_response_callback('*', lambda x: x.decode() if x else x)
        app.extensions['redis'] = conn
