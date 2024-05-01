#!/usr/bin/env python3
"""
Module to implement an expiring web cache and tracker.
Uses Redis to store cached web pages and track page request counts.
"""

import requests
import redis
from functools import wraps

redis_client = redis.Redis()


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
        # Check if the cache already contains this URL
        cached_content = redis_client.get(url)
        if cached_content:
            return cached_content.decode()

        # Fetch new data and cache it
        response = func(url)
        redis_client.setex(url, 10, response)  # Cache expires in 10 seconds
        return response
    return wrapper


@count_requests
@cache_response
def get_page(url: str) -> str:
    """Fetch the HTML content of a specified URL and cache the result."""
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    # Example usage
    url = 'http://slowwly.robertomurray.co.uk/delay/5000/url/' \
          'http://www.google.com'
    print(get_page(url))  # First time fetches and caches the content
    print(get_page(url))  # Subsequent calls within 10 seconds use cached data
