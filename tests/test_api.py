import pytest
from app import app 

@pytest.fixture
def client():
    app.config["TESTING"] = True
    
    with app.test_client() as client:
        yield client
        
@pytest.fixture
def auth_token(client):
    """Logs in and returns a valid JWT string."""
    login_data = {
        "user": "test", 
        "password": "pass" # Use the credentials defined in app.py /login
    }
    response = client.post("/login", json=login_data)
    assert response.status_code == 200
    return response.get_json()["token"]
    
@pytest.fixture
def auth_headers(auth_token):
    """Creates the Authorization header dictionary."""
    return {"Authorization": f"Bearer {auth_token}"}


def test_health_endpoint_succes(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.content_type == "application/json"
    data = response.get_json()
    assert isinstance(data, dict)
    assert data["status"] == "ok" 
    
def test_get_books_endpoint_return_books(client, auth_headers): 
    book = {
        "title": "Guide to Python",
        "author": "Kenneth Reitz"
    }
    
    client.post("/book", json=book, headers=auth_headers) 
    
    response = client.get("/books")
    assert response.status_code == 200
    data = response.get_json()
    assert data is not None
    
def test_post_book_success(client, auth_headers): 
    book = {
        "title": "Guide to Python",
        "author": "Kenneth Reitz"
    }
    response = client.post("/book", json=book, headers=auth_headers)
    
    assert response.status_code == 201
    data = response.get_json()
    assert isinstance(data, dict)
    
    assert data["title"] == book["title"]
    assert data["author"] == book["author"]
    assert "id" in data
    
def test_post_book_missing_title(client, auth_headers):
    invalid_data = {
        "title": "",
        "author": "Uncle Bob"
    }
    response_post = client.post("/book", json=invalid_data, headers=auth_headers)
    assert response_post.status_code == 400
    response_get = client.get("/books")

def test_delete_book_updates_db(client, auth_headers):
    book = {
        "title": "Book to Delete",
        "author": "A. Tester"
    }
    post_response = client.post("/book", json=book, headers=auth_headers)
    book_id_to_delete = post_response.get_json()["id"] 
    response = client.delete(f"/book/{book_id_to_delete}", headers=auth_headers)
    assert response.status_code == 200
    
    response_get = client.get(f"/book/{book_id_to_delete}")
    assert response_get.status_code == 404
    
    
def test_delete_fails_if_not_found(client, auth_headers): 
    book_id_to_delete = 1 
    response = client.delete(f"/book/{book_id_to_delete}", headers=auth_headers)
    data = response.get_json()
    assert "Book 1 not found" in data["message"]
    
def test_post_book_unauthorized(client):
    book = {
        "title": "Secret Book",
        "author": "No Token"
    }
    response = client.post("/book", json=book)
    
    assert response.status_code == 401
    assert "Token is missing" in response.get_json()["message"]