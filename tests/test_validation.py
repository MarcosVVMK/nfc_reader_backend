"""
Simple validation test to ensure the API structure is working correctly
This test verifies that the new layered architecture maintains the same API interface
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from app.database import get_db, Base

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create test database tables
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_health_endpoint():
    """Test health endpoint"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "message": "API is running"}


def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Programação 3 Backend API is running!"}


def test_user_endpoints_structure():
    """Test that user endpoints maintain the same structure as before"""
    
    # Test GET /users/ (empty initially)
    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    assert response.json() == []
    
    # Test POST /users/
    user_data = {
        "name": "Test User",
        "email": "test@example.com"
    }
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 201
    user = response.json()
    assert user["name"] == "Test User"
    assert user["email"] == "test@example.com"
    assert "id" in user
    assert "created_at" in user
    
    user_id = user["id"]
    
    # Test GET /users/{user_id}
    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["id"] == user_id
    
    # Test PUT /users/{user_id}
    update_data = {"name": "Updated User"}
    response = client.put(f"/api/v1/users/{user_id}", json=update_data)
    assert response.status_code == 200
    updated_user = response.json()
    assert updated_user["name"] == "Updated User"
    assert updated_user["email"] == "test@example.com"  # email unchanged
    
    # Test DELETE /users/{user_id}
    response = client.delete(f"/api/v1/users/{user_id}")
    assert response.status_code == 204
    
    # Verify user is deleted
    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 404


def test_email_validation():
    """Test email validation (business logic is preserved)"""
    
    # Create first user
    user_data = {
        "name": "First User",
        "email": "duplicate@example.com"
    }
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 201
    
    # Try to create user with same email
    user_data2 = {
        "name": "Second User", 
        "email": "duplicate@example.com"
    }
    response = client.post("/api/v1/users/", json=user_data2)
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]


if __name__ == "__main__":
    print("Running validation tests...")
    pytest.main([__file__, "-v"])