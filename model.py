from datetime import date, datetime
class Author:
    def __init__(self, name, biography="No biography available.", native_country="Unknown"):
        self.name = name
        self.biography = biography
        self.native_country = native_country
        self.books_written = []
    def add_book_title(self, title):
        if title not in self.books_written:
            self.books_written.append(title)
    def get_book_count(self):
        return len(self.books_written)
    def update_biography(self, new_bio):
        self.biography = new_bio
    def __str__(self):
        return f"Author: {self.name} (From: {self.native_country}) - {self.biography} [{self.get_book_count()} book(s) in catalog]"
class Book:
    def __init__(self, isbn, title, author, year, total_copies, available_copies=None):
        self.isbn = isbn
        self.title = title
        if isinstance(author, str):
            self.author_obj = Author(name=author)
        else:
            self.author_obj = author
        self.author = self.author_obj.name 
        
        self.year = int(year)
        self.total_copies = int(total_copies)
        if available_copies is None:
            self.available_copies = self.total_copies
        else:
            self.available_copies = int(available_copies)
        self.author_obj.add_book_title(self.title)
    def is_available(self):
        return self.available_copies > 0
        
    def borrow_one(self):
        if not self.is_available():
            raise ValueError("No copies available to borrow.")
        self.available_copies -= 1
        
    def return_one(self):
        if self.available_copies < self.total_copies:
            self.available_copies += 1
            
    def to_row(self):
        return [self.isbn, self.title, self.author, str(self.year),
                str(self.total_copies), str(self.available_copies)]
                
    @classmethod
    def from_row(cls, row):
        isbn, title, author, year, total, available = row
        return cls(isbn, title, author, year, total, available)
        
    def __str__(self):
        status = f"{self.available_copies}/{self.total_copies} available"
        return f"'{self.title}' by {self.author} ({self.year}) [{status}] - ISBN: {self.isbn}"
class Member:
    def __init__(self, member_id, name, email, borrowed=None):
        self.member_id = member_id
        self.name = name
        self.email = email
        self.borrowed = list(borrowed) if borrowed else []
        
    def can_borrow(self, limit):
        return len(self.borrowed) < limit
        
    def add_loan(self, isbn):
        self.borrowed.append(isbn)
        
    def remove_loan(self, isbn):
        if isbn in self.borrowed:
            self.borrowed.remove(isbn)
            
    def to_row(self):
        return [self.member_id, self.name, self.email,
                ";".join(self.borrowed)]
                
    @classmethod
    def from_row(cls, row):
        member_id, name, email, borrowed = row
        borrowed_list = borrowed.split(";") if borrowed else []
        return cls(member_id, name, email, borrowed_list)
        
    def __str__(self):
        return (f"[{self.member_id}] {self.name} <{self.email}> "
                f"- {len(self.borrowed)} book(s) on loan")
                
class Loan:
    DATE_FORMAT = "%Y-%m-%d"

    def __init__(self, loan_id, isbn, member_id, borrow_date,
                 due_date, returned=False):
        self.loan_id = loan_id
        self.isbn = isbn
        self.member_id = member_id
        self.borrow_date = borrow_date
        self.due_date = due_date
        if isinstance(returned, str):
            self.returned = returned.lower() == "true"
        else:
            self.returned = bool(returned)
            
    def is_overdue(self, today=None):
        if self.returned:
            return False
        today = today or date.today()
        due = datetime.strptime(self.due_date, self.DATE_FORMAT).date()
        return today > due
        
    def days_overdue(self, today=None):
        if not self.is_overdue(today):
            return 0
        today = today or date.today()
        due = datetime.strptime(self.due_date, self.DATE_FORMAT).date()
        return (today - due).days
        
    def mark_returned(self):
        self.returned = True
        
    def to_row(self):
        return [self.loan_id, self.isbn, self.member_id,
                self.borrow_date, self.due_date, str(self.returned)]
                
    @classmethod
    def from_row(cls, row):
        loan_id, isbn, member_id, borrow_date, due_date, returned = row
        return cls(loan_id, isbn, member_id, borrow_date,
                   due_date, returned)
                   
    def __str__(self):
        state = "Returned" if self.returned else "On loan"
        return (f"Loan {self.loan_id}: book {self.isbn} -> member "
                f"{self.member_id} (due {self.due_date}) [{state}]")
class Category:
    def __init__(self, name, description, age_restriction=0):
        self.name = name
        self.description = description
        self.age_restriction = int(age_restriction)
        self.books_assigned = []

    # Method 1: Assign a book object to this category
    def assign_book(self, book_isbn):
        if book_isbn not in self.books_assigned:
            self.books_assigned.append(book_isbn)
            return True
        return False

    # Method 2: Check if a user meets the age requirements for this genre
    def is_allowed_for_age(self, user_age):
        return int(user_age) >= self.age_restriction

    # Method 3: Get the total count of books classified here
    def get_total_books(self):
        return len(self.books_assigned)

    # Method 4: String representation for easy display in menus
    def __str__(self):
        restriction = f"({self.age_restriction}+)" if self.age_restriction > 0 else "(General)"
        return f"Category: {self.name} {restriction} - {self.description} [{self.get_total_books()} book(s)]"