from collections import UserDict

# Базовий клас для полів запису
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

# Клас для зберігання імені контакту. Обов'язкове поле
class Name(Field):
    pass

# Клас для зберігання номера телефону. Має валідацію формату (10 цифр)
class Phone(Field):
    def __init__(self, value):
        if not (value.isdigit() and len(value) == 10):
            raise ValueError("Phone number must contain exactly 10 digits.")
        super().__init__(value)

# Клас для зберігання інформації про контакт, включно з іменем та списком телефонів
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

# Додавання телефонів
    def add_phone(self, phone):
        self.phones.append(Phone(phone))

# Пошук телефону
    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

# Видалення телефонів
    def remove_phone(self, phone):
        found = self.find_phone(phone)
        if found:
            self.phones.remove(found)

# Редагування телефонів
    def edit_phone(self, old_phone, new_phone):
        found = self.find_phone(old_phone)
        if not found:
            raise ValueError("Phone number not found.")
        new = Phone(new_phone)
        index = self.phones.index(found)
        self.phones[index] = new

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

# Клас для зберігання записів та керування ними
class AddressBook(UserDict):

# Додавання записів
    def add_record(self, record):
        self.data[record.name.value] = record

# Пошук записів за іменем
    def find(self, name):
        return self.data.get(name)

# Видалення записів за іменем
    def delete(self, name):
        if name in self.data:
            del self.data[name]

# Створення нової адресної книги
def main():
    book = AddressBook()

# Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
# Додавання запису John до адресної книги
    book.add_record(john_record)

# Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

# Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

# Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")
    print(john)

# Пошук конкретного телефону в записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")

# Видалення запису Jane
    book.delete("Jane")


if __name__ == "__main__":
    main()