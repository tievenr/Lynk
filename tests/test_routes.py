import pytest
from fastapi.testclient import TestClient


def test_health(client):
    """Test health endpoint returns healthy status."""
    test_client, _ = client
    response = test_client.get("/health")
    
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_shorten(client):
    """Test URL shortening creates a short code."""
    test_client, storage = client
    response = test_client.post(
        "/shorten",
        json={"url": "https://google.com"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "short_code" in data
    assert "short_url" in data
    assert len(data["short_code"]) == 6
    assert data["short_code"] in data["short_url"]
    
    # Verify URL was stored
    assert data["short_code"] in storage
    assert storage[data["short_code"]] == "https://google.com"


def test_redirect_success(client):
    """Test redirect works for existing short code."""
    test_client, storage = client
    
    # First shorten a URL
    response = test_client.post(
        "/shorten",
        json={"url": "https://github.com"}
    )
    short_code = response.json()["short_code"]
    
    # Then redirect
    response = test_client.get(f"/{short_code}", follow_redirects=False)
    
    assert response.status_code == 307
    assert response.headers["location"] == "https://github.com"


def test_redirect_404(client):
    """Test redirect returns 404 for non-existent code."""
    test_client, _ = client
    response = test_client.get("/invalidcode123")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "URL not found"
