import json
import uuid

from dramatiq.brokers.redis import RedisBroker
from dramatiq.middleware import AsyncIO
from dramatiq.encoder import Encoder

from v1.config import settings

redis_broker = RedisBroker(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    password=settings.REDIS_PASSWORD,
)

redis_broker.add_middleware(AsyncIO())


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            return {"__uuid__": str(obj)}
        return super().default(obj)


class CustomEncoder(Encoder):
    def encode(self, data):
        return json.dumps(data, cls=UUIDEncoder).encode('utf-8')

    def decode(self, data):
        def uuid_decoder(obj):
            if "__uuid__" in obj:
                return uuid.UUID(obj["__uuid__"])
            return obj

        return json.loads(data.decode('utf-8'), object_hook=uuid_decoder)
