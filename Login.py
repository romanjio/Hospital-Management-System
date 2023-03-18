import sqlite3
from tabulate import tabulate

def login_to_the_system():
    try:
        count = 0
        while count < 2:
            print(count)
            login_name = input("Введіть ім'я користувача: ")
            password = input("Введіть пароль: ")
            check_login = f"SELECT login, password, admin_role FROM users WHERE login = '{login_name}' AND password = '{password}'"

            temp_login = False  # для звичайного користувача
            temp_admin_login = False  # для адміна

            with sqlite3.connect('hospital.db') as conn:
                cur = conn.cursor()
                cur.execute(check_login)
                login_result = cur.fetchall()

            if not login_result:
                count += 1
                print("У доступі відхилено.\n")

            elif login_result[0] and login_result[0][2]:
                temp_login = False
                temp_admin_login = True
                count += 2

            elif login_result[0]:
                temp_login = True
                count += 2

        if temp_admin_login:
            while True:
                choose = int(input("\nЯкщо ви хочете подивитись всiх пацієнтів, натисніть '1'.\n"
                                   "Якщо хочете знайти пацієнта, натисніть '2'.\n"
                                   "Якщо хочете додати пацієнта, натисніть '3'\n"
                                   "Для виходу в головне меню, натисніть '0'.\n"))

                if choose == 1:
                    all_pacient()

                elif choose == 2:

                    delete_patient(search_patient)()

                elif choose == 3:
                    add_pacient()

                elif choose == 0:
                    break
                else:
                    print("Такої функції не знайдено! Будь ласка, спробуйте ще раз!")

        if temp_login:
            while True:
                choose = int(input("\nЯкщо ви хочете подивитись всiх пацієнтів, натисніть '1'.\n"
                                   "Якщо хочете знайти пацієнта, натисніть '2'.\n"
                                   "Для виходу в головне меню, натисніть '0'.\n"))

                if choose == 1:
                    all_pacient()

                elif choose == 2:
                    search_patient()

                elif choose == 0:
                    break
                else:
                    print("Такої функції не знайдено! Будь ласка, спробуйте ще раз!")

    except Exception as error:
        print("Не вдалося підключитися.")
        print(f"Головна помилка: {error}")

    finally:
        print("Вихід в головне меню\n")


def all_pacient():
    ''' Функция all_pacient отображает всех пациентов, содержащихся в базе данных, с их именами,
     фамилиями, текущим состоянием здоровья и диагнозом (если есть) '''

    with sqlite3.connect('hospital.db') as conn:
        cursor = conn.cursor()

        # додаємо нового користувача до таблиці
        cursor.execute("SELECT patients.name, patients.surname, patients.health, patients.disease FROM patients")
        result = cursor.fetchall()

        headers = ['Ім`я', 'Фамілія', 'Стан пацієнта', 'Хвороба']
        print(tabulate(result, headers=headers, tablefmt='grid'))

        conn.commit()
        print("Всі пацієнти показані! ")


def add_pacient():
    ''' Эта функция запрашивает у пользователя данные нового пациента
    (имя, фамилию, состояние пациента и болезнь) и добавляет их в базу данных. '''

    new_name = input("Введіть ім'я: ")
    new_surname = input("Введіть фамілію: ")
    new_health = input("Введіть стан пацієнта 'лікар': ")
    new_disease = input("Введіть хворобу пацієнта 'лікар': ")

    # відкриваємо з'єднання з базою даних в контексті with
    with sqlite3.connect('hospital.db') as conn:
        cursor = conn.cursor()

        # додаємо нового користувача до таблиці
        cursor.execute("INSERT INTO patients (name, surname, health, disease) VALUES (?, ?, ?, ?)",
                       (new_name, new_surname, new_health, new_disease))

        conn.commit()
        print("Користувача успішно створено! ")


def search_patient():
    ''' Функция search_patient() осуществляет поиск пациента в базе данных по заданным имени и фамилии. '''

    # відкриваємо з'єднання з базою даних та створюємо курсор
    with sqlite3.connect('hospital.db') as conn:
        cur = conn.cursor()

        # запитуємо прізвище для пошуку
        name = input("Введіть ім'я пацієнта: ")
        surname = input("Введіть прізвище пацієнта: ")

        # виконуємо запит до БД з використанням параметризованого запиту
        cur.execute("SELECT * FROM patients WHERE (name, surname)=(?, ?)", (name, surname))
        result = cur.fetchall()
        print(result)
        # перевіряємо, чи було знайдено хоча б одного пацієнта
        if len(result) == 0:
            print("Пацієнт не знайдений!")
        else:
            # виводимо результат пошуку
            headers = ['Ім`я', 'Фамілія', 'Стан пацієнта', 'Хвороба']
            print(tabulate(result, headers=headers, tablefmt='grid'))
            return result


def delete_patient(func):
    ''' Эта функция представляет собой декоратор, который добавляет функциональность удаления пациента из базы данных. '''

    def wrapper():
        # спочатку викликаємо функцію search_patient()
        result = func()
        name, surname = result[0][1:3]

        answer = input("Чи потрібно видалити пацієнта? (так/ні): ")
        if answer.lower() == "так":
            with sqlite3.connect('hospital.db') as conn:
                cur = conn.cursor()
                cur.execute("DELETE FROM patients WHERE name=? AND surname=?", (name, surname))
                conn.commit()

                print(f"Пацієнта {name} {surname} успішно видалено з бази даних.")

        return result

    return wrapper

