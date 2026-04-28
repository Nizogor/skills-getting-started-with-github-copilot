"""
Tests for POST /activities/{activity_name}/signup using AAA pattern.
"""


def test_signup_successful_adds_email_to_participants(client):
    # Arrange
    activity_name = "Chess Club"
    new_email = "newstudent@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": new_email}
    )

    # Assert
    assert response.status_code == 200
    assert new_email in response.json()["message"]

    # Verify participant added
    all_activities = client.get("/activities").json()
    assert new_email in all_activities[activity_name]["participants"]


def test_signup_duplicate_email_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": existing_email}
    )

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()


def test_signup_for_nonexistent_activity_returns_404(client):
    # Arrange
    fake_activity = "Nonexistent Activity"
    email = "student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{fake_activity}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    assert "activity not found" in response.json()["detail"].lower()


def test_signup_increments_participant_count(client):
    # Arrange
    activity_name = "Programming Class"
    email = "tester@mergington.edu"
    before_count = len(client.get("/activities").json()[activity_name]["participants"])

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    after_count = len(client.get("/activities").json()[activity_name]["participants"])
    assert after_count == before_count + 1
"""
Tests for POST /activities/{activity_name}/signup endpoint.

These tests follow the AAA (Arrange-Act-Assert) pattern:
- Arrange: Set up test data and initial state
- Act: Call the signup endpoint
- Assert: Verify response status, message, and updated participant list
"""

def test_signup_successful_adds_email_to_participants(client):
    """
    ARRANGE: Identify an activity and prepare a new email
    ACT: Sign up the email for the activity
    ASSERT: Verify response indicates success and participant was added
    """
    # Arrange
    activity_name = "Chess Club"
    new_email = "newstudent@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": new_email}
    )
    
    # Assert
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]
    assert new_email in response.json()["message"]
    
    # Verify the participant was actually added
    all_activities = client.get("/activities").json()
    assert new_email in all_activities[activity_name]["participants"]


def test_signup_for_nonexistent_activity_returns_404(client):
    """
    ARRANGE: Prepare data for a non-existent activity and email
    ACT: Attempt to sign up for invalid activity
    ASSERT: Verify response is 404 with appropriate error
    """
    # Arrange
    fake_activity = "Nonexistent Activity"
    email = "student@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{fake_activity}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_signup_duplicate_email_returns_400(client):
    """
    ARRANGE: Identify existing participant in an activity
    ACT: Attempt to sign up same email again
    ASSERT: Verify response is 400 indicating duplicate
    """
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"  # Already signed up
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": existing_email}
    )
    
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()


def test_signup_increments_participant_count(client):
    """
    ARRANGE: Get initial participant count for an activity
    ACT: Sign up a new participant
    ASSERT: Verify participant count increased by exactly 1
    """
    # Arrange
    activity_name = "Programming Class"
    new_email = "testuser123@mergington.edu"
    
    initial_activities = client.get("/activities").json()
    initial_count = len(initial_activities[activity_name]["participants"])
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": new_email}
    )
    
    # Assert
    assert response.status_code == 200
    updated_activities = client.get("/activities").json()
    updated_count = len(updated_activities[activity_name]["participants"])
    assert updated_count == initial_count + 1


def test_signup_multiple_students_same_activity(client):
    """
    ARRANGE: Prepare two different students to sign up for same activity
    ACT: Sign up both students sequentially
    ASSERT: Verify both are successfully added and both exist
    """
    # Arrange
    activity_name = "Drama Club"
    email1 = "student1@mergington.edu"
    email2 = "student2@mergington.edu"
    
    # Act
    response1 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email1}
    )
    response2 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email2}
    )
    
    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 200
    
    final_activities = client.get("/activities").json()
    participants = final_activities[activity_name]["participants"]
    assert email1 in participants
    assert email2 in participants


def test_signup_with_url_encoded_activity_name(client):
    """
    ARRANGE: Use activity name with spaces that need URL encoding
    ACT: Sign up for activity with spaces
    ASSERT: Verify signup works with URL-encoded names like "Chess%20Club"
    """
    # Arrange
    activity_name = "Basketball Team"
    new_email = "athlete@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": new_email}
    )
    
    # Assert
    assert response.status_code == 200
    activities = client.get("/activities").json()
    assert new_email in activities[activity_name]["participants"]


def test_signup_preserves_existing_participants(client):
    """
    ARRANGE: Get initial list of participants for an activity
    ACT: Sign up new participant for that activity
    ASSERT: Verify existing participants are still there along with new one
    """
    # Arrange
    activity_name = "Soccer Club"
    new_email = "newsoccer@mergington.edu"
    
    initial_activities = client.get("/activities").json()
    initial_participants = initial_activities[activity_name]["participants"].copy()
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": new_email}
    )
    
    # Assert
    assert response.status_code == 200
    updated_activities = client.get("/activities").json()
    updated_participants = updated_activities[activity_name]["participants"]
    
    # Check that all original participants are still there
    for original_email in initial_participants:
        assert original_email in updated_participants
    # Check that new email was added
    assert new_email in updated_participants
