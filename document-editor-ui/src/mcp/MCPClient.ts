import { MCPRequest, MCPResponse } from "./types";

export class MCPClient {
  private endpoint: string;

  constructor(endpoint: string) {
    this.endpoint = endpoint;
  }

  async call<T = any>(method: string, params?: any): Promise<T> {
    const payload: MCPRequest = {
      jsonrpc: "2.0",
      id: crypto.randomUUID(),
      method,
      params,
    };

    const response = await fetch(this.endpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    const data: MCPResponse<T> = await response.json();

    if (data.error) {
      throw new Error(data.error.message);
    }

    return data.result as T;
  }

  /** Convenience wrapper for MCP tools */
  async callTool<T = any>(toolName: string, args: Record<string, any>) {
    return this.call<T>("tools/call", {
      name: toolName,
      arguments: args,
    });
  }
}
