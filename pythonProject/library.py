import json
import csv
from abc import ABC, abstractmethod

# Singleton: Zarządzanie katalogiem książek
class LibraryCatalog:
    _instance = None

    @staticmethod
    def get_instance():
        if LibraryCatalog._instance is None:
            LibraryCatalog._instance = LibraryCatalog()
        return LibraryCatalog._instance

    def __init__(self):
        if LibraryCatalog._instance is not None:
            raise Exception("Użyj get_instance(), aby uzyskać dostęp do Singletona.")
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def get_books(self):
        return self.books

# Adapter: Przetwarzanie różnych formatów danych książek
class BookDataAdapter(ABC):
    @abstractmethod
    def adapt_data(self, data):
        pass

class JSONBookAdapter(BookDataAdapter):
    def adapt_data(self, data):
        return json.loads(data)

class CSVBookAdapter(BookDataAdapter):
    def adapt_data(self, data):
        books = []
        reader = csv.DictReader(data.splitlines())
        for row in reader:
            books.append(row)
        return books

# Factory: Tworzenie różnych typów użytkowników
class User(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def get_permissions(self):
        pass

class Student(User):
    def get_permissions(self):
        return "Can borrow up to 3 books."

class Teacher(User):
    def get_permissions(self):
        return "Can borrow up to 10 books."

class Librarian(User):
    def get_permissions(self):
        return "Can manage books and users."

class UserFactory:
    @staticmethod
    def create_user(user_type, name):
        if user_type == "Student":
            return Student(name)
        elif user_type == "Teacher":
            return Teacher(name)
        elif user_type == "Librarian":
            return Librarian(name)
        else:
            raise ValueError(f"Unknown user type: {user_type}")

# Observer: Powiadomienia dla użytkowników
class Observer(ABC):
    @abstractmethod
    def update(self, message):
        pass

class UserObserver(Observer):
    def __init__(self, name):
        self.name = name

    def update(self, message):
        print(f"Powiadomienie dla {self.name}: {message}")

class LibraryNotifier:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, observer):
        self.subscribers.append(observer)

    def unsubscribe(self, observer):
        self.subscribers.remove(observer)

    def notify(self, message):
        for subscriber in self.subscribers:
            subscriber.update(message)

# Facade: Upraszczanie interakcji z biblioteką
class LibraryInterface:
    def __init__(self):
        self.catalog = LibraryCatalog.get_instance()
        self.notifier = LibraryNotifier()

    def add_book(self, book):
        self.catalog.add_book(book)
        self.notifier.notify(f"Książka '{book}' została dodana do katalogu.")

    def borrow_book(self, book, user):
        if book in self.catalog.get_books():
            self.catalog.books.remove(book)
            self.notifier.notify(f"{user.name} wypożyczył/a książkę '{book}'.")
        else:
            print(f"Książka '{book}' nie jest dostępna.")

    def return_book(self, book, user):
        self.catalog.add_book(book)
        self.notifier.notify(f"{user.name} zwrócił/a książkę '{book}'.")

# Iterator: Iteracja po książkach i użytkownikach
class BookIterator:
    def __init__(self, books):
        self.books = books
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.books):
            book = self.books[self.index]
            self.index += 1
            return book
        else:
            raise StopIteration
