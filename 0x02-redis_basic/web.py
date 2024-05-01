#!/usr/bin/env python3
"""
Module to implement an expiring web cache and tracker.
Uses Redis to store cached web pages and track page request counts.
"""

import requests
import redis
from functools import wraps

redis_client = redis.Redis(decode_responses=True)


def count_requests(func):
    """
    Decorator to count the number of times a URL is requested and cache its
    content.
    """
    @wraps(func)
    def wrapper(url):
        key = f"count:{url}"
        redis_client.incr(key)
        cached_content = redis_client.get(f"cached:{url}")
        if cached_content:
            return cached_content

        response = func(url)
        redis_client.setex(f"cached:{url}", 10, response)
        return response
    return wrapper


@count_requests
def get_page(url: str) -> str:
    """Fetch the HTML content of a specified URL and return it."""
    response = requests.get(url)
    return response.text
