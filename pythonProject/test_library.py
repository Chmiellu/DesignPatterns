from library import LibraryCatalog, JSONBookAdapter, CSVBookAdapter, UserFactory, LibraryNotifier, UserObserver, LibraryInterface, BookIterator

# Singleton
catalog = LibraryCatalog.get_instance()

# Adapter: Dodawanie książek z różnych formatów
json_data = '[{"title": "Clean Code"}, {"title": "Design Patterns"}]'
csv_data = "title\nRefactoring\nThe Pragmatic Programmer"

json_adapter = JSONBookAdapter()
csv_adapter = CSVBookAdapter()

for book in json_adapter.adapt_data(json_data):
    catalog.add_book(book["title"])

for book in csv_adapter.adapt_data(csv_data):
    catalog.add_book(book["title"])

# Factory: Tworzenie użytkowników
student = UserFactory.create_user("Student", "Anna")
teacher = UserFactory.create_user("Teacher", "Jan")
librarian = UserFactory.create_user("Librarian", "Maria")

print(student.get_permissions())
print(teacher.get_permissions())
print(librarian.get_permissions())

# Observer: Subskrypcje powiadomień
notifier = LibraryNotifier()
user1 = UserObserver("Anna")
user2 = UserObserver("Jan")
notifier.subscribe(user1)
notifier.subscribe(user2)

notifier.notify("Nowa książka dostępna!")

# Facade: Interakcja z biblioteką
library = LibraryInterface()
library.add_book("Python for Beginners")
library.borrow_book("Clean Code", student)
library.return_book("Clean Code", student)

# Iterator: Iteracja po książkach
books = catalog.get_books()
book_iterator = BookIterator(books)
for book in book_iterator:
    print(book)