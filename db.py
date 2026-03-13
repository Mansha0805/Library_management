"""
Database module for Library Management System.

Handles all database operations including initialization, CRUD for books,
book issuing/returning, and user authentication with hashed passwords.
"""

import sqlite3
import hashlib
import os

DB_NAME = "library.db"


def get_db_path():
    """Return the absolute path to the database file (next to this script)."""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), DB_NAME)


def get_connection():
    """Create and return a new database connection."""
    return sqlite3.connect(get_db_path())


def hash_password(password):
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def initialize_database():
    """
    Create all required tables if they don't exist
    and seed the default admin account.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS login (
            mem_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS book_info (
            ID VARCHAR PRIMARY KEY NOT NULL,
            TITLE TEXT NOT NULL,
            AUTHOR TEXT NOT NULL,
            GENRE TEXT NOT NULL,
            COPIES INTEGER NOT NULL,
            LOCATION VARCHAR NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS book_issued (
            BOOK_ID VARCHAR NOT NULL,
            STUDENT_ID VARCHAR NOT NULL,
            ISSUE_DATE DATE NOT NULL,
            RETURN_DATE DATE NOT NULL,
            PRIMARY KEY (BOOK_ID, STUDENT_ID)
        )
    """)

    # Seed default admin if not present
    cursor.execute("SELECT * FROM login WHERE username = ?", ("admin",))
    if cursor.fetchone() is None:
        cursor.execute(
            "INSERT INTO login (username, password) VALUES (?, ?)",
            ("admin", hash_password("admin")),
        )

    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------

def verify_login(username, password):
    """
    Verify user credentials. Returns True if valid, False otherwise.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM login WHERE username = ? AND password = ?",
        (username, hash_password(password)),
    )
    result = cursor.fetchone()
    conn.close()
    return result is not None


# ---------------------------------------------------------------------------
# Book CRUD
# ---------------------------------------------------------------------------

def add_book(book_id, title, author, genre, copies, location):
    """
    Insert a new book into the database.
    Raises sqlite3.IntegrityError if the book ID already exists.
    """
    conn = get_connection()
    conn.execute(
        "INSERT INTO book_info VALUES (?, ?, ?, ?, ?, ?)",
        (
            book_id.capitalize(),
            title.capitalize(),
            author.capitalize(),
            genre.capitalize(),
            copies,
            location.capitalize(),
        ),
    )
    conn.commit()
    conn.close()


def search_books(query):
    """Search books by ID, title, author, or genre. Returns a list of tuples."""
    conn = get_connection()
    cursor = conn.execute(
        "SELECT * FROM book_info WHERE ID = ? OR TITLE = ? OR AUTHOR = ? OR GENRE = ?",
        (query.capitalize(), query.capitalize(), query.capitalize(), query.capitalize()),
    )
    results = cursor.fetchall()
    conn.close()
    return results


def get_all_books():
    """Return all books as a list of tuples."""
    conn = get_connection()
    cursor = conn.execute("SELECT * FROM book_info")
    results = cursor.fetchall()
    conn.close()
    return results


def delete_book(book_id):
    """
    Delete a book if it is not currently issued.
    Returns (True, message) on success, (False, message) on failure.
    """
    conn = get_connection()
    cursor = conn.execute(
        "SELECT * FROM book_issued WHERE BOOK_ID = ?", (book_id,)
    )
    issued = cursor.fetchall()

    if len(issued) != 0:
        conn.close()
        return False, "Book is currently issued.\nCannot be deleted."

    conn.execute("DELETE FROM book_info WHERE ID = ?", (book_id,))
    conn.commit()
    conn.close()
    return True, "Book deleted successfully."


def update_copies(book_id, delta):
    """
    Adjust the copy count for a book by `delta` (positive to add, negative to remove).
    """
    conn = get_connection()
    conn.execute(
        "UPDATE book_info SET COPIES = COPIES + ? WHERE ID = ?",
        (delta, book_id),
    )
    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# Issue / Return
# ---------------------------------------------------------------------------

def issue_book(book_id, student_id):
    """
    Issue a book to a student.
    Returns (True, message) on success, (False, message) on failure.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT ID, COPIES FROM book_info WHERE ID = ?",
        (book_id.capitalize(),),
    )
    book = cursor.fetchone()

    if book is None:
        conn.close()
        return False, "No such book in the database."

    if book[1] <= 0:
        conn.close()
        return False, "Book unavailable.\nThere are 0 copies of the book."

    try:
        conn.execute(
            "INSERT INTO book_issued VALUES (?, ?, date('now'), date('now', '+7 day'))",
            (book_id.capitalize(), student_id.capitalize()),
        )
        conn.execute(
            "UPDATE book_info SET COPIES = COPIES - 1 WHERE ID = ?",
            (book_id.capitalize(),),
        )
        conn.commit()
        conn.close()
        return True, "Book issued successfully."
    except sqlite3.IntegrityError:
        conn.close()
        return False, "This book is already issued to this student."


def return_book(book_id, student_id):
    """
    Return a book from a student.
    Returns (True, message) on success, (False, message) on failure.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT ID FROM book_info WHERE ID = ?", (book_id.capitalize(),)
    )
    if cursor.fetchone() is None:
        conn.close()
        return False, "No such book.\nPlease add the book to the database first."

    cursor.execute(
        "SELECT * FROM book_issued WHERE BOOK_ID = ? AND STUDENT_ID = ?",
        (book_id.capitalize(), student_id.capitalize()),
    )
    if cursor.fetchone() is None:
        conn.close()
        return False, "No matching issue record found."

    conn.execute(
        "DELETE FROM book_issued WHERE BOOK_ID = ? AND STUDENT_ID = ?",
        (book_id.capitalize(), student_id.capitalize()),
    )
    conn.execute(
        "UPDATE book_info SET COPIES = COPIES + 1 WHERE ID = ?",
        (book_id.capitalize(),),
    )
    conn.commit()
    conn.close()
    return True, "Book returned successfully."


def get_student_activity(query):
    """Search issued-book records by book ID or student ID."""
    conn = get_connection()
    cursor = conn.execute(
        "SELECT * FROM book_issued WHERE BOOK_ID = ? OR STUDENT_ID = ?",
        (query.capitalize(), query.capitalize()),
    )
    results = cursor.fetchall()
    conn.close()
    return results


def get_all_issued():
    """Return all currently issued book records."""
    conn = get_connection()
    cursor = conn.execute("SELECT * FROM book_issued")
    results = cursor.fetchall()
    conn.close()
    return results
