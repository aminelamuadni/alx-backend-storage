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
        cache_key = "cached:" + url
        cached_data = redis_client.get(cache_key)
        if cached_data:
            return cached_data.decode("utf-8")

        count_key = "count:" + url
        page_content = method(url)

        redis_client.incr(count_key)
        redis_client.set(cache_key, page_content, ex=10)
        redis_client.expire(cache_key, 10)
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
    results = requests.get(url)
    return results.text


if __name__ == "__main__":
    get_page("https://httpbin.org/delay/3")
