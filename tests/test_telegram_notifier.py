from telegram_notifier import *


def test_stopper():
    s = Stopper()
    assert s.stop is False
    s.stop = True
    assert s.stop
