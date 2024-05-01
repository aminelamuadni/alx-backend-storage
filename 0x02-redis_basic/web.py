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
    """Decorator to count the number of times a URL is requested."""
    @wraps(func)
    def wrapper(url):
        redis_client.incr(f"count:{url}")
        return func(url)
    return wrapper


def cache_response(func):
    """
    Decorator to cache webpage responses in Redis with an expiration time.
    """
    @wraps(func)
    def wrapper(url):
        cached_content = redis_client.get(url)
        if cached_content:
            return cached_content

        try:
            response = func(url)
            redis_client.setex(url, 10, response.encode('utf-8'))
            return response
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    return wrapper


@count_requests
@cache_response
def get_page(url: str) -> str:
    """Fetch the HTML content of a specified URL and cache the result."""
    response = requests.get(url)
    return response.text
