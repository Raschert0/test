import telebot
import logging

with open('./keys/api_key.txt') as f:
	API_TOKEN = f.read().rstrip()

print(API_TOKEN)

bot = telebot.TeleBot(API_TOKEN)
logger = telebot.logger

from mpy import randPhrase

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello here!")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, randPhrase())
