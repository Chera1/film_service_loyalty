from typing import Optional
from aioredis import Redis


discounts: Optional[Redis] = None
user_cache: Optional[Redis] = None


async def get_redis_discounts() -> Redis:
    return discounts


async def get_redis_users() -> Redis:
    return user_cache
