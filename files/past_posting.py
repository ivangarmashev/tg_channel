from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
# from apscheduler.schedulers.background import BaseScheduler
from .connections import bot
from . import keyboards as kb

scheduler = AsyncIOScheduler()
scheduler.start()


async def tick(ch_id, mes_text, timer, job_name):
    # print(f'Tick! The time is: {datetime.now()}')

    # scheduler.add_job(tick2,
    #                   id=job_name,
    #                   trigger='date',
    #                   run_date=datetime(2020, 9, datetime.now().day, datetime.now().hour, datetime.now().minute, datetime.now().second+int(timer)),
    #                   args=[ch_id, mes_text])
    print(scheduler.get_jobs())
    # await bot.send_message(chat_id=id_u, text='сообщение из pp')


async def tick2(ch_id, mes_text):
    await bot.send_message(chat_id=ch_id, text=mes_text, parse_mode='HTML', reply_markup=kb.favourite)
    # try:
    #     while True:
    #         time.sleep(2)
    #         print('Printing in the main thread.')
    # except KeyboardInterrupt:
    #     pass


async def tick3():
    print(datetime.now())


scheduler.add_job(tick3, id='1234',
                  run_date=datetime(2020, 9, datetime.now().day + 1, datetime.now().hour, datetime.now().minute,
                                    datetime.now().second))
scheduler.add_job(tick3, id='1235',
                  run_date=datetime(2020, 9, datetime.now().day + 1, datetime.now().hour, datetime.now().minute,
                                    datetime.now().second))
scheduler.add_job(tick3, id='1236',
                  run_date=datetime(2020, 9, datetime.now().day + 1, datetime.now().hour, datetime.now().minute,
                                    datetime.now().second))
scheduler.add_job(tick3, id='1233', name='1233',
                  run_date=datetime(2020, 9, datetime.now().day + 1, datetime.now().hour, datetime.now().minute,
                                    datetime.now().second))
# print(scheduler.print_jobs())
s = scheduler.get_jobs()
for x in s:
    print(x.id)
    scheduler.modify_job(job_id=x.id, run_date=datetime(2020, 9, datetime.now().day, datetime.now().hour,
                                                        datetime.now().minute,
                                                        datetime.now().second) + 1)

# print(scheduler.get_jobs().count())
