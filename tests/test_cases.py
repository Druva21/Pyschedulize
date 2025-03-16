import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__) + "/..")))
from app import app  # Update with the correct path

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome" in response.data

