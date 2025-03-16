import pytest
from app import app  # Update with the correct path

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome' in response.data
def test_timetable_creation():
    result = create_timetable(batch='A', subjects=['Math', 'Science'])
    assert len(result) == 2  # Replace with the expected condition
    assert 'Math' in result

def test_api_schedule(client):
    response = client.get('/api/schedule')
    assert response.status_code == 200
    assert 'schedule' in response.json

def test_db_insert():
    create_schedule('Math', '9 AM')  # Example function
    assert check_schedule_exists('Math')  # Replace with actual function

