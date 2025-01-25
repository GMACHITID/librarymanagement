import libsystem
import json

def display_menu():
    print("\nLibrary Management System")
    print("1. Librarian Menu")
    print("2. Patron Menu")
    print("3. Exit")


def display_librarian_menu():
    print("\nLibrarian Menu")
    print("1. Add Book")
    print("2. Remove Book")
    print("3. List All Books")
    print("4. Save Library Data")
    print("5. Back to Main Menu")


def display_patron_menu():
    print("\nPatron Menu")
    print("1. Register as a Patron")
    print("2. Check Out a Book")
    print("3. Check in Book")
    print("4. List Checked-Out Books")
    print("5. Search for a Book")
    print("6. Back to Main Menu")


def main():
    library = libsystem.Library.load_from_file()
    patrons = []

    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            while True:
                display_librarian_menu()
                librarian_choice = input("Enter your choice: ")

                if librarian_choice == "1":  # Add Book
                    book_type = input("Enter book type (PhysicalBook/EBook/AudioBook): ")
                    title = input("Enter book title: ")
                    author = input("Enter author name: ")
                    isbn = input("Enter ISBN: ")

                    if book_type == "PhysicalBook":
                        num_pages = int(input("Enter number of pages: "))
                        book = libsystem.PhysicalBook(title, author, isbn, num_pages)
                    elif book_type == "EBook":
                        file_size_mb = float(input("Enter file size (MB): "))
                        book = libsystem.Ebook(title, author, isbn, file_size_mb)
                    elif book_type == "AudioBook":
                        duration_minutes = int(input("Enter duration (minutes): "))
                        book = libsystem.AudioBook(title, author, isbn, duration_minutes)
                    else:
                        print("Invalid book type!")
                        continue

                    library.add_book(book)
                    print(f"Book '{title}' added to the library.")

                elif librarian_choice == "2":  # Remove Book
                    isbn = input("Enter the ISBN of the book to remove: ")
                    try:
                        library.remove_book(isbn)
                        print("Book removed successfully.")
                    except Exception as e:
                        print(e)

                elif librarian_choice == "3":  # List All Books
                    books = library.list_books()
                    print("\nBooks in Library:")
                    print("\n".join(books) if books else "No books available.")

                elif librarian_choice == "4":  # Save Library Data
                    library.save_to_file()

                elif librarian_choice == "5":
                    break

                else:
                    print("Invalid choice! Please try again.")

        elif choice == "2":
            current_patron = None
            while True:
                display_patron_menu()
                patron_choice = input("Enter your choice: ")

                if patron_choice == "1":
                    name = input("Enter your name: ")
                    patron_id = input("Enter your Patron ID: ")
                    current_patron = libsystem.Patron(name, patron_id)
                    patrons.append(current_patron)
                    print(f"Patron '{name}' registered successfully.")

                elif patron_choice == "2":
                    if not current_patron:
                        print("Please register as a patron first!")
                        continue

                    isbn = input("Enter the ISBN: ")
                    found_book = library.search_books(title=None)
                    found_book = next((book for book in library._books if book.isbn == isbn), None)

                    if not found_book:
                        print("No book found with the provided ISBN.")
                        continue

                    try:
                        current_patron.check_out_book(found_book)
                        print(f"Book '{found_book.title}' checked out successfully.")
                    except Exception as e:
                        print(e)

                elif patron_choice == "3":
                    if not current_patron:
                        print("Please register as a patron first!")
                        continue

                    isbn = input("Enter the ISBN of the book to return: ")
                    found_book = next((book for book in current_patron._checked_out_books if book.isbn == isbn), None)

                    if not found_book:
                        print("You have not checked out this book.")
                        continue

                    try:
                        current_patron.check_in_book(found_book)
                        print(f"Book '{found_book.title}' returned successfully.")
                    except Exception as e:
                        print(e)

                elif patron_choice == "4":
                    if not current_patron:
                        print("Please register as a patron first!")
                        continue

                    books = current_patron.list_checked_out_books()
                    print("\nChecked-Out Books:")
                    print("\n".join(books) if books else "No books checked out.")

                elif patron_choice == "5":
                    title = input("Enter the title of the book to search: ")
                    results = library.search_books(title=title)
                    print("\nSearch Results:")
                    print("\n".join([book.display_info() for book in results]) if results else "No books found.")

                elif patron_choice == "6":
                    break

                else:
                    print("Invalid choice! Please try again.")

        elif choice == "3":
            print("Exiting the Library Management System. Goodbye!")
            break

        else:
            print("Invalid choice! Please try again.")


if __name__ == "__main__":
    main()
