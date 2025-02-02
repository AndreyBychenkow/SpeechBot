import json
from google.cloud import dialogflow_v2 as dialogflow
from google.oauth2 import service_account
from environs import Env


def get_credentials(google_credentials_path):
    credentials = service_account.Credentials.from_service_account_file(
        google_credentials_path,
        scopes=["https://www.googleapis.com/auth/dialogflow"]
    )
    return credentials


def create_intent(
        project_id, display_name, training_phrases, response_text, credentials
):
    client = dialogflow.IntentsClient(credentials=credentials)

    training_phrases_parts = []
    for phrase in training_phrases:
        part = dialogflow.Intent.TrainingPhrase.Part(text=phrase)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases_parts.append(training_phrase)

    message = dialogflow.Intent.Message()
    message.text.text.append(response_text)

    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=training_phrases_parts,
        messages=[message],
    )

    parent = f"projects/{project_id}/agent"
    response = client.create_intent(parent=parent, intent=intent)
    print(f"Создан интент: {response.display_name}")


def main():
    env = Env()
    env.read_env()

    project_id = env.str("PROJECT_ID")
    google_credentials_path = env.str("GOOGLE_APPLICATION_CREDENTIALS")

    credentials = get_credentials(google_credentials_path)

    with open("intents_data.json", "r", encoding="utf-8") as file:
        intents_data = json.load(file)

    for intent_name, intent_data in intents_data.items():
        create_intent(
            project_id,
            intent_name,
            intent_data["questions"],
            intent_data["answer"],
            credentials,
        )


if __name__ == "__main__":
    main()
