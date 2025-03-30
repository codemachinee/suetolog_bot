# библиотека проверки даты
from datetime import datetime

import aiohttp
import yadisk
from aiogram import exceptions
from loguru import logger

import paswords

saved_messages_davinci = []
y = yadisk.YaDisk(token=paswords.yadisk_token)


class Davinci:
    global saved_messages_davinci

    def __init__(self, bot, message, text):
        self.bot = bot
        self.message = message
        self.text = text

    async def answer(self):
        saved_messages_davinci.insert(len(saved_messages_davinci) + 1, {
            "role": "user",
            "text": f'{self.text}'})
        message = await self.bot.send_message(self.message.chat.id, 'секунду..')
        prompt = {
            "modelUri": f"gpt://{paswords.yandex_gpt_catalog_id}/yandexgpt",
            "completionOptions": {
                "stream": False,
                "temperature": 0.2,
                "maxTokens": "1200"
            },
            "messages": []
        }
        prompt['messages'] = {
            "role": "system",
            "text": "Ты Давинчи, бот помощник знающий ответы на все вопросы. Ты даешь краткий и лаконичный "
                    "ответ на любые вопросы, а также способен найти запрашиваемое в интернете. Ты максимально "
                    "вежлив и учтив."
        }, *saved_messages_davinci
        url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {paswords.yandex_gpt_api_key}"
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=prompt, ssl=False) as response:
                try:
                    answer = (await response.json())['result']['alternatives'][0]['message']['text']
                    # await self.bot.send_message(self.message.chat.id, f'{answer}')
                    await self.bot.edit_message_text(f'{answer}', message.chat.id, message.message_id)
                    saved_messages_davinci.insert(len(saved_messages_davinci) + 1, {
                        "role": "assistant",
                        "text": f'{str(answer)}'})
                    if len(saved_messages_davinci) >= 8:
                        del saved_messages_davinci[0:5]
                except Exception:
                    await self.bot.send_message(message.chat.id, f"Ошибка\n"
                                                                 f"Логи:{response.json()}")
                    del saved_messages_davinci[-1]


async def Artur_pozdravlyaet(bot, text):
    prompt = {
        "modelUri": f"gpt://{paswords.yandex_gpt_catalog_id}/yandexgpt",
        "completionOptions": {
            "stream": False,
            "temperature": 0.5,
            "maxTokens": "2000"
        },
        "messages": [
            {
                "role": "system",
                "text": "Ты Артур, бот который профессионально в сатирической форме, развернуто поздравляет с днем "
                        "рождения"
                        " и обязательно дерзко пошутишь над виновником торжества. Ты всегда "
                        "обращаешься к поздравляемым на 'Ты'."
            },
            {
                "role": "user",
                "text": f'{text}'
            },
        ]
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {paswords.yandex_gpt_api_key}"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=prompt, ssl=False) as response:
            try:
                answer = (await response.json())['result']['alternatives'][0]['message']['text']
                await bot.send_message(paswords.group_id, f'{answer}')
            except Exception:
                await bot.send_message(paswords.group_id, "Короче с др брат, ты и так все знаешь.."
                                                 "а эта суета с лишними словами для слабых духом"
                                                 "мы же с тобой сильные... обнял")


class YaDisk:

    def __init__(self, bot, message):
        self.bot = bot
        self.message = message

    async def save_photo(self):
        try:
            file_id = self.message.photo[-1].file_id
            file = await self.bot.get_file(file_id)
            file_path = file.file_path
            src = f'/суетологи/{datetime.now().day}.{datetime.now().month}.{datetime.now().year}'
            try:
                y.upload(await self.bot.download_file(file_path),
                             f'{src}/{datetime.now().hour}.{datetime.now().minute}.{datetime.now().second}.'
                             f'{datetime.now().microsecond}.jpg')
                await self.bot.send_message(self.message.chat.id, 'фото успешно загружено')
            except yadisk.exceptions.ParentNotFoundError:
                y.mkdir(src)
                y.upload(await self.bot.download_file(file_path),
                             f'{src}/{datetime.now().hour}.{datetime.now().minute}.{datetime.now().second}.'
                             f'{datetime.now().microsecond}.jpg')
                await self.bot.send_message(self.message.chat.id, 'фото успешно загружено')
        except Exception as e:
            logger.exception('Ошибка в yandex_services/save_photo', e)
            await self.bot.send_message(self.message.chat.id, f'Отправка не удалась. Сервер перегружен, {e}')

    async def save_doc(self):
        try:
            file_id = self.message.document.file_id
            file = await self.bot.get_file(file_id)
            file_path = file.file_path
            src = f'/суетологи/{datetime.now().day}.{datetime.now().month}.{datetime.now().year}'
            try:
                y.upload(await self.bot.download_file(file_path),
                         f'{src}/{self.message.document.file_name}')
                await self.bot.send_message(self.message.chat.id, 'документ успешно загружен')
            except yadisk.exceptions.ParentNotFoundError:
                y.mkdir(src)
                y.upload(await self.bot.download_file(file_path),
                         f'{src}/{self.message.document.file_name}')
                await self.bot.send_message(self.message.chat.id, 'документ успешно загружен')
            except yadisk.exceptions.PathExistsError:
                y.upload(await self.bot.download_file(file_path),
                         f'{src}/{self.message.document.file_name}.{datetime.now().hour}.{datetime.now().minute}.'
                         f'{datetime.now().second}.')
                await self.bot.send_message(self.message.chat.id, 'документ успешно загружен')
        except exceptions.TelegramBadRequest:
            await self.bot.send_message(self.message.chat.id, 'ОШИБКА! Документ слишком большой')
        except Exception as e:
            logger.exception('Ошибка в yandex_services/save_doc', e)
            await self.bot.send_message(self.message.chat.id, f'Отправка не удалась. Сервер перегружен, {e}')

    async def save_video(self):
        try:
            file_id = self.message.video.file_id
            file = await self.bot.get_file(file_id)
            file_path = file.file_path
            src = f'/суетологи/{datetime.now().day}.{datetime.now().month}.{datetime.now().year}'
            try:
                y.upload(await self.bot.download_file(file_path),
                         f'{src}/{self.message.video.file_unique_id}')
                await self.bot.send_message(self.message.chat.id, 'видео успешно загружено')
            except yadisk.exceptions.ParentNotFoundError:
                y.mkdir(src)
                y.upload(await self.bot.download_file(file_path),
                         f'{src}/{self.message.video.file_unique_id}')
                await self.bot.send_message(self.message.chat.id, 'видео успешно загружено')
        except Exception as e:
            logger.exception('Ошибка в yandex_services/save_video', e)
            await self.bot.send_message(self.message.chat.id, f'Отправка не удалась. Сервер перегружен, {e}')

    async def save_video_note(self):
        try:
            file_id = self.message.video_note.file_id
            file = await self.bot.get_file(file_id)
            file_path = file.file_path
            src = f'/суетологи/{datetime.now().day}.{datetime.now().month}.{datetime.now().year}'
            try:
                y.upload(await self.bot.download_file(file_path),
                         f'{src}/{self.message.video_note.file_id}')
                await self.bot.send_message(self.message.chat.id, 'видео успешно загружено')
            except yadisk.exceptions.ParentNotFoundError:
                y.mkdir(src)
                y.upload(await self.bot.download_file(file_path),
                         f'{src}/{self.message.video_note.file_id}')
                await self.bot.send_message(self.message.chat.id, 'видео успешно загружено')
        except Exception as e:
            logger.exception('Ошибка в yandex_services/video_note', e)
            await self.bot.send_message(self.message.chat.id, f'Отправка не удалась. Сервер перегружен, {e}')
