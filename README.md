# 📚 Library API (Flask & JWT Secured)

This project is a minimalist **RESTful API** for managing a small library's book collection. It is built using the **Flask** micro-framework and includes **JWT (JSON Web Token) authentication** to secure critical write operations.

## 🔗 Live Documentation
[![Run in Postman](https://run.pstmn.io/button.svg)](https://documenter.getpostman.com/view/40133516/2sB3dQw9n4)
**👉 Access the full, interactive API documentation here: [https://documenter.getpostman.com/view/40133516/2sB3dQw9n4](https://documenter.getpostman.com/view/40133516/2sB3dQw9n4)**

## ✨ Features

* **RESTful CRUD Operations:** Create, Read, Update, and Delete (CRUD) operations for books.
* **Health Check Endpoint:** Simple status check (`/health`).
* **In-Memory Database:** Uses a simple Python class (`BookStore`) for data persistence (data resets on server restart).
* **Security:** Implements **JWT Authorization** to protect `POST` and `DELETE` endpoints, ensuring only authorized users can modify the database.

---

## 🛠️ Technology Stack

| **Python 3.14** | The core programming language. |
| **Flask** | The lightweight micro-framework for handling API routing. |
| **Authentication** | **PyJWT** Used for encoding, decoding, and verifying JSON Web Tokens. |
| **Testing** | **Pytest** | Used for running unit tests (`test_unit.py`) and API integration tests (`test_api.py`). |
| **CI/CD** | **GitHub Actions** | Automated workflow to run tests on every push and pull request. |

---

## 🚀 Getting Started

### Prerequisites

You will need **Python 3.14** and **pip** installed.

1.  **Clone the repository:**
    git clone [YOUR_REPOSITORY_URL_HERE]
    cd LibraryAPI

2.  **Set up the Virtual Environment (Recommended):**
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate

3.  **Install dependencies:**
    pip install -r requirements.txt

4.  **Run the application:**
    python app.py

---

## 🔑 Authorization (JWT)

Endpoints that modify data (`POST`, `DELETE`) require a valid JWT included in the request headers.

