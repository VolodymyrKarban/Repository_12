from collections import UserDict, UserList
from datetime import datetime

class Field:
    def __init__(self, value):
         self.value = value
    
    def __str__(self):
        return self.value
    
    def __repr__(self):
        return str(self)


class Name(Field):
    pass

class Phone(Field):
    pass

class Birthday(Field):
    pass

class Record():
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None):
        self.name = name
        self.phones =  []
        if phone:
            self.phones.append(phone)
        self.birthday = birthday

    def add_phone(self, phone: Phone, birthday: Birthday = None ):
        if birthday:
            self.birthday = birthday

        if phone:                                                                   
            if phone.value not in [phone.value for phone in self.phones]:
                self.phones.append(phone)
                return print(f"Номер {phone} було добавлено до контакту {self.name} та збережено.")
            return print (f"Номер {phone} вже записаний у номерах контакту {self.name}")
    
    def add_birthday(self, birthday: Birthday):
            self.birthday = birthday
    
    def change_phone(self,old_phone,new_phone):
        for i,p in enumerate(self.phones):
            if old_phone.value == p.value:
                self.phones[i] = new_phone
                return print(f"Старий номер {old_phone} було змінено на новий номер {new_phone}")
        print (f"Старий номер {old_phone} не знайдено. Новий номер {new_phone} був доданий до контакту {self.name}")
        self.phones.append(new_phone) 


    def days_to_birthday(self):
        if self.birthday:
            year_now = datetime.now().year
            birth_day = datetime.strptime(str(self.birthday), "%d-%m-%Y")

            if birth_day > datetime.now():
                return f"Судячи з записів Ваш контакт ще не народився)))) Перевірте дату. Дата народження: {birth_day.date()})))"
        #Перевірка дня народження у високосній даті
            if (birth_day.month == 2)and(birth_day.day == 29):
                if ((datetime(year_now,3,1) - datetime(year_now,2,28)).days)==2:
                    di = (datetime(year_now,2,29)-datetime.now()).days+1
                if ((datetime(year_now,3,1) - datetime(year_now,2,28)).days)==1:
                    di = (datetime(year_now,3,1)-datetime.now()).days+1
            else:
                di = (datetime(year_now,birth_day.month,birth_day.day)-datetime.now()).days+1        
                
            if di < 0:
                di =  di + 365
            if di == 0:
                return f"Вітайте сьогодні з Днем Народження!!! Дата народження: {birth_day.date()}"
            return f"До дня народження лишилося {di}  днів. Дата народження: {birth_day.date()}"
        return f"Відсутня інформація про дату народження."
        
        
    def __str__(self):
        return f"Ім'я: {self.name} Телефон: {' '.join(str(rec) for rec in self.phones)} День народження: {self.birthday}"  

 
class AddressBook(UserDict):
    #def __init__(self):
        #self.phone_book = {}

    #def show_all(self):
        #return self.phone_book
    
    def add_rec(self, record: Record):
        self.data[record.name.value] = record
        return print(f"Контакт:  {record} було добавлено.")
    
    def add_birthday(self, record: Record):
        self.data[record.birthday.value] = record
    
    def __str__(self) -> str:
        return "\n".join(str(rec) for rec in self.data.values())