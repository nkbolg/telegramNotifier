from os import remove
from os.path import isfile
from random import randint

import pytest

from settings import db_name


# def setup_module(_):
#     if isfile(db_name):
#         remove(db_name)

#
# def teardown_module(_):
#     if isfile(db_name):
#         remove(db_name)


def test_get_user():
    from db_interface import get_user
    user = get_user('')
    assert user is None


@pytest.mark.parametrize('_', range(3))
def test_add_user(_):
    from db_interface import get_user, add_user
    username = 'JohnDoe'
    user_id = randint(0, 1e10)
    add_user(username, user_id)

    user = get_user(username)
    assert username, user_id == (user.username, user.telegram_id)
