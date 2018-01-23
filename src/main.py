import logging
from time import sleep

from telegram_notifier import telegram_notify
from settings import token

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


@telegram_notify(token, 'drBaloo', 'this is a message')
def fn():
    sleep(10)


if __name__ == '__main__':
    fn()
