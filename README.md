# Library-Management-System---Python
# 📚 Library Management System (SQLite + Python)

This is a simple **Library Management System** developed in Python using the built-in **sqlite3** module. It includes features for both **Admin** and **User** roles to manage books and transactions efficiently.

---

## 🚀 Features

### 👤 User Functionalities:

* View all available books
* Search for a book by ID
* Borrow a book
* Return a book
* View user profile

### 🛠️ Admin Functionalities:

* View all registered users
* Add new users
* View all books
* Add new books
* View transaction history

---

## 🗂️ Project Structure

```bash
library_management/
├── library.db        # User and transaction data
├── lib.db            # Book data
├── main.py           # Main Python file with class definitions
├── README.md         # This file
```

---

## 🧠 Technologies Used

* **Python 3.x**
* **SQLite3** for lightweight database operations

---

## 🛠️ Setup Instructions

### 🔹 1. Clone the repository

```bash
git clone https://github.com/yourusername/library-management.git
cd library-management
```

### 🔹 2. Run the program

```bash
python main.py
```

---

## 🔑 Login Credentials

### Admin

* **Username**: `admin`
* **Password**: `Welcome123`

### User

* You can either use an existing user or add a new one via the Admin panel.

---

## 💾 Database Tables

### users_det (in library.db)

| Field        | Type                                             |
| ------------ | ------------------------------------------------ |
| id           | INTEGER                                          |
| name         | TEXT                                             |
| password     | TEXT                                             |
| age          | INTEGER                                          |
| email        | TEXT                                             |
| phone\_no    | TEXT                                             |
| book\_status | TEXT (optional, stores current borrowed book ID) |

### libra (in lib.db)

| Field  | Type    |
| ------ | ------- |
| id     | INTEGER |
| title  | TEXT    |
| author | TEXT    |

### transactions (in library.db)

| Field      | Type     |
| ---------- | -------- |
| trans\_id  | INTEGER  |
| user\_name | TEXT     |
| book\_id   | INTEGER  |
| action     | TEXT     |
| timestamp  | DATETIME |

---

## 📬 Contribution

Pull requests are welcome. If you find bugs or have suggestions, feel free to open an issue.

---

## 📜 License

This project is licensed under the MIT License.

---
