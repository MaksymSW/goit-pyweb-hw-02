

from collections import UserDict
from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    # реалізація класу
    def __init__(self, value):
        self.value = value

class Phone(Field):
    # реалізація класу
    def __init__(self, value):
        if len(value)==10 and value.isdigit():
            super().__init__(value)
        else:
            raise ValueError("The phone number must be a string and consist of 10 digits")
        
class Birthday(Field):
    def __init__(self, value):
        try:
            # Додайте перевірку коректності даних
            # та перетворіть рядок на об'єкт datetime
            date = datetime.strptime(value, "%d.%m.%Y").date()
            super().__init__(date)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")



		

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
    # реалізація класу

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"
    
    def add_phone(self,phone):
        self.phones.append(Phone(phone))


    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        if self.find_phone(old_phone):
            self.remove_phone(old_phone)
            self.add_phone(new_phone)
        else:
            raise ValueError("The phone number does not exist")
         

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None
    
    def add_birthday(self, birthday):
        if self.birthday:
            raise ValueError("A date of birth already exists for this contact")
        self.birthday = Birthday(birthday)


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name: str):
        return self.data.get(name)
        
    def delete(self, name: str):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        
        upcoming_birthdays=[]
        today = datetime.today().date()

        
        for user in self.data.values():   
            if user.birthday is None: continue
            birthday:datetime = user.birthday.value
            birthday_this_year = datetime(today.year, birthday.month, birthday.day).date()

            diffrence = birthday_this_year - today

            if diffrence <= timedelta(days=6) and diffrence >= timedelta(days=0):
                if birthday_this_year.weekday() == 5:
                    birthday_this_year = birthday_this_year + timedelta(days=2)
                if birthday_this_year.weekday() == 6:
                    birthday_this_year = birthday_this_year + timedelta(days=1)
        
                # congrat_date = birthday_this_year.strftime("%Y.%m.%d")

                # to_congratulate = {"name": user["name"], "congratulation_date": congrat_date}
                # upcoming_birthdays.append(to_congratulate.copy())
                upcoming_birthdays.append({'name': user.name.value,
                        'congratulation': birthday_this_year.strftime('%d.%m.%Y')})

            return upcoming_birthdays
    def __str__(self):
        # Представлення телефонної книги у зрозумілому форматі
        return "\n".join(str(user) for user in self.data.values())
