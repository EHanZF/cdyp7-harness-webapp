def test_tools_list_exposes_semantic_search(client):
    res = client.post(
        "/mcp",
        json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "params": {},
        },
    )

    assert res.status_code == 200

    body = res.json()
    tools = body["result"]["tools"]

    names = {tool["name"] for tool in tools}

    assert "memory.semantic_search" in names

    semantic_search = next(
        tool for tool in tools if tool["name"] == "memory.semantic_search"
    )

    assert "inputSchema" in semantic_search
    assert "input_schema" not in semantic_search
