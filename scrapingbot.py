# sending scraped data to bot
import telebot
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon import TelegramClient, sync, events

#from scrapeNumbers import *


# get api_id, api_hash, token from telegram
api_id = '1845059'
api_hash = '54ec497f5d3a23a61fe2f51bd9510966'
token = '1371253322:AAFVfdfVKhyY4cCuBC84Oy6dzdm7zJvOFio'

# your phone number
phone = '015167139457'

# creating a telegram session and assigning
# it to a variable client
client = TelegramClient('session', api_id, api_hash)

# connecting and building the session
client.connect()

# in case of script ran first time it will
# ask either to input token or otp sent to
# number or sent or your telegram id
if not client.is_user_authorized():

	client.send_code_request(phone)

	# signing in the client
	client.sign_in(phone, input('Enter the code: '))


try:
	# receiver user_id and access_hash, use
	# my user_id and access_hash for reference
	receiver = InputPeerUser('user_id', 'user_hash')

	# sending message using telegram client
	client.send_message(receiver, "Henrys Test", parse_mode=None)
except Exception as e:

	# there may be many error coming in while like peer
	# error, wwrong access_hash, flood_error, etc
	print(e)

# disconnecting the telegram session
client.disconnect()
