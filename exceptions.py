class LibraryError(Exception):
    pass

class BookNotFoundError(LibraryError):
    pass

class MemberNotFoundError(LibraryError):
    pass

class BookNotAvailableError(LibraryError):
    pass

class BorrowLimitError(LibraryError):
    pass

class DuplicateRecordError(LibraryError):
    pass