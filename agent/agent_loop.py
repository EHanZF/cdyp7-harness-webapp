import requests
import os
from openai import OpenAI

# ✅ Your deployed MCP API
BASE_URL = os.getenv("MCP_BASE_URL", "http://127.0.0.1:8000")

# ✅ OpenAI / Azure OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ✅ Step 1: fetch tool definitions from MCP
def get_tools():
    response = requests.get(f"{BASE_URL}/mcp/tools/list")
    response.raise_for_status()
    return response.json()["tools"]

# ✅ Step 2: call MCP tool
def call_tool(tool_name, arguments):
    response = requests.post(
        f"{BASE_URL}/mcp/tools/call",
        json={
            "tool_name": tool_name,
            "actor": "agent@runtime",
            "run_id": "agent-run-1",
            "arguments": arguments,
        },
    )
    response.raise_for_status()
    return response.json()["result"]

# ✅ Step 3: agent loop
def run_agent(prompt):
    tools = get_tools()

    response = client.responses.create(
        model="gpt-4.1",
        input=prompt,
        tools=tools,
    )

    # ✅ handle tool calls
    for item in response.output:
        if item.type == "tool_call":

            tool_result = call_tool(
                tool_name=item.name,
                arguments=item.arguments,
            )

            # ✅ feed tool result back to LLM
            final_response = client.responses.create(
                model="gpt-4.1",
                input=[
                    {"role": "user", "content": prompt},
                    {
                        "role": "assistant",
                        "tool_calls": [
                            {
                                "name": item.name,
                                "arguments": item.arguments,
                                "id": item.id
                            }
                        ],
                    },
                    {
                        "role": "tool",
                        "tool_call_id": item.id,
                        "content": str(tool_result),
                    },
                ],
            )

            return final_response.output_text

    return response.output_text


if __name__ == "__main__":
    print(run_agent("Generate a release sheet for ABS system"))
