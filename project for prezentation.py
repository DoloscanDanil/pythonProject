import requests
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackContext

def get_new_movies(api_key, language="en-US"):
    url = f"https://kinopoisk.dev/documentation"
    params = {
        "api_key": api_key,
        "language": language,
        "page": 1
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        print(response.json())
        data = response.json()

        return data["results"]
    else:
        return None

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_text(
        f"Привет, {user.first_name}! Я бот, который покажет вам новые фильмы и их рейтинг."
    )

def new_movies(update: Update, context: CallbackContext) -> None:
    api_key = "3GM6W72-84PM1F5-MHDBN5K-1WCE5J4"
    new_movies = get_new_movies(api_key)
    if new_movies:
        response = "Новые фильмы в прокате:\n"
        for movie in new_movies:
            response += f"Название: {movie['title']}, Рейтинг: {movie['vote_average']}\n"
    else:
        response = "Извините, не удалось получить данные о новых фильмах."
    update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)

def main():
    # Замените "YOUR_TELEGRAM_BOT_TOKEN" на токен вашего бота
    updater = Updater("5801349035:AAE7fDg1ahKfTS2ULv1fxKsJrw4oiEY8EvU")
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("newmovies", new_movies))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
