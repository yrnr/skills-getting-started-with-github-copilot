"""
Integration tests for multi-step workflows across multiple endpoints.
"""

import pytest


def test_signup_retrieve_unregister_workflow(test_client):
    """Test the complete workflow: signup -> retrieve -> unregister -> verify removed."""
    email = "workflow@mergington.edu"
    activity = "Music Ensemble"
    
    # Step 1: Verify student is not in activity initially
    activities = test_client.get("/activities").json()
    initial_participants = activities[activity]["participants"][:]
    assert email not in initial_participants
    
    # Step 2: Sign up
    signup_response = test_client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    assert signup_response.status_code == 200
    
    # Step 3: Retrieve and verify
    activities = test_client.get("/activities").json()
    assert email in activities[activity]["participants"]
    assert len(activities[activity]["participants"]) == len(initial_participants) + 1
    
    # Step 4: Unregister
    unregister_response = test_client.delete(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    assert unregister_response.status_code == 200
    
    # Step 5: Verify removal
    activities = test_client.get("/activities").json()
    assert email not in activities[activity]["participants"]
    assert len(activities[activity]["participants"]) == len(initial_participants)


def test_signup_unregister_signup_again(test_client):
    """Test signup -> unregister -> signup again workflow."""
    email = "rejoin@mergington.edu"
    activity = "Debate Team"
    
    # First signup
    response1 = test_client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    assert response1.status_code == 200
    
    activities = test_client.get("/activities").json()
    assert email in activities[activity]["participants"]
    
    # Unregister
    response2 = test_client.delete(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    assert response2.status_code == 200
    
    activities = test_client.get("/activities").json()
    assert email not in activities[activity]["participants"]
    
    # Sign up again
    response3 = test_client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    assert response3.status_code == 200
    
    activities = test_client.get("/activities").json()
    assert email in activities[activity]["participants"]


def test_multiple_students_same_activity(test_client):
    """Test multiple students signing up and unregistering from the same activity."""
    activity = "Gym Class"
    emails = ["multi1@mergington.edu", "multi2@mergington.edu", "multi3@mergington.edu"]
    
    # All students sign up
    for email in emails:
        response = test_client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert response.status_code == 200
    
    # Verify all are registered
    activities = test_client.get("/activities").json()
    for email in emails:
        assert email in activities[activity]["participants"]
    
    # Remove second student
    response = test_client.delete(
        f"/activities/{activity}/signup",
        params={"email": emails[1]}
    )
    assert response.status_code == 200
    
    # Verify correct one was removed
    activities = test_client.get("/activities").json()
    assert emails[0] in activities[activity]["participants"]
    assert emails[1] not in activities[activity]["participants"]
    assert emails[2] in activities[activity]["participants"]
    
    # Remove first student
    response = test_client.delete(
        f"/activities/{activity}/signup",
        params={"email": emails[0]}
    )
    assert response.status_code == 200
    
    # Verify
    activities = test_client.get("/activities").json()
    assert emails[0] not in activities[activity]["participants"]
    assert emails[2] in activities[activity]["participants"]


def test_student_multiple_activities(test_client):
    """Test a student signing up for multiple activities."""
    email = "versatile@mergington.edu"
    activities = ["Chess Club", "Programming Class", "Drama Club"]
    
    # Sign up for all activities
    for activity in activities:
        response = test_client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert response.status_code == 200
    
    # Verify in all activities
    all_activities = test_client.get("/activities").json()
    for activity in activities:
        assert email in all_activities[activity]["participants"]
    
    # Unregister from middle activity
    response = test_client.delete(
        f"/activities/{activities[1]}/signup",
        params={"email": email}
    )
    assert response.status_code == 200
    
    # Verify still in others but not in the middle one
    all_activities = test_client.get("/activities").json()
    assert email in all_activities[activities[0]]["participants"]
    assert email not in all_activities[activities[1]]["participants"]
    assert email in all_activities[activities[2]]["participants"]


def test_error_recovery_workflow(test_client):
    """Test that system recovers properly after errors."""
    email = "error@mergington.edu"
    activity = "Science Club"
    
    # Try invalid activity first
    response = test_client.post(
        "/activities/Fake Activity/signup",
        params={"email": email}
    )
    assert response.status_code == 404
    
    # Valid signup should still work
    response = test_client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    assert response.status_code == 200
    
    # Try duplicate signup
    response = test_client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    assert response.status_code == 400
    
    # But unregister should still work
    response = test_client.delete(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    assert response.status_code == 200


def test_concurrent_operations_simulation(test_client):
    """Simulate rapid sequential operations (like concurrent requests)."""
    activity = "Basketball Team"
    
    # Rapid signups
    emails = [f"rapid{i}@mergington.edu" for i in range(5)]
    
    for email in emails:
        response = test_client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert response.status_code == 200
    
    # Rapid retrievals should all show all signups
    for _ in range(3):
        activities = test_client.get("/activities").json()
        for email in emails:
            assert email in activities[activity]["participants"]
    
    # Rapid unregisters
    for email in emails:
        response = test_client.delete(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert response.status_code == 200
    
    # Final check - all should be gone
    activities = test_client.get("/activities").json()
    for email in emails:
        assert email not in activities[activity]["participants"]
