import asyncpg


async def get_pool():
    return await asyncpg.create_pool(
                                     # host='localhost',
                                     host='193.123.39.58',
                                     user='admin',
                                     password='admin0550',
                                     database='db'
                                     )