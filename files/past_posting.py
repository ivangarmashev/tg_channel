from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
# from apscheduler.schedulers.background import BaseScheduler
from .connections import bot

scheduler = AsyncIOScheduler()
scheduler.start()


async def tick(id_u, sec):
    # print(f'Tick! The time is: {datetime.now()}')
    scheduler.add_job(tick2,
                      id='впыфпуффыва',
                      trigger='date',
                      run_date=datetime(2020, 9, 26, 0, datetime.now().minute, datetime.now().second+int(sec)),
                      args=[id_u])
    print(scheduler.get_job(job_id='впыфпуффыва').args)
    await bot.send_message(chat_id=id_u, text='сообщение из pp')


async def tick2(id_u):
    await bot.send_message(chat_id=id_u, text='отправлено')
    # try:
    #     while True:
    #         time.sleep(2)
    #         print('Printing in the main thread.')
    # except KeyboardInterrupt:
    #     pass


