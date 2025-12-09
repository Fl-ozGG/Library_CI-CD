import pytest
from ..bookstore import BookStore

def test_add_book_creates_book():
    store = BookStore()
    book = store.add_book("Title", "Author")
    assert book["id"] == 1
    assert book["title"] == "Title"
    assert book["author"] == "Author"

def test_add_book_stores_book_on_db():
    store = BookStore()
    store.add_book("Title1", "Author1")
    store.add_book("Title2", "Author2")
    assert len(store.books) == 2
    
def test_add_book_fails_if_missing_fields():
    store = BookStore()
    with pytest.raises(ValueError):
        store.add_book("","Author")
        
def test_delete_book_eliminate_register_from_database():
    store = BookStore()
    
    store.add_book("Title1", "Author1")
    assert len(store.books) == 1

    store.delete_book(1)
    assert len(store.books) == 0

def test_delete_book_fails_if_id_not_found():
    store = BookStore()
    book_id = 1
    result = store.delete_book(book_id)
    assert result["message"] == f"Book {book_id} not found"