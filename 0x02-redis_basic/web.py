#!/usr/bin/env python3
"""
Web caching and tracking module using Redis.
"""

import redis
import requests
from typing import Callable, Union


# Initialize Redis connection
r = redis.Redis()


def get_page(url: str) -> str:
    """
    Fetch the content of a URL and cache it in Redis for 10 seconds.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The HTML content of the URL.
    """
    # Define cache key and count key
    cache_key = f"cache:{url}"
    count_key = f"count:{url}"

    # Check if content is cached
    cached_content = r.get(cache_key)
    if cached_content:
        return cached_content.decode("utf-8")

    # Fetch content if not cached
    response = requests.get(url)
    html_content = response.text

    # Cache content with a 10-second expiration
    r.setex(cache_key, 10, html_content)

    # Increment access count
    r.incr(count_key)

    return html_content


def get_count(url: str) -> int:
    """
    Get the access count of a URL.

    Args:
        url (str): The URL to check.

    Returns:
        int: The number of times the URL has been accessed.
    """
    count_key = f"count:{url}"
    count = r.get(count_key)
    return int(count) if count else 0


if __name__ == "__main__":
    # Example usage
    test_url = "http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.google.com"

    print("Fetching URL content...")
    print(get_page(test_url))  # First fetch (from the web)

    print("\nFetching again (should use cache)...")
    print(get_page(test_url))  # Second fetch (from cache)

    print("\nAccess count:")
    print(get_count(test_url))  # Should increment on each call

    # Wait for cache expiration (10 seconds)
    import time
    print("\nWaiting for 10 seconds...")
    time.sleep(10)

    print("\nFetching again (cache expired, fetch from web)...")
    print(get_page(test_url))

