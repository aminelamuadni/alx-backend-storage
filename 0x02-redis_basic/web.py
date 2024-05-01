#!/usr/bin/env python3
""" Module to implement an expiring web cache and tracker. """

import redis
import requests

redis_client = redis.Redis()


def get_page(url: str) -> str:
    """
    Fetches the HTML content of a specified URL and caches it. It also tracks
    how many times the URL has been accessed.

    Args:
    url (str): URL to fetch the HTML content from.

    Returns:
    str: HTML content of the page.
    """
    count_key = f"count:{url}"
    redis_client.incr(count_key)

    cache_key = f"cached:{url}"
    cached_content = redis_client.get(cache_key)
    if cached_content:
        return cached_content.decode('utf-8')

    response = requests.get(url)
    html_content = response.text

    redis_client.setex(cache_key, 10, html_content)

    return html_content


if __name__ == "__main__":
    test_url = 'http://slowwly.robertomurray.co.uk/delay/5000/url/' \
               'http://www.google.com'
    print(get_page(test_url))
    print(get_page(test_url))
