import pytest
from examples.unittest.python_sample.library import format_book_info

# Normal Cases
def test_format_book_info_normal_case_1():
    book = {'title': '1984', 'author': 'George Orwell', 'available': 2, 'copies': 5}
    expected = "1984 by George Orwell (2/5 available)"
    assert format_book_info(book) == expected

def test_format_book_info_normal_case_2():
    book = {'title': 'To Kill a Mockingbird', 'author': 'Harper Lee', 'available': 5, 'copies': 5}
    expected = "To Kill a Mockingbird by Harper Lee (5/5 available)"
    assert format_book_info(book) == expected

# Edge Cases
def test_format_book_info_edge_case_1():
    book = {'title': 'The Catcher in the Rye', 'author': 'J.D. Salinger', 'available': 0, 'copies': 5}
    expected = "The Catcher in the Rye by J.D. Salinger (0/5 available)"
    assert format_book_info(book) == expected

def test_format_book_info_edge_case_2():
    book = {'title': 'Pride and Prejudice', 'author': 'Jane Austen', 'available': 5, 'copies': 5}
    expected = "Pride and Prejudice by Jane Austen (5/5 available)"
    assert format_book_info(book) == expected

# Error Handling
def test_format_book_info_error_case_1():
    book = {'author': 'George Orwell', 'available': 2, 'copies': 5}
    with pytest.raises(KeyError):
        format_book_info(book)

def test_format_book_info_error_case_2():
    book = {'title': '1984', 'available': 2, 'copies': 5}
    with pytest.raises(KeyError):
        format_book_info(book)

def test_format_book_info_error_case_3():
    book = {'title': '1984', 'author': 'George Orwell', 'copies': 5}
    with pytest.raises(KeyError):
        format_book_info(book)

def test_format_book_info_error_case_4():
    book = {'title': '1984', 'author': 'George Orwell', 'available': 2}
    with pytest.raises(KeyError):
        format_book_info(book)

# Boundary Conditions
def test_format_book_info_boundary_case_1():
    book = {'title': '1984', 'author': 'George Orwell', 'available': 0, 'copies': 5}
    expected = "1984 by George Orwell (0/5 available)"
    assert format_book_info(book) == expected

def test_format_book_info_boundary_case_2():
    book = {'title': '1984', 'author': 'George Orwell', 'available': 2, 'copies': 0}
    expected = "1984 by George Orwell (2/0 available)"
    assert format_book_info(book) == expected