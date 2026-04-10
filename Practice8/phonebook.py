import psycopg2
import csv
from connect import get_connection
def load_sql_functions():
    """Создаёт все функции и процедуры в БД из SQL-файлов."""
    conn = get_connection()
    cur = conn.cursor()
    for filename in ("functions.sql", "procedures.sql"):
        with open(filename, encoding="utf-8") as f:
            sql = f.read()
        cur.execute(sql)
        print(f"{filename} загружен в БД")
    conn.commit()
    cur.close()
    conn.close()


def show_all():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM phonebook ORDER BY id")
    rows = cur.fetchall()
    if rows:
        for row in rows:
            print(f"ID: {row[0]} | Имя: {row[1]} | Телефон: {row[2]}")
    else:
        print("Телефонная книга пуста")
    cur.close()
    conn.close()

def add_from_csv(filename="contacts.csv"):
    conn = get_connection()
    cur = conn.cursor()
    with open(filename, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                cur.execute(
                    "INSERT INTO phonebook (first_name, phone) VALUES (%s, %s) ON CONFLICT (phone) DO NOTHING",
                    (row["first_name"], row["phone"]),
                )
            except Exception as e:
                print(f"Ошибка: {e}")
    conn.commit()
    cur.close()
    conn.close()
    print("CSV импортирован!")


def search_by_pattern():
    pattern = input("Введи паттерн (имя или часть номера): ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM search_by_pattern(%s)", (pattern,))
    rows = cur.fetchall()
    if rows:
        for row in rows:
            print(f"ID: {row[0]} | Имя: {row[1]} | Телефон: {row[2]}")
    else:
        print("Ничего не найдено")
    cur.close()
    conn.close()

def upsert_contact():
    name  = input("Имя: ")
    phone = input("Телефон: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
    conn.commit()
    print("Готово!")
    cur.close()
    conn.close()

def bulk_insert():
    print("Введи контакты (пустая строка = конец ввода):")
    names  = []
    phones = []
    while True:
        name = input("  Имя (или Enter для завершения): ").strip()
        if not name:
            break
        phone = input("  Телефон: ").strip()
        names.append(name)
        phones.append(phone)

    if not names:
        print("Список пустой")
        return

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL bulk_insert_contacts(%s, %s)", (names, phones))
    conn.commit()

    # Получаем невалидные записи из временной таблицы
    cur.execute("SELECT * FROM invalid_contacts")
    invalid = cur.fetchall()
    if invalid:
        print("\n⚠️  Некорректные записи (не добавлены):")
        for row in invalid:
            print(f"  Имя: {row[0]} | Телефон: {row[1]} | Причина: {row[2]}")
    else:
        print("Все записи успешно добавлены!")

    cur.close()
    conn.close()

def show_paginated():
    try:
        page_size = int(input("Размер страницы (кол-во записей): "))
        page_num  = int(input("Номер страницы (начиная с 1): "))
    except ValueError:
        print("Введи целые числа")
        return

    offset = (page_num - 1) * page_size
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (page_size, offset))
    rows = cur.fetchall()
    if rows:
        print(f"\n--- Страница {page_num} ---")
        for row in rows:
            print(f"ID: {row[0]} | Имя: {row[1]} | Телефон: {row[2]}")
    else:
        print("Нет данных на этой странице")
    cur.close()
    conn.close()


def delete_contact():
    print("1 - Удалить по имени")
    print("2 - Удалить по телефону")
    choice = input("Выбор: ")
    conn = get_connection()
    cur = conn.cursor()
    if choice == "1":
        name = input("Имя: ")
        cur.execute("CALL delete_contact(p_username => %s)", (name,))
    elif choice == "2":
        phone = input("Телефон: ")
        cur.execute("CALL delete_contact(p_phone => %s)", (phone,))
    else:
        print("Неверный выбор")
        cur.close()
        conn.close()
        return
    conn.commit()
    print("Удалено!")
    cur.close()
    conn.close()

def main():
    load_sql_functions()

    while True:
        print("\n=== PhoneBook (Practice 8) ===")
        print("1 - Показать все контакты")
        print("2 - Добавить из CSV")
        print("3 - Добавить / обновить контакт (upsert)")
        print("4 - Массовая вставка с валидацией")
        print("5 - Поиск по паттерну")
        print("6 - Просмотр с пагинацией")
        print("7 - Удалить контакт")
        print("0 - Выход")
        choice = input("Выбор: ")

        if choice == "1":
            show_all()
        elif choice == "2":
            add_from_csv()
        elif choice == "3":
            upsert_contact()
        elif choice == "4":
            bulk_insert()
        elif choice == "5":
            search_by_pattern()
        elif choice == "6":
            show_paginated()
        elif choice == "7":
            delete_contact()
        elif choice == "0":
            print("Выход")
            break
        else:
            print("Неверный выбор")


if __name__ == "__main__":
    main()
