import time

import pymysql
from pymysql.cursors import DictCursor

connect_param = {'host': '18.191.94.4',
                 'user': 'admin0880',
                 'password': '0880',
                 'db': 'users',
                 'charset': 'utf8',
                 'cursorclass': DictCursor
                 }  # connect to server

connect_param2 = {'host': 'localhost',
                  'user': 'root',
                  'password': '',
                  'db': 'devices',
                  'charset': 'utf8',
                  'cursorclass': DictCursor
                  }  # connect to localhost


def add_user(id_user, id_mes):
    print('add user: %s, id message:%s' % (id_user, id_mes))
    connection.cursor().execute('insert into favourite values ("%s", ";%s;")' % (id_user, id_mes))


def add_message(id_user, line):
    print('id user: %s, add message' % id_user)
    connection.cursor().execute('UPDATE favourite SET id_message="%s" WHERE id_user="%s"' % (line, id_user))


def delete_message(id_user, line):
    print('id user: %s, delete message' % id_user)
    connection.cursor().execute('UPDATE favourite SET id_message="%s" WHERE id_user="%s"' % (line, id_user))


def delete_user(id_user):
    print()


def check_user(id_user, id_mes, copy=False, origin=False):
    # id_origin = id_mes
    # id_copy = id_mes
    t_request = time.time()
    with connection.cursor() as cursor:
        user_exist = cursor.execute('select id_message from favourite where id_user=%s' % id_user)
        for row in cursor:
            line = row[0]
            mes_exist = row[0].find(';' + str(id_mes) + ';')

        # if copy:
        #     id_origin = get_origin(id_mes)
        # elif origin:
        #     id_copy = get_copy(id_mes)
        # print('id_orig:%i\nid_copy:%i' % (id_origin, id_copy))

        if user_exist == 0:  # user not exist
            add_user(id_user, id_mes)

        elif user_exist == 1 and mes_exist == -1:  # user exist, message not exist and should be added
            line = line + ';' + str(id_mes) + ';'
            add_message(id_user, line)

        elif user_exist == 1 and mes_exist != -1:  # user exist, message exist and should be deleted
            line = row[0].replace(';' + str(id_mes) + ';', '')
            # print(row[0])
            delete_message(id_user, line)
    connection.commit()  # apply changes (for innodb engine)
    print('Time of request to base:', time.time() - t_request)


def check_user_new(id_user, id_origin=None, id_copy=None):
    # id_origin = id_mes
    # id_copy = id_mes
    t_request = time.time()
    with connection.cursor() as cursor:
        user_exist = cursor.execute('select id_message from favourite where id_user=%s' % id_user)
        for row in cursor:
            # print(row['id_message'])
            line = row['id_message']
            mes_exist = row['id_message'].find(';' + str(id_origin))
            print(line)

        if id_origin is None and id_copy is not None:
            id_origin = get_origin(id_user, id_copy)
        if id_copy is None and id_origin is not None:
            id_copy = get_copy(id_user, id_origin)
        # print('id_orig:%s\nid_copy:%s\nuser:%s\nmes:%s' % (id_origin, id_copy, user_exist, mes_exist))

        if user_exist == 0:  # user not exist
            line = ';' + str(id_origin) + '-' + str(id_copy) + ';'
            add_user(id_user, line)

        elif user_exist == 1 and mes_exist == -1:  # user exist, message not exist and should be added
            line = line + ';' + str(id_origin) + '-' + str(id_copy) + ';'
            add_message(id_user, line)

        elif user_exist == 1 and mes_exist != -1:  # user exist, message exist and should be deleted
            line = row['id_message'].replace(';' + str(id_origin) + '-' + str(id_copy) + ';', '')
            # print(row[0])
            delete_message(id_user, line)
    connection.commit()  # apply changes (for innodb engine)
    print('Time of request to base:', time.time() - t_request)


def get_origin(id_user, id_copy_mes):
    with connection.cursor() as cursor:
        # a = []
        cursor.execute('select * from favourite where id_user=%s' % id_user)
        for row in cursor:
            # print(row['id_message'])
            id_orig_mes = row['id_message'].partition('-' + id_copy_mes + ';')[0].rpartition(';')[2]
            # print(id_orig_mes)
            return id_orig_mes


def get_copy(id_user, id_origin_mes):
    with connection.cursor() as cursor:
        cursor.execute('select * from favourite where id_user=%s' % id_user)
        for row in cursor:
            # print(row['id_message'])
            id_copy_mes = row['id_message'].partition(';' + id_origin_mes + '-')[2].partition(';')[0]
            # print(id_copy_mes)
            return id_copy_mes


t_connect = time.time()
connection = pymysql.connect(**connect_param)
print('Database connected\nTime of connect=', (time.time() - t_connect))
# get_copy('153')
# get_origin('3603')
check_user_new('1223',
               id_origin='154',
               id_copy='3301'
               )
