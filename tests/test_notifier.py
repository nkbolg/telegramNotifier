from functools import partial

from src.notifier import base_notify


class NotificationsAggregator:
    def __init__(self):
        self.pre_called = False
        self.notify_called = False
        self.post_called = False

        self.received_args_pre = None
        self.received_args_notify = None
        self.received_args_post = None

    def pre(self, *args, **kwargs):
        self.received_args_pre = (args, kwargs)
        self.pre_called = True

    def notify(self, *args, **kwargs):
        self.received_args_notify = (args, kwargs)
        self.notify_called = True

    def post(self, *args, **kwargs):
        self.received_args_post = (args, kwargs)
        self.post_called = True


def test_base_notifier():
    aggr = NotificationsAggregator()
    test_notify = partial(base_notify, aggr.notify, pre_fn=aggr.pre, post_fn=aggr.post)
    args_out = (1,2,3)
    kwargs_out = {'kw1':'one', 'kw2':'two', 'kw3':'three'}
    args_in = (4, 5, 6)
    kwargs_in = {'kw4': 'four', 'kw5': 'five', 'kw6': 'six'}

    @test_notify(*args_out, **kwargs_out)
    def decorated_fn(*args, **kwargs):
        assert args == args_in
        assert kwargs == kwargs_in

    assert aggr.pre_called
    assert aggr.received_args_pre == (args_out, kwargs_out)

    assert aggr.notify_called
    assert aggr.received_args_notify == (args_out, kwargs_out)

    assert aggr.post_called
    assert aggr.received_args_post == (args_out, kwargs_out)
