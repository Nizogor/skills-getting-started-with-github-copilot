"""
Tests for DELETE /activities/{activity_name}/signup using AAA pattern.
"""


def test_unregister_removes_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email_to_remove = "michael@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email_to_remove}
    )

    # Assert
    assert response.status_code == 200
    assert email_to_remove not in client.get("/activities").json()[activity_name]["participants"]


def test_unregister_nonexistent_activity_returns_404(client):
    # Arrange
    fake_activity = "Nonexistent Activity"
    email = "student@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{fake_activity}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    assert "activity not found" in response.json()["detail"].lower()


def test_unregister_nonexistent_participant_returns_404(client):
    # Arrange
    activity_name = "Art Studio"
    missing_email = "nobody@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": missing_email}
    )

    # Assert
    assert response.status_code == 404
    assert "participant not found" in response.json()["detail"].lower()


def test_unregister_decrements_participant_count(client):
    # Arrange
    activity_name = "Programming Class"
    email_to_remove = "emma@mergington.edu"
    before_count = len(client.get("/activities").json()[activity_name]["participants"])

    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email_to_remove}
    )

    # Assert
    assert response.status_code == 200
    after_count = len(client.get("/activities").json()[activity_name]["participants"])
    assert after_count == before_count - 1
"""
Tests for DELETE /activities/{activity_name}/signup endpoint.

These tests follow the AAA (Arrange-Act-Assert) pattern:
- Arrange: Set up test data and initial state
- Act: Call the unregister endpoint
- Assert: Verify response status, message, and updated participant list
"""

def test_unregister_removes_participant(client):
    """
    ARRANGE: Identify an existing participant in an activity
    ACT: Unregister that participant
    ASSERT: Verify response indicates success and participant was removed
    """
    # Arrange
    activity_name = "Chess Club"
    email_to_remove = "michael@mergington.edu"  # Known participant
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email_to_remove}
    )
    
    # Assert
    assert response.status_code == 200
    assert "Unregistered" in response.json()["message"]
    
    # Verify participant was actually removed
    activities = client.get("/activities").json()
    assert email_to_remove not in activities[activity_name]["participants"]


def test_unregister_from_nonexistent_activity_returns_404(client):
    """
    ARRANGE: Prepare data for non-existent activity
    ACT: Attempt to unregister from invalid activity
    ASSERT: Verify response is 404
    """
    # Arrange
    fake_activity = "Nonexistent Activity"
    email = "student@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{fake_activity}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_unregister_nonexistent_participant_returns_404(client):
    """
    ARRANGE: Identify an activity and an email not in its participants
    ACT: Attempt to unregister email that was never signed up
    ASSERT: Verify response is 404 indicating participant not found
    """
    # Arrange
    activity_name = "Art Studio"
    email_not_signed_up = "nonmember@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email_not_signed_up}
    )
    
    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_unregister_decrements_participant_count(client):
    """
    ARRANGE: Get initial participant count and identify a participant to remove
    ACT: Unregister the participant
    ASSERT: Verify participant count decreased by exactly 1
    """
    # Arrange
    activity_name = "Programming Class"
    email_to_remove = "emma@mergington.edu"
    
    initial_activities = client.get("/activities").json()
    initial_count = len(initial_activities[activity_name]["participants"])
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email_to_remove}
    )
    
    # Assert
    assert response.status_code == 200
    updated_activities = client.get("/activities").json()
    updated_count = len(updated_activities[activity_name]["participants"])
    assert updated_count == initial_count - 1


def test_unregister_preserves_other_participants(client):
    """
    ARRANGE: Get initial list of participants and identify one to remove
    ACT: Unregister that one participant
    ASSERT: Verify other participants remain unchanged
    """
    # Arrange
    activity_name = "Gym Class"
    email_to_remove = "john@mergington.edu"
    
    initial_activities = client.get("/activities").json()
    initial_participants = initial_activities[activity_name]["participants"].copy()
    other_participants = [e for e in initial_participants if e != email_to_remove]
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email_to_remove}
    )
    
    # Assert
    assert response.status_code == 200
    updated_activities = client.get("/activities").json()
    updated_participants = updated_activities[activity_name]["participants"]
    
    # Verify removed email is not there
    assert email_to_remove not in updated_participants
    # Verify other participants are still there
    for other_email in other_participants:
        assert other_email in updated_participants


def test_unregister_multiple_participants_sequentially(client):
    """
    ARRANGE: Identify multiple participants in an activity
    ACT: Unregister multiple participants one at a time
    ASSERT: Verify each unregister removes the correct participant
    """
    # Arrange
    activity_name = "Debate Team"
    email1 = "mason@mergington.edu"
    email2 = "charlotte@mergington.edu"
    
    initial_activities = client.get("/activities").json()
    assert len(initial_activities[activity_name]["participants"]) >= 2
    
    # Act - Remove first participant
    response1 = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email1}
    )
    
    # Assert - First removal successful
    assert response1.status_code == 200
    after_first = client.get("/activities").json()
    assert email1 not in after_first[activity_name]["participants"]
    assert email2 in after_first[activity_name]["participants"]
    
    # Act - Remove second participant
    response2 = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email2}
    )
    
    # Assert - Second removal successful
    assert response2.status_code == 200
    after_second = client.get("/activities").json()
    assert email1 not in after_second[activity_name]["participants"]
    assert email2 not in after_second[activity_name]["participants"]


def test_unregister_single_participant_from_activity(client):
    """
    ARRANGE: Find activity with only one participant and unregister them
    ACT: Unregister that participant
    ASSERT: Verify activity now has empty participants list
    """
    # Arrange
    activity_name = "Basketball Team"
    email = "james@mergington.edu"
    
    initial_activities = client.get("/activities").json()
    assert email in initial_activities[activity_name]["participants"]
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    final_activities = client.get("/activities").json()
    assert email not in final_activities[activity_name]["participants"]
