from functools import wraps
from time import perf_counter


def timer(func):
    """Print the function runtime"""
    @wraps(func)
    def wrap_timer(*args, **kwargs):
        t0 = perf_counter()
        returned = func(*args, **kwargs)
        t1 = perf_counter()
        print(f"[Time: {t1-t0:.6f} s]")
        return returned
    return wrap_timer
