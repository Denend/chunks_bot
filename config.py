import sqlite3
import string, random

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from random import choices


# @Chunks_bot = '6050973859:AAG7iX9uP5gKZWXTOZCHB3CkgjuHoIXMmPg'
# @TEST0206_bot = '5981739592:AAHqNCNHQyT7j_2jhr3ATQhueCe-TVytNAs'
API_TOKEN = '6050973859:AAG7iX9uP5gKZWXTOZCHB3CkgjuHoIXMmPg'


admins = [1894088037, 466660758]


bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

con = sqlite3.connect('server.db')
cursor = con.cursor()

class CaptchaGroup(StatesGroup):
	captcha = State()

class WalletGroup(StatesGroup):
	new_wallet = State()

user_bot = 'chunks_token_bot'

token_url = 'https://arbiscan.io/token/'

channel_dao = -1001800417419
channel_chunks = -1001856863117

alphabet = ["а","б","в","г","д","е","ё","ж","з","и","й","к","л","м","н","о",
		"п","р","с","т","у","ф","х","ц","ч","ш","щ","ъ","ы","ь","э","ю","я",
		"!","?","&","@","#","$","%","^","*","(",")","№",";",":","_","+","=",
		"<",">",",",".","/"]