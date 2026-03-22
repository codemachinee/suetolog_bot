import os
import sys
from unittest.mock import MagicMock

import pytest

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)  # нужно для норм видимости коневой папки

import functions_file


@pytest.mark.asyncio
async def test_value_plus_one(monkeypatch):
    worksheet = MagicMock()
    worksheet.acell.return_value.value = "5"

    spreadsheet = MagicMock()
    spreadsheet.get_worksheet.return_value = worksheet

    client = MagicMock()
    client.open.return_value = spreadsheet

    monkeypatch.setattr(functions_file, "_build_gspread_client", lambda: client)

    await functions_file.value_plus_one("A2")

    client.open.assert_called_once_with("bot_statistic")
    spreadsheet.get_worksheet.assert_called_once_with(0)
    worksheet.acell.assert_called_once_with("A2")
    worksheet.update.assert_called_once_with("A2", "6")
