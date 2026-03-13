# 📚 Library Management System

A desktop **Library Management System** built with Python, Tkinter, and SQLite. Features an admin login, full CRUD operations for books, and a student book-issuing workflow with due-date tracking.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey?logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## ✨ Features

| Module | Capabilities |
|---|---|
| **Authentication** | Secure admin login with SHA-256 hashed passwords |
| **Book Management** | Add, search, view all, update copies, delete books |
| **Student Management** | Issue books, return books, track student activity |
| **Data Persistence** | SQLite database with auto-initialization |

---

## 📸 Screenshots

**Home Screen**
![image](https://github.com/user-attachments/assets/377edbff-77e5-4faa-9463-b0102c603df7)

**Book Data**
![image](https://github.com/user-attachments/assets/637d8025-e28e-4112-8acb-511514f6086f)

**Student Data**
![image](https://github.com/user-attachments/assets/b2cc018e-5f53-4d31-abf7-500360cedc26)

---

## 🛠️ Tech Stack

- **Language:** Python 3.8+
- **GUI Framework:** Tkinter
- **Image Processing:** Pillow
- **Database:** SQLite3
- **Security:** SHA-256 password hashing (hashlib)

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Mansha0805/Library-Management-System.git
   cd Library-Management-System
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

4. **Login with default credentials**
   | Username | Password |
   |----------|----------|
   | `admin`  | `admin`  |

---

## 📁 Project Structure

```
Library-Management-System/
├── assets/              # Background images
│   ├── finance.png
│   ├── image2.png
│   └── library.png
├── app.py               # Tkinter GUI (LibraryApp class)
├── db.py                # Database layer (SQLite CRUD + auth)
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
├── .gitignore
├── LICENSE
└── README.md
```

---

## 📊 Database Schema

```mermaid
erDiagram
    login {
        INTEGER mem_id PK
        TEXT username
        TEXT password
    }
    book_info {
        VARCHAR ID PK
        TEXT TITLE
        TEXT AUTHOR
        TEXT GENRE
        INTEGER COPIES
        VARCHAR LOCATION
    }
    book_issued {
        VARCHAR BOOK_ID PK
        VARCHAR STUDENT_ID PK
        DATE ISSUE_DATE
        DATE RETURN_DATE
    }
    book_info ||--o{ book_issued : "issued as"
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
