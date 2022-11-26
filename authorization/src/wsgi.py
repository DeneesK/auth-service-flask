from gevent import monkey

monkey.patch_all()

from main import app  # noqa: F401, E402
