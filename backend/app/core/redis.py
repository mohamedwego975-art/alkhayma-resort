import redis.asyncio as redis
from functools import wraps
import json
import hashlib
from app.core.config import settings

# Redis async client
redis_client = redis.from_url(settings.redis_url, decode_responses=True)

# Dependency to get redis client
async def get_redis():
    return redis_client

# Cache decorator
def cache(expire: int = 300, key_prefix: str = "cache"):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key
            key_data = f"{func.__name__}:{args}:{kwargs}"
            key_hash = hashlib.md5(key_data.encode()).hexdigest()
            cache_key = f"{key_prefix}:{key_hash}"
            
            # Try to get from cache
            cached = await redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            await redis_client.setex(cache_key, expire, json.dumps(result, default=str))
            return result
        return wrapper
    return decorator

# Invalidate cache pattern
async def invalidate_pattern(pattern: str):
    keys = await redis_client.keys(pattern)
    if keys:
        await redis_client.delete(*keys)
