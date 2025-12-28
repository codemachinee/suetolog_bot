import ast
import json
import os
import sys

import aiofiles

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)  # нужно для норм видимости коневой папки

import pytest

# from unittest.mock import AsyncMock
# from aiogram import types

# from main import bot, start
#
#
# @pytest.mark.skip(reason="Этот тест запускается только вручную")
# # @pytest.mark.asyncio
# async def test_start_command():
#     # Создаем фиктивное сообщение
#     message = types.Message(
#         message_id=1,
#         date=0,
#         chat=types.Chat(id=123, type="private"),
#         from_user=types.User(id=456, is_bot=False, first_name="TestUser"),
#         text="/start"
#     )
#
#     # Мокаем объект бота и его метод send_message
#     bot.send_message = AsyncMock(return_value=None)
#
#     # Выполняем команду start
#     await start(message)
#
#     # Проверяем, что метод send_message был вызван с ожидаемыми параметрами
#     bot.send_message.assert_called_once_with(
#         123,  # ID чата
#         '''Бот уже инициализирован.
# Я работаю по расписанию. Пидр дня назначается ежедневно
# в 11:00 по московскому времени
#
# /help - справка по боту'''
#     )


@pytest.mark.asyncio
async def test_pidr():
    # Директория, где должны быть файлы
    # Парсит Python-файл и извлекает названия изображений из FSInputFile() в функции pidr().
    with open("main.py", "r", encoding="utf-8") as file:
        tree = ast.parse(file.read(), filename="main.py")  # Разбираем код в AST

    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "FSInputFile"
        ):
            if isinstance(
                node.args[0], ast.Constant
            ):  # Проверяем, что переданный аргумент — строка
                if "ball" in node.args[0].value:
                    pass
                else:
                    assert os.path.isfile(node.args[0].value), (
                        f"Файл {node.args[0].value} отсутствует в папке проекта"
                    )


@pytest.mark.asyncio
async def test_dr():
    test_dr_list = [
        "6.3",
        "20.4",
        "27.4",
        "5.5",
        "19.5",
        "15.6",
        "14.7",
        "16.7",
        "8.9",
        "17.11",
    ]
    async with aiofiles.open("dr.json", "r", encoding="utf-8") as file:
        content = await file.read()
        data = json.loads(content)
        for i in test_dr_list:
            if i in data:
                pass
            else:
                pytest.fail("Несоответствие списка дней рождений")
