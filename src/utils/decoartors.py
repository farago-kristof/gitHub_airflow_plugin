"""This module contains utility decorators for managing function retries and enforcing singleton behavior for classes.

- `exponential_backoff`: A decorator that implements an exponential backoff strategy with optional jitter for retrying
  operations that may intermittently fail (e.g., network requests or API calls).

- `singleton`: A decorator that ensures only one instance of a class is created and returned. The same instance will be
  used for all subsequent calls, applying the Singleton design pattern to the class."""

import time
import random
from functools import wraps
import typing as t


def exponential_backoff(max_retries=3, initial_delay=1, multiplier=2, jitter=True):
    """A decorator that implements exponential backoff.
    This decorator retries a function upon failure, exponentially increasing the delay between retries.
    The delay follows the formula `delay * multiplier` for each retry. Optionally, a random "jitter" can be added
    to avoid overwhelming the target system with simultaneous retries.
    :param max_retries: Maximum number of retries before giving up.
    :param initial_delay: Initial delay between retries (in seconds).
    :param multiplier: Exponential backoff multiplier (each retry is `delay * multiplier`).
    :param jitter: Whether to add random "jitter" to the delay to avoid thundering herd problems.
    :return: The wrapped function that implements exponential backoff."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            delay = initial_delay

            while attempt < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    if attempt >= max_retries:
                        raise RuntimeError(f"Max retries reached. Last error: {e}")

                    if jitter:
                        delay_with_jitter = delay + random.uniform(0, 1)  # Adding some random jitter
                    else:
                        delay_with_jitter = delay

                    print(f"Attempt {attempt} failed, retrying in {delay_with_jitter:.2f} seconds...")
                    time.sleep(delay_with_jitter)
                    delay *= multiplier

        return wrapper

    return decorator


def singleton(cls: t.Type) -> t.Callable:
    """A decorator function that ensures a single instance of a class is created and returned on subsequent calls.
    :param cls: The class for which the singleton pattern is applied.
    :return: The single instance of the class.
    Taken from https://peps.python.org/pep-0318/#examples"""

    instances: t.Dict[t.Type, t.Type] = {}

    @wraps(cls)
    def getinstance() -> t.Type:
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return getinstance
