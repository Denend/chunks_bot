from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, ContentType

channel_dao_link = 'https://t.me/chunks_EN'
channel_chunks_link = 'https://t.me/chunks_token'

def main_menu():
	main_menu = InlineKeyboardMarkup(resize_keyboard=True).add(
		InlineKeyboardButton(text='Wheel of Fortune', callback_data='section_fortune'),
		InlineKeyboardButton(text='Rewards', callback_data='section_awards')).add(
		InlineKeyboardButton(text='Referal Program', callback_data='section_ref_program'),
		InlineKeyboardButton(text='Referal Rating', callback_data='section_ref_rating')).add(
		InlineKeyboardButton(text='About GOB', callback_data='section_about'),
		InlineKeyboardButton(text='Social Media', callback_data='section_soc_media')
		)
	return main_menu

def run_1():
	run = InlineKeyboardMarkup().add(
		InlineKeyboardButton(text='Next', callback_data='run_1')
		)
	return run

def kb_check_ref():
	kb = InlineKeyboardMarkup().add(
		InlineKeyboardButton(text='Update', callback_data='update_ref')
		)
	return kb

def kb_check_sub():
	kb = InlineKeyboardMarkup().add(
		InlineKeyboardButton(text='CHUNKS CHAT', url=channel_dao_link),
		InlineKeyboardButton(text='Chunks - RiskFi Token', url=channel_chunks_link)).add(
		InlineKeyboardButton(text='Check', callback_data='check')
		)
	return kb

def kb_fortune():
	kb = InlineKeyboardMarkup().add(
		InlineKeyboardButton(text='Spin fortune', callback_data='spin_fortune')).add(
		InlineKeyboardButton(text='Main menu', callback_data='menu')
		)
	return kb

def kb_main_menu():
	kb = InlineKeyboardMarkup().add(
		InlineKeyboardButton(text='Main menu', callback_data='menu')
		)
	return kb