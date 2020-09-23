from aiogram.dispatcher import FSMContext
import io

from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.markdown import hide_link
from files import mysql_use
from files import telegraph_use as tgh
from files.bot_states import *
from files.connections import *
from files.keyboards import *


@dp.message_handler(commands=['start'], state="*")
@dp.message_handler(text='Привет', state="*")
async def send_welcome(message: types.Message, state: FSMContext):
    # types.ReplyKeyboardRemove()
    # await bot.send_message(chat_id=ch_id, text='123')
    await message.reply("Привет", reply_markup=kb_start)


@dp.message_handler(text='Написать новый пост', state='*')
async def main_menu(message: types.Message, state: FSMContext):
    await message.answer(text='Добавить/отредактировать:', reply_markup=kb_parts)
    await state.reset_data()
    tgh.delete_media()
    # await state.set_data(name='')
    # await state.set_data(text='')
    await state.set_state('States:menu')


@dp.message_handler(text='Название', state='*')
async def main_menu(message: types.Message, state: FSMContext):
    ReplyKeyboardRemove()
    await bot.send_message(chat_id=message.from_user.id, text='Введите название:')
    await state.set_state('States:add_name')


@dp.message_handler(text='Текст', state='*')
async def main_menu(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id=message.from_user.id, text='Введите текст:')
    await state.set_state('States:add_text')


@dp.message_handler(text='Фото', state='*')
async def main_menu(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id=message.from_user.id, text='Отравьте фото и нажмите "Принять"', reply_markup=kb_next)
    await state.set_state('States:add_photo')


@dp.message_handler(text='test', state='*')
async def main_menu(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Всё хорошо, как же еще может быть ' + hide_link('vk.com'), parse_mode='HTML')


@dp.message_handler(state=States.add_name)
async def main_menu(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    print('name', message.text)
    await bot.send_message(chat_id=message.from_user.id, text='Принято!', reply_markup=kb_parts, )
    await state.set_state('States:menu')


@dp.message_handler(state=States.add_text)
async def main_menu(message: types.Message, state: FSMContext):
    print('text', message.text)
    await state.update_data(text=message.text)
    await bot.send_message(chat_id=message.from_user.id, text='Принято!', reply_markup=kb_parts)
    await state.set_state('States:menu')


@dp.message_handler(state=States.add_photo, content_types=types.ContentTypes.PHOTO)
async def main_menu(message: types.Message, state: FSMContext):
    print(len(message.photo) - 1)
    file_info = await bot.get_file(message.photo[len(message.photo) - 1].file_id)
    downloaded_file = await bot.download_file_by_id(file_info.file_id)
    downloaded_file = io.BytesIO.read(downloaded_file)
    src = 'media/' + message.caption + '.jpg'
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)


@dp.message_handler(text='Меню', state='*', content_types=types.ContentTypes.TEXT)
@dp.message_handler(text='Принять', state='*', content_types=types.ContentTypes.TEXT)
async def show_message(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id=message.from_user.id, text='Принято!', reply_markup=kb_parts)
    await state.set_state('States:menu')


@dp.message_handler(text='Предпросмотр поста', state='*', content_types=types.ContentTypes.TEXT)
async def show_message(message: types.Message, state: FSMContext):
    await message.answer('Загружаю фото..', reply_markup=ReplyKeyboardRemove())
    data = await state.get_data()
    print(data.get('name'))
    if data.get('name') is None:
        await message.answer('Вы не добавили название, введите его:')
        await state.set_state('States:add_name')
        return
        # text = '<b>' + data['name'] + '</b>'
    elif data.get('text') is None:
        await message.answer('Вы не добавили текст, введите его:')
        await state.set_state('States:add_text')
        return
    text = data['name'] + '\n' + data['text']

    # part_name = '<b>' + data['name'] + '\n</b>'
    # part_link = '<a href="' + link + '"> </a>' '\n'
    link = tgh.create_site(data['name'])
    # text += '<a href="' + link + '"> </a>' '\n'
    await state.update_data(link=link)
    await message.answer('Предпросмотр поста:')
    await message.answer(text=text + hide_link(link), parse_mode='HTML', reply_markup=kb_done, )


@dp.message_handler(text='Редактировать пост', state='*', content_types=types.ContentTypes.TEXT)
async def show_message(message: types.Message, state: FSMContext):
    await message.answer('Что именно вы хотите отредактировать?', reply_markup=kb_parts)


@dp.message_handler(text='Удалить пост', state='*', content_types=types.ContentTypes.TEXT)
async def show_message(message: types.Message, state: FSMContext):
    await state.reset_data()
    tgh.delete_media()
    await bot.send_message(chat_id=message.from_user.id,
                           text='Информация для поста очищена, вы можете создать новый',
                           reply_markup=kb_start)


@dp.message_handler(text='Отправить пост', state='*', content_types=types.ContentTypes.TEXT)
async def show_message(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if data.get('name') is None:
        await message.answer('Вы не добавили название, введите его:')
        await state.set_state('States:add_name')
        return
        # text = '<b>' + data['name'] + '</b>'
    elif data.get('text') is None:
        await message.answer('Вы не добавили текст, введите его:')
        await state.set_state('States:add_text')
        return
    elif data.get('link') is None:
        link = tgh.create_site(data['name'])
    else:
        link = data['link']
    text = data['name'] + '\n' + data['text']
    # await message.answer(text=text + hide_link(link), parse_mode='HTML', reply_markup=favourite, )
    data = await state.get_data()
    part_text = data['text']
    part_name = '<b>' + data['name'] + '\n</b>'
    part_link = '<a href="' + data['link'] + '"> </a>' '\n'
    await message.answer('Отправляю..', reply_markup=kb_start)
    print('отправляем сообщение в канал:\n',
          await bot.send_message(chat_id=ch_id,
                                 text=part_name + part_link + part_text,
                                 parse_mode='HTML',
                                 reply_markup=kb_favourite,
                                 )
          )
    await state.reset_data()
    # tgh.delete_media()

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


@dp.callback_query_handler(text='favourite', state='*')
async def process_callback_button1(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer(text='Добавлено в избранное')
    mes = await callback.message.send_copy(chat_id=callback.from_user.id,
                                           reply_markup=kb_favourite,
                                           )
    print(mes.message_id)
    print(callback.message.message_id)
    mysql_use.check_user_new(callback.from_user.id, id_origin=callback.message.message_id, id_copy=mes.message_id)


@dp.callback_query_handler(text='favour12ite', state='*')
async def callback_del(callback: types.CallbackQuery):
    mysql_use.check_user(callback.from_user.id, callback.message.message_id)
    print(callback)
    await callback.answer(text='Удалено из избранного')
    await callback.message.delete()


@dp.message_handler(commands=['show'], state='*', content_types=types.ContentTypes.ANY)
async def show_done(message: types.Message, state: FSMContext):
    data = await state.get_data()
    print(str(data['mes_photo']))
    print(str(data['mes_txt']))
    await bot.send_photo(chat_id=ch_id,
                         caption=data['mes_txt'],
                         photo=data['mes_photo'],
                         )
    a = open('1.png')
    response = telegraph.create_page(
        'Hey',
        html_content='<p>Hello, world!'
                     '<img src="1.png" />'
                     '</p>'

    )
    a.close()
    print('https://telegra.ph/{}'.format(response['path']))
