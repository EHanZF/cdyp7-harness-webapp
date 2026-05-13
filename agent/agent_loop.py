import requests
from openai import OpenAI

BASE_URL = "https://your-api.azurewebsites.net"

client = OpenAI()

# Step 1 — get tools from MCP
def get_tools():
    return requests.get(f"{BASE_URL}/mcp/tools/list").json()["tools"]

# Step 2 — call tool
def call_tool(name, args):
    return requests.post(
        f"{BASE_URL}/mcp/tools/call",
        json={
            "tool_name": name,
            "actor": "copilot@company.com",
            "run_id": "agent-run-1",
            "arguments": args
        }
    ).json()

# Step 3 — agent loop
def run_agent(prompt):
    tools = get_tools()

    response = client.responses.create(
        model="gpt-4.1",
        input=prompt,
        tools=tools
    )

    for item in response.output:
        if item.type == "tool_call":
            result = call_tool(item.name, item.arguments)

            return client.responses.create(
                model="gpt-4.1",
                input=f"Tool output: {result}"
            )

    return response.output_text


print(run_agent("Generate a release sheet for system ABS"))
