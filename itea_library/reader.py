class Reader:
    """Class which describe library subscriber"""
    def __init__(self, name: str, surname: str, age: int):
        self.name = name
        self.surname = surname
        self.age = age
        self.books = []

    def assign_book(self, book) -> bool:
        """
        Method add book to person use list
        :param book: Book
        :return: bool
        """
        if book not in self.books:
            self.books.append(book)
            return True
        else:
            # print(f'{book} already in use in {self}')
            return False

    def unassign_book(self, book) -> bool:
        """
        Method remove book from person use list
        :param book: Book
        :return: bool
        """
        if book in self.books:
            self.books.pop(self.books.index(book))
            return True
        else:
            # print(f'{self} not use {book}')
            return False

    def books_in_use(self, sort: str = 'year') -> list or None:
        """
        Method return person book's use list
        :param sort: use one of sort key 'name, author, year - default'
        :return: sorted list
        """
        books = sorted([book for book in self.books], key=lambda book: book.__getattribute__(sort))
        if books:
            print(f'{self} has in use next books:')
            for book in books:
                print(book)
            return books
        else:
            print(f'{self} has no books in use!')

    def __str__(self):
        return f'Name: {self.name}, age: {self.age}'

    def __repr__(self):
        return f'{self.name}, {self.age}'
