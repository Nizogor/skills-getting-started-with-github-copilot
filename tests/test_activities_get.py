"""
Tests for GET /activities endpoint using AAA pattern.
"""


def test_get_activities_returns_all_activities(client):
    # Arrange
    expected_activity_count = 9

    # Act
    response = client.get("/activities")
    activities = response.json()

    # Assert
    assert response.status_code == 200
    assert isinstance(activities, dict)
    assert len(activities) == expected_activity_count


def test_get_activities_returns_expected_fields(client):
    # Arrange
    required_fields = {"description", "schedule", "max_participants", "participants"}

    # Act
    response = client.get("/activities")
    activities = response.json()

    # Assert
    assert response.status_code == 200
    for activity in activities.values():
        assert required_fields.issubset(activity.keys())


def test_get_activities_participants_are_strings(client):
    # Arrange
    # no setup needed

    # Act
    response = client.get("/activities")
    activities = response.json()

    # Assert
    assert response.status_code == 200
    for activity in activities.values():
        assert all(isinstance(email, str) for email in activity["participants"])
"""
Tests for GET /activities endpoint.

These tests follow the AAA (Arrange-Act-Assert) pattern:
- Arrange: Set up test data and client
- Act: Call the endpoint
- Assert: Verify response status, structure, and content
"""

def test_get_activities_returns_all_activities(client):
    """
    ARRANGE: Prepare the test client
    ACT: Request all activities
    ASSERT: Verify response status and contains all 9 activities
    """
    # Arrange
    expected_activity_count = 9
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    assert response.status_code == 200
    assert isinstance(activities, dict)
    assert len(activities) == expected_activity_count


def test_get_activities_returns_correct_structure(client):
    """
    ARRANGE: Define expected activity fields
    ACT: Request activities and check structure
    ASSERT: Verify each activity has required fields
    """
    # Arrange
    required_fields = {"description", "schedule", "max_participants", "participants"}
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    assert response.status_code == 200
    for activity_name, activity_data in activities.items():
        assert isinstance(activity_data, dict)
        assert required_fields.issubset(activity_data.keys())
        assert isinstance(activity_data["description"], str)
        assert isinstance(activity_data["schedule"], str)
        assert isinstance(activity_data["max_participants"], int)
        assert isinstance(activity_data["participants"], list)


def test_get_activities_participants_are_all_strings(client):
    """
    ARRANGE: Set up expectations for participant data
    ACT: Get activities and inspect participants
    ASSERT: Verify all participants in lists are strings (emails)
    """
    # Arrange
    # (No setup needed)
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    assert response.status_code == 200
    for activity_name, activity_data in activities.items():
        participants = activity_data["participants"]
        for participant in participants:
            assert isinstance(participant, str)
            assert "@" in participant  # Email format check


def test_get_activities_includes_chess_club(client):
    """
    ARRANGE: Identify an expected activity
    ACT: Fetch all activities
    ASSERT: Verify Chess Club exists with correct details
    """
    # Arrange
    expected_activity_name = "Chess Club"
    expected_description = "Learn strategies and compete in chess tournaments"
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    assert response.status_code == 200
    assert expected_activity_name in activities
    activity = activities[expected_activity_name]
    assert activity["description"] == expected_description
    assert activity["max_participants"] == 12


def test_get_activities_has_participants_data(client):
    """
    ARRANGE: Define activities with known initial participants
    ACT: Request activities
    ASSERT: Verify participant counts match expected initial state
    """
    # Arrange
    activities_with_known_participants = {
        "Chess Club": 2,
        "Programming Class": 2,
        "Gym Class": 2,
    }
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    assert response.status_code == 200
    for activity_name, expected_count in activities_with_known_participants.items():
        assert len(activities[activity_name]["participants"]) == expected_count
