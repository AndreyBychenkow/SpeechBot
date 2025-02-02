# 🐍 Проект «Боты для Telegram и ВКонтакте с Dialogflow»


## 📌 Описание проекта

Этот проект включает в себя два бота: Telegram-бот и ВКонтакте-бот, а также скрипт для автоматического добавления интентов в Dialogflow. Боты могут обрабатывать сообщения пользователей и взаимодействовать с API Dialogflow для получения ответов на вопросы.

[Пример VK-бота](https://vk.com/club229238007)
[Пример TG-бота](https://web.telegram.org/k/#@Speech_032_bot)

## 📌 Установка и настройка

### 🔧 Предварительные требования:

- ![Python3.10](https://i.postimg.cc/NjHrf10B/python-3-10-3-12-3-13.jpg)
- Виртуальное окружение (рекомендуется)

1. 📌 **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/AndreyBychenkow/SpeechBot
   ```
   
2. 📌 **Установите зависимости:**
   ```bash
   pip install -r requirements.txt   
   ```
   
3. 📌 **Настройка переменных окружения:**

**Создайте файл .env в корне проекта и добавьте необходимые переменные окружения:**

```bash
# Для Telegram бота:
TG_TOKEN='Ваш telegram_bot_token'
CHAT_ID='Ваш chat_id'

# Для VK бота:
VK_TOKEN='Ваш vk_group_token'

# Для Dialogflow
PROJECT_ID='Ваш dialogflow_project-id'
SESSION_ID='Ваш session_id'
GOOGLE_APPLICATION_CREDENTIALS='Путь до google_credentials.json'
```

## 🚀 Запуск ботов

### 🖋 Запуск Telegram-бота
```bash
   python TG_speech_bot.py   
   ```
   
### 🖋 Запуск VK-бота
```bash
   python VK_speech_bot.py   
   ```
   
### 📝 Добавление интентов в Dialogflow

Dialogflow — это платформа для создания разговорных интерфейсов, таких как чат-боты и голосовые помощники. Она разработана компанией Google и предоставляет инструменты для обработки естественного языка (Natural Language Processing, NLP), что позволяет разработчикам создавать системы, способные понимать и обрабатывать запросы пользователей на естественном языке.

Для автоматического добавления интентов используйте:
```bash
   python create_intents.py intents_data.json   
   ```
Где intents_data.json — JSON-файл с интентами. Скрипт загружает данные из json файла в агент DialogFlow.


## 📌 Как проверить работу ботов?

### 📝 Telegram:

* Откройте чат с ботом в Telegram.

* Отправьте сообщение.

* Бот должен ответить, если сообщение соответствует обученным интентам.

![ТГ_видео](https://github.com/user-attachments/assets/68062f0b-7293-4b3a-9f37-bd1d34d07abf)


### 📝 ВКонтакте:

* Напишите в созданное сообщество ВК.

* Если бот понимает сообщение — он ответит.

* Если не понимает — просто промолчит (чтобы не мешать техподдержке).

![ВК_видео](https://github.com/user-attachments/assets/6ca777bf-59ac-4fd6-8a9c-df971ec173d3)


## 📅 Логи и отладка

* Логи Telegram-бота сохраняются в INFO.log

* Логи VK-бота сохраняются в VK_INFO.log

* Ошибки выводятся в терминал


## ✅ Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).
