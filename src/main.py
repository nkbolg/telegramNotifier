import logging
import argparse
from time import sleep

from telegram_notifier import telegram_notify
from settings import token

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--username', dest='uname')
    parser.add_argument('--message', dest='msg')
    args = parser.parse_args()
    
    @telegram_notify(token, args.uname, args.msg)
    def fn():
        sleep(10)

    fn()

