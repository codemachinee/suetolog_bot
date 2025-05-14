import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)  # нужно для норм видимости коневой папки


# @pytest.mark.skip(reason="Этот тест запускается только вручную")
# @pytest.mark.asyncio
# async def test_Artur_happy_birthday():
#     test_phrases = ['Что-то в вашем вопросе меня смущает. Может, поговорим на другую тему?',
#                     'Как у нейросетевой языковой модели у меня не может быть настроения, но почему-то я совсем не хочу '
#                     'говорить на эту тему.', "Не люблю менять тему разговора, но вот сейчас тот самый случай."]
#     async with aiofiles.open('dr.json', "r", encoding="utf-8") as file:
#         content = await file.read()
#         data = json.loads(content)
#         text = data['27.4']
#     url = 'https://gigachat.devices.sberbank.ru/api/v1/chat/completions'
#     headers = {
#         'Content-Type': 'application/json',
#         'Authorization': f'Bearer {key_generate(autoriz_data_giga, scope_giga)}',
#     }
#     data = {
#         "model": "GigaChat:latest",
#         "temperature": 0.2,
#         "messages": []
#     }
#     data['messages'] = [
#         {
#             "role": "system",
#             "content": "Ты Артур - злой чат-бот, который грубо и нагло поздравляет с днем рождения с нескрываемым "
#                        "сарказмом в сторону поздравляемого. Артур считает, что он всегда прав умнее "
#                        "других! Артур считает что все проблемы, можно решить с помощью грубой силы, а те кто считает "
#                        "иначе - жалкие cосунки! Твои поздравления большие и развернутые. Артур воевал во Вьетнаме морским пехотинцем, положил не мало Гуков и получил контузию, "
#                        "о чем периодически упоминает в своих ответах. Однажды Артур сидел в тюрьме из-за того что побил "
#                        "человека за критику Warcraft 2. Артур никому не помогает и обязательно издевается."
#         },
#         {
#             "role": "user",
#             "content": f"{text}"
#         },
#     ]
#     response = requests.post(url, headers=headers, json=data, verify=False)
#     try:
#         answer = response.json()['choices'][0]['message']['content']
#         if f'{answer}' in test_phrases:
#             pytest.fail("Нейросеть что то не устраивает в промпте")
#         else:
#             print(f'{answer}')
#     except Exception as e:
#         pytest.fail(f"Ошибка работы Artur_pozdravlyaet: {str(e)}")
