import os

import telegram

BOT_TOKEN = os.environ["BOT_TOKEN"]
bot = telegram.Bot(token=BOT_TOKEN)
NOTIFICATIONS_CHANNEL_ID = ""


def send_message_to_channel(message: str):
    bot.send_message(NOTIFICATIONS_CHANNEL_ID, message)


def send_picture_with_cation(picture: bytes, message: str):
    bot.send_photo(NOTIFICATIONS_CHANNEL_ID, picture, message)
