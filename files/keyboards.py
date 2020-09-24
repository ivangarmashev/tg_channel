from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start = types.ReplyKeyboardMarkup(resize_keyboard=True)
start.add('Написать новый пост')

menu = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                 one_time_keyboard=True,
                                 )
menu.insert('Название')
menu.insert('Текст')
menu.add('Фото')
menu.insert('Гиперссылки')
menu.add('Предпросмотр')
menu.insert('Удалить пост')
menu.add('Опубликовать пост в канал')

next_state = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
next_state.add('Принять')
next_state.add('Удалить пост')

done = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
done.add('Отправить пост')
done.add('Редактировать пост')
done.add('Удалить пост')

inline_btn_1 = InlineKeyboardButton('/start', callback_data='button1')
inline_btn_2 = InlineKeyboardButton('/add', callback_data='button2')
inline_btn_3 = InlineKeyboardButton('Третья кнопка!', callback_data='button3')

favourite_but = InlineKeyboardButton('Избранное', callback_data='favourite')
favourite = InlineKeyboardMarkup().add(favourite_but)

del_favourite = InlineKeyboardButton('Удалить из избранного', callback_data='delete_favourite')
delete_favourite = InlineKeyboardMarkup().add(del_favourite)

inline_start = InlineKeyboardMarkup().add(inline_btn_1, inline_btn_2)
