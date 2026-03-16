import pytest
from fastapi.testclient import TestClient
from app.main import app, _reset_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_state():
    """Wipe the in-memory DB before every test so tests are independent."""
    _reset_db()


# Tests for get all users in user_router endpoints 
class TestGetUsers:
    def test_get_users_empty(self):
        resp = client.get("/users")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_get_users_returns_all(self):
        client.post("/users", json={"name": "Alice", "email": "alice@example.com"})
        client.post("/users", json={"name": "Bob", "email": "bob@example.com"})
        resp = client.get("/users")
        assert resp.status_code == 200
        assert len(resp.json()) == 2

    def test_get_users_response_shape(self):
        client.post("/users", json={"name": "Alice", "email": "alice@example.com"})
        users = client.get("/users").json()
        assert {"id", "name", "email"} == set(users[0].keys())


# Tests for get user by ID in user_router endpoints with error handling for not found user
class TestGetUser:
    def test_get_existing_user(self):
        created = client.post("/users", json={"name": "Alice", "email": "alice@example.com"}).json()
        resp = client.get(f"/users/{created['id']}")
        assert resp.status_code == 200
        assert resp.json() == created

    def test_get_nonexistent_user_returns_404(self):
        resp = client.get("/users/999")
        assert resp.status_code == 404
        assert resp.json()["detail"] == "User not found"


# Tests for create user in user_router endpoints with background task to send welcome email and error handling for duplicate email and missing fields
class TestCreateUser:
    def test_create_user_success(self):
        payload = {"name": "Alice", "email": "alice@example.com"}
        resp = client.post("/users", json=payload)
        assert resp.status_code == 201
        body = resp.json()
        assert body["name"] == "Alice"
        assert body["email"] == "alice@example.com"
        assert "id" in body

    def test_create_user_assigns_auto_id(self):
        u1 = client.post("/users", json={"name": "Alice", "email": "a@example.com"}).json()
        u2 = client.post("/users", json={"name": "Bob",   "email": "b@example.com"}).json()
        assert u1["id"] != u2["id"]

    def test_create_user_duplicate_email_returns_400(self):
        client.post("/users", json={"name": "Alice", "email": "alice@example.com"})
        resp = client.post("/users", json={"name": "Alice2", "email": "alice@example.com"})
        assert resp.status_code == 400
        assert resp.json()["detail"] == "Email already registered"

    def test_create_user_missing_field_returns_422(self):
        resp = client.post("/users", json={"name": "Alice"})  # missing email
        assert resp.status_code == 422

    def test_created_user_appears_in_get_users(self):
        client.post("/users", json={"name": "Alice", "email": "alice@example.com"})
        users = client.get("/users").json()
        assert any(u["email"] == "alice@example.com" for u in users)