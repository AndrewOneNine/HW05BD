import psycopg2
from pprint import pprint


def create_tables(cur):
    """Создание таблиц данных"""

    # таблица основных данных клиента
    cur.execute("""
    CREATE TABLE IF NOT EXISTS clients_info(
    id SERIAL PRIMARY KEY,
    client_firstname VARCHAR(100) NOT NULL,
    client_surname VARCHAR(100) NOT NULL,
    client_email VARCHAR(100) NOT NULL
    );  
    """)

    # таблица телефонных номеров
    cur.execute("""
    CREATE TABLE IF NOT EXISTS clients_phones(
    id_phones SERIAL PRIMARY KEY,
    client_id INTEGER NOT NULL REFERENCES clients_info(id),
    client_phone VARCHAR(25) UNIQUE);
    """)

def add_new_client(cur, client_firstname, client_surname, client_email):
    """Добавление нового клиента"""
    cur.execute("""
    INSERT INTO clients_info(client_firstname, client_surname, client_email) VALUES(%s, %s, %s);
    """, (client_firstname, client_surname, client_email))

def add_new_phone(cur, client_id, client_phone):
    """Добавление нового телефона"""
    cur.execute("""
    INSERT INTO clients_phones(client_id, client_phone) VALUES(%s, %s);
    """, (client_id, client_phone))

def change_client_data():
    """Изменение информации о клиенте"""
    print('Для изменения данных о клиенте введите номер действия\n'
          '1-Изменение имени; 2-Изменение фамилии; 3-Изменение e-mail; 4-Изменение номера телефона')

    while True:
        command = int(input())
        if command == 1:
            id_changing_name = input('Введите id клиента, имя которого хотите изменить: ')
            changing_name = input('Новое имя клиента: ')
            cur.execute('''
            UPDATE clients_info SET client_firstname=%s WHERE id=%s;
            ''', (changing_name, id_changing_name))
            break
        elif command == 2:
            id_changing_surname = input('Введите id клиента, фамилию которого хотите изменить: ')
            changing_surname = input('Новая фамилия клиента: ')
            cur.execute('''
            UPDATE clients_info SET client_surname=%s WHERE id=%s;
            ''', (changing_surname, id_changing_surname))
            break
        elif command == 3:
            id_changing_email = input('Введите id клиента e-mail, которого хотите изменить: ')
            changing_email = input('Новый e-mail клиента: ')
            cur.execute('''
            UPDATE clients_info SET client_email=%s WHERE id=%s;
            ''', (changing_email, id_changing_email))
            break
        elif command == 4:
            old_phone = input('Введите номер телефона, который хотите заменить: ')
            new_phone = input('Новый номер телефона: ')
            cur.execute('''
            UPDATE clients_phones SET client_phone=%s WHERE client_phone=%s;
            ''', (new_phone, old_phone))
            break
        else:
            print('Неверная команда, повторите ввод: ')


def delete_client_phone():
    """Удаление номера телефона клиента"""
    client_id_for_delete = input('Введите id клиента, номер телефона которого хотите удалить: ')
    phone_for_delete = input('Введите номер, который хотите удалить: ')
    with conn.cursor() as cur:
        cur.execute('''
        DELETE FROM clients_phones WHERE client_id=%s AND client_phone=%s
        ''', (client_id_for_delete, phone_for_delete))


def delete_client():
    """Удаление информации о клиенте"""
    id_deleting_client = input('Введите id клиента которого хотите удалить: ')
    with conn.cursor() as cur:
        cur.execute('''
        DELETE FROM clients_phones WHERE client_id=%s
        ''', (id_deleting_client,))
        cur.execute('''
        DELETE FROM clients_info WHERE id=%s
        ''', (id_deleting_client,))


def find_client():
    """Поиск информации о клиенте"""
    print("Для поиска данных о клиенте введите номер команды из списка:\n "
          "1-Поиск по имени; 2-Поиск по фамилии; 3-Поиск по e-mail; 4-Поиск по номеру телефона; 0-Выход;")
    while True:
        command = int(input('Введите номер команды для поиска данных о клиенте: '))
        if command == 1:
            finding_name = input('Введите имя: ')
            cur.execute('''
            SELECT id, client_firstname, client_surname, client_email, client_phone FROM clients_info ci
            LEFT JOIN clients_phones cp on ci.id = cp.client_id
            WHERE client_firstname=%s
            ''', (finding_name,))
            print(cur.fetchall())
        elif command == 2:
            finding_surname = input('Введите фамилию: ')
            cur.execute('''
            SELECT id, client_firstname, client_surname, client_email, client_phone FROM clients_info ci
            JOIN clients_phones cp on ci.id = cp.client_id
            WHERE client_surname=%s
            ''', (finding_surname,))
            print(cur.fetchall())
        elif command == 3:
            finding_email = input('Введите e-mail: ')
            cur.execute('''
            SELECT id, client_firstname, client_surname, client_email, client_phone FROM clients_info ci
            JOIN clients_phones cp on ci.id = cp.client_id
            WHERE client_email=%s
            ''', (finding_email,))
            print(cur.fetchall())
        elif command == 4:
            finding_phone = input('Введите номер телефона: ')
            cur.execute('''
            SELECT id, client_firstname, client_surname, client_email, client_phone FROM clients_info ci
            JOIN clients_phones cp on ci.id = cp.client_id
            WHERE client_phone=%s
            ''', (finding_phone,))
            print(cur.fetchall())
        elif command == 0:
            break
        else:
            print('Неверная команда, повторите ввод')


def check_function(cur):
    """Отображение содержимого таблиц"""
    cur.execute('''
    SELECT * FROM clients_info;
    ''')
    pprint(cur.fetchall())
    cur.execute('''
    SELECT * FROM clients_phones;
    ''')
    pprint(cur.fetchall())


with psycopg2.connect(database="new_clients_db", user="postgres", password="fenjlfat16723") as conn:
    with conn.cursor() as cur:
        # cur.execute('''
        # DROP TABLE clients_phones;
        # DROP TABLE clients_info;
        # ''')
        create_tables(cur)
        add_new_client(cur, "Петр", "Петров", "pp7@bk.ru")
        add_new_client(cur, "Михаил", "Потапыч", "potapm@gmail.ru")
        add_new_client(cur, "Анастасия", "Рублева", "rubleva@mail.ru")
        add_new_client(cur, "Семен", "Семенов", "77s@bk.ru")
        add_new_client(cur, "Светлана", "Скорость", "skor@gmail.ru")
        add_new_phone(cur, 1, "787980")
        add_new_phone(cur, 1, "79844565152")
        add_new_phone(cur, 2, "303330")
        add_new_phone(cur, 3, "79455686437")
        add_new_phone(cur, 4, "799788")
        add_new_phone(cur, 5, "414141")
        add_new_phone(cur, 5, "313130")
        check_function(cur)
        change_client_data()
        check_function(cur)
        delete_client_phone()
        check_function(cur)
        delete_client()
        check_function(cur)
        find_client()
conn.close()