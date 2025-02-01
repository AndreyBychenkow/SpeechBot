from environs import Env
import telebot

from loguru import logger
import sys


def echo(message):
    chat_id = message.chat.id
    text = message.text

    logger.info(f"Получено сообщение от пользователя с ID: {chat_id}")
    logger.info(f"Сообщение: {text}")

    try:
        bot.send_message(chat_id, text)
        logger.info(
            f"Отправлено сообщение обратно пользователю: {chat_id}: {text}"
        )
    except Exception as e:
        logger.error(f"Ошибка отправки сообщения пользователю: {chat_id}: {e}")


def main():
    logger.remove()
    logger.add("INFO.log", format="{time} {level} {message}", level="INFO")
    logger.add(sys.stderr, format="{time} {level} {message}", level="ERROR")

    try:
        bot.message_handler(func=lambda message: True)(echo)
        bot.send_message(CHAT_ID, "✈️ Бот успешно запущен!")
        print("Бот успешно запущен!")
        bot.polling()
    except Exception as e:
        logger.critical(f"Фатальная ошибка при запуске бота: {e}")


if __name__ == "__main__":
    env = Env()
    env.read_env()

    CHAT_ID = env.int("chat_id")
    TG_TOKEN = env.str("tg_token")
    bot = telebot.TeleBot(TG_TOKEN)
    main()

