"""
Shared test configuration and fixtures.
"""

import pytest
from fastapi.testclient import TestClient
from src import app as app_module


def reset_activities():
    """Reset the activity database to its original state."""
    app_module.activities.clear()
    app_module.activities.update({
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
            "description": "Competitive basketball training and tournaments",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["james@mergington.edu"]
        },
        "Soccer Club": {
            "description": "Soccer practice and friendly matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 18,
            "participants": ["lucas@mergington.edu", "noah@mergington.edu"]
        },
        "Drama Club": {
            "description": "Theater performance and acting workshops",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 25,
            "participants": ["grace@mergington.edu"]
        },
        "Art Studio": {
            "description": "Painting, drawing, and sculpture techniques",
            "schedule": "Fridays, 3:00 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["isabella@mergington.edu", "ava@mergington.edu"]
        },
        "Science Club": {
            "description": "Explore physics, chemistry, and biology through experiments",
            "schedule": "Mondays, 4:00 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["alexander@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop public speaking and argumentation skills",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 14,
            "participants": ["mason@mergington.edu", "charlotte@mergington.edu"]
        }
    })


@pytest.fixture
def client():
    """Return a fresh TestClient instance with a reset activity database."""
    reset_activities()
    return TestClient(app_module.app)
"""
Shared test configuration and fixtures.
"""

import pytest
from fastapi.testclient import TestClient
from src import app as app_module


def reset_activities():
    """Reset the activities dictionary to initial state."""
    app_module.activities.clear()
    app_module.activities.update({
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
            "description": "Competitive basketball training and tournaments",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["james@mergington.edu"]
        },
        "Soccer Club": {
            "description": "Soccer practice and friendly matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 18,
            "participants": ["lucas@mergington.edu", "noah@mergington.edu"]
        },
        "Drama Club": {
            "description": "Theater performance and acting workshops",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 25,
            "participants": ["grace@mergington.edu"]
        },
        "Art Studio": {
            "description": "Painting, drawing, and sculpture techniques",
            "schedule": "Fridays, 3:00 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["isabella@mergington.edu", "ava@mergington.edu"]
        },
        "Science Club": {
            "description": "Explore physics, chemistry, and biology through experiments",
            "schedule": "Mondays, 4:00 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["alexander@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop public speaking and argumentation skills",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 14,
            "participants": ["mason@mergington.edu", "charlotte@mergington.edu"]
        }
    })


@pytest.fixture
def client():
    """
    Fixture that provides a TestClient instance for the FastAPI app.
    
    Resets the activities database to initial state before each test to ensure
    test isolation and prevent tests from interfering with each other.
    
    This allows tests to make HTTP requests to the app without running
    a live server.
    """
    reset_activities()
    return TestClient(app_module.app)
