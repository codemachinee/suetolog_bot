import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # нужно для норм видимости коневой папки

import pytest
import gspread


# @pytest.mark.skip(reason="Этот тест запускается только вручную")
@pytest.mark.asyncio
async def test_value_plus_one():
    try:
        with open('pidor-of-the-day-af3dd140b860.json', 'r') as f:
            content = f.read()
            print("Содержимое файла JSON:\n", content)
        gc = gspread.service_account(filename='pidor-of-the-day-af3dd140b860.json')
        # Пытаемся открыть таблицу "bot_statistic"
        sh = gc.open("bot_statistic")

        # Пытаемся получить первый лист (worksheet)
        worksheet = sh.get_worksheet(0)
        assert worksheet is not None
        print("Подключение к таблице успешно!")

    except gspread.SpreadsheetNotFound:
        pytest.fail("Таблица 'bot_statistic' не найдена.")
    except Exception as e:
        pytest.fail(f"Ошибка при подключении к таблице: {str(e)}")
