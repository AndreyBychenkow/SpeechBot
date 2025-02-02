from environs import Env
import telebot
from loguru import logger
import sys
from google.cloud import dialogflow_v2 as dialogflow
from google.oauth2 import service_account


def get_credentials(google_credentials_path):
    credentials = service_account.Credentials.from_service_account_file(
        google_credentials_path,
        scopes=["https://www.googleapis.com/auth/dialogflow"]
    )
    return credentials


def detect_intent(credentials, text, project_id, session_id):
    session_client = dialogflow.SessionsClient(credentials=credentials)
    session = session_client.session_path(project_id, str(session_id))

    text_input = dialogflow.TextInput(text=text, language_code="ru")
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session, query_input=query_input)
    return response.query_result.fulfillment_text


def handle_message(message, bot, credentials, project_id, session_id):
    chat_id = message.chat.id
    text = message.text

    logger.info(f"Получено сообщение от пользователя с ID: {chat_id}")
    logger.info(f"Сообщение: {text}")

    try:
        response_text = detect_intent(
            credentials, text, project_id, session_id)
        bot.send_message(chat_id, response_text)
        logger.info(
            f"Отправлено сообщение обратно: {chat_id}: {response_text}"
        )
    except Exception as e:
        logger.error(f"Ошибка отправки сообщения пользователю: {chat_id}: {e}")


def main():
    env = Env()
    env.read_env()

    project_id = env.str("PROJECT_ID")
    session_id = env.int("SESSION_ID")
    google_credentials_path = env.str("GOOGLE_APPLICATION_CREDENTIALS")
    chat_id = env.int("CHAT_ID")
    tg_token = env.str("TG_TOKEN")

    bot = telebot.TeleBot(tg_token)
    credentials = get_credentials(google_credentials_path)

    logger.remove()
    logger.add("INFO.log", format="{time} {level} {message}", level="INFO")
    logger.add(sys.stderr, format="{time} {level} {message}", level="ERROR")

    try:
        bot.message_handler(func=lambda message: True)(
            lambda message: handle_message(
                message, bot, credentials, project_id, session_id
            )
        )
        bot.send_message(chat_id, "Я готов! Задавайте вопросы!")
        print("Бот успешно запущен!")
        bot.polling()
    except Exception as e:
        logger.critical(f"Критическая ошибка при запуске бота: {e}")


if __name__ == "__main__":
    main()
