# Library Management System

A small, menu-driven Library Management System written in Python. It lets
a librarian manage a book catalogue, register members, and handle the
borrowing and returning of books. All data is stored in plain CSV files so
that the catalogue, members and loan history are kept between runs.

This project was built for the **B100 Introduction to Computer Programming
with Python** module and demonstrates classes, methods, control
structures, file input/output, exception handling and a multi-module
program structure.

## Purpose

Libraries need a simple, reliable way to track which books they own, who
their members are, and which books are currently on loan. This program
provides those core functions through a text menu, without requiring any
external libraries.

## Key Features

- Add books to the catalogue (and add extra copies of existing titles)
- Register library members
- Borrow a book, with automatic due-date calculation (14-day loan period)
- Return a book and close the matching loan
- Search the catalogue by title or author
- List all books and all members
- Show any loans that are overdue
- Enforce a borrowing limit of 3 books per member
- Save all data to CSV files and reload it on the next run

## Files

| File            | Purpose                                                     |
|-----------------|-------------------------------------------------------------|
| `main.py`       | Entry point; shows the menu and handles user input          |
| `library.py`    | `Library` controller class; holds the rules and the data    |
| `models.py`     | `Book`, `Member` and `Loan` data classes                    |
| `storage.py`    | Low-level CSV reading and writing helpers                   |
| `exceptions.py` | Custom exception classes used across the program            |
| `data/`         | Sample CSV data files (`books`, `members`, `loans`)         |

## Installation and Execution

This project uses only the Python standard library, so no installation of
external packages is needed.

1. Make sure Python 3.8 or newer is installed:
   ```
   python3 --version
   ```
2. Clone or download this repository.
3. From the project folder, run:
   ```
   python3 main.py
   ```

## Example Usage

```
===== LIBRARY MENU =====
1. Add a book
2. Register a member
3. Borrow a book
4. Return a book
5. Search books
6. List all books
7. List all members
8. Show overdue loans
9. Our Author
0. Save and exit
Choose an option: 3
Member ID: M001
Book ISBN: 978-0451524935
Success! The book is due back on 2026-07-02.
```

If a member tries to borrow a book with no available copies, the program
responds with a clear message instead of crashing:

```
Cannot borrow: '1984' has no copies available right now.
```

## Data Format

Data is stored in three CSV files inside the `data/` folder:

- `books.csv` — `isbn, title, author, year, total_copies, available_copies`
- `members.csv` — `member_id, name, email, borrowed`
- `loans.csv` — `loan_id, isbn, member_id, borrow_date, due_date, returned`
