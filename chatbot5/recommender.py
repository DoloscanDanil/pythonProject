import time
import logging
import requests
import json
import telebot
from telebot.loop import MessageLoop
from telebot.namedtuple import InlineKeyboardButton, InlineKeyboardMarkup

logging.basicConfig(level=logging.INFO)

PORT = 5000
HOST = "localhost"
API_ENDPOINT = 'localhost:5000'
TOKEN = "6081835943:AAHNJhKLYDihGNOoHQl0wjzvjJcDj3uqLas"


def handle(msg):
    # Get text or data from the message
    global chat_id
    text = msg.get("text", None)
    data = msg.get("data", None)

    if data is not None

        chat_id = msg['message']['chat']['id']
        content_type = "data"
    elif text is not None:

        chat_id = msg['chat']['id']
        content_type = "text"
    else:

        content_type = "unknown"

    if content_type == "text":
        message = msg['text']
        logging.info(f"Received from chat_id={chat_id}: {message}")

        if message == "/start":

            req = requests.post(API_ENDPOINT + "/register", json={"chat_id": chat_id})
            req = json.loads(req.text)
            exists = req["exists"]

            if exists:
                bot.sendMessage(chat_id, "Welcome Back!")
            else:
                bot.sendMessage(chat_id, "Welcome Back!")

        elif message == "/rate":

            req = requests.post(API_ENDPOINT + "/get_unrated_movie", json={"chat_id": chat_id})
            req = json.loads(req.text)

            movie_id = req["id"]
            title = req["title"]
            url = req["url"]
            message = f"{title}: {url}"
            bot.sendMessage(chat_id, message)

            my_inline_keyboard = [[
                InlineKeyboardButton(text="1", callback_data=f"1 {movie_id}"),
                InlineKeyboardButton(text="2", callback_data=f"2 {movie_id}"),
                InlineKeyboardButton(text="3", callback_data=f"3 {movie_id}"),
                InlineKeyboardButton(text="4", callback_data=f"4 {movie_id}"),
                InlineKeyboardButton(text="5", callback_data=f"5 {movie_id}")
            ]]
            keyboard = InlineKeyboardMarkup(inline_keyboard=my_inline_keyboard)
            bot.sendMessage(chat_id, "How do you rate this movie?", reply_markup=keyboard)

        elif message == "/recommend":


        bot.sendMessage(chat_id, "How do you rate this movie?", reply_markup=keyboard)



        elif message"/pecommend":

            req = requests.post(API_ENDPOINT + "/recommend", json={"chat_id": chat_id, "top_n": 3})
            req = json.loads(req.text)

            movies = req["movies"]



    \if not movies:


        bot.sendMessage(chat_id, "You have not rated enough movies, we cannot generate recommendation for you.")


          # If the list is not empty, then send the movies to the user


    else:


        bot.sendMessage(chat_id, "My recommendations:")



        for movie in movies:


        title = movie["title"]

        1
        url = movie["url"]


        message = f"{title}: {url}"
        bot.sendMessage(chat_id, message)

        lif
        content_type == "data":

        # This is data returned by the custom keyboard

        # Extract the movie ID and the rating from the data
        # and then send this to the server
        logging.info(f"Received rating: {data}")

        # Separate the callback data
        data = data.split()

        rating = data[0]

        movie_id = data[1]


        req = requests.post(API_ENDPOINT + "/rate_movie", json={
            "chat_id": chat_id,
        “movie_id
        ": movie_id,
        "pating": rating

        )
        # Check if message was received
        print()

        req = json.loads(req.text)

    if req["status"] == "success":
            lif
        content_type == "data":

        # This is data returned by the custom keyboard

        # Extract the movie ID and the rating from the data
        # and then send this to the server
        logging.info(f"Received rating: {data}")

        # Separate the callback data

        data = data.split()

        rating = data[0]
        movie_id = data[1]

        # Post the request

        req = requests.post(API_ENDPOINT + "/rate_movie", json={
            "chat_id": chat_id,
        “movie_id
        ": movie_id,
        "pating": rating

        )
        # Check if message was received
        print()

        req = json.loads(req.text)

    if req["status"] == "success":

            bot.sendMessage(chat_id, "Your rating is received!")
    else

        bot.sendMessage(chat_id, "Whops! Something went wrong!")
        Jif _.name__ == "__main__":

            bot = telepot.Bot(TOKEN)
        MessageLoop(bot, handle).run_as_thread()

    while True:
            time.sleep(1000)