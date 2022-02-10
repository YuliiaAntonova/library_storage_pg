import psycopg as psql

from itea_library.library import Library
from library_client import LibraryClient

if __name__ == '__main__':
    connection = psql.connect('postgresql://postgres:***@localhost:5432/postgres')
    library = Library(connection)

    LibraryClient(library=library)
