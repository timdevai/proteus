"""
Integration test: server registers a user, receives a webhook, processes event end-to-end.
Runs against a live TestClient (no actual network needed).
"""
import asyncio
import sys
import pathlib
import os

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

# Point to temp data dir so test doesn't touch production DB
import tempfile
_tmp = tempfile.mkdtemp()
os.environ["PROTEUS_DATA"] = _tmp

from fastapi.testclient import TestClient
from server.app import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
    print("PASS: /health")


def test_register_and_webhook():
    # Register user
    r = client.post("/register", json={"email": "test@example.com", "tier": "base"})
    assert r.status_code == 200, f"register failed: {r.text}"
    data = r.json()
    token = data["token"]
    assert token
    print(f"PASS: /register -> token={token[:12]}...")

    # Duplicate registration should fail
    r2 = client.post("/register", json={"email": "test@example.com"})
    assert r2.status_code == 400
    print("PASS: duplicate register blocked")

    # Send a webhook event
    r3 = client.post(
        f"/webhook/{token}/gmail",
        content=b"New email from supplier: shipment delayed 3 days, order #4821",
    )
    assert r3.status_code == 200, f"webhook failed: {r3.text}"
    body = r3.json()
    assert body["status"] == "queued"
    assert "event_id" in body
    print(f"PASS: /webhook queued event_id={body['event_id'][:8]}...")

    # Stats
    r4 = client.get(f"/stats/{token}")
    assert r4.status_code == 200
    stats = r4.json()
    assert stats["user"]["email"] == "test@example.com"
    assert stats["user"]["events_total"] == 1
    print(f"PASS: /stats -> {stats['bus']}")

    # Invalid token rejected
    r5 = client.post("/webhook/badtoken/gmail", content=b"test")
    assert r5.status_code == 401
    print("PASS: invalid token rejected")

    # BYOK key storage
    r6 = client.post(f"/apikey/{token}", json={"api_key": "sk-ant-test-key-placeholder"})
    assert r6.status_code == 200
    assert r6.json()["tier"] == "byok"
    print("PASS: /apikey stored, tier upgraded to byok")


def test_upgrade():
    r = client.post("/register", json={"email": "upgrade@example.com", "tier": "base"})
    token = r.json()["token"]
    r2 = client.post(f"/upgrade/{token}", json={"tier": "pro"})
    assert r2.status_code == 200
    assert r2.json()["tier"] == "pro"
    print("PASS: /upgrade base -> pro")


def test_brief_endpoint():
    r = client.post("/register", json={"email": "brief@example.com", "tier": "base"})
    token = r.json()["token"]

    # No briefs yet
    r2 = client.get(f"/brief/{token}")
    assert r2.status_code == 200
    assert r2.json()["status"] == "none"
    print("PASS: /brief returns none when empty")

    # Trigger a brief (fire-and-forget, no API key in test env)
    r3 = client.post(f"/brief/{token}/trigger")
    assert r3.status_code == 200
    assert r3.json()["status"] == "queued"
    print("PASS: /brief/trigger queued")

    # Invalid token rejected
    r4 = client.get("/brief/badtoken")
    assert r4.status_code == 401
    print("PASS: /brief invalid token rejected")


if __name__ == "__main__":
    test_health()
    test_register_and_webhook()
    test_upgrade()
    test_brief_endpoint()
    print("\nAll integration tests passed.")
