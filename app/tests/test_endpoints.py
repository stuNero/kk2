import pytest
from fastapi.testclient import TestClient
import pandas as pd
from io import StringIO

@pytest.fixture
def client() -> TestClient:
    from app.main import app
    return TestClient(app)

@pytest.fixture(autouse=True)
def reset():
    """Reset the uploaded dataset before each test"""
    from app import main
    main.uploaded_dataset = None
    yield
    main.uploaded_dataset = None

def test_health_returns_ok(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}

def test_ask_returns_200(client):
    csv_content = "name,age\nMax,30\nSara,25\n"

    upload_resp = client.post(
        "/data/upload",
        files={"file": ("people.csv", csv_content, "text/csv")},
    )
    assert upload_resp.status_code == 200
    
    resp = client.post("ai/ask", json={"question":"test"})
    assert resp.status_code == 200
    
def test_upload_returns_200(client):
    csv_content = "name,age\nMax,30\nSara,25\n"

    resp = client.post(
        "/data/upload",
        files={
            "file": ("people.csv", csv_content, "text/csv")
        },
    )
    assert resp.status_code == 200

def test_upload_rejects_non_csv(client):
    csv_content = "name,age\nMax,30\nSara,25\n"

    resp = client.post(
        "/data/upload",
        files={
            "file": ("people.txt", csv_content, "text/csv")
        },
    )
    assert resp.status_code == 400

def test_stats_returns_described_dataset(client):
    csv_content = "name,age\nMax,30\nSara,25\n"
    df = pd.read_csv(StringIO(csv_content))
    
    resp = client.post(
        "/data/upload",
        files={
            "file": ("people.csv", csv_content, "text/csv")
        },
    )
    
    assert resp.status_code == 200
    
    resp = client.get("/data/stats")
    
    assert resp.status_code == 200
    assert resp.json()["stats"] == df.describe().to_dict()

def test_stats_returns_404_when_no_dataset(client):
    resp = client.get("/data/stats")
    
    assert resp.status_code == 404