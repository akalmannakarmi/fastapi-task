from taskiq_redis import RedisStreamBroker
from app.core.config import settings

broker = RedisStreamBroker(
    url=settings.REDIS_URL,
)


from app.tasks.customer import *