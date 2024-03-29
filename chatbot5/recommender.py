import time
import logging
import requests
import json
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardButton, InlineKeyboardMarkup
 
logging.basicConfig(level=logging.INFO)

PORT = 5000
HOST = "localhost"
API_ENDPOINT = "http://localhost:5000"
TOKEN = "5801349035:AAE7fDg1ahKfTS2ULv1fxKsJrw4oiEY8EvU"


def handle(msg):
	# Get text or data from the message
	global chat_id
	text = msg.get("text", None)
	data = msg.get("data", None)

	if data is not None:
		# This is a message from a custom keyboard
		chat_id = msg["message"]["chat"]["id"]
		content_type = "data"
	elif text is not None:
		# This is a text message from the user
		chat_id = msg["chat"]["id"]
		content_type = "text"
	else:
		# This is a message we don't know how to handle
		content_type = "unknown"
	
	if content_type == "text":
		message = msg["text"]
		logging.info(f"Received from chat_id={chat_id}: {message}")

		if message == "/start":
			# Check against the server to see
			# if the user is new or not
			req = requests.post(API_ENDPOINT + "/register", json={"chat_id": chat_id})
			req = json.loads(req.text)
			exists = req["exists"]

			if exists:
				bot.sendMessage(chat_id, "Welcome Back!")
			else:
				bot.sendMessage(chat_id, "Welcome!")

		elif message == "/rate":
			# Ask the server to return a random
			# movie, and ask the user to rate the
			req = requests.post(API_ENDPOINT + "/get_unrated_movie", json={"chat_id": chat_id})
			req = json.loads(req.text)
			
			# Create response and answer the bot
			movie_id = req["id"]
			title = req["title"]
			url = req["url"]
			message = f"{title}: {url}"
			bot.sendMessage(chat_id, message)

			# Create a custom keyboard to let user enter rating
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
			# Ask the server to generate a list of
			# recommended movies to the user
			req = requests.post(API_ENDPOINT + "/recommend", json={"chat_id": chat_id, "top_n": 3})
			req = json.loads(req.text)
			movies = req["movies"]

			# Check if list is empty
			if not movies:
				bot.sendMessage(chat_id, "You have not rated enough movies, we cannot generate recommendation for you.")
			
			# If the list is not empty, then send the movies to the user
			else:
				bot.sendMessage(chat_id, "My recommendations:")
				for movie in movies:
					title = movie["title"]
					url = movie["url"]
					message = f"{title}: {url}"
					bot.sendMessage(chat_id, message)
		else:
			# Some command that we don't understand
			bot.sendMessage(chat_id, "I don't understand your command.")

	elif content_type == "data":
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
			"movie_id": movie_id,
			"rating": rating
			})
		
		# Check if message was received
		print()
		req = json.loads(req.text)

		if req["status"] == "success":
			bot.sendMessage(chat_id, "Your rating is received!")
		else:
			bot.sendMessage(chat_id, "Whops! Something went wrong!")


if __name__ == "__main__":
	# Provide your bot's token
	bot = telepot.Bot(TOKEN)
	MessageLoop(bot, handle).run_as_thread()

	while True:
		time.sleep(1000)
