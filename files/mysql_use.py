import time

import pymysql
from pymysql.cursors import DictCursor

connect_param = {'host': '18.191.94.4',
                 'user': 'admin0880',
                 'password': '0880',
                 'db': 'users',
                 'charset': 'utf8',
                 # 'cursorclass': DictCursor
                 }  # connect to server

connect_param2 = {'host': 'localhost',
                  'user': 'root',
                  'password': '',
                  'db': 'devices',
                  'charset': 'utf8',
                  'cursorclass': DictCursor
                  }  # connect to localhost


def add_user(id_user, id_mes):
    # print('add user')
    connection.cursor().execute('insert into favourite values ("%s", ";%s;")' % (id_user, id_mes))


def add_message(id_user, line):
    # print('add message')
    connection.cursor().execute('UPDATE favourite SET id_message="%s" WHERE id_user="%s"' % (line, id_user))


def delete_message(id_user, line):
    # print('delete_message')
    connection.cursor().execute('UPDATE favourite SET id_message="%s" WHERE id_user="%s"' % (line, id_user))


def delete_user(id_user):
    print()


def check_user(id_user, id_mes, copy=False, origin=False):
    id_origin = id_mes
    id_copy = id_mes
    t_request = time.time()
    with connection.cursor() as cursor:
        user_exist = cursor.execute('select id_message from favourite where id_user=%s' % id_user)
        for row in cursor:
            line = row[0]
            mes_exist = row[0].find(';' + str(id_mes) + ';')

        if copy:
            id_origin = get_origin(id_mes)
        elif origin:
            id_copy = get_copy(id_mes)
        print('id_orig:%i\nid_copy:%i' % (id_origin, id_copy))

        if user_exist == 0:  # user not exist
            add_user(id_user, id_mes)

        elif user_exist == 1 and mes_exist == -1:  # user exist, message not exist and should be added
            line = line + ';' + str(id_mes) + ';'
            add_message(id_user, line)

        elif user_exist == 1 and mes_exist != -1:  # user exist, message exist and should be deleted
            line = row[0].replace(';' + str(id_mes) + ';', '')
            delete_message(id_user, line)
    connection.commit()  # apply changes (for innodb engine)
    print('Time of request to base:', time.time() - t_request)


def get_origin(id_copy_mes):
    with connection.cursor() as cursor:
        # a = []
        cursor.execute('select * from favourite where id_user=123')
        for row in cursor:
            print(row['id_message'])
            id_orig_mes = row['id_message'].partition('-' + id_copy_mes + ';')[0].rpartition(';')[2]
            print(id_orig_mes)
            return id_orig_mes


def get_copy(id_origin_mes):
    with connection.cursor() as cursor:
        cursor.execute('select * from favourite where id_user=123')
        for row in cursor:
            print(row['id_message'])
            id_copy_mes = row['id_message'].partition(';' + id_origin_mes + '-')[2].partition(';')[0]
            print(id_copy_mes)
            return id_copy_mes


t_connect = time.time()
connection = pymysql.connect(**connect_param)
print('Database connected\nTime of connect=', (time.time() - t_connect))
# get_copy('153')
# get_origin('3603')
check_user('123', '3603', copy=True)
