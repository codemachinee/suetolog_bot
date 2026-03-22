import asyncio
import json
import logging
from datetime import datetime
from random import choice

import aiofiles  # -*- coding: utf-8 -*-
from aiohttp import ClientError
from aiogram import Bot, Dispatcher, F, Router, types
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.exceptions import TelegramNetworkError, TelegramServerError
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    BotCommand,
    CallbackQuery,
    ErrorEvent,
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
from kinophiles import handlers as kinophiles_handlers
from kinophiles.db import init_db
from kinophiles.handlers import _start_kinophiles_private
from paswords import admin_id, group_id, loggs_acc, major_suetolog, codemashine_test
from SaluteSpeech import (
    Artur,
    Artur_happy_birthday,
    save_audio,
)
from yandex_services import Davinci, YaDisk

# token = lemonade
# token = codemashine_test
token = major_suetolog

BOT_API_TIMEOUT_SECONDS = 90
POLLING_TIMEOUT_SECONDS = 60
NETWORK_NOTICE_COOLDOWN_SECONDS = 120
NETWORK_ISSUE_TEXT = (
    "Сейчас временные проблемы с сетью до Telegram. "
    "Запрос может выполняться дольше обычного, попробуйте повторить через 1-2 минуты."
)

bot_session = AiohttpSession(timeout=BOT_API_TIMEOUT_SECONDS)
bot = Bot(token=token, session=bot_session)
dp = Dispatcher()
main_router = Router()
_last_network_notice_by_chat: dict[int, datetime] = {}

# Подключаем роутеры в правильном порядке
dp.include_router(kinophiles_handlers.kinophiles_router)
dp.include_router(main_router)


# Включаем DEBUG-логирование для aiogram
# logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig(level=logging.INFO)  # Отключено для вывода только в файл

logger.remove()
# Настраиваем логирование в файл с ограничением количества файлов
logger.add(
    "loggs.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="DEBUG",  # <--- Уровень изменен на DEBUG
    # level="INFO",  # <--- Меняем уровень на INFO
    rotation="5 MB",  # Ротация файла каждые 10 MB
    retention="10 days",  # Хранить только 5 последних логов
    compression="zip",  # Сжимать старые логи в архив
    backtrace=True,  # Сохранение трассировки ошибок
    diagnose=True,  # Подробный вывод
)


def _is_temporary_network_issue(exception: Exception) -> bool:
    if isinstance(
        exception,
        (TelegramNetworkError, TelegramServerError, asyncio.TimeoutError, TimeoutError, ClientError),
    ):
        return True

    exception_text = str(exception).lower()
    return any(
        network_hint in exception_text
        for network_hint in ("timeout", "timed out", "network", "connection")
    )


async def _safe_send_log_message(text: str) -> None:
    try:
        await bot.send_message(loggs_acc, text, request_timeout=BOT_API_TIMEOUT_SECONDS)
    except Exception as e:
        logger.warning(f"Не удалось отправить сообщение в лог-чат: {e}")


def _extract_chat_id(event: ErrorEvent) -> int | None:
    update = event.update
    if update.message:
        return update.message.chat.id
    if update.callback_query and update.callback_query.message:
        return update.callback_query.message.chat.id
    if update.edited_message:
        return update.edited_message.chat.id
    if update.channel_post:
        return update.channel_post.chat.id
    return None


async def _notify_network_issue_if_needed(chat_id: int) -> None:
    now = datetime.now()
    last_notice_at = _last_network_notice_by_chat.get(chat_id)
    if (
        last_notice_at
        and (now - last_notice_at).total_seconds() < NETWORK_NOTICE_COOLDOWN_SECONDS
    ):
        return

    _last_network_notice_by_chat[chat_id] = now
    try:
        await bot.send_message(
            chat_id,
            NETWORK_ISSUE_TEXT,
            request_timeout=BOT_API_TIMEOUT_SECONDS,
        )
    except Exception as notify_error:
        logger.warning(
            f"Не удалось уведомить chat_id={chat_id} о сетевой проблеме: {notify_error}"
        )


@dp.error()
async def handle_network_errors(event: ErrorEvent):
    exception = event.exception
    if not isinstance(exception, Exception):
        return False

    if not _is_temporary_network_issue(exception):
        return False

    chat_id = _extract_chat_id(event)
    logger.warning(f"Временная сетевая ошибка при обработке update: {exception}")
    if chat_id is not None:
        await _notify_network_issue_if_needed(chat_id)

    return True

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
        if _is_temporary_network_issue(e):
            await _notify_network_issue_if_needed(group_id)
        await _safe_send_log_message(f"Ошибка: {e}")


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
        await _safe_send_log_message(f"Ошибка: {e}")


@main_router.callback_query(F.data.in_({"bof", "stat_day", "stat_month", "stat_year"}))
async def check_callback(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    try:
        if callback.data == "bof":
            if callback.message:
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
                await bot.send_message(
                    callback.message.chat.id, "...", reply_markup=kb1
                )
        elif callback.data == "stat_day":
            if callback.message:
                load_message = await bot.edit_message_text(
                    "Загрузка..⏳",
                    callback.message.chat.id,
                    callback.message.message_id,
                )
                if isinstance(load_message, Message):
                    kb2 = types.InlineKeyboardMarkup(
                        row_width=1,
                        inline_keyboard=[
                            [
                                InlineKeyboardButton(
                                    text="Статистика по месяцам",
                                    callback_data="stat_month",
                                )
                            ],
                            [
                                InlineKeyboardButton(
                                    text="Статистика по годам",
                                    callback_data="stat_year",
                                )
                            ],
                        ],
                    )
                    await bot.edit_message_text(
                        await pstat("A"),
                        callback.message.chat.id,
                        load_message.message_id,
                    )
                    await bot.edit_message_reply_markup(
                        callback.message.chat.id,
                        callback.message.message_id,
                        reply_markup=kb2,
                    )
        elif callback.data == "stat_month":
            if callback.message:
                load_message = await bot.edit_message_text(
                    "Загрузка..⏳",
                    callback.message.chat.id,
                    callback.message.message_id,
                )
                if isinstance(load_message, Message):
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
                                    text="Статистика по годам",
                                    callback_data="stat_year",
                                )
                            ],
                        ],
                    )
                    await bot.edit_message_text(
                        await pstat("C"),
                        callback.message.chat.id,
                        load_message.message_id,
                    )
                    await bot.edit_message_reply_markup(
                        callback.message.chat.id,
                        callback.message.message_id,
                        reply_markup=kb2,
                    )
        elif callback.data == "stat_year":
            if callback.message:
                load_message = await bot.edit_message_text(
                    "Загрузка..⏳",
                    callback.message.chat.id,
                    callback.message.message_id,
                )
                if isinstance(load_message, Message):
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
                                    text="Статистика по месяцам",
                                    callback_data="stat_month",
                                )
                            ],
                        ],
                    )
                    await bot.edit_message_text(
                        await pstat("D"),
                        callback.message.chat.id,
                        load_message.message_id,
                    )
                    await bot.edit_message_reply_markup(
                        callback.message.chat.id,
                        callback.message.message_id,
                        reply_markup=kb2,
                    )
    except Exception as e:
        logger.exception("Ошибка в main/check_callback", e)
        await _safe_send_log_message(f"Ошибка: {e}")


@main_router.message(Command(commands="help"))
async def help(message, state: FSMContext):
    await state.clear()
    if message.chat.id == admin_id:
        await bot.send_message(
            message.chat.id,
            (
                "Основные команды поддерживаемые ботом:\n"
                "/pidorstat - пидорский рейтинг,\n"
                "/start - инициализация бота,\n"
                "/help - справка по боту,\n"
                "/test - тестирование бота.\n"
                "/sent_message - отправка сообщения в группу.\n"
                "/kinophiles - списки фильмов и сериалов пользователей\n\n"
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
                "/test - тестирование бота.\n"
                "/kinophiles - списки фильмов и сериалов пользователей\n\n"
                "Для вызова Давинчи или Артура необходимо указать имя в сообщении.\n\n"
                "Для перевода воиса(длительность до 1 мин.) в текст ответьте на него "
                'словом "давинчи" или перешлите в личку боту.\n\n'
                "Для отправки фото/видео/документа в общую папку на яндекс отправьте "
                "необходимые файлы в личку боту."
            ),
        )


@main_router.message(Command(commands="start"))
async def start(message: Message, state: FSMContext, command: CommandObject):
    """
    Обработчик команды /start.
    Поддерживает deep link для функции 'Кинофилы'.
    """
    # Если команда вызвана с аргументом 'kinophiles' (deep link)
    if command.args == "kinophiles":
        # Убедимся, что это личный чат
        if message.chat.type == "private":
            # Запускаем сценарий для кинофилов
            await _start_kinophiles_private(message, state)
    else:
        # Стандартное поведение /start
        await state.clear()
        await bot.send_message(
            message.chat.id,
            """Бот уже инициализирован.
Я работаю по расписанию. Пидор дня назначается ежедневно в 11:00 по московскому времени

/help - справка по боту""",
        )


@main_router.message(Command(commands="pidorstat"))
async def stat(message, state: FSMContext):
    await state.clear()
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
        if _is_temporary_network_issue(e):
            await _notify_network_issue_if_needed(message.chat.id)
        else:
            await bot.send_message(
                message.chat.id,
                "Не удалось получить статистику. Попробуй чуть позже.",
                request_timeout=BOT_API_TIMEOUT_SECONDS,
            )
        await _safe_send_log_message(f"Ошибка: {e}")


@main_router.message(Command(commands="test"))
async def test(message, state: FSMContext):
    await state.clear()
    await bot.send_message(
        message.chat.id,
        """Протестируй себя петушок...А моя работа давно проверена и отлажена.

/help - справка по боту""",
    )


@main_router.message(Command(commands="sent_message"))
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
        await _safe_send_log_message(f"Ошибка: {e}")


@main_router.message(step_message.message)
async def perehvat(message, state: FSMContext):
    try:
        await bot.copy_message(group_id, admin_id, message.message_id)
        await Message.answer(message, text="сообщение отправлено", show_alert=True)
        await state.clear()
    except Exception as e:
        logger.exception("Ошибка в main/sent_message", e)
        await _safe_send_log_message(f"Ошибка: {e}")


@main_router.message(F.text)
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
        await _safe_send_log_message(f"Ошибка: {e}")


@main_router.message(F.document, F.chat.type == "private")
async def chek_message_doc(v):
    try:
        await YaDisk(bot, v).save_doc()
    except Exception as e:
        logger.exception("Ошибка в main/chek_message_doc", e)
        await _safe_send_log_message(f"Ошибка: {e}")


@main_router.message(F.photo, F.chat.type == "private")
async def chek_message_photo(v):
    try:
        await YaDisk(bot, v).save_photo()
    except Exception as e:
        logger.exception("Ошибка в main/chek_message_photo", e)
        await _safe_send_log_message(f"Ошибка: {e}")


@main_router.message(F.video, F.chat.type == "private")
async def chek_message_video(v):
    try:
        await YaDisk(bot, v).save_video()
    except Exception as e:
        logger.exception("Ошибка в main/chek_message_video", e)
        await _safe_send_log_message(f"Ошибка: {e}")


@main_router.message(F.video_note, F.chat.type == "private")
async def chek_message_video_note(v):
    try:
        await YaDisk(bot, v).save_video_note()
    except Exception as e:
        logger.exception("Ошибка в main/chek_message_video_note", e)
        await _safe_send_log_message(f"Ошибка: {e}")


@main_router.message(F.voice, F.chat.type == "private")
async def chek_message_voice(v):
    try:
        await save_audio(bot, v)
    except Exception as e:
        logger.exception("Ошибка в main/chek_message_voice", e)
        await _safe_send_log_message(f"Ошибка: {e}")


# --- Асинхронная функция для установки команд бота в меню Telegram ---
async def set_commands():
    """
    Устанавливает список команд, которые будут отображаться в меню бота Telegram.
    """
    commands = [
        BotCommand(command="start", description="запуск/перезапуск бота"),
        BotCommand(command="test", description="тестирование бота"),
        BotCommand(command="help", description="справка по боту"),
        BotCommand(command="pidorstat", description="рейтинг пидорасов"),
        BotCommand(
            command="kinophiles", description="списки фильмов и сериалов пользователей"
        ),
    ]
    await bot.set_my_commands(commands, request_timeout=BOT_API_TIMEOUT_SECONDS)


async def main():
    await init_db()
    try:
        await set_commands()
    except Exception as e:
        if _is_temporary_network_issue(e):
            logger.warning(f"Не удалось установить команды бота из-за сети: {e}")
            await _safe_send_log_message(f"Проблемы сети при set_commands: {e}")
        else:
            raise

    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        pidr, "cron", day_of_week="mon-sun", hour=8, misfire_grace_time=700
    )
    # scheduler.add_job(pidr, trigger="interval", seconds=15)
    scheduler.start()
    await dp.start_polling(bot, polling_timeout=POLLING_TIMEOUT_SECONDS)


if __name__ == "__main__":
    try:
        logger.info("включение бота")
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.exception("выключение бота")
        asyncio.run(_safe_send_log_message("выключение бота"))

