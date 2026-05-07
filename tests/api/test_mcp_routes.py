from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

MCP_HEADERS = {"x-internal-runtime": "intent-boundary"}


def test_mcp_get_returns_405():
    response = client.get("/mcp")
    assert response.status_code == 405


def test_mcp_post_without_guard_header_fails():
    response = client.post(
        "/mcp",
        json={"jsonrpc": "2.0", "id": "test-1", "method": "tools/list"},
    )

    assert response.status_code in {400, 401, 403}


def test_mcp_tools_list_success():
    response = client.post(
        "/mcp",
        headers=MCP_HEADERS,
        json={"jsonrpc": "2.0", "id": "list-001", "method": "tools/list"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["jsonrpc"] == "2.0"
    assert body["id"] == "list-001"
    assert "result" in body


def test_mcp_unknown_method_fails_closed():
    response = client.post(
        "/mcp",
        headers=MCP_HEADERS,
        json={"jsonrpc": "2.0", "id": "bad-001", "method": "unknown.method"},
    )

    assert response.status_code == 200
    body = response.json()
    assert "error" in body
