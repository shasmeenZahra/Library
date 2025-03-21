import json
import streamlit as st
import os

# File to store library data
LIBRARY_FILE = "library.json"

# Function to load the library data from a file
def load_library():
    if not os.path.exists(LIBRARY_FILE):
        return []
    try:
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Function to save the library data to a file
def save_library(library):
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)

# Initialize session state for the library
if "library" not in st.session_state:
    st.session_state.library = load_library()

# Streamlit UI
st.set_page_config(page_title="Personal Library Manager", layout="wide")
st.title("📚 Personal Library Manager")

# Sidebar for actions
st.sidebar.header("Manage Library")

# Add Book
with st.sidebar.expander("➕ Add a Book"):
    title = st.text_input("Book Title", key="title")
    author = st.text_input("Author", key="author")
    year = st.number_input("Publication Year", min_value=0, step=1, format="%d", key="year")
    genre = st.text_input("Genre", key="genre")
    read_status = st.checkbox("Have you read this book?", key="read_status")

    if st.button("Add Book"):
        if title and author and genre:
            st.session_state.library.append({
                "title": title,
                "author": author,
                "year": int(year),
                "genre": genre,
                "read": read_status
            })
            save_library(st.session_state.library)
            st.success(f"'{title}' added successfully!")
            st.rerun()  # Rerun the app to update UI
        else:
            st.warning("Please fill all required fields!")

# Remove Book
with st.sidebar.expander("🗑️ Remove a Book"):
    book_titles = [book["title"] for book in st.session_state.library]
    if book_titles:
        book_to_remove = st.selectbox("Select a book to remove", book_titles)
        if st.button("Remove Book"):
            st.session_state.library = [book for book in st.session_state.library if book["title"] != book_to_remove]
            save_library(st.session_state.library)
            st.success(f"'{book_to_remove}' removed successfully!")
            st.rerun()
    else:
        st.info("No books available to remove.")

# Search & Filter
search_query = st.text_input("🔍 Search by title, author, or genre")
filter_read = st.selectbox("📖 Filter by read status", ["All", "Read", "Unread"])
sort_by = st.selectbox("🔀 Sort by", ["Title", "Author", "Year"])
show_books = st.button("Show Library")

# Display Books
if show_books:
    st.subheader("📚 Library Collection")
    filtered_books = [book for book in st.session_state.library if 
                      search_query.lower() in book["title"].lower() or 
                      search_query.lower() in book["author"].lower() or 
                      search_query.lower() in book["genre"].lower()]

    if filter_read == "Read":
        filtered_books = [book for book in filtered_books if book["read"]]
    elif filter_read == "Unread":
        filtered_books = [book for book in filtered_books if not book["read"]]

    if sort_by == "Title":
        filtered_books.sort(key=lambda x: x["title"].lower())
    elif sort_by == "Author":
        filtered_books.sort(key=lambda x: x["author"].lower())
    elif sort_by == "Year":
        filtered_books.sort(key=lambda x: x["year"], reverse=True)

    if filtered_books:
        for book in filtered_books:
            st.markdown(f"**{book['title']}** by *{book['author']}* ({book['year']})")
            st.text(f"Genre: {book['genre']} | Read: {'Yes' if book['read'] else 'No'}")
            st.markdown("---")
    else:
        st.warning("No matching books found.")

# Display Statistics
st.subheader("📊 Library Statistics")
total_books = len(st.session_state.library)
read_books = sum(1 for book in st.session_state.library if book['read'])
unread_books = total_books - read_books

if total_books > 0:
    st.metric("Total Books", total_books)
    st.metric("Books Read", f"{read_books} ({(read_books / total_books) * 100:.2f}%)")
    st.metric("Books Unread", f"{unread_books} ({(unread_books / total_books) * 100:.2f}%)")
else:
    st.info("No books in the library yet.")
