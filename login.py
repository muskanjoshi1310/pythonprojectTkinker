import tkinter as tk
from tkinter import messagebox
import mysql.connector

# MySQL Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",       # Your MySQL server address
        user="root",            # Your MySQL username
        password="password",    # Your MySQL password
        database="library_system" # Your MySQL database name
    )

# Function to authenticate user
def authenticate_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if username and password match in the database
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()

    conn.close()

    if user:
        return True
    else:
        return False

# Function to handle the login process
def login():
    username = username_entry.get()
    password = password_entry.get()

    if authenticate_user(username, password):
        messagebox.showinfo("Login Success", "Login Successful!")
        root.destroy()  # Close the login window
        open_library_system()  # Open the main library system after login
    else:
        messagebox.showerror("Login Error", "Invalid username or password!")

# Function to open the library system after successful login
def open_library_system():
    # Create a new window for the library system
    library_window = tk.Tk()
    library_window.title("Library Management System")
    
    label = tk.Label(library_window, text="Welcome to the Library System", font=("Arial", 16))
    label.pack(pady=20)

    list_button = tk.Button(library_window, text="List All Books", command=list_books)
    list_button.pack(pady=5)

    borrow_button = tk.Button(library_window, text="Borrow Book", command=borrow_book)
    borrow_button.pack(pady=5)

    return_button = tk.Button(library_window, text="Return Book", command=return_book)
    return_button.pack(pady=5)

    library_window.mainloop()

# Function to list all books
def list_books():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()

    if books:
        books_info = "\n".join([f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Available: {'Yes' if book[3] else 'No'}" for book in books])
        messagebox.showinfo("Books in Library", books_info)
    else:
        messagebox.showinfo("Books in Library", "No books available.")
    
    conn.close()

# Function to borrow a book
def borrow_book():
    book_id = simpledialog.askinteger("Borrow Book", "Enter Book ID to Borrow:")
    if book_id:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT available FROM books WHERE id = %s", (book_id,))
        book = cursor.fetchone()

        if book and book[0]:
            cursor.execute("UPDATE books SET available = %s WHERE id = %s", (False, book_id))
            cursor.execute("INSERT INTO transactions (book_id) VALUES (%s)", (book_id,))
            conn.commit()
            messagebox.showinfo("Success", f"Book {book_id} borrowed successfully!")
        else:
            messagebox.showerror("Error", "Book is not available.")
        
        conn.close()

# Function to return a book
def return_book():
    book_id = simpledialog.askinteger("Return Book", "Enter Book ID to Return:")
    if book_id:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT available FROM books WHERE id = %s", (book_id,))
        book = cursor.fetchone()

        if book and not book[0]:  # If the book is borrowed
            cursor.execute("UPDATE books SET available = %s WHERE id = %s", (True, book_id))
            cursor.execute("UPDATE transactions SET return_date = CURRENT_TIMESTAMP WHERE book_id = %s AND return_date IS NULL", (book_id,))
            conn.commit()
            messagebox.showinfo("Success", f"Book {book_id} returned successfully!")
        else:
            messagebox.showerror("Error", "This book was not borrowed.")
        
        conn.close()

# Setting up the Login Window
root = tk.Tk()
root.title("Login - Library Management System")

# Username and password fields
tk.Label(root, text="Username:").pack(pady=5)
username_entry = tk.Entry(root)
username_entry.pack(pady=5)

tk.Label(root, text="Password:").pack(pady=5)
password_entry = tk.Entry(root, show="*")
password_entry.pack(pady=5)

# Login button
login_button = tk.Button(root, text="Login", command=login)
login_button.pack(pady=10)

root.mainloop()
