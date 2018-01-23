import logging
from time import sleep
from functools import partial

import telegram
from telegram.ext import Updater, CommandHandler
from db_interface import get_user, add_user
from notifier import base_notify

logger = logging.getLogger(__name__)


class Stopper:
    def __init__(self):
        self.stop = False


def on_start(bot: telegram.Bot, update: telegram.Update, stopper):
    bot.send_message(update.message.chat_id, 'We get the job done!')
    add_user(update.message.from_user.username, update.message.from_user.id)
    stopper.stop = True


def ask_for_registration(token):
    updater = Updater(token)
    stopper = Stopper()
    updater.dispatcher.add_handler(CommandHandler('start', partial(on_start, stopper=stopper)))
    updater.start_polling()
    link = f"https:/t.me/{updater.bot.username}"
    print(f'Start conversation to receive notifications: {link}')

    # sleep for 25 seconds or until user registered
    sleeps_count = 0
    while not stopper.stop and sleeps_count < 25:
        sleep(1)
        sleeps_count += 1
    updater.stop()


def send_telegram_notification(token, username, message, elapsed=0):
    if username.startswith('@'):
        username = username[1:]
    user = get_user(username)
    if user:
        Updater(token).bot.send_message(user.telegram_id, f"{message}\n\nTime: {elapsed}")
    else:
        logger.warning('No such user: %s', username)


def check_for_registration(token, username, _):
    user = get_user(username)
    if not user:
        ask_for_registration(token)


telegram_notify = partial(base_notify, send_telegram_notification, pre_fn=check_for_registration)
