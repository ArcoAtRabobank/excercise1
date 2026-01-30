import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

# Initial activities data for reset
INITIAL_ACTIVITIES = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Competitive basketball team for school championships",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["alex@mergington.edu"]
    },
    "Tennis Club": {
        "description": "Learn tennis skills and play friendly matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:00 PM",
        "max_participants": 10,
        "participants": ["isabella@mergington.edu"]
    },
    "Art Studio": {
        "description": "Explore painting, drawing, and sculpture techniques",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["grace@mergington.edu", "noah@mergington.edu"]
    },
    "Drama Club": {
        "description": "Perform in school plays and develop acting skills",
        "schedule": "Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["lucas@mergington.edu"]
    },
    "Debate Team": {
        "description": "Compete in debate competitions and develop critical thinking",
        "schedule": "Mondays and Fridays, 3:30 PM - 4:30 PM",
        "max_participants": 14,
        "participants": ["ava@mergington.edu", "mason@mergington.edu"]
    },
    "Science Club": {
        "description": "Conduct experiments and explore advanced scientific concepts",
        "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["ethan@mergington.edu"]
    }
}

@pytest.fixture(autouse=True)
def reset_activities():
    # Reset activities to initial state before each test
    activities.clear()
    activities.update(INITIAL_ACTIVITIES)

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert data["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"
    assert len(data["Chess Club"]["participants"]) == 2

def test_signup_success():
    response = client.post("/activities/Chess%20Club/signup?email=newstudent@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "Signed up newstudent@mergington.edu for Chess Club" in data["message"]
    
    # Check that participant was added
    response = client.get("/activities")
    data = response.json()
    assert "newstudent@mergington.edu" in data["Chess Club"]["participants"]

def test_signup_already_signed_up():
    response = client.post("/activities/Chess%20Club/signup?email=michael@mergington.edu")
    assert response.status_code == 400
    data = response.json()
    assert "Student is already signed up for this activity" in data["detail"]

def test_signup_activity_not_found():
    response = client.post("/activities/NonExistent/signup?email=test@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]

def test_unregister_success():
    response = client.delete("/activities/Chess%20Club/unregister?email=michael@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "Unregistered michael@mergington.edu from Chess Club" in data["message"]
    
    # Check that participant was removed
    response = client.get("/activities")
    data = response.json()
    assert "michael@mergington.edu" not in data["Chess Club"]["participants"]

def test_unregister_not_signed_up():
    response = client.delete("/activities/Chess%20Club/unregister?email=notsigned@mergington.edu")
    assert response.status_code == 400
    data = response.json()
    assert "Student is not signed up for this activity" in data["detail"]

def test_unregister_activity_not_found():
    response = client.delete("/activities/NonExistent/unregister?email=test@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]

def test_root_redirect():
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307  # Redirect
    assert response.headers["location"] == "/static/index.html"