import os
import sys

import aiohttp
import pytest

from paswords import yandex_gpt_api_key, yandex_gpt_catalog_id
from yandex_services import y

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)  # нужно для норм видимости коневой папки
# from paswords import yandex_gpt_catalog_id, yandex_gpt_api_key
#
#
# @pytest.mark.skip(reason="Этот тест запускается только вручную")
# # @pytest.mark.asyncio
# async def test_artur_pozdravlyaet():
#     test_phrases = ["В интернете есть много сайтов с информацией на эту тему. [Посмотрите, что нашлось в "
#                     "поиске](https://ya.ru)"]
#     async with aiofiles.open('dr.json', "r", encoding="utf-8") as file:
#         content = await file.read()
#         data = json.loads(content)
#         text = data['6.3']
#     prompt = {
#         "modelUri": f"gpt://{yandex_gpt_catalog_id}/yandexgpt",
#         "completionOptions": {
#             "stream": False,
#             "temperature": 0.5,
#             "maxTokens": "2000"
#         },
#         "messages": [
#             {
#                 "role": "system",
#                 "text": f"Ты Артур, бот который профессионально в сатирической форме, развернуто поздравляет с днем "
#                         f"рождения"
#                         f" и обязательно дерзко пошутишь над виновником торжества. Ты всегда "
#                         f"обращаешься к поздравляемым на 'Ты'."
#             },
#             {
#                 "role": "user",
#                 "text": f'{text}'
#             },
#         ]
#     }
#
#     url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": f"Api-Key {yandex_gpt_api_key}"
#     }
#     async with aiohttp.ClientSession() as session:
#         async with session.post(url, headers=headers, json=prompt, ssl=False) as response:
#             try:
#                 answer = (await response.json())['result']['alternatives'][0]['message']['text']
#                 if f'{answer}' in test_phrases:
#                     pytest.fail(f"Нейросеть что то не устраивает в промпте")
#                 else:
#                     print(f'{answer}')
#             except Exception as e:
#                 pytest.fail(f"Ошибка работы Artur_pozdravlyaet: {str(e)}")


@pytest.mark.asyncio
async def test_yadisk():
    if y.check_token() is True:
        pass
    else:
        pytest.fail("Токен яндекс диска не валиден")


@pytest.mark.asyncio
async def test_yagpt():
    prompt = {
        "modelUri": f"gpt://{yandex_gpt_catalog_id}/yandexgpt",
        "completionOptions": {"stream": False, "temperature": 0.2, "maxTokens": "10"},
        "messages": [{"role": "system", "text": "тест"}],
    }
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {yandex_gpt_api_key}",
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url, headers=headers, json=prompt, ssl=False
        ) as response:
            answer = await response.json()
            keys_list = list(answer.keys())
            if "result" in keys_list:
                pass
            elif "error" in keys_list:
                if "Unknown api key" in answer["error"]["message"]:
                    pytest.fail("неверный yandex_gpt_api_key")
                elif "Specified folder ID" in answer["error"]["message"]:
                    pytest.fail("неверный yandex_gpt_catalog_id")
                else:
                    pytest.fail("не валидные параметры авторизации")
            else:
                pytest.fail("Не известная ошибка при проверке подключения yagpt")
