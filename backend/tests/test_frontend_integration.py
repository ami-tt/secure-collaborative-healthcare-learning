import os

import sys

import pytest

from fastapi.testclient import TestClient



sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))



from app.main import app



client = TestClient(app)





def test_frontend_app_endpoint_serves_html():

    """Verify GET /app serves the interactive React single page application."""

    response = client.get("/app")

    assert response.status_code == 200, response.text

    assert "text/html" in response.headers.get("content-type", "")

    assert '<div id="root"></div>' in response.text

    assert "SecureFL Health" in response.text

    assert "react@18" in response.text





def test_root_endpoint_html_content_negotiation():

    """Verify GET / serves HTML when accessed by a browser (Accept: text/html)."""

    headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9"}

    response = client.get("/", headers=headers)

    assert response.status_code == 200

    assert "text/html" in response.headers.get("content-type", "")

    assert '<div id="root"></div>' in response.text





def test_static_bundle_accessible():

    """Verify static assets are mounted and accessible."""

    response = client.get("/static/index.html")

    assert response.status_code == 200

    assert "FedAvg Core" in response.text





def test_all_frontend_api_routes_registered():

    """Verify that all API routes called by the React frontend exist on the backend."""

    openapi_spec = client.get("/openapi.json").json()

    paths = openapi_spec.get("paths", {})



    expected_routes = [

        "/api/v1/auth/login",

        "/api/v1/auth/register",

        "/api/v1/auth/me",

        "/api/v1/users/",

        "/api/v1/institutions/",

        "/api/v1/datasets/",

        "/api/v1/fl/projects",

        "/api/v1/fl/sessions",

        "/api/v1/audit/",

    ]



    for route in expected_routes:

        assert route in paths, f"Route {route} expected by frontend is missing from backend OpenAPI schema"
