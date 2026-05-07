from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_returns_ok():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_mcp_tools_list_returns_tools():
    response = client.get("/mcp/tools/list")

    assert response.status_code == 200
    body = response.json()
    assert "tools" in body
    assert any(tool["name"] == "harness.generate_release_sheet" for tool in body["tools"])


def test_mcp_tools_call_unknown_tool_fails_closed():
    response = client.post(
        "/mcp/tools/call",
        json={
            "tool_name": "unknown.tool",
            "arguments": {},
            "actor": "user@example.com",
            "run_id": "run-test",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"]["fail_closed"] is True


def test_outputs_missing_file_returns_404():
    response = client.get("/outputs/does-not-exist.docx")

    assert response.status_code == 404
