"""
Pytest configuration and shared fixtures for the activities API tests.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def test_client():
    """Provide a TestClient instance for making requests to the API."""
    return TestClient(app)


@pytest.fixture
def sample_activity():
    """Sample activity data for testing."""
    return {
        "name": "Sample Activity",
        "description": "A sample test activity",
        "schedule": "Mondays, 3:00 PM - 4:00 PM",
        "max_participants": 10,
        "participants": ["sample@test.edu"]
    }
