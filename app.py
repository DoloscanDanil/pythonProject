import logging
from typing import Dict
from telegram import ReplyKeyboardMarkup, Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
    CallbackQueryHandler,
)
from src.recommendation_engine.inference import predict_cuisine, get_similar_recipes
from src.recognition_engine.inference import classify_image

# Enable Logging
logging.basicConfig(
    # filename='telegramBot.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Main interactions
CHOOSING, GET_TEXT, GET_IMAGE = range(3)

# Callback data
CALLBACK1, CALLBACK2 = range(3, 5)

reply_keyboard = [
    ['Show ingredients', 'Get recipes'],
    ['Remove item', 'Done'],
]

markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

def start(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info(f"{user.first_name}: Start")

    context.user_data['chat_id'] = update.message.chat_id
    update.message.reply_text(
        "Hi! I am your recipe bot. What ingredients do you currently have?\n"
        "You can send an image or add ingredients by typing them in one or two words.",
        reply_markup=markup,
    )
    return CHOOSING


def get_basket_txt(list_ingredients):
    txt = 'Here are your current ingredients:\n'
    for ingredient in list_ingredients:
        txt += f"- {ingredient}\n"
    return txt


def received_image_information(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('infer_image.png')
    logger.info("Photo of %s: %s", user.first_name, 'infer_image.jpg')
    user_data = context.user_data

    # Infer image prediction
    ingredient = classify_image('infer_image.png')

    keyboard = [
        [
            InlineKeyboardButton(ingredient[0], callback_data=ingredient[0]),
            InlineKeyboardButton(ingredient[1], callback_data=ingredient[1]),
            InlineKeyboardButton(ingredient[2], callback_data=ingredient[2]),
        ],
        [
            InlineKeyboardButton(ingredient[3], callback_data=ingredient[3]),
            InlineKeyboardButton(ingredient[4], callback_data=ingredient[4]),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    update.message.reply_text("Choose the ingredients you have in your image!", reply_markup=reply_markup)
    return CALLBACK1


def button1(update: Update, context: CallbackContext) -> int:
    logger.info(f"button1")

    query = update.callback_query
    query.answer()

    user_data = context.user_data

    if 'ingredients_list' not in user_data:
        user_data['ingredients_list'] = [query.data]
    else:
        user_data['ingredients_list'].append(query.data)

    query.edit_message_text(text=f"Ok, you selected: {query.data}")

    txt = get_basket_txt(user_data['ingredients_list'])
    context.bot.send_message(chat_id=context.user_data['chat_id'], text=txt)

    return CHOOSING


def recipes_query(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info(f"{user.first_name}: recipes_query")

    user_data = context.user_data

    input_text = ' '.join(user_data['ingredients_list'])

    # Predict cuisine
    cuisine = predict_cuisine(input_text)

    keyboard = [
        [
            InlineKeyboardButton(cuisine[0], callback_data=cuisine[0]),
            InlineKeyboardButton(cuisine[1], callback_data=cuisine[1]),
            InlineKeyboardButton(cuisine[2], callback_data=cuisine[2]),
        ],
        [
            InlineKeyboardButton(cuisine[3], callback_data=cuisine[3]),
            InlineKeyboardButton(cuisine[4], callback_data=cuisine[4]),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    update.message.reply_text("Choose the type of cuisine you want!", reply_markup=reply_markup)

    return CALLBACK2


def button2(update: Update, context: CallbackContext) -> int:
    logger.info("button2")

    query = update.callback_query
    query.answer()

    # Get recipes
    recipes = get_similar_recipes(context.user_data['ingredients_list'], query.data)

    sep = '\n\n'
    for index, row in recipes.iterrows():
        title = 'Title: ' + row['title']
        ingredients = ''

        list_ing = row['ingredients'].replace('ADVERTISEMENT', '').strip('][').split(', ')
        for ingredient in list_ing:
            ingredients += ingredient.replace("'", "") + '\n'

        ingredients = 'Ingredients: ' + '\n' + ingredients
        instructions = 'Instruction: ' + '\n' + row['instructions']

        txt = title + sep + ingredients + sep + instructions

        context.bot.send_message(chat_id=context.user_data['chat_id'], text=txt)

    return CHOOSING


def main():
    # Initialize the Updater and pass your bot token
    # Add your bot token here:
    token = "YOUR_BOT_TOKEN"
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with entry points and states
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [
                MessageHandler(Filters.text & ~Filters.command, received_text_information),
                MessageHandler(Filters.photo & ~Filters.command, received_image_information),
            ],
            CALLBACK1: [
                CallbackQueryHandler(button1),
            ],
            CALLBACK2: [
                CallbackQueryHandler(button2),
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dp.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
