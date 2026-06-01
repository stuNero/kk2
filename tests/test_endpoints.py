import pytest
from fastapi.testclient import TestClient
import pandas as pd
from io import StringIO

@pytest.fixture
def client() -> TestClient:
    from app.main import app
    return TestClient(app)

def test_health_returns_ok(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}

def test_ask_returns_200(client):
    resp = client.post("ai/ask", json={"prompt":"test"})
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
    
    assert resp.json() == df.describe().to_dict()
    assert resp.status_code == 200