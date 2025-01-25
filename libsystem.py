from abc import ABC, abstractmethod
import json

class Book(ABC):
    def __init__(self, title, author, isbn):
        self._title = title
        self._author = author
        self._isbn = isbn
        self._is_checked_out = False


    @abstractmethod
    def get_format(self):
        pass


    @property  #title getter
    def title(self):
        return self._title

    @property #author getter
    def author(self):
        return self._author

    @property #isbn getter
    def isbn(self):
        return self._isbn

    def check_out(self):
        if self._is_checked_out:
            raise Exception("The mentioned book is already checked out.")
        self._is_checked_out = True

    def return_book(self):
        if not self._is_checked_out:
            raise Exception("The book is not currently checked out.")
        self._is_checked_out = False

    def is_available(self):
        return not self._is_checked_out

    def to_dict(self):
        return {
            "title": self._title,
            "author": self._author,
            "isbn": self._isbn,
            "is_checked_out": self._is_checked_out,
            "type": self.__class__.__name__,
        }

class PhysicalBook(Book):
    def __init__(self, title, author, isbn, cover_type):
        super().__init__(title,author,isbn)
        self._cover_type = cover_type

    def get_format(self):
        return f"[Physical book] Title: {self._title}, Author: {self._author}, isbn = {self._isbn}, Number of pages: {self._cover_type}"
    def to_dict(self):
        data = super().to_dict()
        data["num_pages"] = self._cover_type
        return data

class Ebook(Book):
    def __init__(self, title, author, isbn, file_format):
        super().__init__(title, author, isbn)
        self._file_format  = file_format

    def get_format(self):
        return f"[Ebook] Title: {self._title}, Author: {self._author}, isbn = {self._isbn}, File size in MB: {self._file_format}"
    def to_dict(self):
        data = super().to_dict()
        data["file_format"] = self._file_format
        return data
class AudioBook(Book):
    def __init__(self, title, author, isbn, audio_format):
        super().__init__(title,author,isbn)
        self._audio_format = audio_format

    def get_format(self):
        return f"[Audio Book] Title: {self._title}, Author: {self._author}, isbn = {self._isbn}, Duration in Minutes: {self._audio_format}"
    def to_dict(self):
        data = super().to_dict()
        data["audio_format"] = self._audio_format
        return data

class Library:
    def __init__(self):
        self._books = []

    def add_book(self,book):
        self._books.append(book)

    def search_book(self, title=None, author = None):
        result = []
        for book in self._books:
            book_title = book.title if book.title else ""
            book_author = book.author if book.author else ""

            if (title and title.lower() in book_title.lower()) or (author and author.lower() in book_author.lower()):
                result.append(book)
        return result

    def remove_book(self, isbn):
        for book in self._books:
            if book.isbn == isbn:
                self._books.remove(book)
                return True
        raise Exception(f"No book found with this ISBN: {isbn}")

    def list_books(self):
        return [book.get_format() for book in self._books]

    def to_dict(self):
        return {"books": [book.to_dict() for book in self._books]}

    def save_to_file(self, filename="library_data.json"):
        with open(filename, "w") as f:
            json.dump(self.to_dict(), f, indent=4)
        print(f"Library data saved to {filename}")

    @classmethod
    def load_from_file(cls, filename="library.json"):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                library = cls()
                for book_data in data.get("books", []):
                    book_type = book_data.pop("type")
                    if book_type == "PhysicalBook":
                        book = PhysicalBook(**book_data)
                    elif book_type == "EBook":
                        book = Ebook(**book_data)
                    elif book_type == "AudioBook":
                        book = AudioBook(**book_data)
                    else:
                        continue
                    library.add_book(book)
                return library
        except (FileNotFoundError, json.JSONDecodeError):  # Handle missing or invalid file
            print("No valid library data found. Initializing an empty library.")
            return cls()
class Patron:
    def __init__(self, name, patron_id):
        self._name = name
        self._patron_id = patron_id
        self._checked_out_books = []

    def check_out_book(self,book):
        if not book.is_available():
            raise Exception(f"Book {book.title} is not available.")
        book.check_out()
        self._checked_out_books.append(book)


    def check_in_book(self,book):
        if book not in self._checked_out_books:
            raise Exception(f"Book {book.title} is not checked out by {self._name}")
        book.return_book()
        self._checked_out_books.remove(book)

    def list_checked_out_books(self):
        return [book.get_format() for book in self._checked_out_books]

    def to_dict(self):
        return {
            "name": self._name,
            "patron_id": self._patron_id,
            "checked_out_books": [book.to_dict() for book in self._checked_out_books],
        }

    @staticmethod
    def from_dict(data):
        patron = Patron(data["name"], data["patron_id"])
        return patron

