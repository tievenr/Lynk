import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient


@pytest.fixture
def mock_redis():
    """Mock Redis storage for testing."""
    storage = {}
    
    mock = Mock()
    mock.set = lambda code, url: storage.update({code: url})
    mock.get = lambda code: storage.get(code)
    
    return mock, storage


@pytest.fixture
def client(mock_redis):
    """FastAPI test client with mocked Redis."""
    mock, storage = mock_redis
    
    with patch('app.store.r', mock):
        from app.main import app
        yield TestClient(app), storage
