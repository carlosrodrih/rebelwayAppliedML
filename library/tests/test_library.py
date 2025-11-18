import pytest
from library.book import Book
from library.user import User

@pytest.fixture
def user():
    database =  "./tests/test_database.json"
    u = User(database)
    u._load_database()
    return u

#----------------------
# TESTS
#----------------------

def test_load_database(user):
	assert len(user.database["Books"]) > 0

def test_search_books(user):
    results = user.search_books("Dune")
    assert len(results) == 1

def test_search_books_no_results(user):
    results = user.search_books("MachineLearning")
    assert results == []

def test_get_total_book_count(user):
    count = user.get_total_book_count()
    assert count == 3

def test_get_total_available_book_count(user):
    # books where stock > 0
    count = user.get_total_available_book_count()
    assert count == 2

def test_borrow_book_success(user):
    book_id = "IDIMIJ"  # Dune
    user.rent_book(book_id)
    assert user.database["Books"][book_id]["stock"] == 2
    assert book_id in user.rented_books

def return_book_by_id(user):
    book_id = "IDIMIJ"  # Dune
    user.rent_book(book_id)
    assert user.database["Books"][book_id]["stock"] == 2
    user.return_book(book_id)
    assert user.database["Books"][book_id]["stock"] == 3
    assert book_id not in user.rented_books
   