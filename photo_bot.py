from os import environ
from time import sleep

from additional import get_random_photo
from dotenv import load_dotenv
from telegram.ext import Updater


def send_photo(updater, CHAT_ID):
    updater.bot.send_photo(
        chat_id=CHAT_ID,
        photo=get_random_photo()
        )
    print("Фотография отправлена")


def main(token, chat_id, TIME_SLEEP) -> None:
    updater = Updater(token)
    updater.start_polling()
    print("Бот запущен")
    while True:
        send_photo(updater, chat_id)
        sleep(TIME_SLEEP)


if __name__ == "__main__":
    load_dotenv()
    TOKEN_TELEGRAM = environ.get('TOKEN_TELEGRAM')
    CHAT_ID = environ.get('CHANNEL_TELEGRAM_ID')
    TIME_SLEEP = int(environ.get('TIME_SLEEP'))

    main(TOKEN_TELEGRAM, CHAT_ID, TIME_SLEEP)
