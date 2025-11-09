import asyncio
import json
from datetime import datetime
from random import choice

import aiofiles  # -*- coding: utf-8 -*-
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    FSInputFile,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger

from FSM import step_message
from functions_file import (
    ball_of_fate,
    celebrate_day,
    obnulenie_stat,
    pstat,
    value_plus_one,
)
from paswords import admin_id, group_id, loggs_acc, major_suetolog
from SaluteSpeech import (
    Artur,
    Artur_happy_birthday,
    save_audio,
)
from yandex_services import Davinci, YaDisk

# token = lemonade
# token = codemashine_test
token = major_suetolog

bot = Bot(token=token)
dp = Dispatcher()

logger.remove()
# Настраиваем логирование в файл с ограничением количества файлов
logger.add(
    "loggs.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="INFO",
    rotation="5 MB",  # Ротация файла каждые 10 MB
    retention="10 days",  # Хранить только 5 последних логов
    compression="zip",  # Сжимать старые логи в архив
    backtrace=True,  # Сохранение трассировки ошибок
    diagnose=True,  # Подробный вывод
)


async def pidr():
    try:
        x = choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        if x == 1:
            await dr()
            file1 = FSInputFile(r"Я.jpg", "rb")
            y = ("Игорь", file1)
            await value_plus_one("A2")
            await bot.send_photo(group_id, y[1], request_timeout=300)
            await bot.send_message(
                group_id,
                f"{await celebrate_day()}\n"
                f"{datetime.now().day}.{datetime.now().month}.{datetime.now().year} "
                f"объявляется {y[0]}\nСправка по боту: /help",
            )

        elif x == 2:
            await dr()
            file1 = FSInputFile(r"Филч.jpg", "rb")
            y = ("Филч", file1)
            await value_plus_one("A1")
            await bot.send_photo(group_id, y[1], request_timeout=300)
            await bot.send_message(
                group_id,
                f"{await celebrate_day()}\n"
                f"{datetime.now().day}.{datetime.now().month}.{datetime.now().year} "
                f"объявляется {y[0]}\nСправка по боту: /help",
            )

        elif x == 3:
            await dr()
            file1 = FSInputFile(r"Серега.jpg", "rb")
            y = ("Серега", file1)
            await value_plus_one("A3")
            await bot.send_photo(group_id, y[1], request_timeout=300)
            await bot.send_message(
                group_id,
                f"{await celebrate_day()}\n"
                f"{datetime.now().day}.{datetime.now().month}.{datetime.now().year} "
                f"объявляется {y[0]}\nСправка по боту: /help",
            )

        elif x == 4:
            await dr()
            file1 = FSInputFile(r"Леха.jpg", "rb")
            y = ("Леха(Demix)", file1)
            await value_plus_one("A5")
            await bot.send_photo(group_id, y[1], request_timeout=300)
            await bot.send_message(
                group_id,
                f"{await celebrate_day()}\n"
                f"{datetime.now().day}.{datetime.now().month}.{datetime.now().year} "
                f"объявляется {y[0]}\nСправка по боту: /help",
            )

        elif x == 5:
            await dr()
            file1 = FSInputFile(r"фитиль.jpg", "rb")
            y = ("Леха(Фитиль)", file1)
            await value_plus_one("A6")
            await bot.send_photo(group_id, y[1], request_timeout=300)
            await bot.send_message(
                group_id,
                f"{await celebrate_day()}\n"
                f"{datetime.now().day}.{datetime.now().month}.{datetime.now().year} "
                f"объявляется {y[0]}\nСправка по боту: /help",
            )

        elif x == 6:
            await dr()
            file1 = FSInputFile(r"маугли.jpg", "rb")
            y = ("Диман", file1)
            await value_plus_one("A7")
            await bot.send_photo(group_id, y[1], request_timeout=300)
            await bot.send_message(
                group_id,
                f"{await celebrate_day()}\n"
                f"{datetime.now().day}.{datetime.now().month}.{datetime.now().year} "
                f"объявляется {y[0]}\nСправка по боту: /help",
            )

        elif x == 7:
            await dr()
            file1 = FSInputFile(r"саня.jpg", "rb")
            y = ("Саня", file1)
            await value_plus_one("A4")
            await bot.send_photo(group_id, y[1], request_timeout=300)
            await bot.send_message(
                group_id,
                f"{await celebrate_day()}\n"
                f"{datetime.now().day}.{datetime.now().month}.{datetime.now().year} "
                f"объявляется {y[0]}\nСправка по боту: /help",
            )

        elif x == 8:
            await dr()
            file1 = FSInputFile(r"Кирилл.jpg", "rb")
            y = ("Кирюха подкастер", file1)
            await value_plus_one("A8")
            await bot.send_photo(group_id, y[1], request_timeout=300)
            await bot.send_message(
                group_id,
                f"{await celebrate_day()}\n"
                f"{datetime.now().day}.{datetime.now().month}.{datetime.now().year} "
                f"объявляется {y[0]}\nСправка по боту: /help",
            )

        elif x == 9:
            await dr()
            file1 = FSInputFile(r"Женек.jpg", "rb")
            y = ("Женек спасатель", file1)
            await value_plus_one("A9")
            await bot.send_photo(group_id, y[1], request_timeout=300)
            await bot.send_message(
                group_id,
                f"{await celebrate_day()}\n"
                f"{datetime.now().day}.{datetime.now().month}.{datetime.now().year} "
                f"объявляется {y[0]}\nСправка по боту: /help",
            )

        elif x == 10:
            await dr()
            file1 = FSInputFile(r"Евгений.png", "rb")
            y = ("Женек старый", file1)
            await value_plus_one("A10")
            await bot.send_photo(group_id, y[1], request_timeout=300)
            await bot.send_message(
                group_id,
                f"{await celebrate_day()}\n"
                f"{datetime.now().day}.{datetime.now().month}.{datetime.now().year} "
                f"объявляется {y[0]}\nСправка по боту: /help",
            )
    except Exception as e:
        logger.exception("Ошибка в main/pidr", e)
        await bot.send_message(loggs_acc, f"Ошибка в main/pidr: {e}")


async def dr():
    try:
        await obnulenie_stat(bot)
        async with aiofiles.open("dr.json", "r", encoding="utf-8") as file:
            content = await file.read()
            data = json.loads(content)
        if f"{datetime.now().day}.{datetime.now().month}" in data:
            await Artur_happy_birthday(
                bot, text=data[f"{datetime.now().day}.{datetime.now().month}"]
            )
            # await Artur_pozdravlyaet(bot, text=data[f'{datetime.now().day}.{datetime.now().month}'])
            await bot.send_message(
                group_id, "твой подарок - https://www.youtube.com/watch?v=N6nJpNIK4PU"
            )
            await asyncio.sleep(0.3)
            await bot.send_message(group_id, "понравилось поздравление?")
        else:
            pass
    except Exception as e:
        logger.exception("Ошибка в main/dr", e)
        await bot.send_message(loggs_acc, f"Ошибка в main/dr: {e}")


@dp.callback_query(F.data)
async def check_callback(callback: CallbackQuery):
    try:
        if callback.data == "bof":
            start_file = FSInputFile(r"ball/start_image.png", "rb")
            await bot.send_photo(
                callback.message.chat.id, start_file, request_timeout=60
            )
            await bot.send_message(
                callback.message.chat.id,
                "Решил попытать удачу или просто переложить "
                "ответственность? Что ж.. Чтобы все прошло как надо "
                "просто переведи сотку моему создателю на сбер и "
                "погладь шар",
            )
            kb1 = types.ReplyKeyboardMarkup(
                resize_keyboard=True,
                row_width=1,
                keyboard=[
                    [types.KeyboardButton(text="Погладить шар")],
                    [types.KeyboardButton(text="Шар съебись")],
                ],
            )
            await bot.send_message(callback.message.chat.id, "...", reply_markup=kb1)
        elif callback.data == "stat_day":
            load_message = await bot.edit_message_text(
                "Загрузка..⏳", callback.message.chat.id, callback.message.message_id
            )
            kb2 = types.InlineKeyboardMarkup(
                row_width=1,
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="Статистика по месяцам", callback_data="stat_month"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="Статистика по годам", callback_data="stat_year"
                        )
                    ],
                ],
            )
            await bot.edit_message_text(
                await pstat("A"), callback.message.chat.id, load_message.message_id
            )
            await bot.edit_message_reply_markup(
                callback.message.chat.id, callback.message.message_id, reply_markup=kb2
            )
        elif callback.data == "stat_month":
            load_message = await bot.edit_message_text(
                "Загрузка..⏳", callback.message.chat.id, callback.message.message_id
            )
            kb2 = InlineKeyboardMarkup(
                row_width=1,
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="Статистика по дням", callback_data="stat_day"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="Статистика по годам", callback_data="stat_year"
                        )
                    ],
                ],
            )
            await bot.edit_message_text(
                await pstat("C"), callback.message.chat.id, load_message.message_id
            )
            await bot.edit_message_reply_markup(
                callback.message.chat.id, callback.message.message_id, reply_markup=kb2
            )
        elif callback.data == "stat_year":
            load_message = await bot.edit_message_text(
                "Загрузка..⏳", callback.message.chat.id, callback.message.message_id
            )
            kb2 = InlineKeyboardMarkup(
                row_width=1,
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="Статистика по дням", callback_data="stat_day"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="Статистика по месяцам", callback_data="stat_month"
                        )
                    ],
                ],
            )
            await bot.edit_message_text(
                await pstat("D"), callback.message.chat.id, load_message.message_id
            )
            await bot.edit_message_reply_markup(
                callback.message.chat.id, callback.message.message_id, reply_markup=kb2
            )
    except Exception as e:
        logger.exception("Ошибка в main/check_callback", e)
        await bot.send_message(loggs_acc, f"Ошибка в main/check_callback: {e}")


@dp.message(Command(commands="help"))
async def help(message):
    if message.chat.id == admin_id:
        await bot.send_message(
            message.chat.id,
            (
                "Основные команды поддерживаемые ботом:\n"
                "/orel - вызвать орловского помощника,\n"
                "/pidorstat - пидорский рейтинг,\n"
                "/start - инициализация бота,\n"
                "/help - справка по боту,\n"
                "/test - тестирование бота.\n"
                "/sent_message - отправка сообщения в группу.\n\n"
                "Для вызова Давинчи или Артура необходимо указать имя в сообщении.\n\n"
                "Для перевода воиса(длительность до 1 мин.) в текст ответьте на него "
                'словом "давинчи" или перешлите в личку боту.\n\n'
                "Для отправки фото/видео/документа в общую папку на яндекс отправьте "
                "необходимые файлы в личку боту."
            ),
        )
    else:
        await bot.send_message(
            message.chat.id,
            (
                "Основные команды поддерживаемые ботом:\n"
                "/pidorstat - пидорский рейтинг,\n"
                "/start - инициализация бота,\n"
                "/help - справка по боту,\n"
                "/test - тестирование бота.\n\n"
                "Для вызова Давинчи или Артура необходимо указать имя в сообщении.\n\n"
                "Для перевода воиса(длительность до 1 мин.) в текст ответьте на него "
                'словом "давинчи" или перешлите в личку боту.\n\n'
                "Для отправки фото/видео/документа в общую папку на яндекс отправьте "
                "необходимые файлы в личку боту."
            ),
        )


@dp.message(Command(commands="start"))
async def start(message):
    await bot.send_message(
        message.chat.id,
        """Бот уже инициализирован.
Я работаю по расписанию. Пидр дня назначается ежедневно в 11:00 по московскому времени

/help - справка по боту""",
    )


@dp.message(Command(commands="pidorstat"))
async def stat(message):
    try:
        b = await bot.send_message(message.chat.id, "Загрузка..⏳")
        kb2 = InlineKeyboardMarkup(
            row_width=1,
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Статистика по месяцам", callback_data="stat_month"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Статистика по годам", callback_data="stat_year"
                    )
                ],
            ],
        )
        await bot.edit_message_text(
            await pstat("A"), message.chat.id, b.message_id, reply_markup=kb2
        )
    except Exception as e:
        logger.exception("Ошибка в main/stat", e)
        await bot.send_message(loggs_acc, f"Ошибка в main/stat: {e}")


@dp.message(Command(commands="test"))
async def test(message):
    await bot.send_message(
        message.chat.id,
        """Протестируй себя петушок...А моя работа давно проверена и отлажена.

/help - справка по боту""",
    )


@dp.message(Command(commands="sent_message"))
async def sent_message(message, state: FSMContext):
    try:
        if message.chat.id == admin_id:
            await bot.send_message(admin_id, "Введите текст сообщения")
            await state.set_state(step_message.message)

        else:
            await bot.send_message(
                message.chat.id, "У Вас нет прав для использования данной команды"
            )
    except Exception as e:
        logger.exception("Ошибка в main/sent_message", e)
        await bot.send_message(loggs_acc, f"Ошибка в main/sent_message: {e}")


@dp.message(step_message.message)
async def perehvat(message, state: FSMContext):
    try:
        await bot.copy_message(group_id, admin_id, message.message_id)
        await Message.answer(message, text="сообщение отправлено", show_allert=True)
        await state.clear()
    except Exception as e:
        logger.exception("Ошибка в main/sent_message", e)
        await bot.send_message(loggs_acc, f"Ошибка в main/sent_message: {e}")


@dp.message(F.text)
async def chek_message(message):
    try:
        sosal_list = [
            "да",
            "Да",
            "Конечно",
            "конечно",
            "Очень",
            "очень",
            "Сильно",
            "сильно",
            "Великолепно",
            "великолепно",
            "Это было великолепно",
            "это было великолепно",
            "волшебно",
            "Волшебно",
            "Потрясающе",
            "потрясающе",
            "Хорошее",
            "хорошее",
        ]
        if (
            message.reply_to_message
            and message.reply_to_message.from_user.is_bot is True
        ):
            if "Нет" in message.text or "нет" in message.text:
                await message.reply("Пидора ответ")
            else:
                for i in sosal_list:
                    if i in message.text:
                        await bot.edit_message_text(
                            "Сосал?",
                            message.chat.id,
                            message.reply_to_message.message_id,
                        )
                pass
        elif message.text == "Погладить шар":
            await bot.send_photo(
                message.chat.id, await ball_of_fate(), request_timeout=60
            )
        elif message.text == "Шар съебись":
            kb2 = types.ReplyKeyboardRemove()
            await bot.send_message(message.chat.id, "...", reply_markup=kb2)
        elif "Давинчи" in message.text:
            try:
                if message.reply_to_message.voice.file_id:
                    await save_audio(bot, message.reply_to_message)
            except AttributeError:
                b = (
                    str(message.text)
                    .replace("Давинчи ", "", 1)
                    .replace("Давинчи, ", "", 1)
                    .replace("Давинчи,", "", 1)
                    .replace(" Давинчи", "", 1)
                )
                await Davinci(bot, message, b).answer()
            # else:
            #     await bot.send_message(message.chat.id, 'нет доступа')
        elif "давинчи" in message.text:
            try:
                if message.reply_to_message.voice.file_id:
                    await save_audio(bot, message.reply_to_message)
            except AttributeError:
                b = (
                    str(message.text)
                    .replace("давинчи ", "", 1)
                    .replace("давинчи, ", "", 1)
                    .replace("давинчи,", "", 1)
                    .replace(" давинчи", "", 1)
                )
                await Davinci(bot, message, b).answer()
            # else:
            #     await bot.send_message(message.chat.id, 'нет доступа')
        elif "Артур" in message.text:
            b = (
                str(message.text)
                .replace("Артур ", "", 1)
                .replace("Артур, ", "", 1)
                .replace("Артур,", "", 1)
                .replace(" Артур", "", 1)
            )
            if (
                message.reply_to_message
                and message.reply_to_message.from_user.is_bot is True
            ):
                try:
                    if "Нет" in b or "нет" in b:
                        await message.reply("Пидора ответ")
                    else:
                        for i in sosal_list:
                            if i in message.text:
                                await bot.edit_message_text(
                                    "Сосал?",
                                    message.chat.id,
                                    message.reply_to_message.message_id,
                                )
                        pass
                except AttributeError:
                    await Artur(bot, message, b)
            else:
                await Artur(bot, message, b)
        elif "артур" in message.text:
            b = (
                str(message.text)
                .replace("артур ", "", 1)
                .replace("артур, ", "", 1)
                .replace("артур,", "", 1)
                .replace(" артур", "", 1)
            )
            if (
                message.reply_to_message
                and message.reply_to_message.from_user.is_bot is True
            ):
                try:
                    if "Нет" in b or "нет" in b:
                        await message.reply("Пидора ответ")
                    else:
                        for i in sosal_list:
                            if i in message.text:
                                await bot.edit_message_text(
                                    "Сосал?",
                                    message.chat.id,
                                    message.reply_to_message.message_id,
                                )
                        pass
                except AttributeError:
                    await Artur(bot, message, b)
            else:
                await Artur(bot, message, b)
    except Exception as e:
        logger.exception("Ошибка в main/chek_message", e)
        await bot.send_message(loggs_acc, f"Ошибка в main/chek_message: {e}")


@dp.message(F.document, F.chat.type == "private")
async def chek_message_doc(v):
    try:
        await YaDisk(bot, v).save_doc()
    except Exception as e:
        logger.exception("Ошибка в main/chek_message_doc", e)
        await bot.send_message(loggs_acc, f"Ошибка в main/chek_message_doc: {e}")


@dp.message(F.photo, F.chat.type == "private")
async def chek_message_photo(v):
    try:
        await YaDisk(bot, v).save_photo()
    except Exception as e:
        logger.exception("Ошибка в main/chek_message_photo", e)
        await bot.send_message(loggs_acc, f"Ошибка в main/chek_message_photo: {e}")


@dp.message(F.video, F.chat.type == "private")
async def chek_message_video(v):
    try:
        await YaDisk(bot, v).save_video()
    except Exception as e:
        logger.exception("Ошибка в main/chek_message_video", e)
        await bot.send_message(loggs_acc, f"Ошибка в main/chek_message_video: {e}")


@dp.message(F.video_note, F.chat.type == "private")
async def chek_message_video_note(v):
    try:
        await YaDisk(bot, v).save_video_note()
    except Exception as e:
        logger.exception("Ошибка в main/chek_message_video_note", e)
        await bot.send_message(loggs_acc, f"Ошибка в main/chek_message_video_note: {e}")


@dp.message(F.voice, F.chat.type == "private")
async def chek_message_voice(v):
    try:
        await save_audio(bot, v)
    except Exception as e:
        logger.exception("Ошибка в main/chek_message_voice", e)
        await bot.send_message(loggs_acc, f"Ошибка в main/chek_message_voice: {e}")


async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        pidr, "cron", day_of_week="mon-sun", hour=8, misfire_grace_time=700
    )
    # scheduler.add_job(pidr, trigger="interval", seconds=15)
    scheduler.start()
    await dp.start_polling(bot, polling_timeout=20)


if __name__ == "__main__":
    try:
        logger.info("включение бота")
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.exception("выключение бота")
        asyncio.run(bot.send_message(loggs_acc, "выключение бота"))
