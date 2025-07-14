
"""Utilities module for nested access, JSON fetching, and memoization."""
from typing import Mapping, Any, Sequence, Callable
import requests


def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:
    """Access a nested map with a sequence of keys."""
    for key in path:
        nested_map = nested_map[key]
    return nested_map


def get_json(url: str) -> Any:
    """GET request to URL and return JSON response."""
    response = requests.get(url)
    return response.json()


def memoize(fn: Callable) -> Callable:
    """Memoization decorator."""
    attr_name = "_memoized_" + fn.__name__

    def memoized(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)

    return property(memoized)
