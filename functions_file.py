# библиотека работы с гугл таблицами
import gspread
# библиотека проверки даты
from datetime import datetime
# библиотека рандома
from random import *
from aiogram.types import FSInputFile

from paswords import *


# функция открывает гугл таблицу статистики, начисляет балл и возвращает новое значение
async def value_plus_one(j):
    gc = gspread.service_account(filename='pidor-of-the-day-af3dd140b860.json')
    sh = gc.open("bot_statistic")
    worksheet = sh.get_worksheet(0)
    worksheet.update(j, str(int(worksheet.acell(j).value) + 1))


# функция открывает гугл таблицу статистики и возвращает все значения в отсортированном виде
async def pstat(cell):
    gc = gspread.service_account(filename='pidor-of-the-day-af3dd140b860.json')
    sh = gc.open("bot_statistic")
    worksheet = sh.get_worksheet(0)
    d1 = [(int(worksheet.acell(f'{cell}1').value), "Филч"), (int(worksheet.acell(f'{cell}2').value), "Игорь"),
          (int(worksheet.acell(f'{cell}3').value), "Серега"), (int(worksheet.acell(f'{cell}4').value), "Саня"),
          (int(worksheet.acell(f'{cell}5').value), "Леха(Demix)"),
          (int(worksheet.acell(f'{cell}6').value), "Леха(Фитиль)"),
          (int(worksheet.acell(f'{cell}7').value), "Диман"),
          (int(worksheet.acell(f'{cell}8').value), "Кирюха подкастер"),
          (int(worksheet.acell(f'{cell}9').value), "Женек спасатель"),
          (int(worksheet.acell(f'{cell}10').value), "Женек старый")]
    d1_sort = sorted(d1, reverse=True)
    return (f'''РЕЙТИНГ ПИДАРАСОВ:

 1. {d1_sort[0][1]} -----> {d1_sort[0][0]} раз(а)
 2. {d1_sort[1][1]} -----> {d1_sort[1][0]} раз(а)
 3. {d1_sort[2][1]} -----> {d1_sort[2][0]} раз(а)
 4. {d1_sort[3][1]} -----> {d1_sort[3][0]} раз(а)
 5. {d1_sort[4][1]} -----> {d1_sort[4][0]} раз(а)
 6. {d1_sort[5][1]} -----> {d1_sort[5][0]} раз(а)
 7. {d1_sort[6][1]} -----> {d1_sort[6][0]} раз(а)
 8. {d1_sort[7][1]} -----> {d1_sort[7][0]} раз(а)
 9. {d1_sort[8][1]} -----> {d1_sort[8][0]} раз(а)
10. {d1_sort[9][1]} -----> {d1_sort[9][0]} раз(а)

Да здравствует наш чемпион {d1_sort[0][1]}! Его результативности 
может позавидовать Элтон Джон и другие Великие. Пожелаем
ему здоровья, успехов в личной жизни и новыйх побед.

/help - справка по боту''')


# функция обнуляющая все значения статистики в первый день нового месяца
async def obnulenie_stat(bot):
    champions = []
    if datetime.now().day == 1 and datetime.now().month != 1:
        gc = gspread.service_account(filename='pidor-of-the-day-af3dd140b860.json')
        sh = gc.open("bot_statistic")
        worksheet = sh.get_worksheet(0)
        d1 = [(int(worksheet.acell('A1').value), "Филч"), (int(worksheet.acell('A2').value), "Игорь"),
              (int(worksheet.acell('A3').value), "Серега"), (int(worksheet.acell('A4').value), "Саня"),
              (int(worksheet.acell('A5').value), "Леха(Demix)"), (int(worksheet.acell('A6').value), "Леха(Фитиль)"),
              (int(worksheet.acell('A7').value), "Диман"), (int(worksheet.acell('A8').value), "Кирюха подкастер"),
              (int(worksheet.acell('A9').value), "Женек спасатель"),
              (int(worksheet.acell('A10').value), "Женек старый")]
        d1_sort = sorted(d1, reverse=True)
        cells = worksheet.findall(str(d1_sort[0][0]), in_column=1)
        for cell in cells:
            worksheet.update(f'C{cell.row}', f'{int(worksheet.acell(f"C{cell.row}").value) + 1}')
            champions.append(str(worksheet.acell(f"B{cell.row}").value))
        if len(champions) == 1:
            await bot.send_message(group_id, f'''ИТОГИ МЕСЯЦА:

 1. {d1_sort[0][1]} -----> {d1_sort[0][0]} раз(а)
 2. {d1_sort[1][1]} -----> {d1_sort[1][0]} раз(а)
 3. {d1_sort[2][1]} -----> {d1_sort[2][0]} раз(а)
 4. {d1_sort[3][1]} -----> {d1_sort[3][0]} раз(а)
 5. {d1_sort[4][1]} -----> {d1_sort[4][0]} раз(а)
 6. {d1_sort[5][1]} -----> {d1_sort[5][0]} раз(а)
 7. {d1_sort[6][1]} -----> {d1_sort[6][0]} раз(а)
 8. {d1_sort[7][1]} -----> {d1_sort[7][0]} раз(а)
 9. {d1_sort[8][1]} -----> {d1_sort[8][0]} раз(а)
10. {d1_sort[9][1]} -----> {d1_sort[9][0]} раз(а)

Да здравствует наш чемпион месяца {d1_sort[0][1]}🎉🎉🎉! В тяжелейшей борьбе он таки вырвал свою заслуженную победу.
Пожелаем ему здоровья, успехов в личной жизни и новых побед.''')
        else:
            await bot.send_message(group_id, f'''ИТОГИ МЕСЯЦА:

 1. {d1_sort[0][1]} -----> {d1_sort[0][0]} раз(а)
 2. {d1_sort[1][1]} -----> {d1_sort[1][0]} раз(а)
 3. {d1_sort[2][1]} -----> {d1_sort[2][0]} раз(а)
 4. {d1_sort[3][1]} -----> {d1_sort[3][0]} раз(а)
 5. {d1_sort[4][1]} -----> {d1_sort[4][0]} раз(а)
 6. {d1_sort[5][1]} -----> {d1_sort[5][0]} раз(а)
 7. {d1_sort[6][1]} -----> {d1_sort[6][0]} раз(а)
 8. {d1_sort[7][1]} -----> {d1_sort[7][0]} раз(а)
 9. {d1_sort[8][1]} -----> {d1_sort[8][0]} раз(а)
10. {d1_sort[9][1]} -----> {d1_sort[9][0]} раз(а)

Да здравствуют наши чемпионы месяца {", ".join(champions)}! В тяжелейшей борьбе они таки вырвали свою заслуженную победу.
Пожелаем им здоровья, успехов в личной жизни и новых побед.''')
        worksheet.update('A1:A10', [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0]])
    elif datetime.now().day == 31 and datetime.now().month == 12:
        await bot.send_message(group_id, f'🚨🚨🚨Внимание!🚨🚨🚨 Пидр Клаус подводит итоги...\n'
                                         f'Кто же станет пидаром года?')
        file = FSInputFile(r'gif_mr.Bin.mp4', 'rb')
        await bot.send_video(group_id, file)
        gc = gspread.service_account(filename='pidor-of-the-day-af3dd140b860.json')
        sh = gc.open("bot_statistic")
        worksheet = sh.get_worksheet(0)
        d1 = [(int(worksheet.acell('C1').value), "Филч"), (int(worksheet.acell('C2').value), "Игорь"),
              (int(worksheet.acell('C3').value), "Серега"), (int(worksheet.acell('C4').value), "Саня"),
              (int(worksheet.acell('C5').value), "Леха(Demix)"), (int(worksheet.acell('C6').value), "Леха(Фитиль)"),
              (int(worksheet.acell('C7').value), "Диман"), (int(worksheet.acell('C8').value), "Кирюха подкастер"),
              (int(worksheet.acell('C9').value), "Женек спасатель"),
              (int(worksheet.acell('C10').value), "Женек старый")]
        d1_sort = sorted(d1, reverse=True)
        cells = worksheet.findall(str(d1_sort[0][0]), in_column=3)
        for cell in cells:
            worksheet.update(f'D{cell.row}', f'{int(worksheet.acell(f"D{cell.row}").value) + 1}')
            champions.append(str(worksheet.acell(f"B{cell.row}").value))
        if len(champions) == 1:
            await bot.send_message(group_id,
                                   f'🍾🍾🍾ии.. им становится {d1_sort[0][1]}! Самый главный пидрила черезвычайно'
                                   f' пидарского года!!! {d1_sort[0][1]} прийми наши поздравления, а также '
                                   f'обязательства по амбассадорству "Голубой устрицы". На ближайший год '
                                   f'на всех наших тусовках ты на разливе ибо больше всех заинтересован поскорее '
                                   f'споить пацанов. Тебе также полагается денежный приз в размере всех денег '
                                   f'накопленных в нашем фонде (в случае их отсутствия возмещаем глубоким '
                                   f'уважением. Хорошего нового года в новом статусе!')
            await bot.send_message(group_id, f'''ИТОГИ ГОДА:

 1. {d1_sort[0][1]} -----> {d1_sort[0][0]} раз(а) 🎉🎉🎉
 2. {d1_sort[1][1]} -----> {d1_sort[1][0]} раз(а)
 3. {d1_sort[2][1]} -----> {d1_sort[2][0]} раз(а)
 4. {d1_sort[3][1]} -----> {d1_sort[3][0]} раз(а)
 5. {d1_sort[4][1]} -----> {d1_sort[4][0]} раз(а)
 6. {d1_sort[5][1]} -----> {d1_sort[5][0]} раз(а)
 7. {d1_sort[6][1]} -----> {d1_sort[6][0]} раз(а)
 8. {d1_sort[7][1]} -----> {d1_sort[7][0]} раз(а)
 9. {d1_sort[8][1]} -----> {d1_sort[8][0]} раз(а)
10. {d1_sort[9][1]} -----> {d1_sort[9][0]} раз(а)

Да здравствует наш ПИДАРАС года {d1_sort[0][1]}! В тяжелейшей борьбе он таки вырвал свою заслуженную победу.
Пожелаем ему здоровья, успехов в личной жизни и новых побед.''')
            await bot.send_message(group_id, f'За тобой приехали..')
            file = FSInputFile(r'gif_zverev.mp4', 'rb')
            await bot.send_video(group_id, file)
        else:
            await bot.send_message(group_id,
                                   f'🍾🍾🍾ии.. ими становятся {", ".join(champions)}! Выдающиеся пидрилы черезвычайно'
                                   f' пидарского года!!! {", ".join(champions)} приймите наши поздравления, а также '
                                   f'обязательства по амбассадорству "Голубой устрицы". На ближайший год '
                                   f'на всех наших тусовках вы на разливе ибо больше всех заинтересованы поскорее '
                                   f'споить пацанов. Вам также полагается денежный приз в размере всех денег '
                                   f'накопленных в нашем фонде (в случае их отсутствия возмещаем глубоким '
                                   f'уважением. Хорошего Нового года в новом статусе!')
            await bot.send_message(group_id, f'''ИТОГИ ГОДА:

1. {d1_sort[0][1]} -----> {d1_sort[0][0]} раз(а)
2. {d1_sort[1][1]} -----> {d1_sort[1][0]} раз(а)
3. {d1_sort[2][1]} -----> {d1_sort[2][0]} раз(а)
4. {d1_sort[3][1]} -----> {d1_sort[3][0]} раз(а)
5. {d1_sort[4][1]} -----> {d1_sort[4][0]} раз(а)
6. {d1_sort[5][1]} -----> {d1_sort[5][0]} раз(а)
7. {d1_sort[6][1]} -----> {d1_sort[6][0]} раз(а)
8. {d1_sort[7][1]} -----> {d1_sort[7][0]} раз(а)
9. {d1_sort[8][1]} -----> {d1_sort[8][0]} раз(а)
10. {d1_sort[9][1]} -----> {d1_sort[9][0]} раз(а)

Да здравствует наши ПИДАРАСы года {", ".join(champions)}🎉🎉🎉! В тяжелейшей борьбе они таки вырвали свою заслуженную победу. 
Пожелаем им здоровья, успехов в личной жизни и новых побед.''')
            await bot.send_message(group_id, f'За вами приехали..')
            file = FSInputFile(r'gif_zverev.mp4', 'rb')
            await bot.send_video(group_id, file)
        worksheet.update('A1:A10', [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0]])
        worksheet.update('C1:C10', [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0]])


async def celebrate_day():
    if datetime.now().day == 31 and datetime.now().month == 12:
        return '🎉Новогодним пидарасом🎉'
    elif datetime.now().day == 7 and datetime.now().month == 1:
        return '🎉Рождественским пидарасом🎉'
    elif datetime.now().day == 14 and datetime.now().month == 1:
        return '🎉Староновогодним пидарасом🎉'
    elif datetime.now().day == 14 and datetime.now().month == 2:
        return '🎉Личным пидарасом Валентина🎉'
    elif datetime.now().day == 23 and datetime.now().month == 2:
        return '🎉Защищенным пидарасом🎉'
    elif datetime.now().day == 1 and datetime.now().month == 3:
        return '🎉Весенним пидарасом🎉'
    elif datetime.now().day == 8 and datetime.now().month == 3:
        return '🎉Международным женским пидарасом🎉'
    elif datetime.now().day == 1 and datetime.now().month == 5:
        return '🎉Мирным трудолюбивым и майским пидарасом🎉'
    elif datetime.now().day == 1 and datetime.now().month == 6:
        return '🎉Летним пидарасом🎉'
    elif datetime.now().day == 1 and datetime.now().month == 9:
        return '🎉Школьным осенним пидарасом🎉'
    elif datetime.now().day == 4 and datetime.now().month == 11:
        return '🎉Народным пидарасом🎉'
    elif datetime.now().day == 1 and datetime.now().month == 12:
        return '🎉Зимним пидарасом🎉'
    else:
        return 'Пидарасом дня'


# функция шара судьбы
async def ball_of_fate():
    ball_choice = choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    if ball_choice == 1:
        ball_answer = FSInputFile(r"ball/var_one.png", 'rb')
        return ball_answer
    elif ball_choice == 2:
        ball_answer = FSInputFile(r"ball/var_two.png", 'rb')
        return ball_answer
    elif ball_choice == 3:
        ball_answer = FSInputFile(r"ball/var_tree.png", 'rb')
        return ball_answer
    elif ball_choice == 4:
        ball_answer = FSInputFile(r"ball/var_four.png", 'rb')
        return ball_answer
    elif ball_choice == 5:
        ball_answer = FSInputFile(r"ball/var_five.png", 'rb')
        return ball_answer
    elif ball_choice == 6:
        ball_answer = FSInputFile(r"ball/var_six.png", 'rb')
        return ball_answer
    elif ball_choice == 7:
        ball_answer = FSInputFile(r"ball/var_seven.png", 'rb')
        return ball_answer
    elif ball_choice == 8:
        ball_answer = FSInputFile(r"ball/var_eight.png", 'rb')
        return ball_answer
    elif ball_choice == 9:
        ball_answer = FSInputFile(r"ball/var_nine.png", 'rb')
        return ball_answer
    elif ball_choice == 10:
        ball_answer = FSInputFile(r"ball/var_ten.png", 'rb')
        return ball_answer
    elif ball_choice == 11:
        ball_answer = FSInputFile(r"ball/var_eleven.png", 'rb')
        return ball_answer