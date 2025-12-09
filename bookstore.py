class BookStore: 
    def __init__(self):
        self.books = []
        self.next_id = 1
        
    def add_book(self, title, author):
        cleaned_title = title.strip() if isinstance(title, str) else title
        cleaned_author = author.strip() if isinstance(author, str) else author
        
        if not cleaned_title:
            raise ValueError("Title is required and cannot be empty.")
        
        if not cleaned_author:
            raise ValueError("Author is required and cannot be empty.")
            
        book = {
            "id": self.next_id,
            "title": cleaned_title, 
            "author": cleaned_author
        }
        self.books.append(book)
        self.next_id += 1
        return book

    def get_books(self):
        
        return self.books

    def get_book(self, book_id):
        for b in self.books:
            if b["id"] == book_id:
                return b
        return None

    def delete_book(self, book_id):
        before = len(self.books)
        
        self.books = [b for b in self.books if b["id"] != book_id]
        
        if(len(self.books) < before):
            return {"deleted": True, "message": f"Book {book_id} deleted"}
        
        return {"deleted": False, "message": f"Book {book_id} not found"}