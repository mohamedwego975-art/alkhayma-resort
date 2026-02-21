from redis.asyncio import Redis
from typing import AsyncGenerator, Callable, Any
from functools import wraps
import json
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

redis_client: Redis = Redis.from_url(REDIS_URL, decode_responses=True)


async def get_redis() -> AsyncGenerator[Redis, None]:
    yield redis_client


async def store_refresh_token(user_id: int, refresh_token: str, expire_days: int = 30):
    """Store refresh token in Redis with TTL"""
    key = f"refresh_token:{refresh_token}"
    await redis_client.setex(key, expire_days * 24 * 60 * 60, str(user_id))


async def get_user_from_refresh_token(refresh_token: str) -> int | None:
    """Get user ID from refresh token"""
    key = f"refresh_token:{refresh_token}"
    user_id = await redis_client.get(key)
    return int(user_id) if user_id else None


async def blacklist_refresh_token(refresh_token: str):
    """Blacklist a refresh token"""
    blacklist_key = f"blacklist:{refresh_token}"
    await redis_client.setex(blacklist_key, 30 * 24 * 60 * 60, "1")
    
    # Delete from valid tokens
    token_key = f"refresh_token:{refresh_token}"
    await redis_client.delete(token_key)


async def is_token_blacklisted(refresh_token: str) -> bool:
    """Check if token is blacklisted"""
    blacklist_key = f"blacklist:{refresh_token}"
    return await redis_client.exists(blacklist_key) > 0


def cache(expire: int = 300, key_prefix: str = "cache"):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            cache_key = f"{key_prefix}:{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            cached = await redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
            
            result = await func(*args, **kwargs)
            await redis_client.setex(cache_key, expire, json.dumps(result))
            return result
        
        return wrapper
    return decorator


async def invalidate_pattern(pattern: str) -> int:
    keys = []
    async for key in redis_client.scan_iter(match=pattern):
        keys.append(key)
    
    if keys:
        return await redis_client.delete(*keys)
    return 0
