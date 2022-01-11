"""
1. Доповніть програму-банкомат наступним функціоналом:
   - новий пункт меню, який буде виводити поточний курс валют (API Приватбанк)
2. Написати скрипт, який буде приймати від користувача назву валюти і початкову дату.
   - Перелік валют краще принтануть.
   - Також не забудьте указати, в якому форматі коритувач повинен ввести дату.
   - Додайте перевірку, чи введена дата не знаходиться у майбутньому ;)
   - Також перевірте, чи введена правильна валюта.
   Виконуючи запроси до API архіву курсу валют Приватбанку, вивести інформацію про зміну
   курсу обраної валюти (Нацбанк) від введеної дати до поточної. Приблизний вивід наступний:
   Currency: USD
   Date: 12.12.2021
   NBU:  27.1013   -------
   Date: 13.12.2021
   NBU:  27.0241   -0,0772
   Date: 14.12.2021
   NBU:  26.8846   -0,1395
3. Конвертер валют. Прийматиме від користувача назву двох валют і суму (для першої).
   Робить запрос до API архіву курсу валют Приватбанку (на поточну дату) і виконує
   конвертацію введеної суми з однієї валюти в іншу.
P.S. Не забувайте про файл requirements.txt
P.P.S. Не треба сходу ДДОСить Приватбанк - додайте хоча б по 0.5 секунди між запросами.
       Хоч у них і не написано за троттлінг, але будьмо чемними ;)
Інформація для виконання:
- документація API Приватбанка:
  - архів курсів: https://api.privatbank.ua/#p24/exchangeArchive
  - поточний курс: https://api.privatbank.ua/#p24/exchange
- інформація про використання форматування дати в Python: https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
- модуль requests: https://docs.python-requests.org/en/latest/
"""

import requests
from time import sleep
from datetime import timedelta, datetime


class BankRate(object):
    @classmethod
    def __exchange_rates(cls):
        try:
            url = "https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5"
            rec_well = requests.get(url)
            rec_well = rec_well.json()
            if str(requests.get(url)) == "<Response [200]>":
                print(f"""currency               sale                buy
      {rec_well[0]["ccy"]:5.5s}{float(rec_well[0]["buy"]):20.2f}{float(rec_well[0]["sale"]):20.2f}
      {rec_well[1]["ccy"]:5.5s}{float(rec_well[1]["buy"]):20.2f}{float(rec_well[1]["sale"]):20.2f}
      {rec_well[2]["ccy"]:5.5s}{float(rec_well[2]["buy"]):20.2f}{float(rec_well[2]["sale"]):20.2f}
      {rec_well[3]["ccy"]:5.5s}{float(rec_well[3]["buy"]):20.2f}{float(rec_well[3]["sale"]):20.2f}""")
            else:
                print("<the server does not respond>")
        except:
            raise Exception("<no network>")

    @classmethod
    def __daterange(cls, start_date):
        for n in range(int((datetime.now() - start_date).days + 1)):
            yield start_date + timedelta(n)

    @classmethod
    def __get_currency_exchange_rate_by_date(cls, date_in):
        url_string: str = f"https://api.privatbank.ua/p24api/exchange_rates?json&"
        req = requests.get(url=url_string, params={
            "date": date_in
        })
        req_data = req.json()
        return req_data

    @classmethod
    def __get_currency_by_date_range(cls, start_date, currency: str):
        try:
            data_list: list = []
            rate: str = None
            currency_string: str
            currency_list: list = ["USD", "EUR", "RUB", "CHF", "GBP", "PLZ", "SEK", "CAD"]

            for curr in currency_list:
                if currency == curr:
                    currency_string = curr
                    print(f"Current currency: {curr}")

            if currency in currency_list:
                for single_date in cls.__daterange(start_date):
                    data: dict = cls.__get_currency_exchange_rate_by_date(single_date.strftime("%d.%m.%Y"))

                    date_value: str = data["date"]
                    temp_val = data["exchangeRate"]

                    for i in range(0, len(temp_val)):
                        for j in currency_list:
                            if list(temp_val[i].values())[1:][0] == currency_string:
                                rate = list(temp_val[i].values())[1:][1]

                    data_list.append([date_value, rate])

                for num_list in range(0, len(data_list)):
                    sleep(1)
                    if num_list == 0:
                        print(f"Date:       {data_list[num_list][0]}")
                        print(f"NBU Rate:   {data_list[num_list][1]}    {'---'}")
                    else:
                        print(f"Date:       {data_list[num_list][0]}")
                        print(
                            f"NBU Rate:   {data_list[num_list][1]}    {data_list[num_list][1] - data_list[num_list - 1][1]:.4f}")
            else:
                print(f"{currency} currency unavailable")
        except:
            raise Exception("<no network>")

    @classmethod
    def __currency_converter(cls, arg_1: str = "", arg_2: str = "", arg_3: float = 1):
        try:
            data_list: list = []
            currency_string: str
            rate_1: str = "1"
            rate_2: str = "1"
            currency_list: list = ["UAH", "USD", "EUR", "RUB", "CHF", "GBP", "PLZ", "SEK", "CAD"]

            data: dict = cls.__get_currency_exchange_rate_by_date(datetime.now().strftime("%d.%m.%Y"))
            date_value: str = data["date"]
            temp_val = data["exchangeRate"]
            # print(temp_val)
            if len(temp_val) == 0:
                day = int(datetime.now().strftime("%d"))
                month = int(datetime.now().strftime("%m"))
                year = int(datetime.now().strftime("%Y"))

                date = datetime(year, month, day)
                date -= timedelta(days=1)

                data: dict = cls.__get_currency_exchange_rate_by_date(date.now().strftime("%d.%m.%Y"))
                date_value: str = data["date"]
                temp_val = data["exchangeRate"]
                print(f"Exchange rate for {date_value}")

            for curr in currency_list:
                if arg_1 == curr:
                    currency_string = curr
                    # print(f"Current currency: {curr}")

            for i in range(0, len(temp_val)):
                # for j in currency_list:
                if list(temp_val[i].values())[1:][0] == currency_string:
                    rate_1 = list(temp_val[i].values())[1:][1]
            # print(rate_1)

            for curr in currency_list:
                if arg_2 == curr:
                    currency_string = curr
                    # print(f"Current currency: {curr}")

            for i in range(0, len(temp_val)):
                # for j in currency_list:
                if list(temp_val[i].values())[1:][0] == currency_string:
                    rate_2 = list(temp_val[i].values())[1:][1]
            # print(rate_2)

            difference = float(rate_1) / float(rate_2)
            sum_cur = float(arg_3) * difference
            return sum_cur
        except:
            raise Exception("<no network>")

    @classmethod
    def currency_console(cls, valid):
        while True:
            if valid:
                print("*" * 32)
                print("1. Сurrent exchange rate: ")
                print("2. Archive of exchange rate changes: ")
                print("3. Currency Converter: ")  # змінити кількість купюр
                print("4. Exit")
                print("*" * 32)
                menu_item = input("Choose : ")
                if int(menu_item) == 1:
                    cls.__exchange_rates()
                elif int(menu_item) == 2:
                    while True:
                        try:
                            print("*" * 100)
                            print("database starts from 01.12.2014.")
                            print(
                                "Available courses \"USD\", \"EUR\", \"RUB\", \"CHF\", \"GBP\", \"PLZ\", \"SEK\", \"CAD\"")
                            print("*" * 100)

                            course_abbreviation = input("enter the abbreviation code of the course -> ").upper()
                            if course_abbreviation in ["USD", "EUR", "RUR", "CHF", "GBP", "PLZ", "SEK", "XAU", "CAD"]:

                                day = int(input("1. enter the day of the week in the range -> 1–31. -> "))
                                if day in range(1, 31 + 1):

                                    mounth = int(input("2. enter the month in the range -> 1–12. -> "))
                                    if mounth in range(1, 12 + 1):

                                        year = int(
                                            input(f"3. enter the month in the range -> 2014–{datetime.now().year} -> "))
                                        if year <= datetime.now().year:
                                            start_date = datetime(year, mounth, day)
                                            cls.__get_currency_by_date_range(start_date, course_abbreviation)

                                            print("*" * 60)
                                            yes = input('if you want to leave the program press "Y" if not then "N": ')
                                            print("*" * 60)
                                            if "y" == yes.lower():
                                                break
                                            else:
                                                continue
                                        else:
                                            print(
                                                f"you have exceeded the current year limit or entered an incorrect number -> {year}")

                                    else:
                                        print(
                                            f"<you have exceeded the month limit of the year or entered a wrong number -> {mounth}.>")

                                else:
                                    print(
                                        f"<you have exceeded the limit of the day of the month or entered a wrong number - > {day}.>")

                            else:
                                print(f"<{course_abbreviation} currency unavailable>")
                        except Exception as err:
                            print(f"<error -> {err}>")

                elif int(menu_item) == 3:
                    while True:
                        try:
                            print("*" * 100)
                            print("currency converter 1.UHA -> 2.USA = 3.USA ")
                            print(
                                "Available courses \"UAH\", \"USD\", \"EUR\", \"RUB\", \"CHF\", \"GBP\", \"PLZ\", \"SEK\", \"CAD\"")
                            print("*" * 100)

                            base_unit = input("1. -> ").upper()
                            if base_unit in ["UAH", "USD", "EUR", "RUB", "CHF", "GBP", "PLZ", "SEK", "XAU", "CAD"]:

                                secondary_unit = input("2. -> ").upper()
                                if secondary_unit in ["UAH", "USD", "EUR", "RUB", "CHF", "GBP", "PLZ", "SEK", "CAD"]:

                                    base_currency_number = input("enter the amount -> ")
                                    if isinstance(float(base_currency_number), (float, int)):
                                        resul = cls.__currency_converter(base_unit, secondary_unit,
                                                                         float(base_currency_number))
                                        print(
                                            f"{base_currency_number} {base_unit} -> {resul:.4f} {secondary_unit}")

                                        print("*" * 60)
                                        yes = input('if you want to leave the program press "Y" if not then "N": ')
                                        print("*" * 60)
                                        if "y" == yes.lower():
                                            break
                                        else:
                                            continue

                                    else:
                                        print(f"<you entered not a number -> {base_currency_number}.>")
                                        continue

                                else:
                                    print(f"<{secondary_unit} currency unavailable>")

                            else:
                                print(f"<{base_unit} currency unavailable>")
                        except Exception as err:
                            print(f"<error -> {err}>")

                elif int(menu_item) == 4:
                    exit()
                else:
                    print("<choice error>")

# BankRate.currency_console(True)
