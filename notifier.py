import sys
import time
from functools import wraps

if sys.platform == "win32":
    timer = time.clock
else:
    timer = time.time


def base_notify(notify_fn, *args, pre_fn=None, post_fn=None, **kwargs):
    """
    Measure evaluation time of decorated function and finally call notify_fn
    :param pre_fn: function to be called before wrapper construction
    :param post_fn: function to be called after wrapper construction
    :param notify_fn: function to be called after the decorated
    :param args: unnamed arguments for notify_fn
    :param kwargs: named arguments for notify_fn
    """
    def decorator(doer_fn):

        if pre_fn:
            pre_fn(*args, **kwargs)

        @wraps(doer_fn)
        def wrapped(*args_in, **kwargs_in):
            t0 = timer()
            res = doer_fn(*args_in, **kwargs_in)
            t1 = timer()
            t = t1 - t0
            notify_fn(elapsed=t, *args, **kwargs)
            return res

        if post_fn:
            post_fn(*args, **kwargs)

        return wrapped
    return decorator
