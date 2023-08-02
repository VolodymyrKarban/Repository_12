#from collections import UserDict, UserList
from datetime import datetime
from classes import  Field, Name, Phone, Birthday, Record, AddressBook
import re, os, pickle
#import keyboard
#import click 

def error(function):
    def error_processing(list_input):
        try:
            return function(list_input)
        except ValueError:
            return print("Трапилася помилка: ValueError")
        except IndexError:
            return print("Трапилася помилка: IndexError Було введено не вірні данні")
        except TypeError:
            return print("Трапилася помилка: TypeError")
    return error_processing

def hi(*args):
    return print("How can I help you?")

#Перевірка дати та телефону на введення.
def input_date_check(str_date):
    try:
        return datetime.strptime(str_date, "%d-%m-%Y").date()
    except ValueError:
        print("Введіть коректну дату. Формат: dd-mm-yyyy")
        return None  

def input_phone_check(str_phone):
    if re.findall(r'[+][0-9]{12}', str_phone) and (len(str_phone) == 13):
        return True
    else:
        print("Введіть коректно телефонний номер у міжнародному форматі: +380********* ")
        return None

@error
def add(list_input):

    phone = None
    bd = None
    name = Name(list_input[1].capitalize())

    if len(list_input)>=3:
        if (input_phone_check(list_input[2])):           
            phone = Phone(list_input[2])
    if len(list_input)>=4:
        if (input_date_check(list_input[3])):    
            bd = Birthday(list_input[3]) 

    rec: Record = phone_book.get(str(name))
    
    if rec:
        
        return rec.add_phone(phone,bd)
    rec = Record(name,phone,bd)
    phone_book.add_rec(rec)

def add_bd(list_input):
    if len(list_input)>=4:
        if input_date_check(list_input[3]):
            for i in phone_book.keys():
                if i == list_input[2].capitalize():
                    bd = Birthday(list_input[3])
                    rec: Record = phone_book.get(str(i))
                    rec.add_birthday(bd)
                    return print ("До контакту ",i," було добавлено дату народження ", list_input[3])
            print("Такого імені немає в контактах")    
    print ("Введіть після команди 'add bd' ім'я та дату народження у форматі: dd-mm-yyyy ")            

def search_contact(list_input):
    if len(list_input) >= 2:
        print("Шукаємо: ",list_input[1])
        for i in phone_book.keys():
            rec = phone_book.get(str(i))        
            if ((i.lower()).find(list_input[1].lower())) != -1:
                print("Співпадіння:  ", phone_book.get(str(i)), rec.days_to_birthday())
                #print("Співпадіння:  ", (rec.__dict__).get("name")," ",(rec.__dict__).get("phones"))
            for f in (rec.__dict__).get("phones"):
                if (str(f).find(list_input[1])) != -1:
                    print("Співпадіння:  ", phone_book.get(str(i)), rec.days_to_birthday())

    else:
        return print(f"Введіть для пошуку коректну інфу: ' Команду: sc < Ім'я >, або його частину, або номер чи його частину.\nВ такому разі Вам роздрукую всі співпадіння'")

def change(list_input):
    if (len(list_input) < 4) and ((input_phone_check(list_input[2]))and(input_phone_check(list_input[3]))):
        return print("Для зміни номеру введіть після команди 'change' ім'я та номер який треба змінити та новий номер  у форматі: dd-mm-yyyy.")
    if len(list_input) >= 4:
        for i in phone_book.keys():
            if (list_input[1].capitalize()) == i:
                old_ph = Phone(list_input[2])
                new_ph = Phone(list_input[3])
                rec: Record = phone_book.get(str(i))
                if rec:
                    rec.change_phone(old_ph,new_ph)
                return None
    print("Контакт з таким ім'ям не знайдено тому було сформовано новий контакт та збережено обидва номери")              
    name = Name(list_input[1].capitalize())
    phone = Phone(list_input[2])
   
    rec = Record(name, phone)
    phone = Phone(list_input[3])
    rec.add_phone(phone)
    phone_book.add_rec(rec)

def phone(list_input):
    for i in phone_book.keys():
            if (list_input[1].capitalize()) == i:
                rec: Record = phone_book.get(str(i))
                return print(f"Ваш контакт:\n{phone_book[i]} {rec.days_to_birthday()}")
    return print(f"Ваш контакт {list_input[1].capitalize()} не знайдено.")
             
def show_all(list_input):
    if len(list_input) == 2:
        print("Ваш список контактів:")
        print(phone_book)
    elif len(list_input) > 2:
        try:
            int(list_input[2])
        except ValueError:
            list_input[2]=0
        nstr = int(list_input[2])
        if nstr>0:
            long = len(phone_book)
            if long <= nstr:
                print("Ваш список контактів:")
                print(phone_book)
            else:
                print_page(nstr)
        else:
            print("Ваш список контактів:")
            print(phone_book)


def  print_page(n):
    f=0
    fn=0
    for i in phone_book.keys():
        f =f+1
        fn=fn+1 
        print(fn," ",phone_book.get(str(i)))
        if f == n:
            f = 0
            #click.pause('Чтобы продолжить, нажмите Enter.')
            nn = True
            while nn:
                nn = (input(f"Щоб подивитися наступні {n} контакти натисніть Enter."))
                nn = False
    print("Всі контакти показано.\n")


def show_birthday(list_input):
    f = True
    for i in phone_book.keys():
        f = None
        rec: Record = phone_book.get(str(i))
        print(f"Ім'я: {rec.name}, Контактний номер: {' '.join(str(rec) for rec in rec.phones)} {rec.days_to_birthday()}")
    if f:
        print("Ваш список контактів порожній.")    
    
def not_know():
    str_out = "Сommands not recognized.\nEnter commands that I know: "
    for i in list_out:
        str_out += (str(i) + ", ")
    str_out += "if you want me to finish working.\nOr one of the commands: "
    for i in dict_def.keys():
        str_out += (i + ", ")
    str_out += "if you want me to help you."
    return str_out

def  double_commands(list):
    if (len(list)>1) and ((list[0] == "show") and (list[1].lower() == "all")):
        return "show_all" 
    
    if (len(list)>1) and ((list[0] == "add") and (list[1].lower() == "bd")):
        return "add_bd" 
        
    return list[0]

def load_bot_book():
    path_bot_12 = ("save_bot_12_book.bin")
    if os.path.exists(path_bot_12):
        with open(path_bot_12,"br") as fbr:
            fbr_list = pickle.load(fbr)
        return fbr_list
    else:
        return None  
    
def save_bot_book(list):
    path_bot_12 = ("save_bot_12_book.bin")
    with open(path_bot_12,"bw") as fwb:
        pickle.dump(list, fwb)
    print("Записник збережено.\n")

list_out = ["good bye","close","exit","e"]
dict_def = {"hello": hi, "add": add, "change": change, "phone": phone, "show_all": show_all, "add_bd":  add_bd, "bd": show_birthday, "sc": search_contact}

def bot_start():
    print("\nHi, I'm a helper bot))). How can I help you?")
    list_command = []
    while True:
        input_text = input("Waiting for commands: ").lower()
        list_command = re.split(r"[ ]+",input_text)
        list_command[0] = double_commands(list_command)
        if list_command[0] in dict_def.keys():
            dict_def[list_command[0]](list_command)
        elif input_text in list_out:
            print("Good bye!")
            break
        else:
            print(not_know())

phone_book = AddressBook()

if load_bot_book():
    phone_book = load_bot_book()
    print("\nЗаписник загружено.")
else:
    print("\nЗаписник порожній.")

bot_start()

save_bot_book(phone_book)


#       python C:\Repository\Repository_12\bot_12_02.py