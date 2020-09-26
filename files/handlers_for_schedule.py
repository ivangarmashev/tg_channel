from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hide_link
from datetime import datetime
from files import keyboards as kb
from files.bot_states import States
from files.connections import dp
from files import past_posting as pp
import files.telegraph_use as tgh


@dp.message_handler(text='Расписание', state='*', content_types=types.ContentTypes.TEXT)
async def menu_schedule(message: types.Message):
    await message.answer('Что вы хотите?', reply_markup=kb.sched)


@dp.message_handler(text='Добавить текущий пост в расписание', state='*', content_types=types.ContentTypes.TEXT)
async def add_to_schedule(message: types.Message, state: FSMContext):
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
        link = tgh.create_site(data['name'])
        if link == -1:
            await message.answer('Вы не добавили фото для Telegraph')
            await message.answer('Добавте их прямо сейчас:')
            await state.set_state('States:add_photo')
            return
        await state.update_data(link=link)

    await message.answer(text='Введите время в формате:\n ' + datetime.now().strftime("%d.%m.%y %H:%M"))
    await state.set_state('States:add_schedule')


@dp.message_handler(state=States.add_schedule, content_types=types.ContentTypes.TEXT)
async def add_to_schedule_pt2(message: types.Message, state: FSMContext):
    data = await state.get_data()
    text = '<b>' + data['name'] + '</b>\n' \
           + hide_link(data['link']) + data['hyperlinks'] + '\n' \
           + '\n' + data['text']
    try:
        await pp.tick(job_name=data['name'], timer=message.text, mes_text=text)
    except ValueError:
        await message.answer('Введена неверная дата, попробуйте еще:')
    await state.set_state('States:menu')
    await message.answer('Пост добавлен в расписание', reply_markup=kb.start)
