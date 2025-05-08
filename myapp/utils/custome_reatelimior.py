from django_ratelimit.decorators import ratelimit
from functools import wraps

def rate_limited_view(view_func, rate='100/h', key='ip', block=True):
    return ratelimit(key=key, rate=rate, block=block)(view_func)