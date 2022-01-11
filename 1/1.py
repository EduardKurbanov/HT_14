"""
Домашнє завдання №14: Переписати останню версію банкомата з використанням ООП.
Для уніфікації перевірки, в базі повинні бути 3 користувача:
  ім'я: user1, пароль: user1
  ім'я: user2, пароль: user2
  ім'я: admin, пароль: admin, special_key: admin (у цього коритувача - права інкасатора)
"""

from database import DataBase
from exchange_rate_processing import BankRate
from atm import Atm


def start():
    count = 3
    while True:
        try:
            login = input("enter login: ")
            password = input("enter password: ")
            print("if there is no additional key press skip the step: ")
            special_key = input("enter additional key: ")
            valid = Atm.set_valid_log_pass(login, password,special_key)
            while count > 0:
                if valid == "incasation":
                    Atm.console_admin(valid)

                if valid:
                    print("*" * 25)
                    print("1. Look at the balance")
                    print("2. Replenish the balance")  # пополнить счет
                    print("3. Withdraw cash")  # снять наличные
                    print("4. Сurrent exchange rate")
                    print("5. Exit")
                    print("*" * 25)
                    menu_item = input("Choose : ")
                    if int(menu_item) == 1:
                        Atm.get_check_balance(login)
                    elif int(menu_item) == 2:
                        Atm.get_replenish_balance(login)
                    elif int(menu_item) == 3:
                        Atm.get_withdraw_balance(login)
                    elif int(menu_item) == 4:
                        BankRate.currency_console(valid)
                    else:
                        DataBase.close_database()
                        exit()
                else:
                    count -= 1
                    print(f"attempt -> {count}")
                    break

                if count > 0:
                    continue
                else:
                    print("<exit the program automatically>")
            if count == 0:
                break

        except Exception as err:
            print(f"<error -> {err}>")


if __name__ in "__main__":
    start()
