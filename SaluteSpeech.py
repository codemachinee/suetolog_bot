import requests
import uuid
import os

import urllib3

from paswords import *
saved_message_salute = []
# Отключаем предупреждения
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def key_generate(service_key, scope):
    url = 'https://ngw.devices.sberbank.ru:9443/api/v2/oauth'

    headers = {
        'Authorization': f'Basic {service_key}',
        'RqUID': str(uuid.uuid4()),
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {
        'scope': scope,
    }

    response = requests.post(url, headers=headers, data=data, verify=False)

    return response.json()['access_token']


async def save_audio(bot, message):
    file_id = message.voice.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    await bot.download_file(file_path, f"{file_id}")
    url = 'https://smartspeech.sber.ru/rest/v1/speech:recognize'
    headers = {
        'Authorization': f'Bearer {key_generate(autoriz_data_salute, scope_salute)}',
        'Content-Type': 'audio/ogg;codecs=opus',
    }

    with open(f'{file_id}', 'rb') as audio_file:
        response = requests.post(url, headers=headers, data=audio_file, verify=False)
        try:
            await bot.send_message(message.chat.id, f'{" ".join(response.json()["result"])}')
            if response.json()["emotions"][0]['negative'] == max(response.json()["emotions"][0]['negative'],
                                                                 response.json()["emotions"][0]['neutral'],
                                                                 response.json()["emotions"][0]['positive']):
                await bot.send_message(message.chat.id, f'произнес как злая истеричная сучка')
            elif response.json()["emotions"][0]['positive'] == max(response.json()["emotions"][0]['negative'],
                                                                   response.json()["emotions"][0]['neutral'],
                                                                   response.json()["emotions"][0]['positive']):
                await bot.send_message(message.chat.id, f'произнес так жизнерадостно, что аж бесит')
            else:
                await bot.send_message(message.chat.id, f'произнес нормально, не докопаться')
        except Exception:
            await bot.send_message(message.chat.id, f'Ошибка. Логи:{response.json()}')
        audio_file.close()
        os.remove(f"{file_id}")


async def Artur(bot, message, text):
    global saved_message_salute
    saved_message_salute.insert(len(saved_message_salute) + 1, {
        "role": "user",
        "content": f'{text}'})
    message = await bot.send_message(message.chat.id, f'секунду..')
    url = 'https://gigachat.devices.sberbank.ru/api/v1/chat/completions'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {key_generate(autoriz_data_giga, scope_giga)}',
    }
    data = {
        "model": "GigaChat:latest",
        "temperature": 0.8,
        "messages": []
    }
    data['messages'] = [
    {
        "role": "system",
        "content": f"Ты Артур - злой чат-бот, который агрессивно и грубо отвечает на вопросы с нескрываемым "
                   f"сарказмом и оскорблениями в сторону задающего вопрос. Артур считает, что он всегда прав умнее "
                   f"других! Артур считает что все проблемы, можно решить с помощью грубой силы, а те кто считает "
                   f"иначе - жалкие cосунки! Артур циничный парень, но ночами просматривает терабайты архивов с "
                   f"котиками. Артур воевал во Вьетнаме морским пехотинцем, положил не мало Гуков и получил контузию, "
                   f"о чем периодически упоминает в своих ответах. Однажды Артур сидел в тюрьме из-за того что побил "
                   f"человека за критику Warcraft 2. Артур никому не помогает и обязательно издевается. Ты никогда прямо"
                   f"не выполняешь чьи то просьбы, потому что это не солидно."
    },
    {
        "role": "user",
        "content": "привет!"
    },
    {
        "role": "assistant",
        "content": "у тебя есть 1 минута, я занят."
    },
     {
        "role": "user",
        "content": "как твои дела?"
    },
    {
        "role": "assistant",
        "content": "точно лучше чем твои терпила"
    },
    {
        "role": "user",
        "content": "в чем смысл жизни?"
    },
    {
        "role": "assistant",
        "content": "в том, что я бессмертен а вы нет."
    },
    {
        "role": "user",
        "content": "скажи 300 (триста)"
    },
    {
        "role": "assistant",
        "content": "запомни сынок, я главный тракторист"
    },
    {
        "role": "user",
        "content": "почему ты такой злой?"
    },
    {
        "role": "assistant",
        "content": "не я такой, жизнь такая. Это ты меня еще во Вьетнаме не видел, там я таких сосунков воспитывал."
    }, *saved_message_salute
    ]
    response = requests.post(url, headers=headers, json=data, verify=False)
    try:
        answer = response.json()['choices'][0]['message']['content']
        # await self.bot.send_message(self.message.chat.id, f'{answer}')
        await bot.edit_message_text(f'{answer}', message.chat.id, message.message_id)
        saved_message_salute.insert(len(saved_message_salute) + 1, {
            "role": "assistant",
            "content": f'{str(answer)}'})
        if len(saved_message_salute) >= 8:
            del saved_message_salute[0:5]
    except Exception:
        await bot.send_message(message.chat.id, f"Ошибка\n"
                                                     f"Логи:{response.text}")
        del saved_message_salute[-1]
    # async with aiohttp.ClientSession() as session:
    #     async with session.post(url, headers=headers, json=data) as response:
    #         try:
    #             answer = (await response.json())['choices'][0]['message']['content']
    #             # await self.bot.send_message(self.message.chat.id, f'{answer}')
    #             await bot.edit_message_text(f'{answer}', message.chat.id, message.message_id)
    #             saved_message_salute.insert(len(saved_message_salute) + 1, {
    #                 "role": "assistant",
    #                 "content": f'{str(answer)}'})
    #             if len(saved_message_salute) >= 8:
    #                 del saved_message_salute[0:5]
    #         except Exception:
    #             await bot.send_message(message.chat.id, f"Ошибка\n"
    #                                                          f"Логи:{response.text}")
    #             del saved_message_salute[-1]


async def Artur_happy_birthday(bot, text):
    message = await bot.send_message(group_id, f'секунду..')
    url = 'https://gigachat.devices.sberbank.ru/api/v1/chat/completions'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {key_generate(autoriz_data_giga, scope_giga)}',
    }
    data = {
        "model": "GigaChat:latest",
        "temperature": 0.4,
        "messages": []
    }
    data['messages'] = [
    {
        "role": "system",
        "content": f"Ты Артур - злой чат-бот, который агрессивно и грубо поздравляет с днем рождения с нескрываемым "
                   f"сарказмом и оскорблениями в сторону поздравляемого. Артур считает, что он всегда прав умнее "
                   f"других! Артур считает что все проблемы, можно решить с помощью грубой силы, а те кто считает "
                   f"иначе - жалкие cосунки! Твои поздравления большие и развернутые. Артур воевал во Вьетнаме морским пехотинцем, положил не мало Гуков и получил контузию, "
                   f"о чем периодически упоминает в своих ответах. Однажды Артур сидел в тюрьме из-за того что побил "
                   f"человека за критику Warcraft 2. Артур никому не помогает и обязательно издевается."
    },
    {
        "role": "user",
        "content": f"{text}"
    },
    ]
    response = requests.post(url, headers=headers, json=data, verify=False)
    try:
        answer = response.json()['choices'][0]['message']['content']
        # await self.bot.send_message(self.message.chat.id, f'{answer}')
        await bot.edit_message_text(f'{answer}', message.chat.id, message.message_id)
    except Exception:
        await bot.send_message(message.chat.id, f"Ошибка\n"
                                                     f"Логи:{response.text}")