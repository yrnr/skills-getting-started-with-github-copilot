"""
Tests for the GET /activities endpoint.
"""

import pytest


def test_get_activities_success(test_client):
    """Test that GET /activities returns all activities with correct structure."""
    response = test_client.get("/activities")
    
    assert response.status_code == 200
    activities = response.json()
    
    # Verify it's a dictionary
    assert isinstance(activities, dict)
    
    # Verify all expected activities are present
    expected_activities = [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Basketball Team",
        "Tennis Club",
        "Drama Club",
        "Music Ensemble",
        "Debate Team",
        "Science Club"
    ]
    for activity in expected_activities:
        assert activity in activities


def test_get_activities_structure(test_client):
    """Test that each activity has the correct structure."""
    response = test_client.get("/activities")
    activities = response.json()
    
    required_keys = {"description", "schedule", "max_participants", "participants"}
    
    for activity_name, activity_data in activities.items():
        # Check all required keys are present
        assert required_keys.issubset(activity_data.keys()), \
            f"Activity '{activity_name}' missing required keys"
        
        # Validate types
        assert isinstance(activity_data["description"], str)
        assert isinstance(activity_data["schedule"], str)
        assert isinstance(activity_data["max_participants"], int)
        assert isinstance(activity_data["participants"], list)
        
        # Validate participants are all strings (emails)
        for participant in activity_data["participants"]:
            assert isinstance(participant, str)


def test_get_activities_participants_count(test_client):
    """Test that participant count matches the participants list length."""
    response = test_client.get("/activities")
    activities = response.json()
    
    for activity_name, activity_data in activities.items():
        participants_list = activity_data["participants"]
        # Verify the participants list is valid
        assert len(participants_list) <= activity_data["max_participants"], \
            f"Activity '{activity_name}' has more participants than max allowed"


def test_get_activities_valid_emails(test_client):
    """Test that all participants have valid email-like formats."""
    response = test_client.get("/activities")
    activities = response.json()
    
    for activity_name, activity_data in activities.items():
        for participant in activity_data["participants"]:
            # Basic email validation: contains @ and domain
            assert "@" in participant, \
                f"Participant '{participant}' in '{activity_name}' is not a valid email format"
            assert participant.endswith(".edu"), \
                f"Participant '{participant}' in '{activity_name}' does not end with .edu"


def test_get_activities_empty_response_structure(test_client):
    """Test that the response structure is valid even with empty data."""
    response = test_client.get("/activities")
    
    # Response should always be valid JSON
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
