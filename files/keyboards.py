from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# from datetime import datetime

start = types.ReplyKeyboardMarkup(resize_keyboard=True)
start.add('Написать новый пост')
start.add('Показать отложенные посты')

menu = types.ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
)
menu.add('Название')
menu.insert('Текст')
menu.insert('Фото')
menu.add('Гиперссылки')
menu.insert('Telegraph')
menu.add('Удалить все фото')
menu.insert('Предпросмотр')
menu.add('Удалить пост')
menu.insert('Расписание')
menu.add('Опубликовать сейчас')

next_state = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                       # one_time_keyboard=True,
                                       )
next_state.add('Принять')
next_state.add('Удалить все фото')
next_state.add('Удалить пост')

done = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
done.add('Опубликовать сейчас')
done.add('Расписание')
done.add('Редактировать пост')
done.add('Удалить пост')

sched = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
sched.add('Показать отложенные посты')
sched.add('Добавить текущий пост в расписание')
sched.add('Меню редактирования')

sched_edit = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
sched_edit.add('Редактировать время отправки')
sched_edit.add('Удалить пост из расписания')
sched_edit.add('Удалить пост полностью')
sched_edit.add('Главное меню')

favourite_but = InlineKeyboardButton('В избранное \U00002764', callback_data='favourite')
favourite = InlineKeyboardMarkup().add(favourite_but)

del_favourite = InlineKeyboardButton('Удалить из избранного \U0000274C', callback_data='delete_favourite')
delete_favourite = InlineKeyboardMarkup().add(del_favourite)


async def create_schedule(ids):
    a = []
    for x in ids:
        a.append(InlineKeyboardButton(text='"' + str(x.id) + '" ' + str(x.next_run_time.strftime("%d.%m.%y %H:%M")),
                                      callback_data=x.id))
    schedule_keyboard = InlineKeyboardMarkup(row_width=1).add(*a)
    return schedule_keyboard
