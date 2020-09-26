from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start = types.ReplyKeyboardMarkup(resize_keyboard=True)
start.add('Написать новый пост')
start.add('Показать отложенные посты')

menu = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                 one_time_keyboard=True,
                                 )
menu.insert('Название')
menu.add('Текст')
menu.add('Гиперссылки')
menu.add('Фото')
menu.add('Предпросмотр')
menu.add('Удалить пост')
menu.add('Удалить фото')
menu.add('Расписание')
menu.add('Опубликовать сейчас')

next_state = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
next_state.add('Принять')
next_state.add('Удалить фото')
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

inline_btn_1 = InlineKeyboardButton('/start', callback_data='button1')
inline_btn_2 = InlineKeyboardButton('/add', callback_data='button2')
inline_btn_3 = InlineKeyboardButton('Третья кнопка!', callback_data='button3')

favourite_but = InlineKeyboardButton('Избранное', callback_data='favourite')
favourite = InlineKeyboardMarkup().add(favourite_but)

del_favourite = InlineKeyboardButton('Удалить из избранного', callback_data='delete_favourite')
delete_favourite = InlineKeyboardMarkup().add(del_favourite)

inline_start = InlineKeyboardMarkup().add(inline_btn_1, inline_btn_2)
