import requests
import json
import telebot
from telebot import TeleBot

TOKEN = '5801349035:AAE7fDg1ahKfTS2ULv1fxKsJrw4oiEY8EvU'

bot: TeleBot = telebot.TeleBot(TOKEN)

Mydict = {
    '/eur': 'EUR',
    '/usd': 'USD',
    '/ron': 'RON',
    '/mdl': 'mdl',
}


class ConvertionException(Exception):
    pass


# First commands
@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'For new operation type : /conversion'
    bot.reply_to(message, text)



@bot.message_handler(commands=['conversion'])
def operations(message: telebot.types.Message):
    text = 'Actual currency:\n  /pln_to_usd \n  /pln_to_ron \n  /pln_to_eur \n /pln_to_mdl \n  /usd_to_pln \n' \
            '/ron_to_pln \n  /eur_to_pln'
    r1 = requests.get('http://api.nbp.pl/api/exchangerates/rates/a/eur/')
    texts1 = json.loads(r1.content)
    rates1 = texts1.get('rates')
    eur1 = str(rates1[0].get('mid'))

    r2 = requests.get('http://api.nbp.pl/api/exchangerates/rates/a/usd/')
    texts2 = json.loads(r2.content)
    rates2 = texts2.get('rates')
    usd1 = str(rates2[0].get('mid'))

    r3 = requests.get('http://api.nbp.pl/api/exchangerates/rates/a/ron/')
    texts3 = json.loads(r3.content)
    rates3 = texts3.get('rates')
    ron1 = str(rates3[0].get('mid'))

    r4 = requests.get('https://api.nbp.pl/api/exchangerates/rates/b/mdl/')
    texts4 = json.loads(r4.content)
    rates4 = texts4.get('rates')
    mdl1 = str(rates4[0].get('mid'))

    Mydict = {
        'eur': '',
        'usd': '',
        'ron': '',
        'mdl': '',
    }

    Mydict['eur'] = eur1
    Mydict['usd'] = usd1
    Mydict['ron'] = ron1
    Mydict['mdl'] = mdl1
    for key in Mydict.keys():
        text = '\n'.join((text, key, '->', Mydict[key]))
    bot.reply_to(message, text)


# Part 2

@bot.message_handler(commands=['pln_to_usd'])
def pln_to_usd(message):
    bot.send_message(message.chat.id, 'Type how pln, you want to convert to usd: ')

    @bot.message_handler(content_types=['text', ])
    def pln_usd(message):
        r = requests.get('http://api.nbp.pl/api/exchangerates/rates/a/usd/')
        texts = json.loads(r.content)
        rates = texts.get('rates')
        usd = rates[0].get('mid')
        amount = int(message.text)
        total = round((amount / usd), 2)
        result = f'{amount} pln is {total} usd'
        if type(amount) == str:
            raise  ConvertionException(f'Did not manage to convert {amount}')
        bot.send_message(message.chat.id, result)


@bot.message_handler(commands=['pln_to_ron'])
def pln_to_ron(message):
    bot.send_message(message.chat.id, 'Type how many pln,you want to convert to ron: ')

    @bot.message_handler(content_types=['text', ])
    def pln_ron(message):
        r4 = requests.get('http://api.nbp.pl/api/exchangerates/rates/a/ron/')
        texts4 = json.loads(r4.content)
        rates4 = texts4.get('rates')
        ron4 = rates4[0].get('mid')
        amount4 = int(message.text)
        total4 = round((amount4 / ron4), 2)
        result4 = f'{amount4} pln is {total4} ron'
        bot.send_message(message.chat.id, result4)


@bot.message_handler(commands=['pln_to_mdl'])
def pln_to_mdl(message):
    bot.send_message(message.chat.id, 'Type how many pln,you want to convert to mdl: ')

    @bot.message_handler(content_types=['text', ])
    def pln_mdl(message):
        r5 = requests.get('https://api.nbp.pl/api/exchangerates/rates/b/mdl')
        texts5 = json.loads(r5.content)
        rates5 = texts5.get('rates')
        mdl5 = rates5[0].get('mid')
        amount5 = int(message.text)
        total5 = round((amount5 / mdl5), 2)
        result5 = f'{amount5} pln is {total5} mdl'
        bot.send_message(message.chat.id, result5)


bot.polling(non_stop=True)

