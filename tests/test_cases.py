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

# Test case 1: Home Page  
def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Time Table Generator" in response.data

# Test case 2: Login Page Load
def test_login_page(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b"Login" in response.data  # Check if "Login" text appears on the page

# Test case 3: Successful Login
def test_valid_login(client):
    response = client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Dashboard" in response.data  # Assuming dashboard is shown after login

# Test case 4: Failed Login
def test_invalid_login(client):
    response = client.post('/login', data={'username': 'wrong', 'password': 'wrongpass'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Invalid credentials" in response.data  # Assuming the app displays an error message

# Test case 5: Timetable Page Access
def test_timetable_page(client):
    response = client.get('/timetable')
    assert response.status_code == 200
    assert b"Generate Timetable" in response.data  # Check if page loads correctly

# Test case 6: 404 Error Handling
def test_404_page(client):
    response = client.get('/nonexistentpage')
    assert response.status_code == 404
    assert b"Page Not Found" in response.data  # Assuming the app has a custom 404 page

