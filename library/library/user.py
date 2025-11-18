import json
from dataclasses import dataclass, field
from library.book import Book
from library.random_number_utils import RandomUtils
from library.file_io import Fstream

@dataclass

class User: 
	database_path: str
	isEmpty: bool = True
	isActive: bool = False
	id: str = field(init=False, default_factory=RandomUtils.generate_random_id)

	database: dict = field(init=False)
	rented_books: dict = field(init=False, default_factory=dict)

	def __post_init__(self):
		self.database = self._load_database()
		self.rented_books = {} 

	def _load_database(self) -> dict:

	#Load database
		try:
			with open(self.database_path, 'r') as file:
				data = json.load(file)
		except FileNotFoundError:
				data = {"Books": {}}

		if data["Books"]:
			self.isEmpty = False
			self.isActive = True

		return data
		
	def _save_database(self):
		"""
		Write updated database to file.
		"""
		with open(self.database_path, 'w') as file:
		    json.dump(self.database, file, indent=4)	    

	def get_all_books(self, verbose=0) -> dict:
		"""
        Return all books in memory
        """
		if verbose == 1:
			for book_id, info in self.database["Books"].items():
				print(f"{book_id}: {info}")
        		
		return self.database

	def search_books(self, query: str) -> list[Book]:
	        """
	        Search books by name or type
	        """
	        matching = []
	        for book_id, book_data in self.database["Books"].items():
	            book = Book(
	                id=book_id,
	                name=book_data["name"],
	                type=book_data["type"],
	                stock=book_data["stock"]
	            )
	            if query.lower() in book.search_string.lower():
	                matching.append(book)

	        if len(matching) == 0:
	            print("No books found.")
	        else:
	            for b in matching:
	                print(f"Found: {b.name} ({b.id})")

	        return matching

	def get_total_book_count(self)->int:
		"""
		Returns the total number of books registered in the system
		"""
		return len(self.database["Books"])

	def get_total_available_book_count(self)->int:
		"""
		Returns the total number of books available to rent in the system
		"""
		available = [
			book for book in self.database["Books"].values()
			if book["stock"] > 0
		]
		return len(available)

	def rent_book(self, book_id: str):
	    """
	    Rent a book if available
	    """
	    books = self.database["Books"]
	    if book_id not in books:
	        print("Book ID not found.")
	        

	    elif books[book_id]["stock"] <= 0:
	        print("This book is currently out of stock.")

	    elif book_id in self.rented_books:
	    	print("User already has rented this book")

	    else:
		    books[book_id]["stock"] -= 1
		    if book_id not in self.rented_books:
		        self.rented_books[book_id] = 0
		    self.rented_books[book_id] += 1
		    print(f"Book rented successfully: {books[book_id]['name']}")


	def return_book_by_id(self, book_id: str):
		"""
		Return a previously rented book

		"""
		if book_id not in self.rented_books:
			print("This user has not rented that book.")
     
		else:
			self.rented_books[book_id] -= 1

			if self.rented_books[book_id] <= 0:
				del self.rented_books[book_id]

			self.database["Books"][book_id]["stock"] += 1
			print(f"Returned book {book_id}")	    

	def return_book_by_query(self, query: str):
		"""
		Return a previously rented book
		"""
		books_to_return = []

		for book_id, book_data in self.database["Books"].items():
			if query.lower() in book_data["name"].lower() or query.lower() in book_data["type"].lower():
				books_to_return.append(book_id)

		if not books_to_return:
			print(f"No rented books match that query")

		for book_id in books_to_return:
			self.rented_books[book_id] -= 1
			if self.rented_books[book_id] <= 0:
				del self.rented_books[book_id]

			self.database["Books"][book_id]["stock"] += 1
			print(f"Returned book {book_id}")

	def return_all_books(self):
		"""
		Return all books rented
		"""
		for book_id, amount in self.rented_books.items():
			self.database["Books"][book_id]["stock"]+= amount
			print(f"Returned {self.database['Books'][book_id]['name']}")
		self.rented_books ={}
		print("All books returned")