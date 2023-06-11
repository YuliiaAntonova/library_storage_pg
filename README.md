# library_storage_pg
Implement a Library that stores all data in a database (using only SQL).

1. Books (id(serial), title, author, years, reader_id)
2. Readers (id(serial), name, surname, age)

1. The program creates the database if it doesn't exist (data can be loaded from a file) (CREATE TABLE IF NOT EXISTS).

2. The Library supports the following commands:
- Add/Delete a book/reader,
- Display the list of books/readers
- Display the list of available books
- Borrow a book
- Return a book
- Show the name/surname of the user who has the book with the specified id
3. All changes in the Library are recorded in the database
4. The reader_id field of the Book class is either set to None or to the id of the reader who borrowed the book.
