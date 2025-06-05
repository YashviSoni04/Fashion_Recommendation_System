import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "Fashion Recommendation API" in data["message"]

def test_fashion_types_endpoint():
    """Test fashion types reference endpoint"""
    response = client.get("/fashion-types")
    assert response.status_code == 200
    data = response.json()
    assert "fashion_types" in data
    assert "casual" in data["fashion_types"]