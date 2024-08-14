import pytest
from examples.unittest.python_sample.library import Library

@pytest.fixture
def library():
    return Library()

def test_add_book(library):
    library.add_book(1, "Book Title", "Author Name", 3)
    assert library.books[1] == {'title': "Book Title", 'author': "Author Name", 'copies': 3, 'available': 3}

def test_remove_book(library):
    library.add_book(1, "Book Title", "Author Name", 3)
    assert library.remove_book(1, 2) is True
    assert library.books[1]['copies'] == 1
    assert library.books[1]['available'] == 1

def test_register_member(library):
    assert library.register_member(1, "Member Name") is True
    assert library.members[1] == {'name': "Member Name", 'books_borrowed': []}

def test_borrow_book(library):
    library.add_book(1, "Book Title", "Author Name", 3)
    library.register_member(1, "Member Name")
    assert library.borrow_book(1, 1) is True
    assert library.books[1]['available'] == 2
    assert 1 in library.members[1]['books_borrowed']

def test_return_book(library):
    library.add_book(1, "Book Title", "Author Name", 3)
    library.register_member(1, "Member Name")
    library.borrow_book(1, 1)
    assert library.return_book(1, 1) is True
    assert library.books[1]['available'] == 3
    assert 1 not in library.members[1]['books_borrowed']

def test_get_available_books(library):
    library.add_book(1, "Book Title", "Author Name", 3)
    library.add_book(2, "Another Book", "Another Author", 0)
    available_books = library.get_available_books()
    assert 1 in available_books
    assert 2 not in available_books

def test_get_member_borrowed_books(library):
    library.add_book(1, "Book Title", "Author Name", 3)
    library.register_member(1, "Member Name")
    library.borrow_book(1, 1)
    borrowed_books = library.get_member_borrowed_books(1)
    assert "Book Title" in borrowed_books

def test_remove_more_copies_than_available(library):
    library.add_book(1, "Book Title", "Author Name", 3)
    assert library.remove_book(1, 4) is False
    assert library.books[1]['copies'] == 3

def test_borrow_book_no_copies_available(library):
    library.add_book(1, "Book Title", "Author Name", 1)
    library.register_member(1, "Member Name")
    library.borrow_book(1, 1)
    assert library.borrow_book(1, 1) is False

def test_return_book_not_borrowed(library):
    library.add_book(1, "Book Title", "Author Name", 3)
    library.register_member(1, "Member Name")
    assert library.return_book(1, 1) is False

def test_get_available_books_none(library):
    available_books = library.get_available_books()
    assert len(available_books) == 0

def test_get_member_borrowed_books_none(library):
    library.register_member(1, "Member Name")
    borrowed_books = library.get_member_borrowed_books(1)
    assert len(borrowed_books) == 0

def test_remove_nonexistent_book(library):
    assert library.remove_book(1) is False

def test_register_existing_member(library):
    library.register_member(1, "Member Name")
    assert library.register_member(1, "Another Name") is False

def test_borrow_nonexistent_book(library):
    library.register_member(1, "Member Name")
    assert library.borrow_book(1, 1) is False

def test_borrow_nonexistent_member(library):
    library.add_book(1, "Book Title", "Author Name", 3)
    assert library.borrow_book(1, 1) is False

def test_return_nonexistent_book(library):
    library.register_member(1, "Member Name")
    assert library.return_book(1, 1) is False

def test_return_nonexistent_member(library):
    library.add_book(1, "Book Title", "Author Name", 3)
    assert library.return_book(1, 1) is False

def test_add_book_zero_copies(library):
    library.add_book(1, "Book Title", "Author Name", 0)
    assert library.books[1] == {'title': "Book Title", 'author': "Author Name", 'copies': 0, 'available': 0}

def test_remove_book_zero_copies(library):
    library.add_book(1, "Book Title", "Author Name", 3)
    assert library.remove_book(1, 0) is True
    assert library.books[1]['copies'] == 3

def test_register_member_empty_name(library):
    assert library.register_member(1, "") is True
    assert library.members[1] == {'name': "", 'books_borrowed': []}

def test_borrow_book_one_copy(library):
    library.add_book(1, "Book Title", "Author Name", 1)
    library.register_member(1, "Member Name")
    assert library.borrow_book(1, 1) is True
    assert library.books[1]['available'] == 0

def test_return_book_one_copy(library):
    library.add_book(1, "Book Title", "Author Name", 1)
    library.register_member(1, "Member Name")
    library.borrow_book(1, 1)
    assert library.return_book(1, 1) is True
    assert library.books[1]['available'] == 1