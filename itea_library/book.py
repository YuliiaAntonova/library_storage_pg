from itea_library.reader import Reader


class Book:
    """Class which describe book"""
    def __init__(self, book_id: int, name: str, author: str, year: int):
        self.__book_id = book_id
        self.__person = None
        self.name = name
        self.author = author
        self.year = year

    def assign_user(self, person: Reader) -> bool:
        """
        Method assign bok to user
        :param person: Person
        :return: bool
        """
        if not self.__person:
            self.__person = person
            return True
        else:
            return False

    def unassign_user(self, person: Reader) -> bool:
        """
        Method unassign book to user
        :param person: Person
        :return: bool
        """
        if self.__person == person:
            self.__person = None
            return True
        else:
            return False

    def in_use(self) -> bool:
        """
        Method return True if book in use, else False
        :return: bool
        """
        if self.__person:
            return True
        else:
            return False

    def __str__(self):
        return f'"{self.name}, {self.author}, {self.year}"'

    def __repr__(self):
        return f'"{self.name}, {self.author}, {self.year}"'
