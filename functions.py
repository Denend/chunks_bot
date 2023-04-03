from config import *
from keyboard import *

def select_captcha_comp(id_user):
	select_captcha_comp = cursor.execute(f'SELECT captcha_comp FROM users WHERE user_id = {id_user}').fetchone()[0]
	return select_captcha_comp


def generating_numbers(one, two):
	rand = random.randint(one, two)
	return rand


def check_captcha_ban(id_user):
	select_user = cursor.execute(f'SELECT captcha_comp FROM users WHERE user_id = {id_user}').fetchone()[0]
	if select_user == 'no':
		True
	else:
		False

async def social_sub(id_user):
	sub_channel_dao = await bot.get_chat_member(channel_dao, id_user)
	sub_channel_chunks = await bot.get_chat_member(channel_chunks, id_user)

	if sub_channel_dao.status == 'left' or sub_channel_chunks.status == 'left':
		return False
	return True


async def check_act(id_user):
	select_quantity_ref = cursor.execute(f'SELECT quantity_ref FROM users WHERE user_id = {id_user}').fetchone()[0]
	if select_quantity_ref >= 3:
		cursor.execute(f'UPDATE users SET menu_dostup = "yes" WHERE user_id = {id_user}')
		con.commit()
	select_act = cursor.execute(f'SELECT menu_dostup FROM users WHERE user_id = {id_user}').fetchone()[0]
	return select_act

async def check_wallet(id_user):
	select_wallet = cursor.execute(f'SELECT wallet FROM users WHERE user_id = {id_user}').fetchone()[0]
	return select_wallet

async def startig_func(id_user, msg_id, user_first_name, types):
	if await check_act(id_user) is None:
		select_quantity_ref = cursor.execute(f'SELECT quantity_ref FROM users WHERE user_id = {id_user}').fetchone()[0]
		await bot.send_message(
			id_user,
			f'''You ll get one free wheel spin for every 3 people you invite. One invited person is considered valid only if invites 3+ people

Your referral: <code>https://t.me/{user_bot}?start={id_user}</code>

<b>It remains to invite:</b> {str(select_quantity_ref - 3)[1:]}''',
			parse_mode='HTML',
			reply_markup=kb_check_ref()
			)
		return False
	elif await check_wallet(id_user) is None:
		if types == 'call':
			await bot.delete_message(
				id_user,
				msg_id
				)
		await bot.send_message(
				id_user,
				f'<b>{user_first_name}</b>, enter you <b>albitrum one</b> wallet address',
				parse_mode='HTML'
				)
		await WalletGroup.new_wallet.set()
		return False
	else:
		if types == 'call':
			await bot.edit_message_text(
				'The action is outdated',
				id_user,
				msg_id
				)
			return False

async def spin_fortune_func(id_user, msg_id, msg_caption, call_id):
	select_q_spin = cursor.execute(f'SELECT spin FROM users WHERE user_id = {id_user}').fetchone()[0]
	select_text_q_spin = (msg_caption[msg_caption.index("available wheel spins: ") + len("available wheel spins: "):msg_caption.index("\n\nWheel")])
	if select_q_spin > 0:
		cursor.execute(f'UPDATE users SET spin = spin - 1 WHERE user_id = {id_user}')
		con.commit()
		if int(select_text_q_spin) != (select_q_spin - 1):
			await bot.edit_message_caption(
				caption=f'''Number of your available wheel spins: <b>{select_q_spin - 1}</b>

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
				chat_id=id_user,
				message_id=msg_id,
				parse_mode='HTML',
				reply_markup=kb_fortune()
				)
		else:
			await bot.answer_callback_query(call_id)

		randomayzer = choices(
			[
			'Nothing',
			'1 Bonus Cards',
			'2 Bonus Cards',
			'3 Bonus Cards',
			'1 Card Pack',
			'2 Card Pack',
			'3 Card Pack',
			'BOD NFTs',
			'WOB LAND NFTs',
			'GOB Tokens',
			'Goon NFT'
			],
			weights=[38.5, 15, 12, 10, 8, 6, 4, 3, 2, 1, 0.5]
			)

		if randomayzer[0] == 'Nothing':
			await bot.send_photo(id_user, open('img/awards/rekt.jpg', 'rb'))

		elif randomayzer[0] == '1 Bonus Cards':
			await bot.send_photo(id_user, open('img/awards/1_bonus_card.jpg', 'rb'))
			cursor.execute(f'UPDATE awards SET bonus_card_1 = bonus_card_1 + 1 WHERE user_id = {id_user}')

		elif randomayzer[0] == '2 Bonus Cards':
			await bot.send_photo(id_user, open('img/awards/2_bonus_card.jpg', 'rb'))
			cursor.execute(f'UPDATE awards SET bonus_card_2 = bonus_card_2 + 1 WHERE user_id = {id_user}')

		elif randomayzer[0] == '3 Bonus Cards':
			await bot.send_photo(id_user, open('img/awards/3_bonus_card.jpg', 'rb'))
			cursor.execute(f'UPDATE awards SET bonus_card_3 = bonus_card_3 + 1 WHERE user_id = {id_user}')

		elif randomayzer[0] == '1 Card Pack':
			await bot.send_photo(id_user, open('img/awards/1_gob_card.jpg', 'rb'))
			cursor.execute(f'UPDATE awards SET gob_card_1 = gob_card_1 + 1 WHERE user_id = {id_user}')

		elif randomayzer[0] == '2 Card Pack':
			await bot.send_photo(id_user, open('img/awards/2_gob_card.jpg', 'rb'))
			cursor.execute(f'UPDATE awards SET gob_card_2 = gob_card_2 + 1 WHERE user_id = {id_user}')

		elif randomayzer[0] == '3 Card Pack':
			await bot.send_photo(id_user, open('img/awards/3_gob_card.jpg', 'rb'))
			cursor.execute(f'UPDATE awards SET gob_card_3 = gob_card_3 + 1 WHERE user_id = {id_user}')

		elif randomayzer[0] == 'BOD NFTs':
			await bot.send_photo(id_user, open('img/awards/bod_nft.jpg', 'rb'))
			cursor.execute(f'UPDATE awards SET bod_nft = bod_nft + 1 WHERE user_id = {id_user}')

		elif randomayzer[0] == 'WOB LAND NFTs':
			await bot.send_photo(id_user, open('img/awards/land.jpg', 'rb'))
			cursor.execute(f'UPDATE awards SET land = land + 1 WHERE user_id = {id_user}')

		elif randomayzer[0] == 'GOB Tokens':
			await bot.send_photo(id_user, open('img/awards/token.jpg', 'rb'))
			cursor.execute(f'UPDATE awards SET token = token + 6969 WHERE user_id = {id_user}')

		elif randomayzer[0] == 'Goon NFT':
			await bot.send_photo(id_user, open('img/awards/goon_nft.jpg', 'rb'))
			cursor.execute(f'UPDATE awards SET goon_nft = goon_nft + 1 WHERE user_id = {id_user}')

		con.commit()
	else:
		if int(select_text_q_spin) > 0:
			await bot.edit_message_caption(
				caption=f'''Number of your available wheel spins: <b>{select_q_spin}</b>

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
				chat_id=id_user,
				message_id=msg_id,
				parse_mode='HTML',
				reply_markup=kb_fortune()
				)
		await bot.answer_callback_query(
			call_id,
			"You don't have any spins for fortune!",
			show_alert=True
			)
