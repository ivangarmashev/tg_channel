from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from files.connections import bot, ch_id
from files import keyboards as kb

scheduler = AsyncIOScheduler(job_defaults={'misfire_grace_time': 5*60})
scheduler.start()


async def add_to_schedule(mes_text, timer, job_name):
    dt = datetime.strptime(timer, "%d.%m.%y %H:%M")
    print(scheduler.get_jobs())
    scheduler.add_job(send_from_schedule,
                      id=job_name,
                      next_run_time=dt,
                      args=[mes_text]
                      )


async def send_from_schedule(mes_text):
    await bot.send_message(chat_id=ch_id, text=mes_text, parse_mode='HTML', reply_markup=kb.favourite)


async def send_for_edit(id_job):
    return scheduler.get_job(id_job).args[0]


async def edit_time_send(timer, job_name):
    dt = datetime.strptime(timer, "%d.%m.%y %H:%M")
    scheduler.modify_job(job_id=job_name, next_run_time=dt)


async def get_schedule():
    s = scheduler.get_jobs()
    return await kb.create_schedule(s)


async def del_schedule(job_name):
    try:
        scheduler.remove_job(job_id=job_name)
    except:
        pass




#
# scheduler.add_job(tick3, id='1234',
#                   run_date=datetime(2020, 9, datetime.now().day + 1, datetime.now().hour, datetime.now().minute,
#                                     datetime.now().second))
# scheduler.add_job(tick3, id='1235',
#                   run_date=datetime(2020, 9, datetime.now().day + 1, datetime.now().hour, datetime.now().minute,
#                                     datetime.now().second))
# scheduler.add_job(tick3, id='1236',
#                   run_date=datetime(2020, 9, datetime.now().day + 1, datetime.now().hour, datetime.now().minute,
#                                     datetime.now().second))
# scheduler.add_job(tick3, id='1233', name='1233',
#                   run_date=datetime(2020, 9, datetime.now().day + 1, datetime.now().hour, datetime.now().minute,
#                                     datetime.now().second))
# # print(scheduler.print_jobs())
# s = scheduler.get_jobs()
# for x in s:
#     print(x.id)
#     scheduler.modify_job(job_id=x.id, run_date=datetime(2020, 9, datetime.now().day, datetime.now().hour,
#                                                         datetime.now().minute,
#                                                         datetime.now().second) + 1)

# print(scheduler.get_jobs().count())
