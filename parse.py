import requests
from time import sleep
import telebot
from telebot import types
import threading


bot = telebot.TeleBot("1691014755:AAGR1yh-i8n6YuVf9FTVG3kCfICCEoi9Ucc")

MembersListForTeleMail = []

def TelegramMail():
	@bot.message_handler(content_types=['text'])
	def regInInform(message):
		if message.text.lower() == '/start':
			bot.send_message(message.chat.id, 'Добро пожаловать!')
		if message.text.lower() == '/regs':
			if message.chat.id not in MembersListForTeleMail:
				MembersListForTeleMail.append(message.chat.id)
				bot.send_message(message.chat.id, 'Этот чат добавлен в базу.')
			else:
				bot.send_message(message.chat.id, 'Уже в базе.')
	bot.polling( none_stop = True, interval=0 )

lastlist_match = []
def Parse(Posttext):
	global lastlist_match
	if lastlist_match == []:
		for i in range(1, len(Posttext.split('<td class="hidden" data-mutable-id="eventJsonInfo">'))):
			lastlist_match.append(Posttext.split('<td class="hidden" data-mutable-id="eventJsonInfo">\n {"treeId":')[i].split(',"', maxsplit = 1)[0])
		print(lastlist_match)
	else:
		current_matchlist = []
		for i in range(1, len(Posttext.split('<td class="hidden" data-mutable-id="eventJsonInfo">'))):
			current_matchlist.append(Posttext.split('<td class="hidden" data-mutable-id="eventJsonInfo">\n {"treeId":')[i].split(',"', maxsplit = 1)[0])
		new_matchlist = [item for item in current_matchlist if item not in lastlist_match]
		if new_matchlist != []:
			Info_of_newmatch = []
			for i in new_matchlist:
				Info_of_newmatch.append(Posttext.split('<td class="member-area-button" id="event-more-view-' + i)[0].split('class="category-label simple-live"><span class="nowrap">')[-1].split('</span>')[0] + 'Матч:\n' + Posttext.split('<div class="bg coupon-row" data-event-treeId="' + i + '" data-event-name="', maxsplit = 1)[1].split('"', maxsplit = 1)[0] + '\n *-' + Posttext.split('<td class="member-area-button" id="event-more-view-' + i)[1].split('data-selection-price="', maxsplit = 2)[1].split('"', maxsplit = 1)[0] + '-*   *-' + Posttext.split('<td class="member-area-button" id="event-more-view-' + i)[1].split('data-selection-price="', maxsplit = 2)[2].split('"', maxsplit = 1)[0] + '-*' + '\n\n')
			if MembersListForTeleMail != []:
				for i in MembersListForTeleMail:
					bot.send_message(i, ''.join(Info_of_newmatch))
		lastlist_match = current_matchlist

threading.Thread(target=TelegramMail).start()
while True:
	post = requests.get('https://www.marathonbet.ru/su/live/1372932').text
	Parse(post)
	sleep(1)
