from library.book import Book
from library.user import User

if __name__ == "__main__":

    database = "./database.json"
    user = User(database)


    #search for an item
    print("Searching for books with 'Dune'...")
    results = user.search_books("Dune")
    print("----------------------------")

    #get the total amount of available books
    print(f"Total available books in the library: {user.get_total_book_count()}")
    print("----------------------------")

    print("Current library status:")
    user.get_all_books(verbose=1)

    #borrow some books
    print("Renting books...")
    user.rent_book("IDIMIJ")
    user.rent_book("YRZLDK")
    user.rent_book("LYRZDK")

    print("----------------------------")

    #get all the books borrowed
    print("All rented books by the user:")
    if user.rented_books:
        for book_id in user.rented_books:
            book = user.database["Books"][book_id]
            print(f"- {book['name']}")
    else:
        print("No books rented.")
    print("----------------------------")

    #return a book
    print("Returning books by query 'Fantasy'...")
    user.return_book_by_query("Fantasy")
    print("----------------------------")

    print("Current library status:")
    user.get_all_books(verbose=1)

    #try to borrow the same book
    user.rent_book("IDIMIJ")

    #return all books
    user.return_all_books()
    print("----------------------------")

    print("Current library status:")
    user.get_all_books(verbose=1)

