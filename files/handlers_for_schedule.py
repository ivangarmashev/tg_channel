from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hide_link
from datetime import datetime
from files import keyboards as kb
from files.bot_states import States
from files.connections import dp
from files import past_posting as pp
import files.telegraph_use as tgh
from files import all_states as ast


@dp.message_handler(text='Расписание', state=ast.all_state, content_types=types.ContentTypes.TEXT)
async def menu_schedule(message: types.Message, state: FSMContext):
    await message.answer('Что вы хотите?', reply_markup=kb.sched)
    await state.set_state('States:menu')


@dp.message_handler(text='Добавить текущий пост в расписание',
                    state=ast.all_state,
                    content_types=types.ContentTypes.TEXT)
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

    await message.answer(text='Введите время в формате:\n ' + datetime.now().strftime("%d.%m.%y %H:%M"))
    await state.set_state('States:add_schedule')


@dp.message_handler(text='Показать отложенные посты', state=ast.all_state, content_types=types.ContentTypes.TEXT)
async def show_schedulers(message: types.Message, state: FSMContext):
    await message.answer('Вот список отложенных постов:', reply_markup=await pp.get_schedule())
    await state.set_state('States:select_in_schedule')


@dp.callback_query_handler(state=ast.all_state)         # Выбор и предпросмотр поста из списка расписания
async def callback_sched(callback: types.CallbackQuery, state: FSMContext):
    try:
        text_from_sched = await pp.send_for_edit(callback.data)
        await state.update_data(id_job=callback.data)
        await state.set_state('States:select_in_schedule')
        await callback.answer()
        await callback.message.answer(text=text_from_sched, parse_mode='HTML', reply_markup=kb.sched_edit)
    except AttributeError:
        await callback.message.answer(text='Запись в расписании не существует.', reply_markup=kb.start)
        await callback.answer()


@dp.message_handler(text='Редактировать время отправки', state=States.select_in_schedule)
async def edit_date(message: types.Message, state: FSMContext):
    await message.answer(text='Введите время в формате:\n ' + datetime.now().strftime("%d.%m.%y %H:%M"))
    await state.set_state('States:edit_time')


@dp.message_handler(state=States.edit_time, content_types=types.ContentTypes.TEXT)
async def edit_date(message: types.Message, state: FSMContext):
    data = await state.get_data()

    try:
        await pp.edit_time_send(job_name=data['id_job'], timer=message.text)
        await state.set_state('States:menu')
        await message.answer('Время публикации изменено', reply_markup=kb.start)
        await state.reset_data()
        tgh.delete_media()
    except ValueError:
        await message.answer('Введена неверная дата, попробуйте еще:')


@dp.message_handler(text='Удалить пост из расписания', state=ast.all_state, content_types=types.ContentTypes.TEXT)
async def edit_date(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await pp.del_schedule(data['id_job'])
    await state.set_state('States:menu')
    await message.answer('Пост удален', reply_markup=kb.start)


@dp.message_handler(text='Удалить пост полностью', state=ast.all_state, content_types=types.ContentTypes.TEXT)
async def edit_date(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await pp.del_schedule(data['id_job'])
    await state.set_state('States:menu')
    await state.reset_data()
    tgh.delete_media()
    await message.answer('Пост удален', reply_markup=kb.start)


@dp.message_handler(state=States.add_schedule, content_types=types.ContentTypes.TEXT)
async def add_to_schedule_pt2(message: types.Message, state: FSMContext):
    data = await state.get_data()
    text = '<b>' + data['name'] + '</b>\n' \
           + hide_link(data['link']) + data['hyperlinks'] + '\n' \
           + '\n' + data['text']
    try:
        await pp.add_to_schedule(job_name=data['name'], timer=message.text, mes_text=text)
        await state.set_state('States:menu')
        await message.answer('Пост добавлен в расписание', reply_markup=kb.start)
        await state.reset_data()
        tgh.delete_media()
    except ValueError:
        await message.answer('Введена неверная дата, попробуйте еще:')

