import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
from exceptions import LibraryError
from library import Library
from model import Book, Member
from model import Book, Member, Author
def print_menu():
    print("\n===== LIBRARY MENU =====")
    print("1. Add a book")
    print("2. Register a member")
    print("3. Borrow a book")
    print("4. Return a book")
    print("5. Search books")
    print("6. List all books")
    print("7. List all members")
    print("8. Show overdue loans")
    print("9. Our Authur ")
    print("0. Save and exit")
    
def add_book_flow(library):
    isbn = input("ISBN: ").strip()
    title = input("Title: ").strip()
    author = input("Author: ").strip()
    year = input("Year: ").strip()
    copies = input("Number of copies: ").strip()
    try:
        book = Book(isbn, title, author, year, copies)
        library.add_book(book)
        print(f"Added: {book}")
    except ValueError:
        print("Year and copies must be whole numbers. Book not added.")
        
def register_member_flow(library):
    member_id = input("Member ID: ").strip()
    name = input("Name: ").strip()
    email = input("Email: ").strip()
    try:
        member = Member(member_id, name, email)
        library.register_member(member)
        print(f"Registered: {member}")
    except LibraryError as error:
        print(f"Could not register member: {error}")
        
def borrow_flow(library):
    member_id = input("Member ID: ").strip()
    isbn = input("Book ISBN: ").strip()
    try:
        loan = library.borrow_book(member_id, isbn)
        print(f"Success! The book is due back on {loan.due_date}.")
    except LibraryError as error:
        print(f"Cannot borrow: {error}")
        
def return_flow(library):
    member_id = input("Member ID: ").strip()
    isbn = input("Book ISBN: ").strip()
    try:
        library.return_book(member_id, isbn)
        print("Book returned. Thank you!")
    except LibraryError as error:
        print(f"Cannot return: {error}")
        
def search_flow(library):
    keyword = input("Search keyword: ").strip()
    results = library.search_books(keyword)
    if not results:
        print("No matching books found.")
    else:
        print(f"Found {len(results)} book(s):")
        for book in results:
            print(f"  {book}")
            
def list_books(library):
    if not library.books:
        print("The catalogue is empty.")
        return
    for book in library.books.values():
        print(f"  {book}")
        
def list_members(library):
    if not library.members:
        print("No members registered yet.")
        return
    for member in library.members.values():
        print(f"  {member}")
def show_overdue(library):
    overdue = library.list_overdue()
    if not overdue:
        print("There are no overdue loans.")
    else:
        for loan in overdue:
            print(f"  {loan} - {loan.days_overdue()} day(s) overdue")
def main():
    library = Library()
    library.load_all()
    print("Library data loaded.")
    while True: 
        print_menu()
        choice = input("Choose an option: ").strip()
        if choice == "1":
            add_book_flow(library)
        elif choice == "2":
            register_member_flow(library)
        elif choice == "3":
            borrow_flow(library)
        elif choice == "4":
            return_flow(library)
        elif choice == "5":
            search_flow(library)
        elif choice == "6":
            list_books(library)
        elif choice == "7":
            list_members(library)
        elif choice == "8":
            show_overdue(library)
        elif choice == "9":
            print("\n---Author ---")
            if library.books:
                first_book = list(library.books.values())[0]
                author_info = first_book.author_obj
                author_info.update_biography("A renowned novelist in our library collection.")
                print(author_info)
            else:
                print("No books available in the catalog to inspect author data.")
                print("Please add a book (Option 1) first, then try Option 9 again!")
        elif choice == "0":
            library.save_all()
        elif choice == "0":
            library.save_all()
            print("Data saved. Goodbye!")
            break
        else:
            print("Invalid option. Please choose a number from the menu.")
if __name__ == "__main__":
    main()
