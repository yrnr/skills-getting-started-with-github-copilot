"""
Tests for the POST /activities/{activity_name}/signup endpoint.
"""

import pytest


def test_signup_success(test_client):
    """Test successful signup for an activity."""
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    
    response = test_client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity in data["message"]


def test_signup_adds_participant(test_client):
    """Test that signup actually adds the participant to the activity."""
    email = "newstudent@mergington.edu"
    activity = "Programming Class"
    
    # Get initial state
    initial = test_client.get("/activities").json()
    initial_count = len(initial[activity]["participants"])
    
    # Sign up
    response = test_client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    assert response.status_code == 200
    
    # Verify participants increased
    updated = test_client.get("/activities").json()
    updated_count = len(updated[activity]["participants"])
    assert updated_count == initial_count + 1
    assert email in updated[activity]["participants"]


def test_signup_activity_not_found(test_client):
    """Test signup fails for non-existent activity."""
    response = test_client.post(
        "/activities/Nonexistent Activity/signup",
        params={"email": "test@mergington.edu"}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data


def test_signup_duplicate_signup(test_client):
    """Test that signing up twice for the same activity fails."""
    email = "duplicate@mergington.edu"
    activity = "Chess Club"
    
    # First signup should succeed
    response1 = test_client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    assert response1.status_code == 200
    
    # Second signup should fail with 400 (Bad Request)
    response2 = test_client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    assert response2.status_code == 400
    data = response2.json()
    assert "detail" in data


def test_signup_different_activities_same_student(test_client):
    """Test that a student can sign up for multiple different activities."""
    email = "multitask@mergington.edu"
    activities = ["Chess Club", "Programming Class", "Drama Club"]
    
    for activity in activities:
        response = test_client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert response.status_code == 200
    
    # Verify student is in all activities
    all_activities = test_client.get("/activities").json()
    for activity in activities:
        assert email in all_activities[activity]["participants"]


def test_signup_email_with_special_characters(test_client):
    """Test signup with email containing special characters."""
    email = "student.name+test@mergington.edu"
    activity = "Gym Class"
    
    response = test_client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    # Should accept the email as-is
    assert response.status_code == 200
    
    # Verify it was added correctly
    activities = test_client.get("/activities").json()
    assert email in activities[activity]["participants"]


def test_signup_activity_name_with_spaces(test_client):
    """Test signup for activity names containing spaces."""
    email = "test@mergington.edu"
    activities_with_spaces = [
        "Chess Club",
        "Programming Class",
        "Basketball Team",
        "Tennis Club",
        "Drama Club",
        "Music Ensemble",
        "Debate Team",
        "Science Club"
    ]
    
    for activity in activities_with_spaces:
        response = test_client.post(
            f"/activities/{activity}/signup",
            params={"email": f"student{activities_with_spaces.index(activity)}@mergington.edu"}
        )
        assert response.status_code == 200, \
            f"Failed to signup for activity '{activity}'"


def test_signup_case_sensitivity_email(test_client):
    """Test that emails with different cases are treated as different."""
    activity = "Gym Class"
    email1 = "testuser@mergington.edu"
    email2 = "TESTUSER@mergington.edu"
    
    # Sign up with lowercase
    response1 = test_client.post(
        f"/activities/{activity}/signup",
        params={"email": email1}
    )
    assert response1.status_code == 200
    
    # Try signup with uppercase (should be treated as different email)
    response2 = test_client.post(
        f"/activities/{activity}/signup",
        params={"email": email2}
    )
    # Both should be accepted as the system doesn't normalize case
    assert response2.status_code == 200


def test_signup_response_message_format(test_client):
    """Test that signup response has the expected message format."""
    email = "format@mergington.edu"
    activity = "Science Club"
    
    response = test_client.post(
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
