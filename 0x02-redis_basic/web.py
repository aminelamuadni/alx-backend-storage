#!/usr/bin/env python3
"""
web.py - A module for fetching web pages with caching and access count tracking
using Redis.
"""

import redis
import requests
from functools import wraps

redis_client = redis.Redis()


def cache_page(func):
    """
    Decorator to cache the webpage content and track the number of accesses
    using Redis.
    """
    @wraps(func)
    def wrapper(url):
        count_key = f"count:{url}"
        cache_key = f"cache:{url}"

        redis_client.incr(count_key)

        cached_data = redis_client.get(cache_key)
        if cached_data:
            return cached_data.decode('utf-8')

        page_content = func(url)
        redis_client.setex(cache_key, 10, page_content)
        return page_content

    return wrapper


@cache_page
def get_page(url: str) -> str:
    """
    Fetches the webpage content from the given URL.
    """
    response = requests.get(url)
    return response.text
