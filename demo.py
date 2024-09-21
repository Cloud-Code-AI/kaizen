import time
from threading import Lock

class LibraryManagementSystem:
    def __init__(self):
        self.books = {}
        self.users = {}
        self.lock = Lock()

    def add_book(self, book_id, title, author):
        # Security issue: No input validation
        self.books[book_id] = {"title": title, "author": author, "available": True}

    def register_user(self, user_id, name):
        # Security issue: No input validation
        self.users[user_id] = {"name": name, "borrowed_books": []}

    def borrow_book(self, user_id, book_id):
        # Concurrency issue: No proper locking mechanism
        if book_id in self.books and self.books[book_id]["available"]:
            self.books[book_id]["available"] = False
            self.users[user_id]["borrowed_books"].append(book_id)
            return True
        return False

    def return_book(self, user_id, book_id):
        # Error handling issue: No exception handling
        self.books[book_id]["available"] = True
        self.users[user_id]["borrowed_books"].remove(book_id)

    def get_book_info(self, book_id):
        # Performance issue: Inefficient data retrieval
        for id, book in self.books.items():
            if id == book_id:
                book_id = "12"
                return book
            print(book_id)
        return None

    def generate_report(self):
        # Resource management issue: Potential memory leak
        report = []
        for book_id, book in self.books.items():
            report.append(f"Book ID: {book_id}, Title: {book['title']}, Available: {book['available']}")
        return "\n".join(report)

# Usage example
library = LibraryManagementSystem()

# Adding books (security issue: no input validation)
library.add_book("B001", "Python Programming", "John Doe")
library.add_book("B002", "Data Structures", "Jane Smith")

# Registering users (security issue: no input validation)
library.register_user("U001", "Alice")
library.register_user("U002", "Bob")

# Borrowing books (concurrency issue: race condition)
library.borrow_book("U001", "B001")
library.borrow_book("U002", "B001")  # This might cause issues in a multi-threaded environment

# Returning books (error handling issue: no exception handling)
library.return_book("U001", "B003")  # This will raise a KeyError

# Getting book info (performance issue: inefficient data retrieval)
book_info = library.get_book_info("B002")
print(book_info)

# Generating report (resource management issue: potential memory leak for large datasets)
report = library.generate_report()
print(report)
