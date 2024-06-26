#!/usr/bin/env python3
"""
Module for caching and tracking web page requests using Redis.

This module provides functionality to fetch web pages while caching their
contents and tracking the number of requests for each URL.
"""

import redis
import requests
from functools import wraps

# Initialize Redis connection
redis_client = redis.Redis()


def cache_page(method):
    """
    Decorator to cache the webpage content and track the number of accesses.

    Args:
        method (Callable): The function to fetch web page content.

    Returns:
        Callable: Decorated function that returns cached or fetched content.
    """
    @wraps(method)
    def wrapper(url):
        cache_key = f"cached:{url}"
        count_key = f"count:{url}"

        # Increment the count regardless of cache hit or miss
        redis_client.incr(count_key)

        # Attempt to get cached data
        cached_data = redis_client.get(cache_key)
        if cached_data:
            return cached_data.decode("utf-8")

        # Fetch the content as it's not in the cache
        page_content = method(url)

        # Set the cache with expiration
        redis_client.setex(cache_key, 10, page_content)  # Set with expiration

        return page_content

    return wrapper


@cache_page
def get_page(url: str) -> str:
    """
    Fetches and returns the content of a webpage.

    Args:
        url (str): The URL of the webpage to fetch.

    Returns:
        str: The content of the webpage.
    """
    response = requests.get(url)
    return response.text
