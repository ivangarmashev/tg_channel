from aiogram.dispatcher import FSMContext
import io
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.markdown import hide_link
from aiogram.utils import exceptions
from files import mysql_use as db
from files import telegraph_use as tgh
from files.bot_states import *
from files.connections import *
import files.keyboards as kb
from aiogram import types
import os

from datetime import datetime, timedelta
from files import all_states as ast


@dp.message_handler(text='Главное меню', state=ast.all_state, content_types=types.ContentTypes.TEXT)
async def show_start_message(message: types.Message, state: FSMContext):
    await message.answer(text='Принято!', reply_markup=kb.start)
    await state.set_state('States:menu')


@dp.message_handler(text='Меню редактирования', state=ast.all_state, content_types=types.ContentTypes.TEXT)
@dp.message_handler(text='Меню', state=ast.all_state, content_types=types.ContentTypes.TEXT)
@dp.message_handler(text='Принять', state=ast.all_state, content_types=types.ContentTypes.TEXT)
async def show_message(message: types.Message, state: FSMContext):
    if message.text == 'Принять':
        await message.answer(text='Принято!', reply_markup=kb.menu)
    else:
        await message.answer(text='Открываю меню', reply_markup=kb.menu)
    await state.set_state('States:menu')


@dp.message_handler(commands=['start'], state="*")
async def send_welcome(message: types.Message, state: FSMContext):
    await message.reply('Поздравляем! \n'
                        'Теперь Вы можете использовать избранное в чате! \n'
                        'Места, которые вы отметили избранными, будут появляться здесь)')


@dp.message_handler(text='Написать новый пост', state=ast.all_state)
async def main_menu(message: types.Message, state: FSMContext):
    await message.answer(text='Добавить/отредактировать:', reply_markup=kb.menu)
    await state.reset_data()
    tgh.delete_media()
    await state.set_state('States:menu')


@dp.message_handler(text='Название', state=ast.without_name)
async def main_menu(message: types.Message, state: FSMContext):
    ReplyKeyboardRemove()
    await bot.send_message(chat_id=message.from_user.id, text='Введите название:')
    await state.set_state('States:add_name')


@dp.message_handler(text='Текст', state=ast.without_text)
async def main_menu(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id=message.from_user.id, text='Введите текст:')
    await state.set_state('States:add_text')


@dp.message_handler(text='Гиперссылки', state=ast.without_hyperlinks)
async def main_menu(message: types.Message, state: FSMContext):
    await message.answer(text='Введите ссылки в формате HTML:')
    await message.answer(text='<a href="url">Txt</a>')
    await state.set_state('States:add_hyperlinks')


@dp.message_handler(text='Telegraph', state=ast.without_tgh_text)
async def telegraph(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id=message.from_user.id, text='Введите текст для Telegraph:')
    await state.set_state('States:add_telegraph_text')


@dp.message_handler(text='Фото', state=ast.all_state)
async def main_menu(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Отравьте фото и нажмите "Принять"',
                           reply_markup=kb.next_state)
    await state.update_data(link=None)
    await state.set_state('States:add_photo')


@dp.message_handler(state=States.add_name)
async def main_menu(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    print('name', message.text)
    await bot.send_message(chat_id=message.from_user.id, text='Принято!', reply_markup=kb.menu, )
    await state.set_state('States:menu')


@dp.message_handler(state=States.add_text)
async def main_menu(message: types.Message, state: FSMContext):
    print('text', message.text)
    await state.update_data(text=message.text)
    await bot.send_message(chat_id=message.from_user.id, text='Принято!', reply_markup=kb.menu)
    await state.set_state('States:menu')


@dp.message_handler(state=States.add_hyperlinks)
async def main_menu(message: types.Message, state: FSMContext):
    print('text', message.text)
    await state.update_data(hyperlinks=message.text)
    await bot.send_message(chat_id=message.from_user.id, text='Принято!', reply_markup=kb.menu)
    await state.set_state('States:menu')


@dp.message_handler(state=States.add_telegraph_text)
async def main_menu(message: types.Message, state: FSMContext):
    print('tgh text', message.text)
    await state.update_data(tgh_text=message.text, link=None)
    await bot.send_message(chat_id=message.from_user.id, text='Принято!', reply_markup=kb.menu)
    await state.set_state('States:menu')


@dp.message_handler(state=States.add_photo, content_types=types.ContentTypes.PHOTO)
async def main_menu(message: types.Message, state: FSMContext):
    print(len(message.photo) - 1)
    file_info = await bot.get_file(message.photo[len(message.photo) - 1].file_id)
    downloaded_file = await bot.download_file_by_id(file_info.file_id)
    downloaded_file = io.BytesIO.read(downloaded_file)
    if message.caption is None:
        message.caption = ''

    src = 'media/' + str(len(os.listdir('media'))) + '@' + str(message.caption) + '.jpg'
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)


@dp.message_handler(text='Предпросмотр', state=ast.all_state, content_types=types.ContentTypes.TEXT)
async def show_message(message: types.Message, state: FSMContext):
    data = await state.get_data()
    print(data.get('name'))
    if data.get('name') is None:
        await message.answer('Вы не добавили название, введите его:')
        await state.set_state('States:add_name')
        return

    elif data.get('text') is None:
        await message.answer('Вы не добавили текст, введите его:')
        await state.set_state('States:add_text')
        return

    elif data.get('hyperlinks') is None:
        await message.answer('Вы не добавили гиперссылки, введите их:')
        await state.set_state('States:add_hyperlinks')
        return

    elif data.get('link') is None:
        await message.answer('Загружаю фото..')
        if data.get('tgh_text') is not None:
            link = tgh.create_site(name=data['name'], text=data['tgh_text'])
        else:
            link = tgh.create_site(name=data['name'])
        if link == -1:
            await message.answer('Вы не добавили фото для Telegraph')
            await message.answer('Добавте их прямо сейчас и нажмите принять:', reply_markup=kb.next_state)
            await state.set_state('States:add_photo')
            return
        await state.update_data(link=link)
    else:
        link = data['link']

    text = '<b>' + data['name'] + '</b>' + '\n' \
           + hide_link(link) + data['hyperlinks'] + '\n' \
           + '\n' + data['text']

    await message.answer('Предпросмотр поста:')
    await message.answer(text=text, parse_mode='HTML', reply_markup=kb.done, )


@dp.message_handler(text='Редактировать пост', state=ast.all_state, content_types=types.ContentTypes.TEXT)
async def show_message(message: types.Message, state: FSMContext):
    await message.answer('Что именно вы хотите отредактировать?', reply_markup=kb.menu)


@dp.message_handler(text='Удалить пост', state=ast.all_state, content_types=types.ContentTypes.TEXT)
async def show_message(message: types.Message, state: FSMContext):
    await state.reset_data()
    tgh.delete_media()
    await bot.send_message(chat_id=message.from_user.id,
                           text='Информация для поста очищена, вы можете создать новый',
                           reply_markup=kb.start)


@dp.message_handler(text='Удалить все фото', state=ast.all_state, content_types=types.ContentTypes.TEXT)
async def show_message(message: types.Message, state: FSMContext):
    tgh.delete_media()
    await state.update_data(link=None)
    await bot.send_message(chat_id=message.from_user.id,
                           text='Фото удалены, можете добавить новые',
                           reply_markup=kb.menu)


@dp.message_handler(text='Опубликовать сейчас', state=ast.all_state, content_types=types.ContentTypes.TEXT)
async def show_message(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if data.get('name') is None:
        await message.answer('Вы не добавили название, введите его:')
        await state.set_state('States:add_name')
        return
    elif data.get('text') is None:
        await message.answer('Вы не добавили текст, введите его:')
        await state.set_state('States:add_text')
        return
    elif data.get('hyperlinks') is None:
        await message.answer('Вы не добавили гиперссылки, введите их:')
        await state.set_state('States:add_hyperlinks')
        return
    elif data.get('link') is None:
        await message.answer('Загружаю фото..')
        if data.get('tgh_text') is not None:
            link = tgh.create_site(name=data['name'], text=data['tgh_text'])
        else:
            link = tgh.create_site(name=data['name'])
        if link == -1:
            await message.answer('Вы не добавили фото для Telegraph')
            await message.answer('Добавте их прямо сейчас и нажмите принять:', reply_markup=kb.next_state)
            await state.set_state('States:add_photo')
            return
        await state.update_data(link=link)
    else:
        link = data['link']

    await message.answer('Отправляю..', reply_markup=kb.start)
    print('отправляем сообщение в канал:')
    text = '<b>' + data['name'] + '</b>' + '\n' \
           + hide_link(link) + data['hyperlinks'] + '\n' \
           + '\n' + data['text']

    await state.update_data(link=link)
    await bot.send_message(chat_id=ch_id,
                           text=text,
                           parse_mode='HTML',
                           reply_markup=kb.favourite,
                           )
    await state.reset_data()


@dp.callback_query_handler(text='favourite', state='*')
async def process_callback_button1(callback: types.CallbackQuery, state: FSMContext):
    id_copy = db.get_copy(callback.from_user.id, callback.message.message_id)
    print('id copy', id_copy)
    if id_copy is None or id_copy == '':
        try:
            mes = await callback.message.send_copy(chat_id=callback.from_user.id,
                                                   reply_markup=kb.delete_favourite,
                                                   )
        except exceptions.Unauthorized:
            await callback.answer(url=bot_link)
            return

        id_copy = mes.message_id
        print(id_copy)

    print(id_copy)
    if db.check_user_new(callback.from_user.id, id_origin=callback.message.message_id, id_copy=id_copy) == -1:
        await bot.delete_message(chat_id=callback.from_user.id, message_id=id_copy)
        await callback.answer(text='Удалено из избранного!')
    else:
        await callback.answer(text='Добавлено в избранное')


@dp.callback_query_handler(text='delete_favourite', state='*')
async def callback_del(callback: types.CallbackQuery):
    db.check_user_new(callback.from_user.id, id_copy=callback.message.message_id)
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    if datetime.now() - callback.message.date > timedelta(days=2):
        await callback.answer(text='Из-за ограничений Telegram мы не '
                                   'можем удалить сообщение после 48-ми часов,'
                                   ' однако вы всегда можете удалить его вручную)',
                              show_alert=True,
                              )
    else:
        await callback.answer(text='Удалено из избранного!')

# handlers for scheduler:
# =# @dp.message_handler(text='Расписание', state='*', content_types=types.ContentTypes.TEXT)
# =# async def menu_schedule(message: types.Message, state: FSMContext):
# =#     await message.answer('Что вы хотите?', reply_markup=kb.sched)
# =#
# =#
# =# @dp.message_handler(text='Добавить текущий пост в расписание', state='*', content_types=types.ContentTypes.TEXT)
# =# async def add_to_schedule(message: types.Message, state: FSMContext):
# =#     data = await state.get_data()
# =#     if data.get('name') is None:
# =#         await message.answer('Вы не добавили название, введите его:')
# =#         await state.set_state('States:add_name')
# =#         return
# =#     elif data.get('text') is None:
# =#         await message.answer('Вы не добавили текст, введите его:')
# =#         await state.set_state('States:add_text')
# =#         return
# =#     elif data.get('hyperlinks') is None:
# =#         await message.answer('Вы не добавили гиперссылки, введите их:')
# =#         await state.set_state('States:add_hyperlinks')
# =#         return
# =#     elif data.get('link') is None:
# =#         await message.answer('Загружаю фото..')
# =#         link = tgh.create_site(data['name'])
# =#         if link == -1:
# =#             await message.answer('Вы не добавили фото для Telegraph')
# =#             await message.answer('Добавте их прямо сейчас:')
# =#             state.set_state('States:add_photo')
# =#             return
# =#         await state.update_data(link=link)
# =#
# =#     await message.answer(text='Введите время в формате:\n ' + datetime.now().strftime("%d.%m.%y %H:%M"))
# =#     await state.set_state('States:add_schedule')
# =#
# =#
# =# @dp.message_handler(state=States.add_schedule, content_types=types.ContentTypes.TEXT)
# =# async def add_to_schedule_pt2(message: types.Message, state: FSMContext):
# =#     data = await state.get_data()
# =#     text = '<b>' + data['name'] + '</b>\n' \
# =#            + hide_link(data['link']) + data['hyperlinks'] + '\n' \
# =#            + '\n' + data['text']
# =#     try:
# =#         await pp.tick(job_name=data['name'], timer=message.text, mes_text=text)
# =#     except ValueError:
# =#         await message.answer('Введена неверная дата, попробуйте еще:')
# =#     await state.set_state('States:menu')
# =#     await message.answer('Пост добавлен в расписание', reply_markup=kb.start)
# =#
# =#
# =# @dp.message_handler(state='*')
# =# async def pastp(message: types.Message, state: FSMContext):
# =#     data = await state.get_data()
# =#     part_text = data['text']
# =#     part_name = '<b>' + data['name'] + '\n</b>'
# =#     part_link = '<a href="' + data['link'] + '"> </a>' '\n'
# =#     text = part_name + part_link + part_text
# =#     await pp.tick(mes_text=text, timer=message.text, job_name=data['name'])
# =

# await bot.send_message(chat_id=message.from_user.id, reply_markup=kb_start)

# print(await state.get_data())

# media_id = await state.get_data()
# # media_id = str(media_id) + ';' + str(file_info.file_id)
#
# media_id['media'] = ';' + str(file_info.file_id)
# row = media_id.get('media')
# row += ';' + str(file_info.file_id)
# await state.update_data(media=str(row))
#
# @dp.message_handler(commands=['link'], state="*")
# async def add(message: types.Message, state: FSMContext):
#     lnk = 'https://telegra.ph/Title-09-01-10'
#     await message.answer('Ссылка на телеграф:<a href="' +
#                          lnk + '"> </a>'
#                                '\n<b>Открывай чтобы увидеть больше!</b>',
#                          parse_mode='HTML',
#                          reply_markup=inline_favrt)
#     print(telegraph.get_page(path="Title-09-01-10"))
#
#
# @dp.message_handler(commands=['add'], state="*")
# async def add(message: types.Message, state: FSMContext):
#     await message.answer('Введите название:',
#                          parse_mode='HTML',
#                          reply_markup=ReplyKeyboardRemove())
#     current_state = await state.get_state()
#     print(current_state)
#     await state.set_state('States:add_text')
#     current_state = await state.get_state()
#     print(current_state)
#
#
# @dp.message_handler(state=States.add_text, content_types=types.ContentTypes.TEXT)
# async def add_txt(message: types.Message, state: FSMContext):
#     txt = message.text
#     await state.update_data(mes_txt=txt)
#     await message.answer(txt)
#     # await bot.send_message(chat_id=ch_id, text=txt)
#     await state.set_state('States:add_photo')
#     print(await state.get_state())
#
#
# @dp.message_handler(state='*', content_types=types.ContentTypes.ANY)
# @dp.message_handler(state=States.sent, content_types=types.ContentTypes.ANY)
# async def sent_mes(message: types.Message, state: FSMContext):
#     await bot.send_message(chat_id=ch_id, text=message.text, reply_markup=inline_favrt)








