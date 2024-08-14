class Library:
    def __init__(self):
        self.books = {}
        self.members = {}

    def add_book(self, book_id, title, author, copies=1):
        if book_id in self.books:
            self.books[book_id]['copies'] += copies
        else:
            self.books[book_id] = {'title': title, 'author': author, 'copies': copies, 'available': copies}

    def remove_book(self, book_id, copies=1):
        if book_id in self.books:
            if self.books[book_id]['copies'] >= copies:
                self.books[book_id]['copies'] -= copies
                self.books[book_id]['available'] = min(self.books[book_id]['available'], self.books[book_id]['copies'])
                if self.books[book_id]['copies'] == 0:
                    del self.books[book_id]
                return True
        return False

    def register_member(self, member_id, name):
        if member_id not in self.members:
            self.members[member_id] = {'name': name, 'books_borrowed': []}
            return True
        return False

    def borrow_book(self, book_id, member_id):
        if book_id in self.books and member_id in self.members:
            if self.books[book_id]['available'] > 0:
                self.books[book_id]['available'] -= 1
                self.members[member_id]['books_borrowed'].append(book_id)
                return True
        return False

    def return_book(self, book_id, member_id):
        if book_id in self.books and member_id in self.members:
            if book_id in self.members[member_id]['books_borrowed']:
                self.books[book_id]['available'] += 1
                self.members[member_id]['books_borrowed'].remove(book_id)
                return True
        return False

    def get_available_books(self):
        return {k: v for k, v in self.books.items() if v['available'] > 0}

    def get_member_borrowed_books(self, member_id):
        if member_id in self.members:
            return [self.books[book_id]['title'] for book_id in self.members[member_id]['books_borrowed']]
        return []

def calculate_late_fee(days_overdue):
    if days_overdue <= 0:
        return 0
    elif days_overdue <= 7:
        return days_overdue * 0.5
    else:
        return 3.5 + (days_overdue - 7) * 1

def format_book_info(book):
    return f"{book['title']} by {book['author']} ({book['available']}/{book['copies']} available)"