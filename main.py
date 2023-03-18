from Login import *
from db_create import *


def register_user():
    with sqlite3.connect('hospital.db') as conn:
        cursor = conn.cursor()

        login = input("Введіть логін: ")
        password = input("Введіть пароль: ")
        admin_role = 0

        # додаємо нового користувача до таблиці
        cursor.execute("INSERT INTO users (login, password, admin_role) VALUES (?, ?, ?)",
                       (login, password, admin_role))

        conn.commit()
        print("Користувача успішно створено! ")

     
def main():
    is_runnig = True
    create_db()
    while is_runnig:
        print("1: Вхід\n2: Реєстрація\n0: Завершення програми\n")
        
        choose = int(input("Оберіть, що вам потрібно: 1, 2 або 0: "))
    
        if choose == 1:
            login_to_the_system()
            
        elif choose == 2:
            register_user()
            
        elif choose == 0:
            print("Бережіть себе!")
            break
            
        else: 
            print("Такої функції не знайдено! Будь ласка, спробуйте ще раз!")
            continue


main()
