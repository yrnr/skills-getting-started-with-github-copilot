"""
Tests for the root endpoint and general API behavior.
"""

import pytest


def test_root_redirect(test_client):
    """Test that GET / redirects to the static HTML."""
    response = test_client.get("/", follow_redirects=False)
    
    # Should return a redirect status
    assert response.status_code == 307  # Temporary redirect
    
    # Should redirect to static/index.html
    assert response.headers["location"] == "/static/index.html"


def test_root_redirect_follows(test_client):
    """Test that following the root redirect works."""
    response = test_client.get("/", follow_redirects=True)
    
    # Should eventually succeed
    assert response.status_code == 200
