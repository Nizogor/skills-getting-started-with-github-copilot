"""
Multi-step integration tests for FastAPI activity signup/unregister flows.
"""


def test_signup_then_unregister_same_student(client):
    # Arrange
    activity_name = "Science Club"
    email = "newstudent@mergington.edu"
    before_count = len(client.get("/activities").json()[activity_name]["participants"])

    # Act
    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert signup_response.status_code == 200
    assert email in client.get("/activities").json()[activity_name]["participants"]

    # Act
    unregister_response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert unregister_response.status_code == 200
    after_count = len(client.get("/activities").json()[activity_name]["participants"])
    assert after_count == before_count


def test_signup_unregister_then_signup_again(client):
    # Arrange
    activity_name = "Art Studio"
    email = "artist@mergington.edu"

    # Act
    first_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert first_response.status_code == 200
    assert email in client.get("/activities").json()[activity_name]["participants"]

    # Act
    delete_response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert delete_response.status_code == 200
    assert email not in client.get("/activities").json()[activity_name]["participants"]

    # Act
    second_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert second_response.status_code == 200
    assert email in client.get("/activities").json()[activity_name]["participants"]


def test_student_can_signup_to_multiple_activities(client):
    # Arrange
    email = "multi@mergington.edu"
    activity_names = ["Chess Club", "Drama Club", "Programming Class"]

    # Act
    responses = [
        client.post(f"/activities/{name}/signup", params={"email": email})
        for name in activity_names
    ]

    # Assert
    for response in responses:
        assert response.status_code == 200

    for name in activity_names:
        assert email in client.get("/activities").json()[name]["participants"]


def test_multiple_students_signup_and_one_unregisters(client):
    # Arrange
    activity_name = "Soccer Club"
    students = ["player1@mergington.edu", "player2@mergington.edu", "player3@mergington.edu"]
    for student in students:
        client.post(f"/activities/{activity_name}/signup", params={"email": student})

    before_count = len(client.get("/activities").json()[activity_name]["participants"])

    # Act
    remove_response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": students[1]}
    )

    # Assert
    assert remove_response.status_code == 200
    after_participants = client.get("/activities").json()[activity_name]["participants"]
    assert students[1] not in after_participants
    assert len(after_participants) == before_count - 1
"""
Integration tests for multi-step workflows.

These tests follow the AAA (Arrange-Act-Assert) pattern and test scenarios
that involve multiple endpoint calls in sequence to verify state changes
across the application.
"""

def test_signup_then_unregister_same_student(client):
    """
    ARRANGE: Select an activity and email to use
    ACT: Sign up, then unregister the same email
    ASSERT: Verify both operations succeed and participant count returns to initial state
    """
    # Arrange
    activity_name = "Science Club"
    email = "newsci@mergington.edu"
    
    initial_activities = client.get("/activities").json()
    initial_count = len(initial_activities[activity_name]["participants"])
    
    # Act - Sign up
    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert - Sign up succeeded
    assert signup_response.status_code == 200
    after_signup = client.get("/activities").json()
    assert email in after_signup[activity_name]["participants"]
    assert len(after_signup[activity_name]["participants"]) == initial_count + 1
    
    # Act - Unregister
    unregister_response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert - Unregister succeeded and participant is removed
    assert unregister_response.status_code == 200
    after_unregister = client.get("/activities").json()
    assert email not in after_unregister[activity_name]["participants"]
    assert len(after_unregister[activity_name]["participants"]) == initial_count


def test_signup_unregister_then_signup_again(client):
    """
    ARRANGE: Select activity and email for signup/unregister/signup cycle
    ACT: Sign up, unregister, then sign up again
    ASSERT: Verify can re-signup after unregistering and all states are correct
    """
    # Arrange
    activity_name = "Art Studio"
    email = "artist@mergington.edu"
    
    initial_activities = client.get("/activities").json()
    initial_count = len(initial_activities[activity_name]["participants"])
    
    # Act - First signup
    response1 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert - First signup worked
    assert response1.status_code == 200
    after_first_signup = client.get("/activities").json()
    assert email in after_first_signup[activity_name]["participants"]
    
    # Act - Unregister
    response2 = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert - Unregister worked
    assert response2.status_code == 200
    after_unregister = client.get("/activities").json()
    assert email not in after_unregister[activity_name]["participants"]
    
    # Act - Sign up again
    response3 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert - Second signup worked
    assert response3.status_code == 200
    after_second_signup = client.get("/activities").json()
    assert email in after_second_signup[activity_name]["participants"]


def test_multiple_students_signup_for_same_activity(client):
    """
    ARRANGE: Prepare multiple email addresses for the same activity
    ACT: Sign up all students for the activity
    ASSERT: Verify all students are enrolled and count matches
    """
    # Arrange
    activity_name = "Drama Club"
    students = [
        f"actor{i}@mergington.edu" for i in range(1, 4)
    ]
    
    initial_activities = client.get("/activities").json()
    initial_count = len(initial_activities[activity_name]["participants"])
    
    # Act - Sign up all students
    responses = []
    for email in students:
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        responses.append(response)
    
    # Assert - All signups successful
    for response in responses:
        assert response.status_code == 200
    
    final_activities = client.get("/activities").json()
    final_participants = final_activities[activity_name]["participants"]
    
    # Verify all students are in the list
    for email in students:
        assert email in final_participants
    
    # Verify total count increased by number of students
    assert len(final_participants) == initial_count + len(students)


def test_student_signup_to_multiple_activities(client):
    """
    ARRANGE: Select one student email and multiple activities
    ACT: Sign up same student to multiple different activities
    ASSERT: Verify student appears in all activity participant lists
    """
    # Arrange
    email = "multiactivity@mergington.edu"
    activities = ["Chess Club", "Programming Class", "Drama Club"]
    
    # Act - Sign up for multiple activities
    responses = []
    for activity_name in activities:
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        responses.append(response)
    
    # Assert - All signups successful
    for response in responses:
        assert response.status_code == 200
    
    # Verify student is in all activities
    final_activities = client.get("/activities").json()
    for activity_name in activities:
        assert email in final_activities[activity_name]["participants"]


def test_remove_one_student_from_group(client):
    """
    ARRANGE: Sign up multiple students for an activity, then identify one to remove
    ACT: Remove one student from a group
    ASSERT: Verify only that student is removed, others remain
    """
    # Arrange
    activity_name = "Soccer Club"
    students = ["player1@mergington.edu", "player2@mergington.edu", "player3@mergington.edu"]
    
    # Sign up all students first
    for email in students:
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
    
    initial_activities = client.get("/activities").json()
    initial_count = len(initial_activities[activity_name]["participants"])
    
    # Act - Remove one student
    student_to_remove = students[1]
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": student_to_remove}
    )
    
    # Assert - Removal successful
    assert response.status_code == 200
    
    final_activities = client.get("/activities").json()
    final_participants = final_activities[activity_name]["participants"]
    
    # Verify only one was removed
    assert len(final_participants) == initial_count - 1
    
    # Verify removed student is gone
    assert student_to_remove not in final_participants
    
    # Verify other students are still there
    for student_email in students:
        if student_email != student_to_remove:
            assert student_email in final_participants


def test_signup_after_failed_duplicate_attempt(client):
    """
    ARRANGE: Select a student and activity, sign them up, then attempt duplicate
    ACT: Try to duplicate signup (should fail), then unregister and try again
    ASSERT: Verify error on duplicate, but can re-signup after unregister
    """
    # Arrange
    activity_name = "Debate Team"
    email = "debater@mergington.edu"
    
    # Act - First signup
    response1 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert - First signup successful
    assert response1.status_code == 200
    
    # Act - Try duplicate signup
    response2 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert - Duplicate fails with 400
    assert response2.status_code == 400
    
    # Verify student is still only in the list once
    activities = client.get("/activities").json()
    participant_count = activities[activity_name]["participants"].count(email)
    assert participant_count == 1
    
    # Act - Unregister
    response3 = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert - Unregister successful
    assert response3.status_code == 200
    
    # Act - Sign up again
    response4 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert - Can sign up again after unregister
    assert response4.status_code == 200


def test_state_persistence_across_requests(client):
    """
    ARRANGE: Perform signup operations and get initial state
    ACT: Make multiple GET requests and signup/unregister operations
    ASSERT: Verify state is consistent and persisted across all requests
    """
    # Arrange
    activity_name = "Basketball Team"
    email = "baller@mergington.edu"
    
    initial_state = client.get("/activities").json()
    initial_participants = initial_state[activity_name]["participants"].copy()
    
    # Act & Assert - Sign up and verify immediately
    client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    state_after_signup_1 = client.get("/activities").json()
    participants_1 = state_after_signup_1[activity_name]["participants"]
    assert email in participants_1
    assert len(participants_1) == len(initial_participants) + 1
    
    # Act & Assert - Get state again and verify consistency
    state_after_signup_2 = client.get("/activities").json()
    participants_2 = state_after_signup_2[activity_name]["participants"]
    assert participants_1 == participants_2
    
    # Act & Assert - Unregister and verify
    client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    state_after_unregister = client.get("/activities").json()
    participants_3 = state_after_unregister[activity_name]["participants"]
    assert email not in participants_3
    assert len(participants_3) == len(initial_participants)
    
    # Act & Assert - Final verification that state is back to initial
    final_state = client.get("/activities").json()
    final_participants = final_state[activity_name]["participants"]
    assert final_participants == initial_participants
