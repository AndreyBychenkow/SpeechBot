import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from loguru import logger
import sys
from google.cloud import dialogflow_v2 as dialogflow
from google.oauth2 import service_account
from environs import Env


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

    return response.query_result


def handle_vk_message(event, vk, credentials, project_id, session_id):
    user_id = event.user_id
    text = event.text

    logger.info(f"Новое сообщение от {user_id}: {text}")

    try:
        response = detect_intent(credentials, text, project_id, session_id)

        if response.intent.is_fallback:
            logger.info(f"Бот не понял сообщение от {user_id}. Ответа нет.")
            return

        vk.messages.send(
            user_id=user_id, message=response.fulfillment_text, random_id=0
        )
        logger.info(
            f"Ответ отправлен {user_id}: {response.fulfillment_text}"
        )
    except Exception as e:
        logger.error(f"Ошибка отправки сообщения: {e}")


def main():
    env = Env()
    env.read_env()

    vk_token = env.str("VK_TOKEN")
    project_id = env.str("PROJECT_ID")
    session_id = env.int("SESSION_ID")
    google_credentials_path = env.str("GOOGLE_APPLICATION_CREDENTIALS")

    vk_session = vk_api.VkApi(token=vk_token)
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    credentials = get_credentials(google_credentials_path)

    logger.remove()
    logger.add("VK_INFO.log", format="{time} {level} {message}", level="INFO")
    logger.add(sys.stderr, format="{time} {level} {message}", level="ERROR")

    print("VK бот запущен!")

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            handle_vk_message(event, vk, credentials, project_id, session_id)


if __name__ == "__main__":
    main()
