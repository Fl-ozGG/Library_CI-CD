from flask import Flask, jsonify, request
from bookstore import BookStore
import jwt #
from functools import wraps
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_super_secret_and_complex_key_for_jwt'
store = BookStore()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'message': 'Token is missing or improperly formatted!'}), 401
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            # The 'current_user' is just the payload data, you can use it if needed
            current_user = data 
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 401
        
        # Pass the decoded token data to the decorated function
        return f(current_user, *args, **kwargs)

    return decorated

@app.route('/login', methods=['POST'])
def login():
    auth = request.get_json()
    
    if auth and auth.get('user') == 'test' and auth.get('password') == 'pass':
        payload = {
            'user': auth['user'],
        }
        
        token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm="HS256")
        
        return jsonify({'token': token}), 200

    return jsonify({'message': 'Could not verify'}), 401


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
@token_required
def post_book(current_user):
    data = request.get_json()
    title = data.get("title")
    author = data.get("author")
    try:
        book = store.add_book(title, author)
        return jsonify(book), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route("/book/<int:book_id>", methods=["DELETE"])
@token_required
def delete_book(current_user, book_id):
    return jsonify(store.delete_book(book_id)), 200




if __name__ == "__main__":
    app.run(debug=True)
