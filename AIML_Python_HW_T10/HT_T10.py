from collections import UserDict
from datetime import datetime, date, timedelta

# Базовий клас для полів запису
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

# Клас для зберігання імені контакту. Обов'язкове поле
class Name(Field):
    pass

# Клас для зберігання номера телефону. Має формат (10 цифр)
class Phone(Field):
    def __init__(self, value):
        if not (value.isdigit() and len(value) == 10):
            raise ValueError("Phone number must contain exactly 10 digits.")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
# додано перевірку коректності даних та перетворено рядок на об'єкт datetime
            date_value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(date_value)

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")

# Клас для зберігання інформації про контакт, включно з іменем та списком телефонів
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def remove_phone(self, phone):
        found = self.find_phone(phone)
        if found:
            self.phones.remove(found)

    def edit_phone(self, old_phone, new_phone):
        found = self.find_phone(old_phone)
        if not found:
            raise ValueError("Phone number not found.")
        new = Phone(new_phone)
        index = self.phones.index(found)
        self.phones[index] = new

# додано день народження до контакту
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones = "; ".join(p.value for p in self.phones)
        result = f"Contact name: {self.name.value}, phones: {phones}"
        if self.birthday:
            result += f", birthday: {self.birthday}"
        return result

def replace_year(day, year):
    try:
        return day.replace(year=year)
    except ValueError:
        return date(year, 3, 1)

# Клас для зберігання записів та керування ними
class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):

        today = datetime.today().date()
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday is None:
                continue

            birthday = record.birthday.value
            birthday_this_year = birthday.replace(year=today.year)

# Якщо день народження в цьому році вже минув, беремо наступний рік
            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            days_until = (birthday_this_year - today).days

            if 0 <= days_until <= 7:
                congratulation_date = birthday_this_year

# Субота -> понеділок (+2 дні), неділя -> понеділок (+1 день)
                if congratulation_date.weekday() == 5:
                    congratulation_date += timedelta(days=2)
                elif congratulation_date.weekday() == 6:
                    congratulation_date += timedelta(days=1)

                upcoming_birthdays.append({
                    "name": record.name.value,
                    "congratulation_date": congratulation_date.strftime("%d.%m.%Y"),
                })
        return upcoming_birthdays

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as error:
            return str(error)
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Enter the argument for the command."
    return inner

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book: AddressBook):
    if len(args) < 2:
        raise ValueError("Give me name and phone please.")
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    is_new = record is None
    if is_new:
        record = Record(name)
        message = "Contact added."
    record.add_phone(phone)
    if is_new:
        book.add_record(record)
    return message

@input_error
def change_contact(args, book: AddressBook):
    if len(args) < 3:
        raise ValueError("Give me name, old phone and new phone please.")
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    record.edit_phone(old_phone, new_phone)
    return "Contact updated."

@input_error
def show_phone(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError
    if not record.phones:
        return f"{name} has no phones."
    return "; ".join(p.value for p in record.phones)

@input_error
def show_all(book: AddressBook):
    if not book.data:
        return "No contacts saved."
    return "\n".join(str(record) for record in book.data.values())

@input_error
def add_birthday(args, book: AddressBook):
    if len(args) < 2:
        raise ValueError("Give me name and birthday please.")
    name, birthday, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    record.add_birthday(birthday)
    return "Birthday added."

@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError
    if record.birthday is None:
        return f"{name} has no birthday set."
    return str(record.birthday)

@input_error
def birthdays(args, book: AddressBook):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No birthdays in the next 7 days."
    return "\n".join(
        f"{item['name']}: {item['congratulation_date']}" for item in upcoming
    )

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        if not user_input.strip():
            continue

        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()