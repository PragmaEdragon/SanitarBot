# -*- coding: utf-8 -*-

"""
#
#
#
#
#
"""

import vk_api
from vk_api import VkUpload
from vk_api.bot_longpoll import VkBotLongPoll
import threading
import random
import string
import time
import os

# [id{event.message['from_id']}|@шизойд]
FILE_LIST = os.listdir(os.path.dirname(os.path.abspath(__file__)) + r'\sanitars')


def shiza_phrazi(NAME):
    return [f'{NAME}Ты] как из палаты сбежал, уважаемый?',
            f'{NAME}Тебе] кто блять интернет в палату провел?',
            f'{NAME}Ты] как блять смирительную рубашку снял',
            f'{NAME}Наш] пациент',
            f'{NAME}Дурка] есть дурка. Грузим',
            f'{NAME}Сука] ну ты внатуре псих блять)))',
            f'Попался, {NAME}шизойд]',
            f'О, {NAME}шизойд] тонет. А ну спасаем и в каюту, то есть в палату',
            f'Отдай мой колпак, {NAME}сын бляди]',
            f'Мужики, скручиваем {NAME}его] и в дурку',
            f"{NAME}Загружайте]",
            f"{NAME}По-чему] не в палате?",
            f"{NAME}Бе ды с ба шкой]"]


def upload_photo(botApi_session):
    upload = VkUpload(botApi_session)
    os.chdir(os.path.dirname(os.path.abspath(__file__)) + r'\sanitars')
    with open(f"{random.choice(FILE_LIST)}", 'rb') as file:
        photo = upload.photo_messages(photos=[file])
    return 'photo{}_{}'.format(photo[0]['owner_id'], photo[0]['id'])


def isSmile():
    pass


def randomMessage(bot_api, event, current_time):
    if current_time in str([random.randint(0, 61) for _ in range(13)]):
        print("[+] Sleep initiated! ")
        name = f"[id{bot_api.messages.getConversationMembers(peer_id=event.message['peer_id'])['items'][random.randint(0, bot_api.messages.getConversationMembers(peer_id=event.message['peer_id'])['count'] - 1)]['member_id']}|@"
        if '-195313690' not in name:
            time.sleep(random.randint(0, 360))
            bot_api.messages.send(
                message=random.choice(shiza_phrazi(name)),
                random_id=random.getrandbits(32),
                chat_id=event.chat_id
            )
        else:
            randomMessage(bot_api, event, current_time)
    else:
        return None


def main():
    bot_session = vk_api.VkApi(token=
                               'urtoken')
    bot_api = bot_session.get_api()
    longpoll = VkBotLongPoll(bot_session, 'urid')

    print("[+] Bot process initiated ")
    for event in longpoll.listen():
        # full message info - print(event.message)
        print(event.message)

        if event.type == vk_api.bot_longpoll.VkBotEventType.MESSAGE_NEW:
            NAME = f"[id{event.message['from_id']}|@"
            threading.Thread(target=randomMessage,
                             args=[bot_api, event, time.ctime().split(" ")[3][6:], ]).start()

            # print(threading.active_count())
            wordlist = "".join(items for items in event.message['text'].replace(' ', '')
                               if items not in string.punctuation and items not in string.digits)
            if all(x.isupper() for x in str(wordlist)) and len(wordlist) > 0:
                bot_api.messages.send(
                    message=random.choice(shiza_phrazi(NAME)),
                    attachment=upload_photo(bot_session),
                    random_id=random.getrandbits(32),
                    chat_id=event.chat_id
                )
            else:
                for step in range(1, len(event.message['text']) - 1):
                    for start in range(step):
                        if len(set(event.message['text'][start:: step])) != 1:
                            break
                    else:
                        bot_api.messages.send(
                            message=random.choice(shiza_phrazi(NAME)),
                            random_id=random.getrandbits(32),
                            chat_id=event.chat_id
                        )
                        break


main()
