import pytest
from LibraryApi.app import app # type: ignore



@pytest.fixture
def client():
    app.config["TESTING"] = True
    
    with app.test_client() as client:
        yield client
        
        
def test_health_endpoint_succes(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.content_type == "application/json"
    data = response.get_json()
    assert isinstance(data, dict)
    assert data["status"] == "ok" 
    
def test_get_books_endpoint_return_books(client):
    book = {
        "title": "Guide to Python",
        "author": "Kenneth Reitz"
    }
    client.post("/book", json=book)
    response = client.get("/books")
    assert response.status_code == 200
    data = response.get_json()
    assert data is not None
    
def test_post_book_success(client):
    book = {
        "title": "Guide to Python",
        "author": "Kenneth Reitz"
    }
    response = client.post("/book", json=book)
    
    assert response.status_code == 201
    data = response.get_json()
    assert isinstance(data, dict)
    
    assert data["title"] == book["title"]
    assert data["author"] == book["author"]
    assert "id" in data
    
def test_post_book_missing_title(client):
    invalid_data = {
        "title": "",
        "author": "Uncle Bob"
    }
    client.post("/book", json=invalid_data)
    response = client.get("/books")
    assert response.status_code == 200
    data = response.get_json()
    

def test_delete_book_updates_db(client):
    book = {
        "title": "Guide to Python",
        "author": "Kenneth Reitz"
    }
    client.post("/book", json=book)
    book_id_to_delete = 1
    response = client.delete(f"/book/{book_id_to_delete}")
    assert response.status_code == 200
    
    response_get = client.get(f"/book/{book_id_to_delete}")
    assert response_get.status_code == 404
    
    
def test_delete_fails_if_not_found(client):
    
    book_id_to_delete = 1
    response = client.delete(f"/book/{book_id_to_delete}")
    data = response.get_json()
    assert "Book 1 not found" in data["message"]

