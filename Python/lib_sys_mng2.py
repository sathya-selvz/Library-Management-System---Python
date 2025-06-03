import sqlite3

# ---------- TABLE SETUP (Run once to initialize) ----------
def setup_tables():
    with sqlite3.connect("library.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users_det (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            password TEXT NOT NULL,
            age INTEGER NOT NULL,
            email TEXT NOT NULL,
            phone_no TEXT NOT NULL
        )''')

    with sqlite3.connect("lib.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS libra (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL
        )''')
  
    with sqlite3.connect("library.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            trans_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL,
            book_id INTEGER NOT NULL,
            action TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')
 
# ---------- BASE USER CLASS ----------
class User:
    def __init__(self, name, password):
        self.name = name
        self.password = password

# ---------- LIBRARY CLASS ----------
class Library(User):
    def book_list(self):
        with sqlite3.connect("lib.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM libra")
            books = cursor.fetchall()
            for book in books:
                print(book)

    def log_transaction(self, book_id, action):
            print(f"Logging transaction: {action} book ID {book_id} by user {self.name}")
            with sqlite3.connect("library.db") as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO transactions (user_name, book_id, action)
                    VALUES (?, ?, ?)''', (self.name, book_id, action))
                conn.commit()


    def find_book(self):
        book_id = input("Enter the book ID to find: ")
        with sqlite3.connect("lib.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM libra WHERE id = ?", (book_id,))
            result = cursor.fetchone()
            if result:
                print("Book Found:", result)
            else:
                print("Book Not Found.")

    def borrow_book(self):
        book_id = int(input("Enter book ID to borrow: "))
        with sqlite3.connect("lib.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM libra WHERE id = ?", (book_id,))
            book = cursor.fetchone()
            if book:
                print("Borrowed Book:", book)
                cursor.execute("DELETE FROM libra WHERE id = ?", (book_id,))
                print("Book Borrowed Successfully!")
                self.log_transaction(book_id, "borrowed")
                return str(book_id)
            else:
                print("Book Not Found.")
                return None
            
    def return_book(self):
            with sqlite3.connect("library.db") as user_conn:
                user_cursor = user_conn.cursor()
                user_cursor.execute("SELECT book_status FROM users_det WHERE name = ? AND password = ?",
                                    (self.name, self.password))
                result = user_cursor.fetchone()
                if result and result[0]:
                    book_id = int(result[0])
                    title = input("Enter the book title to return: ")
                    author = input("Enter the book author: ")

                    # Insert book back into the libra table
                    with sqlite3.connect("lib.db") as lib_conn:
                        lib_cursor = lib_conn.cursor()
                        lib_cursor.execute("INSERT INTO libra(id, title, author) VALUES (?, ?, ?)",
                                        (book_id, title, author))
                        print("Book returned successfully.")

                    # Clear book_status in users_det
                    user_cursor.execute("UPDATE users_det SET book_status = NULL WHERE name = ? AND password = ?",
                                        (self.name, self.password))
                    user_conn.commit()
                    self.log_transaction(book_id, "returned")
                else:
                    print("You have no book to return.")


    def view_profile(self):
        with sqlite3.connect("library.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users_det WHERE name = ? AND password = ?",
                           (self.name, self.password))
            cursor.execute("SELECT id, name, age, email, phone_no FROM users_det")
            profile = cursor.fetchone()
            if profile:
                print("ID | Name | Age | Email | Phone ")
                print("-------------------------------")
                print(profile)
            else:
                print("Profile not found.")

    def user_menu(self):
        while True:
            print("\n1. View All Books\n2. Find Book\n3. Borrow Book\n4. Return Book\n5. View Profile\n6. Exit")
            choice = input("Choose an option: ")
            if choice == '1':
                self.book_list()
            elif choice == '2':
                self.find_book()
            elif choice == '3':
                book_status = self.borrow_book()
                if book_status:
                    self.update_book_status(book_status) 
            elif choice == '4':
                self.return_book()           
            elif choice == '5':
                self.view_profile()
            elif choice == '6':
                print("Exiting...")
                break
            else:
                print("Invalid choice.")

    def update_book_status(self, book_status):
        with sqlite3.connect("library.db") as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE users_det SET book_status = ? WHERE name = ? AND password = ?",
                           (book_status, self.name, self.password))
            conn.commit()

# ---------- ADMIN CLASS ----------
class Admin(Library):
    def admin_menu(self):
        while True:
            print("\n1. View All Users\n2. Add New User\n3. View All Books\n4. Add Book\n5. View Transaction\n6. Exit")
            choice = input("Choose an option: ")
            if choice == '1':
                self.view_users()
            elif choice == '2':
                self.add_user()
            elif choice == '3':
                self.book_list()
            elif choice == '4':
                self.add_book()
            elif choice == '5':
                self.view_transactions()
            elif choice == '6': 
                print("Admin logged out.")
                break
            else:
                print("Invalid choice.")

    def view_users(self):
        with sqlite3.connect("library.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users_det")
            users = cursor.fetchall()
            print("ID | Name | Password | Age | Email | Phone | Book Status")
            print("----------------------------------------------------------")
            for user in users:
                print(user)

    def add_user(self):
        name = input("Enter new user name: ")
        password = input("Enter password: ")
        age = int(input("Age: "))
        email = input("Email: ")
        phone = input("Phone: ")
        with sqlite3.connect("library.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users_det (name, password, age, email, phone_no)
                VALUES (?, ?, ?, ?, ?)""", (name, password, age, email, phone))
            print("User added successfully.")


    def add_book(self):
        choice = input("Do you want to add a book? (yes/no): ").lower()
        if choice == 'yes':
            title = input("Book title: ")
            author = input("Author: ")
            book_id = int(input("Book ID: "))
            with sqlite3.connect("lib.db") as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO libra(id, title, author) VALUES (?, ?, ?)",
                               (book_id, title, author))
                print("Book Added Successfully.")

    
    def view_transactions(self):
            with sqlite3.connect("library.db") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM transactions")
                transactions = cursor.fetchall()
                print("\nTransaction History:")
                print("ID | User | Book ID | Action | Timestamp")
                print("-------------------------------------------")
                for trans in transactions:
                    print(trans)



# ---------- MAIN ENTRY POINT ----------
def main():
    setup_tables()

    name = input("Enter username: ")
    password = input("Enter password: ")

    if name == "admin":
        admin_password = input("Enter admin passphrase: ")
        if admin_password == "Welcome123":
            admin = Admin(name, password)
            admin.admin_menu()
        else:
            print("Incorrect admin password.")
    else:
        # Check if user exists
        with sqlite3.connect("library.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users_det WHERE name = ? AND password = ?", (name, password))
            user = cursor.fetchone()
            if user:
                lib_user = Library(name, password)
                lib_user.user_menu()
            else:
                print("Invalid username or password.")

if __name__ == "__main__":
    main()