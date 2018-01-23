import logging

import telegram
from telegram.ext import Updater, CommandHandler
from db_interface import get_user, add_user
from notifier import base_notify
from functools import partial

logger = logging.getLogger(__name__)


def on_start(bot: telegram.Bot, update: telegram.Update):
    bot.send_message(update.message.chat_id, 'We get the job done!')
    add_user(update.message.from_user.username, update.message.from_user.id)


def wait_for_registration(token):
    updater = Updater(token)
    updater.dispatcher.add_handler(CommandHandler('start', on_start))
    updater.start_polling()
    return updater.bot.username


def send_telegram_notification(token, username, message, elapsed=0):
    if username.startswith('@'):
        username = username[1:]
    user = get_user(username)
    if user:
        Updater(token).bot.send_message(user.telegram_id, message)
        Updater(token).bot.send_message(user.telegram_id, f"Time: {elapsed}")
    else:
        logger.warning('No such user: %s', username)


def check_for_registration(token, username, message):
    user = get_user(username)
    if not user:
        bot_name = wait_for_registration(token)
        link = f"https:/t.me/{bot_name}"
        print(f'Start conversation to receive notifications: {link}')


telegram_notify = partial(base_notify, send_telegram_notification, pre_fn=check_for_registration)
