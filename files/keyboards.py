from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

kb_start = types.ReplyKeyboardMarkup(resize_keyboard=True)
kb_start.add('Написать новый пост')

kb_parts = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_parts.insert('Название')
kb_parts.insert('Текст')
kb_parts.insert('Фото')
kb_parts.add('Предпросмотр поста')
kb_parts.add('Удалить пост')

kb_next = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_next.add('Принять')
kb_next.add('Удалить пост')

kb_done = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_done.add('Отправить пост')
kb_done.add('Редактировать пост')
kb_done.add('Удалить пост')

inline_btn_1 = InlineKeyboardButton('/start', callback_data='button1')
inline_btn_2 = InlineKeyboardButton('/add', callback_data='button2')
inline_btn_3 = InlineKeyboardButton('Третья кнопка!', callback_data='button3')
favourite = InlineKeyboardButton('Избранное', callback_data='favourite')
inline_favrt = InlineKeyboardMarkup().add(favourite)
del_fvrt = InlineKeyboardButton('Удалить из избранного', callback_data='favourite')
inline_del_fvrt = InlineKeyboardMarkup().add(del_fvrt)
inline_start = InlineKeyboardMarkup().add(inline_btn_1, inline_btn_2)
