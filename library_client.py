from threading import Thread

from itea_library.library import Library


class LibraryClient(Thread):
    def __init__(self, library: Library = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__library = library
        self.__terminal_options = "1 - Add book\n2 - Add reader\n3 - Del book\n4 - Del reader\n5 - Show members\n" \
                                  "6 - Show all books\n7 - Show available books\n8 - Give book\n9 - Return book\n" \
                                  "10 - Show book reader\n0 - close terminal\nPlease, make your choice: "
        self.start()

    @staticmethod
    def _input_numeric(msg: str):
        while True:
            inp = input(msg)
            if inp.isnumeric():
                return int(inp)
            else:
                print('Wrong input!')
                input('Press Enter to continue...')

    def _user_choice(self):
        while True:
            choice = input("What are you want?\n" + self.__terminal_options)
            if not choice.isnumeric() or int(choice) < 0 or int(choice) > 11:
                print('Wrong input!')
                input('Press Enter to continue...')
            else:
                return int(choice)

    def run(self):
        try:
            while True:
                choice = self._user_choice()
                # 1 - add book to library
                if choice == 1:
                    title = input('Enter the title of the book: ')
                    author = input('Enter the author of the book: ')
                    years = self._input_numeric('Enter the year of publication of the book: ')

                    self.__library.add_book(title, author, years)

                # 2 - add reader
                if choice == 2:
                    name = input('Enter the name of the reader: ')
                    surname = input('Enter the surname of the reader: ')
                    years = self._input_numeric('Enter the year of birth of the reader: ')

                    self.__library.add_reader(name, surname, years)

                # 3 - remove book from library
                if choice == 3:
                    book_id = self._input_numeric('Enter book id: ')

                    self.__library.del_book(book_id)

                # 4 - remove reader from library
                if choice == 4:
                    reader_id = self._input_numeric('Enter reader id: ')

                    self.__library.del_reader(reader_id)

                # 5 - show all readers in the library
                if choice == 5:
                    for reader in self.__library.get_member_list():
                        print(reader)
                    print()

                # 6 - show all books in the library
                if choice == 6:
                    for book in self.__library.get_all_books():
                        print(book)
                    print()

                # 7 - show available books in the library
                if choice == 7:
                    for book in self.__library.get_available_books():
                        print(book)
                    print()

                # 8 - give book
                if choice == 8:
                    book_id = self._input_numeric('Enter book id: ')
                    reader_id = self._input_numeric('Enter reader id: ')

                    self.__library.give_book(book_id, reader_id)

                # 9 - return book
                if choice == 9:
                    book_id = self._input_numeric('Enter book id: ')
                    reader_id = self._input_numeric('Enter reader id: ')

                    self.__library.return_book(book_id, reader_id)

                # 10 - get current book reader
                if choice == 10:
                    book_id = self._input_numeric('Enter book id: ')

                    print(self.__library.show_current_reader(book_id))
                    print()

                # 0 - exit
                if choice == 0:
                    exit(0)
        except ConnectionError:
            print(f'Connection was interrupted unexpectedly!')
