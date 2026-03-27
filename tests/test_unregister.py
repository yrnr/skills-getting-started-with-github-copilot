"""
Tests for the DELETE /activities/{activity_name}/signup endpoint.
"""

import pytest


def test_unregister_success(test_client):
    """Test successful unregistration from an activity."""
    email = "test@mergington.edu"
    activity = "Programming Class"
    
    # First sign up
    signup_response = test_client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    assert signup_response.status_code == 200
    
    # Then unregister
    response = test_client.delete(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity in data["message"]


def test_unregister_removes_participant(test_client):
    """Test that unregister actually removes the participant from the activity."""
    email = "removeme@mergington.edu"
    activity = "Chess Club"
    
    # Sign up first
    test_client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    # Verify signup worked
    activities = test_client.get("/activities").json()
    assert email in activities[activity]["participants"]
    initial_count = len(activities[activity]["participants"])
    
    # Unregister
    response = test_client.delete(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    assert response.status_code == 200
    
    # Verify participant was removed
    updated = test_client.get("/activities").json()
    assert email not in updated[activity]["participants"]
    assert len(updated[activity]["participants"]) == initial_count - 1


def test_unregister_activity_not_found(test_client):
    """Test unregister fails for non-existent activity."""
    response = test_client.delete(
        "/activities/Nonexistent Activity/signup",
        params={"email": "test@mergington.edu"}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data


def test_unregister_student_not_registered(test_client):
    """Test that unregistering a student not in the activity fails."""
    email = "notregistered@mergington.edu"
    activity = "Gym Class"
    
    response = test_client.delete(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data


def test_unregister_twice(test_client):
    """Test that unregistering twice fails on the second attempt."""
    email = "removeme@mergington.edu"
    activity = "Drama Club"
    
    # Sign up
    test_client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    # First unregister should succeed
    response1 = test_client.delete(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    assert response1.status_code == 200
    
    # Second unregister should fail
    response2 = test_client.delete(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    assert response2.status_code == 400


def test_unregister_preserves_other_participants(test_client):
    """Test that unregistering one student doesn't affect others."""
    activity = "Science Club"
    email1 = "keep1@mergington.edu"
    email2 = "remove@mergington.edu"
    email3 = "keep3@mergington.edu"
    
    # Sign up multiple students
    for email in [email1, email2, email3]:
        test_client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
    
    # Verify all signed up
    activities = test_client.get("/activities").json()
    for email in [email1, email2, email3]:
        assert email in activities[activity]["participants"]
    
    # Unregister one
    response = test_client.delete(
        f"/activities/{activity}/signup",
        params={"email": email2}
    )
    assert response.status_code == 200
    
    # Verify only the correct one was removed
    updated = test_client.get("/activities").json()
    assert email1 in updated[activity]["participants"]
    assert email2 not in updated[activity]["participants"]
    assert email3 in updated[activity]["participants"]


def test_unregister_case_sensitivity(test_client):
    """Test email case sensitivity in unregister."""
    activity = "Basketball Team"
    email_lower = "casesensitive@mergington.edu"
    
    # Sign up with lowercase
    test_client.post(
        f"/activities/{activity}/signup",
        params={"email": email_lower}
    )
    
    # Try unregister with different case
    email_upper = "CASESENSITIVE@mergington.edu"
    response = test_client.delete(
        f"/activities/{activity}/signup",
        params={"email": email_upper}
    )
    
    # With case-sensitive matching, this should fail
    # (unless the system normalizes case, which it doesn't currently)
    # Verify the lowercase email is still registered
    activities = test_client.get("/activities").json()
    assert email_lower in activities[activity]["participants"]


def test_unregister_response_message_format(test_client):
    """Test that unregister response has the expected message format."""
    email = "format@mergington.edu"
    activity = "Tennis Club"
    
    # Sign up first
    test_client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    # Unregister
    response = test_client.delete(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    message = data["message"]
    
    # Message should be readable and contain relevant info
    assert isinstance(message, str)
    assert len(message) > 0
