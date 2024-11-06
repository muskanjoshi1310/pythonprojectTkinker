def add_book(title, author):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    
    # Insert a new book into the books table
    cursor.execute('''
    INSERT INTO books (title, author, available)
    VALUES (?, ?, ?)''', (title, author, True))
    
    conn.commit()
    conn.close()
    print(f"Book '{title}' by {author} added to the library.")
def list_books():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    
    # Retrieve all books from the books table
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()
    
    if books:
        for book in books:
            print(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Available: {book[3]}")
    else:
        print("No books available.")
    
    conn.close()
def borrow_book(book_id):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    
    # Check if the book is available
    cursor.execute('SELECT available FROM books WHERE id = ?', (book_id,))
    book = cursor.fetchone()
    
    if book and book[0]:  # If book is available
        # Update the book's availability to False (borrowed)
        cursor.execute('UPDATE books SET available = ? WHERE id = ?', (False, book_id))
        
        # Log the transaction
        cursor.execute('INSERT INTO transactions (book_id) VALUES (?)', (book_id,))
        
        conn.commit()
        print(f"Book with ID {book_id} has been borrowed.")
    else:
        print(f"Sorry, the book with ID {book_id} is not available.")
    
    conn.close()
