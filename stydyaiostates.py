from aiogram.utils import executor
from files.handlers import *
from files.handlers_for_schedule import *

if __name__ == '__main__':

    executor.start_polling(dp)


    # ids = []
    # ids = await state.get_data()
    # print(ids.get('mes_id'))
    # if str(ids.get('mes_id')) == 'None':
    #     await state.update_data(id_user=str(callback_query.from_user.id), mes_id=str(message.message_id))
    #     print('if')
    # else:
    #     if ids['mes_id'].find(str(message.message_id)) == -1:
    #         ids['mes_id'] += ';' + str(message.message_id)
    #         await state.update_data(mes_id=ids['mes_id'])
    #     # print(ids['mes_id'].find('115'))
    #
    # # ids.append(message.message_id)
    # print(ids)
    # ids.update(await state.get_data())
    # print(ids)
    # print(ids.items())
    # ids1 = {'mes_id': message.message_id}
    # print(ids1)
    # print(ids1.items())
    # # eval(ids1)
    # ids.update(ids1)
    # print(ids)
    # ids['mes_id'] += ';' + str(message.message_id)
    # # ids1 = {'mes_id': ids}
    # print(await state.update_data(mes_id=ids['mes_id']))
    # print(await state.get_data('mes_id'))

    # await state.update_data(mes_id=ids)
    #
    # # await callback_query.message.answer(text=callback_query.message.date)
    # # await callback_query.message.answer(text=callback_query.chat_instance)
    # mes_idd = await state.get_data(['mes_id'])
    # print(mes_idd)
    # for r in ids:
    #     print(r)
    # # print(ids)

# import aiogram.utils.markdown as md
# from aiogram.dispatcher.filters import Text
# from aiogram.types import ParseMode
# from aiogram.utils import exceptions

# telegraph = Telegraph()
# telegraph.create_account(short_name='2142122235')

# tracemalloc.start()
# API_TOKEN = '1179364946:AAFTTG57jQNLIEprI13JZzFi81Mg0OovUcw'
# logging.basicConfig(level=logging.INFO)
# ch_id = '@vantobotch'
# bot = Bot(token=API_TOKEN)
# storage = MemoryStorage()
# dp = Dispatcher(bot, storage=storage)
# dp.middleware.setup(LoggingMiddleware())


# @dp.message_handler(commands=['start'], state="*")
# # @dp.message_handler(message: 'привет', state="*")
# async def send_welcome(message: types.Message, state: FSMContext):
#     # types.ReplyKeyboardRemove()
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     keyboard.add('/start')
#     keyboard.add('/add')
#     keyboard.add('/link')
#     keyboard.add('/send')
#     # await bot.send_message(chat_id=ch_id, text='123', reply_markup=inline_kb1)
#     await message.reply("Привет", reply_markup=keyboard)
