from flask import Flask, jsonify, request
from .bookstore import BookStore

app = Flask(__name__)
store = BookStore()

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/books", methods=["GET"])
def get_books():
    books = store.get_books()
    if books is None:
        return jsonify({"error": "No Books found"}), 404
    return jsonify(books), 200

@app.route("/book/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = store.get_book(book_id)
    
    if book is None:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(book), 200

@app.route("/book", methods=["POST"])
def post_book():
    data = request.get_json()
    title = data.get("title")
    author = data.get("author")
    try:
        book = store.add_book(title, author)
        return jsonify(book), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route("/book/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    return jsonify(store.delete_book(book_id)), 200




if __name__ == "__main__":
    app.run(debug=True)
