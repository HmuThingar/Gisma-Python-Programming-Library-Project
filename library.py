import os
from datetime import date, timedelta

from exceptions import (
    BookNotAvailableError,
    BookNotFoundError,
    BorrowLimitError,
    DuplicateRecordError,
    LibraryError,
    MemberNotFoundError,
)
from model import Book, Loan, Member
import storage


class Library:
    BORROW_LIMIT = 4    
    LOAN_PERIOD_DAYS = 7

    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.books = {}
        self.members = {}
        self.loans = []
        self._next_loan_id = 1

#book
    def add_book(self, book):
        if book.isbn in self.books:
            existing = self.books[book.isbn]
            existing.total_copies += book.total_copies
            existing.available_copies += book.total_copies
        else:
            self.books[book.isbn] = book

    def find_book(self, isbn):
        if isbn not in self.books:
            raise BookNotFoundError(f"No book found with ISBN '{isbn}'.")
        return self.books[isbn]

    def search_books(self, keyword):
        keyword = keyword.lower()
        matches = []
        for book in self.books.values():
            if (keyword in book.title.lower()
                    or keyword in book.author.lower()):
                matches.append(book)
        return matches
        
# member
    def register_member(self, member):
        if member.member_id in self.members:
            raise DuplicateRecordError(
                f"Member ID '{member.member_id}' already exists.")
        self.members[member.member_id] = member

    def find_member(self, member_id):
        if member_id not in self.members:
            raise MemberNotFoundError(
                f"No member found with ID '{member_id}'.")
        return self.members[member_id]

#borrow and return
    def borrow_book(self, member_id, isbn):
        """Lending copy of book to member"""
        member = self.find_member(member_id)
        book = self.find_book(isbn)
        if not member.can_borrow(self.BORROW_LIMIT):
            raise BorrowLimitError(
                f"{member.name} already holds the maximum of "
                f"{self.BORROW_LIMIT} books.")
        if not book.is_available():
            raise BookNotAvailableError(
                f"'{book.title}' has no copies available right now.")
        book.borrow_one()
        member.add_loan(isbn)
        today = date.today()
        due = today + timedelta(days=self.LOAN_PERIOD_DAYS)
        loan = Loan(str(self._next_loan_id), isbn, member_id,
                    today.isoformat(), due.isoformat())
        self.loans.append(loan)
        self._next_loan_id += 1
        return loan

    def return_book(self, member_id, isbn):
        member = self.find_member(member_id)
        book = self.find_book(isbn)
        if isbn not in member.borrowed:
            raise LibraryError(
                f"{member.name} has not borrowed '{book.title}'.")
        book.return_one()
        member.remove_loan(isbn)
        for loan in self.loans:
            if (loan.member_id == member_id and loan.isbn == isbn
                    and not loan.returned):
                loan.mark_returned()
                break
    def list_overdue(self):
        return [loan for loan in self.loans if loan.is_overdue()]
    def load_all(self):
        books_path = os.path.join(self.data_dir, "books.csv")
        members_path = os.path.join(self.data_dir, "members.csv")
        loans_path = os.path.join(self.data_dir, "loans.csv")

        for row in storage.read_rows(books_path):
            book = Book.from_row(row)
            self.books[book.isbn] = book
        for row in storage.read_rows(members_path):
            member = Member.from_row(row)
            self.members[member.member_id] = member
        
        highest_id = 0
        for row in storage.read_rows(loans_path):
            loan = Loan.from_row(row)
            self.loans.append(loan)
            highest_id = max(highest_id, int(loan.loan_id))
        self._next_loan_id = highest_id + 1
        
    def save_all(self):
        storage.write_rows(
            os.path.join(self.data_dir, "books.csv"),
            ["isbn", "title", "author", "year",
             "total_copies", "available_copies"],
            [book.to_row() for book in self.books.values()])
        storage.write_rows(
            os.path.join(self.data_dir, "members.csv"),
            ["member_id", "name", "email", "borrowed"],
            [member.to_row() for member in self.members.values()])
        storage.write_rows(
            os.path.join(self.data_dir, "loans.csv"),
            ["loan_id", "isbn", "member_id", "borrow_date",
             "due_date", "returned"],
            [loan.to_row() for loan in self.loans])