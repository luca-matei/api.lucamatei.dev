import dramatiq

from v1.workers.broker import redis_broker, CustomEncoder

dramatiq.set_encoder(CustomEncoder())
dramatiq.set_broker(redis_broker)

from v1.resources import tasks as resources_tasks  # noqa
