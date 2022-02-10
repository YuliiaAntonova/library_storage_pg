from psycopg import connect


class Library:
    """Class which describe library"""

    def __init__(self, conn: connect):
        self.__conn = conn
        self.__cursor = self.__conn.cursor()
        self.__library_tables = ['books', 'readers']
        self.__queries = {
            'books': """create table "books" ("id" SERIAL NOT NULL, "name" TEXT, "author" TEXT, "year" integer, "reader_id" integer , PRIMARY KEY (ID));""",
            'readers': """create table "readers" ("id" SERIAL NOT NULL, "name" TEXT, "surname" TEXT, "age" integer, PRIMARY KEY (ID));"""
        }

        self.__cursor.execute("""select table_name from information_schema.tables where table_schema=\'public\';""")
        exist_tables = [table_name[0] for table_name in self.__cursor.fetchall()]
        for table in self.__library_tables:
            if table not in exist_tables:
                print(f'Creating table {table}...')
                self.__cursor.execute(self.__queries[table])
                self.__conn.commit()
                print(f'Table {table} created successfully!')
            else:
                print(f'Table {table} already exist!')

    def add_books_from_file(self, filename):
        with open(filename) as f:
            for line in f:
                book_list = line.strip().split(',')
                self.__cursor.execute(f'insert into books (name, author, year) '
                                      f'values(\'{book_list[0]}\', \'{book_list[1]}\', \'{int(book_list[2])}\');')
                self.__conn.commit()

    def get_member_list(self) -> list:
        """
        Method return list of all library members
        :return: sorted list
        """
        try:
            self.__cursor.execute('select * from "readers";')
        except Exception as error:
            return [f'Error occurred while getting member list! Error: {error}']
        else:
            members = self.__cursor.fetchall()
            if members:
                return list(members)
            else:
                return ["Library member is empty!"]

    def get_all_books(self, sort: str = 'year') -> list or None:
        """
        Method return sorted(default by year) list of all books in library
        :param sort: use one of sort key 'name, author, year - default'
        :return: sorted list
        """
        try:
            self.__cursor.execute(f'select * from "books" order by {sort};')
        except Exception as error:
            print(f'Error occurred while getting all books list! Error: {error}')
        else:
            books = self.__cursor.fetchall()
            if books:
                return list(books)
            else:
                return ["Library is empty!"]

    def get_available_books(self, sort: str = 'id') -> list or None:
        """
        Method return sorted(default by year) list of available books in library
        :param sort: use one of sort key 'name, author, year - default'
        :return: str
        """
        try:
            self.__cursor.execute(f'select * from "books" where reader_id is null order by {sort};')
        except Exception as error:
            return f'Error occurred while getting available books list! Error: {error}'
        else:
            books = self.__cursor.fetchall()
            if books:
                return list(books)
            else:
                return ["No available books!"]

    def add_book(self, title: str, author: str, year: int) -> bool:
        """
        Method add book to library
        :param author:
        :param book:
        :param year:
        :return: bool
        """
        try:
            self.__cursor.execute(
                f'insert into books (name, author, year) values(\'{title}\', \'{author}\', \'{year}\');')
        except Exception as error:
            print(f'Error occurred while adding books list! Error: {error}')
            self.__conn.rollback()
            return False
        else:
            self.__conn.commit()
            return True

    def del_book(self, book_id: int) -> bool:
        """
        Method delete book from library
        :param book_id: id
        :return: bool
        """
        try:
            self.__cursor.execute(f'select * from books where id = {book_id};')
        except Exception as error:
            print(f'Error occurred while getting book! Error: {error}')
            return False
        else:
            book = self.__cursor.fetchone()
            if book:
                try:
                    self.__cursor.execute(f'delete from books where id = {book_id};')
                except Exception as error:
                    self.__conn.rollback()
                    print(f'Error occurred while deleting book ! Error: {error}')
                    return False
                else:
                    self.__conn.commit()
                    print(f'Book {book[0]}, {book[1]} deleted successfully!')
                    return True
            else:
                print(f'Error occurred while deleting book ! Book with id {book_id} absent!')
                return False

    def give_book(self, book_id: int, reader_id: int) -> bool:
        """
        Method assign book to person
        :param person: Person
        :param book: Book
        :return: str
        """
        try:
            self.__cursor.execute(f'select * from books where id = {book_id} and reader_id is null;')
        except Exception as error:
            print(f'Error occurred while getting book! Error: {error}')
            return False
        else:
            book = self.__cursor.fetchone()
            if book:
                try:
                    self.__cursor.execute(f'update books set reader_id = {reader_id} where id = {book_id};')
                except Exception as error:
                    self.__conn.rollback()
                    print(f'Error occurred while giving book! Error: {error}')
                    return False
                else:
                    self.__conn.commit()
                    print(f'Book {book[0]}, {book[1]} gave successfully!')
                    return True
            else:
                print(f'Book with book id {book_id} is busy or absent!')
                return False

    def return_book(self, book_id: int, reader_id: int) -> bool:
        """
        Method unassign book from person
        :param person: Person
        :param book: Book
        :return: None
        """
        try:
            self.__cursor.execute(f'select * from books where id = {book_id} and reader_id = {reader_id};')
        except Exception as error:
            print(f'Error occurred while getting book! Error: {error}')
            return False
        else:
            book = self.__cursor.fetchone()
            if book:
                try:
                    self.__cursor.execute(f'update books set reader_id = null where id = {book_id};')
                except Exception as error:
                    self.__conn.rollback()
                    print(f'Error occurred while returning book! Error: {error}')
                    return False
                else:
                    self.__conn.commit()
                    print(f'Book {book[0]}, {book[1]} returned successfully!')
                    return True
            else:
                print(f'Book with book id {book_id} is free or absent!')
                return False

    def add_reader(self, name: str, surname: str, age: int) -> bool:
        """
        Method add reader to library
        :param reader:
        :return: None
        """
        try:
            self.__cursor.execute(
                f'insert into readers (name, surname, age) values(\'{name}\', \'{surname}\', \'{age}\');')
        except Exception as error:
            self.__conn.rollback()
            print(f'Error occurred while adding reader! Error: {error}')
            return False
        else:
            self.__conn.commit()
            print(f'Reader {name}, {surname} added successfully!')
            return True

    def del_reader(self, reader_id: int) -> bool:
        """
        Method delete reader from library
        :param reader_id:
        :return: str
        """
        try:
            self.__cursor.execute(f'select * from readers where id = {reader_id};')
        except Exception as error:
            print(f'Error occurred while getting reader! Error: {error}')
            return False
        else:
            reader = self.__cursor.fetchone()
            if reader:
                try:
                    self.__cursor.execute(f'delete from readers where id = {reader_id};')
                except Exception as error:
                    self.__conn.rollback()
                    print(f'Error occurred while deleting reader! Error: {error}')
                    return False
                else:
                    self.__conn.commit()
                    print(f'Reader {reader[1], reader[2]} deleted successfully!')
                    return True
            else:
                print(f'Error occurred while deleting reader! Reader with id {reader_id} absent!')
                return False

    def show_current_reader(self, book_id: int) -> list or str:
        """
        Method return reader if current book busy
        :param book_id:
        :return:
        """
        try:
            self.__cursor.execute(f'select * from books where id = {book_id} and reader_id is not null;')
        except Exception as error:
            print(f'Error occurred while getting book! Error: {error}')
            return None
        else:
            book = self.__cursor.fetchone()
            if book:
                try:
                    self.__cursor.execute(f'select * from readers where id = {book[4]};')
                except Exception as error:
                    print()
                    return f'Error occurred while adding reader! Error: {error}'
                else:
                    reader = self.__cursor.fetchone()
                    if reader:
                        return reader
            else:
                return f'Book with id {book_id} absent or available!'
