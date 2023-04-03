import openpyxl
import datetime

from openpyxl.styles import Font, Fill

from text import *
from keyboard import *
from functions import *
from config import *

cursor.execute("""CREATE TABLE IF NOT EXISTS users
	(
		user_id INT PRIMARY KEY UNIQUE NOT NULL,
		referrer_id INT,
		activ_ref TEXT,
		quantity_ref INT DEFAULT 0,
		quantity_ref_act INT DEFAULT 0,
		liga_ref INT DEFAULT 0,
		menu_dostup TEXT,
		wallet TEXT UNIQUE,
		captcha INT,
		captcha_life INT DEFAULT 3,
		captcha_comp TEXT,
		verification TEXT,
		date_reg TEXT,
		spin INT DEFAULT 1,
		admin TEXT,
		banned TEXT,
		score_ref INT DEFAULT 0
		)"""
	)
con.commit()

cursor.execute("""CREATE TABLE IF NOT EXISTS awards
	(
		user_id INT PRIMARY KEY UNIQUE NOT NULL,
		wallet TEXT UNIQUE,
		bonus_card_1 INT DEFAULT 0,
		bonus_card_2 INT DEFAULT 0,
		bonus_card_3 INT DEFAULT 0,
		gob_card_1 INT DEFAULT 0,
		gob_card_2 INT DEFAULT 0,
		gob_card_3 INT DEFAULT 0,
		bod_nft INT DEFAULT 0,
		land INT DEFAULT 0,
		token INT DEFAULT 0,
		goon_nft INT DEFAULT 0
		)"""
	)
con.commit()

@dp.message_handler(commands=['members'])
async def quantity_members(message):
	if message.chat.type != 'private':
		return

	id_user = message.from_user.id
	if id_user not in admins:
		return

	select_members = cursor.execute('SELECT user_id FROM users').fetchall()
	await bot.send_message(
		id_user,
		f'Кол-во участников в боте: {len(select_members)}'
		)

@dp.message_handler(commands=['start'])
async def start_bot(message):
	if message.chat.type != 'private':
		return

	id_user = message.from_user.id
	user_first_name = message.from_user.first_name
	start_command = str(message.text[7:])

	select_user = cursor.execute(f'SELECT user_id FROM users WHERE user_id = {id_user}').fetchone()
	select_referrer = cursor.execute(f'SELECT user_id FROM users WHERE user_id = "{start_command}"').fetchone()

	if select_user is None:
		if select_referrer is None:
			cursor.execute(f'INSERT INTO users(user_id) VALUES({id_user})')
		else:
			cursor.execute(f'INSERT INTO users(user_id, referrer_id) VALUES({id_user}, {start_command})')
		cursor.execute(f'INSERT INTO awards(user_id) VALUES({id_user})')
		con.commit()

	if check_captcha_ban(id_user) == True:
		return

	select_verif = cursor.execute(f'SELECT verification FROM users WHERE user_id = {id_user}').fetchone()[0]

	if select_captcha_comp(id_user) is None:
		await bot.send_message(
			id_user,
			'Solve captcha'
			)

		count_1 = generating_numbers(2, 99)
		count_2 = generating_numbers(2, 99)
		cursor.execute(f'UPDATE users SET captcha = {count_1 + count_2} WHERE user_id = {id_user}')
		con.commit()

		await bot.send_message(
			id_user,
			f'{count_1} + {count_2} = ?'
			)

		return await CaptchaGroup.captcha.set()

	if select_verif is None:
		await bot.send_message(
			id_user,
			run_1_text(),
			reply_markup=run_1()
			)
		return

	if await startig_func(id_user, message.message_id, user_first_name, types='message') == False:
		return

	await bot.send_message(
		id_user,
		f'<b>{user_first_name}</b>, welcome to the main menu',
		parse_mode='HTML',
		reply_markup=main_menu()
		)


@dp.callback_query_handler()
async def callback(call):
	if call.message.chat.type != 'private':
		return
	id_user = call.from_user.id
	msg_id = call.message.message_id
	msg_text = call.message.text
	msg_caption = call.message.caption
	user_first_name = call.from_user.first_name

	if check_captcha_ban(id_user) == True:
		return

	# await bot.answer_callback_query(call.id)
	select_verif = cursor.execute(f'SELECT verification FROM users WHERE user_id = {id_user}').fetchone()[0]

	if call.data == 'run_1':
		await bot.edit_message_reply_markup(id_user, msg_id, ReplyKeyboardRemove())
		if await social_sub(id_user) == False:
			await bot.send_message(
				id_user,
				'To continue subscribe to our channel',
				reply_markup=kb_check_sub()
				)
		else:
			cursor.execute(f'UPDATE users SET verification = "yes" WHERE user_id = {id_user}')
			con.commit()

			await startig_func(id_user, msg_id, user_first_name, types='call')

	elif call.data == 'check':
		if await social_sub(id_user) == False:
			await bot.answer_callback_query(
				call.id,
				'You are not subscribed to our channels! Subscribe and try again!',
				show_alert=True
				)
			return

		await bot.edit_message_text(
			'Verification passed!',
			id_user,
			msg_id
			)
		cursor.execute(f'UPDATE users SET verification = "yes" WHERE user_id = {id_user}')
		con.commit()

		await startig_func(id_user, msg_id, user_first_name, types='call')

	elif call.data == 'update_ref':
		if await check_act(id_user) is None:
			await bot.delete_message(id_user, msg_id)
		await startig_func(id_user, msg_id, user_first_name, types='call')

	elif call.data == 'section_fortune':
		await bot.delete_message(id_user, msg_id)
		select_q_spin = cursor.execute(f'SELECT spin FROM users WHERE user_id = {id_user}').fetchone()[0]
		await bot.send_photo(
			id_user,
			open('img/awards/wheel_of_fortune.png', 'rb'),
			f'''Number of your available wheel spins: <b>{select_q_spin}</b>

<b>Wheel of Fortune Win Probabilities:</b>

◾️Nothing = 38.5%
◾️1 Bonus Cards = 15%
◾️2 Bonus Cards = 12%
◾️3 Bonus Cards = 10%
◾️1 Card Pack = 8%
◾️2 Card Packs= 6%
◾️3 Card Packs = 4%
◾️BOD NFTs = 3%
◾️WOB LAND NFTs = 2%
◾️GOB Tokens = 1%
◾️Goon NFT = 0.5%''',
			parse_mode='HTML',
			reply_markup=kb_fortune()
			)

	elif call.data == 'section_about':
		await bot.delete_message(id_user, msg_id)
		await bot.send_message(
			id_user,
			text_about(),
			parse_mode='HTML',
			reply_markup=kb_main_menu(),
			disable_web_page_preview=True
			)

	elif call.data == 'section_soc_media':
		await bot.delete_message(
			id_user,
			msg_id
			)
		await bot.send_message(
			id_user,
			text_social_media(),
			parse_mode='HTML',
			reply_markup=kb_main_menu(),
			disable_web_page_preview=True
			)

	elif call.data == 'section_buy':
		await bot.delete_message(id_user, msg_id)
		await bot.send_message(
			id_user,
			text_how_to_buy(),
			parse_mode='HTML',
			reply_markup=kb_main_menu(),
			disable_web_page_preview=True
			)

	elif call.data == 'spin_fortune':
		await spin_fortune_func(id_user, msg_id, msg_caption, call.id)

	elif call.data == 'section_ref_rating':
		select_users = cursor.execute(f'SELECT user_id, wallet, liga_ref FROM users WHERE wallet is not NULL ORDER BY liga_ref DESC').fetchall()[:10]
		if len(select_users) < 10:
			await bot.answer_callback_query(
				call.id,
				'The table has not been loaded yet!',
				show_alert=True
				)
			return
		await bot.delete_message(id_user, msg_id)
		num = 0
		i_top = 'no'
		post_rating = '<b>Top referrers</b> 🌟\n\n'
		for x in select_users:
			num += 1
			wallet_link = x[1][:5] + '.....' + x[1][-5:]
			if x[0] == id_user:
				i_top = 'yes'
				post_rating += f'<b>{num}. <a href="{token_url + x[1]}">{wallet_link}</a> | Referrals: {x[2]}</b> 🟢\n'
			else:
				post_rating += f'{num}. <a href="{token_url + x[1]}">{wallet_link}</a> | Referrals: {x[2]}\n'

		if i_top == 'no':
			select_my_rating = cursor.execute(f'SELECT user_id, wallet, liga_ref FROM users WHERE wallet is not NULL ORDER BY liga_ref DESC').fetchall()
			select_my_info = cursor.execute(f'SELECT user_id, wallet, liga_ref FROM users WHERE user_id = {id_user}').fetchone()
			for i in range(len(select_my_rating)):
				members_quantity = i + 1
				if select_my_rating[i][0] == id_user:
					my_rating = i + 1
			wallet_link = select_my_info[1][:5] + '.....' + select_my_info[1][-5:]
			post_rating += f'...\n<b>{my_rating}. <a href="{token_url + select_my_info[1]}">{wallet_link}</a> | Referrals: {select_my_info[2]}</b> 🔴\n'

		post_rating += f'\nReferral link for inviting friends:\n<code>https://t.me/{user_bot}?start={id_user}</code>'

		await bot.send_message(
			id_user,
			post_rating,
			parse_mode='HTML',
			reply_markup=kb_main_menu(),
			disable_web_page_preview=True
			)

	elif call.data == 'section_awards':
		await bot.delete_message(id_user, msg_id)
		select_awards = cursor.execute(f'SELECT * FROM awards WHERE user_id = {id_user}').fetchone()
		await bot.send_message(
			id_user,
			f'''<b>My rewards</b> 🏆

1 Bonus Cards: <b>{select_awards[2]}pc</b>
2 Bonus Cards: <b>{select_awards[3]}pc</b>
3 Bonus Cards: <b>{select_awards[4]}pc</b>
1 Card Pack: <b>{select_awards[5]}pc</b>
2 Card Packs: <b>{select_awards[6]}pc</b>
3 Card Packs: <b>{select_awards[7]}pc</b>
BOD NFTs: <b>{select_awards[8]}pc</b>
WOB LAND NFTs: <b>{select_awards[9]}pc</b>
GOB Tokens: <b>{select_awards[10]}pc</b>
Goon NFT: <b>{select_awards[11]}pc</b>''',
			parse_mode='HTML',
			reply_markup=kb_main_menu()
			)

	elif call.data == 'menu':
		await bot.delete_message(id_user, msg_id)
		await bot.send_photo(
			id_user,
			open('img/GoBonus_menu.png', 'rb'),
			f'<b>{call.from_user.first_name}</b>, welcome to the main menu',
			parse_mode='HTML',
			reply_markup=main_menu()
			)

	elif call.data == 'section_ref_program':
		await bot.delete_message(id_user, msg_id)
		await bot.send_message(
			id_user,
			f'You ll get one free wheel spin for every 3 people you invite. One invited person is considered valid only if invites 3+ people\n\nYour referral: <code>https://t.me/{user_bot}?start={id_user}</code>',
			parse_mode='HTML',
			reply_markup=kb_main_menu()
			)


@dp.message_handler(state=CaptchaGroup.captcha)
async def captcha(message, state: FSMContext):
	if message.chat.type != 'private':
		return
	id_user = message.from_user.id
	msg_text = message.text

	if message.text == '/start':
		await bot.send_message(
			id_user,
			'Solve captcha'
			)

		count_1 = generating_numbers(2, 99)
		count_2 = generating_numbers(2, 99)

		cursor.execute(f'UPDATE users SET captcha = {count_1 + count_2} WHERE user_id = {id_user}')
		con.commit()
		await bot.send_message(
			id_user,
			f'{count_1} + {count_2} = ?'
			)
		return

	select_captcha = cursor.execute(f'SELECT captcha FROM users WHERE user_id = {id_user}').fetchone()[0]

	if str(msg_text) != str(select_captcha):
		cursor.execute(f'UPDATE users SET captcha_life = captcha_life - 1 WHERE user_id = {id_user}')
		con.commit()
		select_captcha_life = cursor.execute(f'SELECT captcha_life FROM users WHERE user_id = {id_user}').fetchone()[0]
		if select_captcha_life > 0:
			if select_captcha_life == 2:
				text_captcha = 'Incorrect. 🤨 You have 2 attempts left.'
			elif select_captcha_life == 1:
				text_captcha = 'Incorrect. 😕 You have 1 attempt left.'

			await bot.send_message(
				id_user,
				text_captcha
				)

			count_1 = generating_numbers(2, 99)
			count_2 = generating_numbers(2, 99)

			cursor.execute(f'UPDATE users SET captcha = {count_1 + count_2} WHERE user_id = {id_user}')
			con.commit()
			await bot.send_message(
				id_user,
				f'{count_1} + {count_2} = ?'
				)
		else:
			await bot.send_message(
				id_user,
				'Incorrect. ☹️ You run out of attempts. You are blocked. ❌'
				)
			cursor.execute(f'UPDATE users SET captcha = None, captcha_comp = "no" WHERE user_id = {id_user}')
			con.commit()
			await state.finish()

	else:
		select_referrer = cursor.execute(f'SELECT referrer_id FROM users WHERE user_id = {id_user}').fetchone()[0]
		if select_referrer is not None:
			cursor.execute(f'UPDATE users SET quantity_ref = quantity_ref + 1 WHERE user_id = {select_referrer}')
		cursor.execute(f'UPDATE users SET captcha_comp = "yes" WHERE user_id = {id_user}')
		con.commit()
		await bot.send_message(
			id_user,
			'Correct!'
			)
		await bot.send_message(
			id_user,
			run_1_text(),
			reply_markup=run_1()
			)
		await state.finish()


@dp.message_handler(state=WalletGroup.new_wallet)
async def get_wallet(message, state: FSMContext):
	await state.update_data(msg_wallet=message.text)

	id_user = message.from_user.id
	msg_text = message.text

	for x in alphabet:
		if x in msg_text.lower():
			return await bot.send_message(
				id_user,
				'Enter a valid <b>albitrum one</b> address',
				parse_mode='HTML'
				)
	if len(msg_text) < 20:
		return await bot.send_message(
			id_user,
			'Enter a valid <b>albitrum one</b> address',
			parse_mode='HTML'
			)

	select_wallet = cursor.execute(f'SELECT wallet FROM users WHERE wallet = "{msg_text}"').fetchone()
	if select_wallet is not None:
		return await bot.send_message(
			id_user,
			'This address was previously specified! Please enter the new address of <b>albitrum one</b>',
			parse_mode='HTML'
			)
	data_wallet = await state.get_data()
	cursor.execute(f'UPDATE users SET wallet = "{data_wallet["msg_wallet"]}" WHERE user_id = {id_user}')
	cursor.execute(f'UPDATE awards SET wallet = "{data_wallet["msg_wallet"]}" WHERE user_id = {id_user}')
	select_referrer = cursor.execute(f'SELECT referrer_id FROM users WHERE user_id = {id_user}').fetchone()[0]
	if select_referrer is not None:
		cursor.execute(f'UPDATE users SET activ_ref = "yes" WHERE user_id = {id_user}')
		cursor.execute(f'UPDATE users SET quantity_ref_act = quantity_ref_act + 1, liga_ref = liga_ref + 1, score_ref = score_ref + 1 WHERE user_id = {select_referrer}')
		con.commit()
		select_q_ref = cursor.execute(f'SELECT score_ref FROM users WHERE user_id = {select_referrer}').fetchone()[0]
		if select_q_ref >= 3:
			cursor.execute(f'UPDATE users SET spin = spin + 1 WHERE user_id = {select_referrer}')
			cursor.execute(f'UPDATE users SET score_ref = score_ref - 3 WHERE user_id = {select_referrer}')
	con.commit()
	await bot.send_photo(
		id_user,
		open('img/GoBonus_menu.png', 'rb'),
		f'You are all set! Menu is now available',
		parse_mode='HTML',
		reply_markup=main_menu()
		)
	await state.finish()


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)