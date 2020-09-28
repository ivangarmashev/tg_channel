import logging
import tracemalloc

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from telegraph import Telegraph


telegraph = Telegraph()
telegraph.create_account(short_name='2142122235')
tracemalloc.start()
#API_TOKEN = '1179364946:AAFTTG57jQNLIEprI13JZzFi81Mg0OovUcw' #vantobot
API_TOKEN = '934521129:AAEoQbANZpKPNks-Q9wa9cN0A8uE--mWjuo'
logging.basicConfig(level=logging.INFO)
#ch_id = '@vantobotch'
ch_id = '@mesta4insta'
#bot_link = 'https://t.me/Vanto_bot?start=1'
bot_link = 'https://t.me/mesta4insta_bot?start=1'
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

# scheduler = BackgroundScheduler()
# scheduler.start()
