import streamlit as st
from streamlit_option_menu import option_menu
from datetime import datetime, timedelta

class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.available = True

class Member:
    def __init__(self, name, member_id):
        self.name = name
        self.member_id = member_id
        self.borrowed_books = []

class RentalTransaction:
    rental_id_counter = 1
    
    def __init__(self, member, book):
        self.member = member
        self.book = book
        self.due_date = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
        self.rental_id = RentalTransaction.rental_id_counter
        RentalTransaction.rental_id_counter += 1

class Library:
    def __init__(self):
        self.books = []
        self.members = []
        self.rental_transactions = []
    
    def add_book(self, title, author, isbn):
        book = Book(title, author, isbn)
        self.books.append(book)
        return book
    
    def remove_book(self, book):
        if book in self.books:
            self.books.remove(book)
    
    def add_member(self, name, member_id):
        member = Member(name, member_id)
        self.members.append(member)
        return member
    
    def remove_member(self, member):
        if member in self.members:
            self.members.remove(member)
    
    def rent_book(self, member, book):
        if book.available:
            transaction = RentalTransaction(member, book)
            self.rental_transactions.append(transaction)
            member.borrowed_books.append(book)
            book.available = False
            return transaction
        else:
            return None

# Streamlit UI
st.set_page_config(page_title='Library Management System', page_icon='📚')
st.title("Library Management System")

if "library" not in st.session_state:
    st.session_state.library = Library()

with st.sidebar:
    selected = option_menu(
        menu_title = "Main Menu",
        options = ["Display Details", "Add Book", "Remove Book", "Add Member", "Remove Member", "Rent Book"],
        icons = ["collection-fill", "plus-square", "trash", "person-add", "person-x", "book"],
        menu_icon="bookshelf",
    )

if selected == "Display Details":
    # Display All Books Section
    st.header("All Books:")
    for book in st.session_state.library.books:
        st.write(f"Title: {book.title}, Author: {book.author}, ISBN: {book.isbn}, Available: {'Yes' if book.available else 'No'}")

    # Display All Members Section
    st.header("All Members:")
    for member in st.session_state.library.members:
        st.write(f"Name: {member.name}, Member ID: {member.member_id}")
        st.write(f"Borrowed Books: {[book.title for book in member.borrowed_books]}")
        st.write("---")

# Add Book Section
if selected == "Add Book":
    st.header("Add Book")
    book_title = st.text_input("Book Title")
    book_author = st.text_input("Author")
    book_isbn = st.number_input("ISBN", min_value=0, step=1)
    if st.button("Add Book"):
        book = st.session_state.library.add_book(book_title, book_author, book_isbn)
        st.success(f"Book '{book.title}' added successfully!")

if selected == "Remove Book":
# Remove Book Section
    st.header("Remove Book")
    book_to_remove = st.selectbox("Select Book to Remove", [book.title for book in st.session_state.library.books])
    if st.button("Remove Book"):
        selected_book = next((b for b in st.session_state.library.books if b.title == book_to_remove), None)
        if selected_book:
            st.session_state.library.remove_book(selected_book)
            st.success(f"Book '{selected_book.title}' removed successfully!")
        else:
            st.warning("Book not found!")

if selected == "Add Member":
    # Add Member Section
    st.header("Add Member")
    member_name = st.text_input("Member Name")
    member_id = st.number_input("Member ID", min_value=1, step=1)
    if st.button("Add Member"):
        member = st.session_state.library.add_member(member_name, member_id)
        st.success(f"Member '{member.name}' added successfully!")

if selected == "Remove Member":
    # Remove Member Section
    st.header("Remove Member")
    member_to_remove = st.selectbox("Select Member to Remove", [member.name for member in st.session_state.library.members])
    if st.button("Remove Member"):
        selected_member = next((m for m in st.session_state.library.members if m.name == member_to_remove), None)
        if selected_member:
            st.session_state.library.remove_member(selected_member)
            st.success(f"Member '{selected_member.name}' removed successfully!")
        else:
            st.warning("Member not found!")

if selected == "Rent Book":
# Rent Book Section
    st.header("Rent Book")
    member_name_rent = st.selectbox("Select Member", [member.name for member in st.session_state.library.members])
    book_title_rent = st.selectbox("Select Book", [book.title for book in st.session_state.library.books])
    if st.button("Rent Book"):
        selected_member_rent = next((m for m in st.session_state.library.members if m.name == member_name_rent), None)
        selected_book_rent = next((b for b in st.session_state.library.books if b.title == book_title_rent), None)
        if selected_member_rent and selected_book_rent:
            transaction = st.session_state.library.rent_book(selected_member_rent, selected_book_rent)
            if transaction:
                st.success(f"Book '{transaction.book.title}' rented to '{transaction.member.name}' successfully! Due Date: {transaction.due_date}")
            else:
                st.warning(f"Book '{selected_book_rent.title}' is not available!")
        else:
            st.warning("Member or book not found!")

    # Rental Transactions Section
    st.header("Rental Transactions")
    for transaction in st.session_state.library.rental_transactions:
        st.write(f"Transaction ID: {transaction.rental_id}, Member: {transaction.member.name}, Book: {transaction.book.title}, Due Date: {transaction.due_date}")

    # Borrowed Books by Members Section
    st.header("Borrowed Books by Members")
    for member in st.session_state.library.members:
        st.write(f"Member: {member.name}, Borrowed Books: {[book.title for book in member.borrowed_books]}")
