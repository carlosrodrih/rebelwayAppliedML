from library.book import Book

def test_book_name():
    book = Book(name="Dune", type="SciFi", stock=5)
    assert len(book.name) > 0

def test_book_id_length():
    book = Book(name="Dune", type="SciFi", stock=5)
    assert len(book.id) == 6

def test_book_stock():
    book = Book(name="Dune", type="SciFi", stock=5)
    assert book.stock >= 0