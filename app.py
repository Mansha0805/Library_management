"""
Library Management System — Main Application UI.

A Tkinter-based GUI for managing books, issuing/returning books,
and tracking student activity. Uses a modular database backend (db.py).
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

import db

# ---------------------------------------------------------------------------
# Asset paths (relative to this script's directory)
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS = {
    "library": os.path.join(BASE_DIR, "assets", "library.png"),
    "dashboard": os.path.join(BASE_DIR, "assets", "image2.png"),
    "login": os.path.join(BASE_DIR, "assets", "finance.png"),
}

# ---------------------------------------------------------------------------
# Fonts & colours used throughout the app
# ---------------------------------------------------------------------------
FONT_TITLE = ("Papyrus", 30, "bold")
FONT_HEADING = ("Papyrus", 22, "bold")
FONT_LABEL = ("Papyrus", 15, "bold")
FONT_FIELD = ("Papyrus", 12, "bold")
FONT_BUTTON = ("Papyrus", 10, "bold")

FG_PRIMARY = "orange"
FG_ACCENT = "yellow"
BG_DARK = "black"


class LibraryApp:
    """Top-level application controller handling login → main menu → views."""

    def __init__(self):
        db.initialize_database()
        self._build_login_window()

    # ------------------------------------------------------------------
    # Login screen
    # ------------------------------------------------------------------

    def _build_login_window(self):
        """Create the login window."""
        self.root = tk.Tk()
        self.root.title("Library Management System — Login")
        self._maximize_window(self.root)

        w = self.root.winfo_screenwidth()
        h = self.root.winfo_screenheight()
        self.canvas = self._create_canvas(self.root, ASSETS["login"], w, h)

        # Variables
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        # Title
        tk.Label(
            self.canvas, text="ADMIN   LOGIN", font=FONT_TITLE,
            bg=BG_DARK, fg=FG_PRIMARY,
        ).place(x=500, y=100)

        # Username
        tk.Label(
            self.canvas, text="Username:", font=FONT_LABEL,
            bd=4, bg=BG_DARK, fg=FG_PRIMARY,
        ).place(x=500, y=230)
        tk.Entry(
            self.canvas, textvariable=self.username_var, font=(None, 14),
            bg=BG_DARK, fg=FG_PRIMARY, bd=6,
        ).place(x=650, y=230)

        # Password
        tk.Label(
            self.canvas, text="Password:", font=FONT_LABEL,
            bd=3, bg=BG_DARK, fg=FG_PRIMARY,
        ).place(x=500, y=330)
        tk.Entry(
            self.canvas, textvariable=self.password_var, show="*",
            font=(None, 14), bg=BG_DARK, fg=FG_PRIMARY, bd=6,
        ).place(x=650, y=330)

        # Status label
        self.lbl_status = tk.Label(self.canvas)
        self.lbl_status.place(x=450, y=500)

        # Login button
        btn = tk.Button(
            self.canvas, text="LOGIN", font=FONT_LABEL, width=25,
            command=self._handle_login, bg=BG_DARK, fg=FG_PRIMARY,
        )
        btn.place(x=500, y=400)
        btn.bind("<Return>", lambda e: self._handle_login())

    def _handle_login(self):
        """Validate credentials and switch to the main menu on success."""
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()

        if not username or not password:
            messagebox.showinfo("Error", "Please complete all required fields!")
            return

        if db.verify_login(username, password):
            self.root.destroy()
            self._build_main_menu()
        else:
            messagebox.showinfo("Error", "Invalid username or password.")
            self.username_var.set("")
            self.password_var.set("")

    # ------------------------------------------------------------------
    # Main menu
    # ------------------------------------------------------------------

    def _build_main_menu(self):
        """Create the main menu window with Book Data / Student Data."""
        self.root = tk.Tk()
        self.root.title("Library Management System")
        self._maximize_window(self.root)

        self.canvas = self._create_canvas(
            self.root, ASSETS["library"],
            self.root.winfo_screenwidth(), self.root.winfo_screenheight(),
        )

        tk.Button(
            self.canvas, text="BOOK DATA", font=FONT_HEADING,
            fg=FG_ACCENT, bg=BG_DARK, width=19, padx=10, borderwidth=0,
            command=self._show_book_menu,
        ).place(x=100, y=500)

        tk.Button(
            self.canvas, text="STUDENT DATA", font=FONT_HEADING,
            fg=FG_ACCENT, bg=BG_DARK, width=19, padx=10, borderwidth=0,
            command=self._show_student_menu,
        ).place(x=800, y=500)

        self.root.mainloop()

    # ------------------------------------------------------------------
    # Book menu
    # ------------------------------------------------------------------

    def _show_book_menu(self):
        """Display the book management sub-menu."""
        self.canvas.destroy()
        self.canvas = self._create_canvas(
            self.root, ASSETS["dashboard"],
            self.root.winfo_screenwidth(), self.root.winfo_screenheight(),
        )

        buttons = [
            ("Add Books", 100, self._show_add_book),
            ("Search Books", 200, self._show_search_book),
            ("All Books", 300, self._show_all_books),
            ("<< Main Menu", 500, self._return_to_main_menu),
        ]
        for text, y, cmd in buttons:
            tk.Button(
                self.canvas, text=text, font=FONT_HEADING,
                fg=FG_PRIMARY, bg=BG_DARK, width=15, padx=10, command=cmd,
            ).place(x=12, y=y)

    # ------------------------------------------------------------------
    # Add book
    # ------------------------------------------------------------------

    def _show_add_book(self):
        """Display the add-book form."""
        self.book_id_var = tk.StringVar()
        self.book_title_var = tk.StringVar()
        self.book_author_var = tk.StringVar()
        self.book_genre_var = tk.StringVar()
        self.book_copies_var = tk.IntVar()
        self.book_location_var = tk.StringVar()

        self.form_frame = tk.Frame(self.canvas, height=500, width=650, bg=BG_DARK)
        self.form_frame.place(x=500, y=100)

        fields = [
            ("Book ID :", self.book_id_var, 50),
            ("Title :", self.book_title_var, 100),
            ("Author :", self.book_author_var, 150),
            ("Genre :", self.book_genre_var, 200),
            ("Copies :", self.book_copies_var, 250),
            ("Location :", self.book_location_var, 300),
        ]
        for label, var, y in fields:
            tk.Label(
                self.form_frame, text=label, font=FONT_FIELD,
                fg=FG_PRIMARY, bg=BG_DARK, pady=1,
            ).place(x=50, y=y)
            tk.Entry(
                self.form_frame, width=45, bg=FG_PRIMARY, fg=BG_DARK,
                textvariable=var,
            ).place(x=150, y=y)

        self.form_frame.grid_propagate(False)

        tk.Button(
            self.form_frame, text="Add", font=FONT_BUTTON,
            fg=BG_DARK, bg=FG_PRIMARY, width=15, bd=3,
            command=self._add_book_data,
        ).place(x=150, y=400)

        tk.Button(
            self.form_frame, text="Back", font=FONT_BUTTON,
            fg=BG_DARK, bg=FG_PRIMARY, width=15, bd=3,
            command=self._close_form,
        ).place(x=350, y=400)

    def _add_book_data(self):
        """Validate and insert a new book record."""
        book_id = self.book_id_var.get().strip()
        title = self.book_title_var.get().strip()
        author = self.book_author_var.get().strip()
        genre = self.book_genre_var.get().strip()
        copies = self.book_copies_var.get()
        location = self.book_location_var.get().strip()

        if not all([book_id, title, author, genre, location]):
            messagebox.showinfo("Error", "All fields are required.")
            return

        try:
            db.add_book(book_id, title, author, genre, copies, location)
            messagebox.showinfo("Success", "Book added successfully.")
        except Exception as e:
            messagebox.showinfo("Error", f"Book already exists.\n{e}")

    # ------------------------------------------------------------------
    # Search book
    # ------------------------------------------------------------------

    def _show_search_book(self):
        """Display the search-book form."""
        self.search_var = tk.StringVar()
        self.form_frame = tk.Frame(self.canvas, height=500, width=650, bg=BG_DARK)
        self.form_frame.place(x=500, y=100)

        tk.Label(
            self.form_frame, text="Book ID / Title / Author / Genre:",
            font=FONT_FIELD, bd=2, fg=FG_PRIMARY, bg=BG_DARK,
        ).place(x=20, y=40)

        tk.Entry(
            self.form_frame, width=25, bd=5, bg=FG_PRIMARY, fg=BG_DARK,
            textvariable=self.search_var,
        ).place(x=260, y=40)

        tk.Button(
            self.form_frame, text="Search", bg=FG_PRIMARY, font=FONT_BUTTON,
            width=9, bd=2, command=self._execute_search,
        ).place(x=500, y=37)

        tk.Button(
            self.form_frame, text="Back", bg=FG_PRIMARY, font=FONT_BUTTON,
            width=10, bd=2, command=self._close_form,
        ).place(x=250, y=450)

    def _execute_search(self):
        """Run the search query and display results."""
        query = self.search_var.get().strip()
        if not query:
            messagebox.showinfo("Error", "Search field cannot be empty.")
            return

        columns = ("BOOK ID", "TITLE", "AUTHOR", "GENRE", "COPIES", "LOCATION")
        self.tree = self._create_treeview(self.form_frame, columns)
        self.tree.place(x=25, y=150)

        results = db.search_books(query)
        if not results:
            messagebox.showinfo("Error", "No matching books found.")
            return

        for row in results:
            self.tree.insert("", tk.END, values=row)

        # Action combobox
        self.action_var = tk.StringVar(value="Select Action:")
        self.combo = ttk.Combobox(
            self.form_frame, textvariable=self.action_var,
            state="readonly", font=FONT_LABEL, height=50, width=15,
            values=("Add Copies", "Delete Copies", "Delete Book"),
        )
        self.combo.place(x=50, y=100)
        self.combo.bind("<<ComboboxSelected>>", self._handle_book_action)

    def _handle_book_action(self, _event):
        """Dispatch the selected book action."""
        idx = self.combo.current()
        if idx in (0, 1):
            self._show_copies_entry(idx)
        elif idx == 2:
            self._confirm_delete_book()

    def _show_copies_entry(self, action_idx):
        """Show an entry field for adding/removing copies."""
        try:
            cur_item = self.tree.focus()
            self.selected_book_id = self.tree.item(cur_item, "values")[0]
            self.selected_copies = int(self.tree.item(cur_item, "values")[4])
        except (IndexError, ValueError):
            messagebox.showinfo("Empty", "Please select a book first.")
            return

        self.copies_entry_var = tk.IntVar()
        self.copies_entry = tk.Entry(
            self.form_frame, width=20, textvariable=self.copies_entry_var,
        )
        self.copies_entry.place(x=310, y=100)

        cmd = self._add_copies if action_idx == 0 else self._delete_copies
        tk.Button(
            self.form_frame, text="Update", font=FONT_BUTTON,
            bg=FG_PRIMARY, fg=BG_DARK, width=9, bd=3, command=cmd,
        ).place(x=500, y=97)

    def _add_copies(self):
        """Add copies to the selected book."""
        count = self.copies_entry_var.get()
        if count < 0:
            messagebox.showinfo("Error", "Number of copies cannot be negative.")
            return
        db.update_copies(self.selected_book_id, count)
        messagebox.showinfo("Updated", "Copies added successfully.")
        self._execute_search()

    def _delete_copies(self):
        """Remove copies from the selected book."""
        count = self.copies_entry_var.get()
        if count < 0:
            messagebox.showinfo("Error", "Number of copies cannot be negative.")
            return
        if count > self.selected_copies:
            messagebox.showinfo(
                "Error", "Number of copies to delete exceeds available copies."
            )
            return
        db.update_copies(self.selected_book_id, -count)
        messagebox.showinfo("Updated", "Copies deleted successfully.")
        self._execute_search()

    def _confirm_delete_book(self):
        """Delete the selected book after confirmation."""
        try:
            cur_item = self.tree.focus()
            book_id = self.tree.item(cur_item, "values")[0]
        except (IndexError, ValueError):
            messagebox.showinfo("Empty", "Please select a book first.")
            return

        success, msg = db.delete_book(book_id)
        if success:
            self.tree.delete(cur_item)
        messagebox.showinfo("Result", msg)

    # ------------------------------------------------------------------
    # All books
    # ------------------------------------------------------------------

    def _show_all_books(self):
        """Display every book in the database."""
        self.form_frame = tk.Frame(self.canvas, height=500, width=650, bg=BG_DARK)
        self.form_frame.place(x=500, y=100)

        tk.Button(
            self.form_frame, text="Back", bg=FG_PRIMARY, fg=BG_DARK,
            width=10, bd=3, command=self._close_form,
        ).place(x=250, y=400)

        columns = ("BOOK ID", "TITLE", "AUTHOR", "GENRE", "COPIES", "LOCATION")
        tree = self._create_treeview(self.form_frame, columns)
        tree.place(x=25, y=50)

        for row in db.get_all_books():
            tree.insert("", tk.END, values=row)

    # ------------------------------------------------------------------
    # Student menu
    # ------------------------------------------------------------------

    def _show_student_menu(self):
        """Display the student management sub-menu."""
        self.canvas.destroy()
        self.canvas = self._create_canvas(
            self.root, ASSETS["dashboard"],
            self.root.winfo_screenwidth(), self.root.winfo_screenheight(),
        )

        buttons = [
            ("Issue Book", 100, self._show_issue_book),
            ("Return Book", 200, self._show_return_book),
            ("Student Activity", 300, self._show_activity),
            ("<< Main Menu", 600, self._return_to_main_menu),
        ]
        for text, y, cmd in buttons:
            tk.Button(
                self.canvas, text=text, font=FONT_HEADING,
                fg=FG_PRIMARY, bg=BG_DARK, width=15, padx=10, command=cmd,
            ).place(x=12, y=y)

    # ------------------------------------------------------------------
    # Issue book
    # ------------------------------------------------------------------

    def _show_issue_book(self):
        """Display the issue-book form."""
        self.issue_book_id_var = tk.StringVar()
        self.issue_student_id_var = tk.StringVar()

        self.form_frame = tk.Frame(self.canvas, height=550, width=500, bg=BG_DARK)
        self.form_frame.place(x=500, y=100)

        tk.Label(
            self.form_frame, text="Book ID :", font=FONT_LABEL,
            bg=BG_DARK, fg=FG_PRIMARY,
        ).place(x=50, y=100)
        tk.Entry(
            self.form_frame, width=25, bd=4, bg=FG_PRIMARY,
            textvariable=self.issue_book_id_var,
        ).place(x=180, y=100)

        tk.Label(
            self.form_frame, text="Student ID :", font=FONT_LABEL,
            bg=BG_DARK, fg=FG_PRIMARY,
        ).place(x=50, y=150)
        tk.Entry(
            self.form_frame, width=25, bd=4, bg=FG_PRIMARY,
            textvariable=self.issue_student_id_var,
        ).place(x=180, y=150)

        tk.Button(
            self.form_frame, text="Back", font=FONT_BUTTON,
            fg=BG_DARK, bg=FG_PRIMARY, width=10, bd=3,
            command=self._close_form,
        ).place(x=50, y=250)

        tk.Button(
            self.form_frame, text="Issue", font=FONT_BUTTON,
            fg=BG_DARK, bg=FG_PRIMARY, width=10, bd=3,
            command=self._issue_book_action,
        ).place(x=200, y=250)

    def _issue_book_action(self):
        """Validate and issue a book."""
        book_id = self.issue_book_id_var.get().strip()
        student_id = self.issue_student_id_var.get().strip()

        if not book_id or not student_id:
            messagebox.showinfo("Error", "All fields are required.")
            return

        success, msg = db.issue_book(book_id, student_id)
        title = "Success" if success else "Error"
        messagebox.showinfo(title, msg)

    # ------------------------------------------------------------------
    # Return book
    # ------------------------------------------------------------------

    def _show_return_book(self):
        """Display the return-book form."""
        self.return_book_id_var = tk.StringVar()
        self.return_student_id_var = tk.StringVar()

        self.form_frame = tk.Frame(self.canvas, height=550, width=500, bg=BG_DARK)
        self.form_frame.place(x=500, y=100)
        self.form_frame.grid_propagate(False)

        tk.Label(
            self.form_frame, text="Book ID :", font=FONT_LABEL,
            fg=FG_PRIMARY, bg=BG_DARK,
        ).place(x=50, y=100)
        tk.Entry(
            self.form_frame, width=25, bd=4, bg=FG_PRIMARY,
            textvariable=self.return_book_id_var,
        ).place(x=180, y=100)

        tk.Label(
            self.form_frame, text="Student ID :", font=FONT_LABEL,
            fg=FG_PRIMARY, bg=BG_DARK,
        ).place(x=50, y=150)
        tk.Entry(
            self.form_frame, width=25, bd=4, bg=FG_PRIMARY,
            textvariable=self.return_student_id_var,
        ).place(x=180, y=150)

        tk.Button(
            self.form_frame, text="Back", font=FONT_BUTTON,
            bg=FG_PRIMARY, fg=BG_DARK, width=10, bd=3,
            command=self._close_form,
        ).place(x=50, y=250)

        tk.Button(
            self.form_frame, text="Return", font=FONT_BUTTON,
            bg=FG_PRIMARY, fg=BG_DARK, width=10, bd=3,
            command=self._return_book_action,
        ).place(x=200, y=250)

    def _return_book_action(self):
        """Validate and return a book."""
        book_id = self.return_book_id_var.get().strip()
        student_id = self.return_student_id_var.get().strip()

        if not book_id or not student_id:
            messagebox.showinfo("Error", "All fields are required.")
            return

        success, msg = db.return_book(book_id, student_id)
        title = "Success" if success else "Error"
        messagebox.showinfo(title, msg)

    # ------------------------------------------------------------------
    # Student activity
    # ------------------------------------------------------------------

    def _show_activity(self):
        """Display the student activity search form."""
        self.activity_var = tk.StringVar()

        self.form_frame = tk.Frame(self.canvas, height=550, width=500, bg=BG_DARK)
        self.form_frame.place(x=500, y=80)
        self.form_frame.grid_propagate(False)

        columns = ("BOOK ID", "STUDENT ID", "ISSUE DATE", "RETURN DATE")
        self.activity_tree = self._create_treeview(self.form_frame, columns)
        self.activity_tree.place(x=50, y=150)

        tk.Label(
            self.form_frame, text="Book / Student ID :", font=FONT_LABEL,
            fg=FG_PRIMARY, bg=BG_DARK,
        ).place(x=50, y=30)

        tk.Entry(
            self.form_frame, width=20, bd=4, bg=FG_PRIMARY,
            textvariable=self.activity_var,
        ).place(x=280, y=35)

        tk.Button(
            self.form_frame, text="Search", bg=FG_PRIMARY, font=FONT_BUTTON,
            width=10, bd=3, command=self._search_activity,
        ).place(x=40, y=450)

        tk.Button(
            self.form_frame, text="All", bg=FG_PRIMARY, font=FONT_BUTTON,
            width=10, bd=3, command=self._show_all_activity,
        ).place(x=190, y=450)

        tk.Button(
            self.form_frame, text="Back", bg=FG_PRIMARY, font=FONT_BUTTON,
            width=10, bd=3, command=self._close_form,
        ).place(x=340, y=450)

    def _search_activity(self):
        """Search for issued-book records by book or student ID."""
        query = self.activity_var.get().strip()
        if not query:
            messagebox.showinfo("Error", "Search field cannot be empty.")
            return

        # Refresh treeview
        columns = ("BOOK ID", "STUDENT ID", "ISSUE DATE", "RETURN DATE")
        self.activity_tree = self._create_treeview(self.form_frame, columns)
        self.activity_tree.place(x=50, y=150)

        results = db.get_student_activity(query)
        if not results:
            messagebox.showinfo("Error", "No records found.")
            return
        for row in results:
            self.activity_tree.insert("", tk.END, values=row)

    def _show_all_activity(self):
        """Show all issued-book records."""
        columns = ("BOOK ID", "STUDENT ID", "ISSUE DATE", "RETURN DATE")
        self.activity_tree = self._create_treeview(self.form_frame, columns)
        self.activity_tree.place(x=50, y=150)

        for row in db.get_all_issued():
            self.activity_tree.insert("", tk.END, values=row)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _close_form(self):
        """Destroy the current form frame."""
        if hasattr(self, "form_frame") and self.form_frame.winfo_exists():
            self.form_frame.destroy()

    def _return_to_main_menu(self):
        """Restart the app at the main menu (skip login)."""
        self.root.destroy()
        self._build_main_menu()

    @staticmethod
    def _maximize_window(window):
        """Maximize the window cross-platform (Windows, macOS, Linux)."""
        try:
            window.state("zoomed")  # Windows
        except tk.TclError:
            try:
                window.attributes("-zoomed", True)  # Linux
            except tk.TclError:
                w = window.winfo_screenwidth()
                h = window.winfo_screenheight()
                window.geometry(f"{w}x{h}+0+0")  # macOS fallback

    @staticmethod
    def _create_canvas(parent, image_path, width, height):
        """Create a full-screen canvas with a background image."""
        img = Image.open(image_path)
        img_resized = img.resize((width, height), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img_resized)

        canvas = tk.Canvas(parent, width=width, height=height)
        canvas.grid(row=0, column=0)
        canvas.grid_propagate(False)
        canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        canvas.image = photo  # prevent garbage collection
        return canvas

    @staticmethod
    def _create_treeview(parent, columns):
        """Create a styled Treeview widget with the given column headings."""
        tree = ttk.Treeview(parent, height=13, columns=columns, show="headings")
        for idx, col in enumerate(columns, start=1):
            tree.heading(f"#{idx}", text=col)
            tree.column(col, width=100)
        return tree

    # ------------------------------------------------------------------
    # Run
    # ------------------------------------------------------------------

    def run(self):
        """Start the application main loop."""
        self.root.mainloop()
