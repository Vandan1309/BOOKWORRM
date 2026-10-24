
from src.book_registry import get_available_books, get_book

def main():
    book = get_book("jungle_book")
    print("Book:", book["title"])
    print("Author:", book["author"])

    books = get_available_books()
    print("\nAvailable books:")
    for book_id, details in books.items():
        print(f"- {book_id}: {details['title']}")

if __name__ == "__main__":
    main()
