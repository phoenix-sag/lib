#BOOK CLASS


class Book:
    def __init__(self, title, author,book_id, borrowed=False):
        self.title = title
        self.author = author
        self.book_id = book_id
        self.borrowed = borrowed

    def show_book(self):
        print(f"Title: {self.title}, Author: {self.author}, Book ID: {self.book_id}, Borrowed: {self.borrowed}")
        return

#MEMBER CLASS
class Member:
    def __init__(self, name, member_id):
        self.name = name
        self.member_id = member_id
        self.borrowed_books = []
    def borrow_book(self, book):
        self.borrowed_books.append(book)
        print(f"{self.name} borrowed {book.title}")
    def return_book(self, book):
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)
            print(f"{self.name} returned {book.title}")
        else:
            print(f"{self.name} did not borrow {book.title}")
    def show_borrowed_books(self):
        print(f"{self.name} has borrowed the following books: ")
        for book in self.borrowed_books:
            book.show_book()

#BORROW CLASS
class Borrow:
    def __init__(self, borrow_id, member, book):
        self.borrow_id = borrow_id
        self.member = member
        self.book = book
    def show_borrow(self):
        print(f"Borrow ID: {self.borrow_id}, Member: {self.member.name}, Book: {self.book.title}")

#LIBRARY CLASS
class Library:
    def __init__(self):
        self.books = []
        self.members = []
        self.borrows = []

    def add_book(self, book):
        if self.find_book(book.book_id) is not None:
            print(f"A book with ID {book.book_id} already exists.")
            return False
        self.books.append(book)
        print(f"Added {book.title} to the library")
        return True

    def add_member(self, member):
        if self.find_member(member.member_id) is not None:
            print(f"A member with ID {member.member_id} already exists.")
            return False
        self.members.append(member)
        print(f"Added {member.name} as a member")
        return True

    def remove_book(self, book_id):
        book = self.find_book(book_id)
        if book is None:
            print("Book not found.")
            return False

        self.books.remove(book)
        print(f"Removed {book.title} from the library.")
        return True

    def view_books(self):
        if not self.books:
            print("There are no books in the library.")
            return []

        for book in self.books:
            book.show_book()
        return self.books

    def borrow_book(self, member_id, book_id, borrow_id=None):
        member = self.find_member(member_id)
        if member is None:
            print("Member not found.")
            return False

        book = self.find_book(book_id)
        if book is None:
            print("Book not found.")
            return False

        if book.borrowed:
            print(f"{book.title} is already borrowed.")
            return False

        if any(existing.book == book and existing.member == member for existing in self.borrows):
            print(f"{member.name} already has {book.title} checked out.")
            return False

        if borrow_id is None:
            borrow_id = len(self.borrows) + 1

        borrow = Borrow(borrow_id, member, book)
        self.borrows.append(borrow)
        member.borrow_book(book)
        book.borrowed = True
        return True

    def return_book(self, member_id, book_id):
        member = self.find_member(member_id)
        if member is None:
            print("Member not found.")
            return False

        book = self.find_book(book_id)
        if book is None:
            print("Book not found.")
            return False

        if not book.borrowed:
            print(f"{book.title} is not currently borrowed.")
            return False

        borrow_record = None
        for borrow in self.borrows:
            if borrow.member == member and borrow.book == book:
                borrow_record = borrow
                break

        if borrow_record is None:
            print(f"{member.name} does not currently have {book.title} borrowed.")
            return False

        member.return_book(book)
        self.borrows.remove(borrow_record)
        book.borrowed = False
        return True

    def find_book(self, book_id):
        for book in self.books:
            if book.book_id == book_id:
                return book
        return None

    def find_member(self, member_id):
        for member in self.members:
            if member.member_id == member_id:
                return member
        return None

    def find_borrow(self, borrow_id):
        for borrow in self.borrows:
            if borrow.borrow_id == borrow_id:
                return borrow
        return None

    def get_statistics(self):
        stats = {
            "total_books": len(self.books),
            "total_members": len(self.members),
            "total_borrows": len(self.borrows),
            "borrowed_books": sum(1 for book in self.books if book.borrowed),
            "available_books": sum(1 for book in self.books if not book.borrowed),
        }
        return stats

def get_number(message):
    while True:
        try:
            number=int(input(message))
            return number
        except ValueError:
            print("Invalid input. Please enter a number.")

#MENU
def show_menu():
    print("="*30)
    print("\n Library Management System")
    print("="*30)
    print("1. Add Book")
    print("2. Add Member")
    print("3. View Books")
    print("4. Search Book")
    print("5. Borrow Book")
    print("6. Return Book")
    print("7. Remove Book")
    print("8. View Statistics")
    print("9. Exit")   
    print("="*30)

def main():
    library = Library()
    while True:
        show_menu()
        choice = get_number("Enter your choice: ")
        if choice == 1:
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            book_id = get_number("Enter book ID: ")
            book = Book(title, author, book_id)
            library.add_book(book)
        elif choice == 2:
            name = input("Enter member name: ")
            member_id = get_number("Enter member ID: ")
            member = Member(name, member_id)
            library.add_member(member)
        elif choice == 3:
            for book in library.books:
                book.show_book()
        elif choice == 4:
            book_id = get_number("Enter book ID to search: ")
            book = library.find_book(book_id)
            if book:
                book.show_book()
            else:
                print("Book not found.")
        elif choice == 5:
            member_id = get_number("Enter member ID: ")
            member = library.find_member(member_id)
            if not member:
                print("Member not found.")
                continue
            book_id = get_number("Enter book ID to borrow: ")
            book = library.find_book(book_id)
            if not book:
                print("Book not found.")
                continue
            if book.borrowed:
                print(f"{book.title} is already borrowed.")
                continue
            member.borrow_book(book)
            book.borrowed = True
        elif choice == 6:
            member_id = get_number("Enter member ID: ")
            member = library.find_member(member_id)
            if not member:
                print("Member not found.")
                continue
            book_id = get_number("Enter book ID to return: ")
            book = library.find_book(book_id)
            if not book:
                print("Book not found.")
                continue
            member.return_book(book)
            book.borrowed = False
        elif choice == 7:
            book_id = get_number("Enter book ID to remove: ")
            book = library.find_book(book_id)
            if not book:
                print("Book not found.")
                continue
            library.books.remove(book)
            print(f"Removed {book.title} from the library.")
        elif choice == 8:
            print(f"Total books: {len(library.books)}")
            print(f"Total members: {len(library.members)}")
        elif choice == 9:
            print("Have a great day!")
            break
        else:
            print("Invalid choice.")
            #this is ur final code for the library management system.\
            


if __name__ == "__main__":
    main()
        
# yes





    