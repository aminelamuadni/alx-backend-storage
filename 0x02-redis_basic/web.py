#!/usr/bin/env python3
""" Module to implement an expiring web cache and tracker.
The function fetches HTML content from URLs, tracks the number of accesses
using Redis, and caches the results with a 10-second expiration time.
"""

import requests
import redis
from functools import wraps

redis_client = redis.Redis(decode_responses=True)


def count_and_cache_requests(func):
    """Decorator to count URL requests and cache HTML content."""
    @wraps(func)
    def wrapper(url):
        count_key = f"count:{url}"
        cache_key = f"cached:{url}"

        cached_content = redis_client.get(cache_key)
        if cached_content:
            return cached_content

        html_content = func(url)

        redis_client.incr(count_key)
        redis_client.setex(cache_key, 10, html_content)

        return html_content
    return wrapper


@count_and_cache_requests
def get_page(url: str) -> str:
    """Fetch HTML content from a specified URL."""
    response = requests.get(url)
    return response.text
