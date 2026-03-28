import psycopg2
import csv
from connect import get_connection

def add_from_csv(filename):
    conn = get_connection()
    cur = conn.cursor()
    with open(filename, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                cur.execute(
                    "INSERT INTO phonebook (first_name, phone) VALUES (%s, %s) ON CONFLICT (phone) DO NOTHING",
                    (row['first_name'], row['phone'])
                )
            except Exception as e:
                print(f"Ошибка: {e}")
    conn.commit()
    cur.close()
    conn.close()
    print("CSV импортирован!")

def add_contact():
    name = input("Имя: ")
    phone = input("Телефон: ")
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)",
            (name, phone)
        )
        conn.commit()
        print("Контакт добавлен!")
    except Exception as e:
        print(f"Ошибка: {e}")
    cur.close()
    conn.close()

def search_contacts():
    query = input("Введи имя или часть номера: ")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM phonebook WHERE first_name ILIKE %s OR phone LIKE %s",
        (f'%{query}%', f'%{query}%')
    )
    rows = cur.fetchall()
    if rows:
        for row in rows:
            print(f"ID: {row[0]} | Имя: {row[1]} | Телефон: {row[2]}")
    else:
        print("Ничего не найдено")
    cur.close()
    conn.close()

def update_contact():
    print("1 - Обновить имя")
    print("2 - Обновить телефон")
    choice = input("Выбор: ")
    phone = input("Введи телефон контакта: ")
    conn = get_connection()
    cur = conn.cursor()
    if choice == '1':
        new_name = input("Новое имя: ")
        cur.execute("UPDATE phonebook SET first_name = %s WHERE phone = %s", (new_name, phone))
    elif choice == '2':
        new_phone = input("Новый телефон: ")
        cur.execute("UPDATE phonebook SET phone = %s WHERE phone = %s", (new_phone, phone))
    conn.commit()
    print("Обновлено!")
    cur.close()
    conn.close()

def delete_contact():
    print("1 - Удалить по имени")
    print("2 - Удалить по телефону")
    choice = input("Выбор: ")
    conn = get_connection()
    cur = conn.cursor()
    if choice == '1':
        name = input("Имя: ")
        cur.execute("DELETE FROM phonebook WHERE first_name = %s", (name,))
    elif choice == '2':
        phone = input("Телефон: ")
        cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))
    conn.commit()
    print("Удалено!")
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

def main():
    while True:
        print("\n=== PhoneBook ===")
        print("1 - Показать все контакты")
        print("2 - Добавить из CSV")
        print("3 - Добавить вручную")
        print("4 - Найти контакт")
        print("5 - Обновить контакт")
        print("6 - Удалить контакт")
        print("0 - Выход")
        choice = input("Выбор: ")

        if choice == '1':
            show_all()
        elif choice == '2':
            add_from_csv('contacts.csv')
        elif choice == '3':
            add_contact()
        elif choice == '4':
            search_contacts()
        elif choice == '5':
            update_contact()
        elif choice == '6':
            delete_contact()
        elif choice == '0':
            break
        else:
            print("Неверный выбор")

if __name__ == "__main__":
    main()