#!/usr/bin/env python3
"""
Web caching and tracking module using Redis.
"""

import redis
import requests
from typing import Callable

r = redis.Redis()


def get_page(url: str) -> str:
    """
    Fetch the content of a URL and cache it in Redis for 10 seconds.

    Args:
        url: The URL to fetch.

    Returns:
        The HTML content of the URL.
    """
    # Check if the URL is cached
    cache_key = f"cache:{url}"
    cached_content = r.get(cache_key)

    if cached_content:
        return cached_content.decode("utf-8")

    # Fetch the URL content if not cached
    response = requests.get(url)
    html_content = response.text

    # Cache the content with a 10-second expiration
    r.setex(cache_key, 10, html_content)

    # Increment access count
    count_key = f"count:{url}"
    r.incr(count_key)

    return html_content


def get_count(url: str) -> int:
    """
    Get the access count of a URL.

    Args:
        url: The URL to check.

    Returns:
        The number of times the URL has been accessed.
    """
    count_key = f"count:{url}"
    count = r.get(count_key)
    return int(count) if count else 0
