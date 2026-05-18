import { MCPClient } from "./MCPClient";

/**
 * MCP server endpoint
 * Example:
 *  - http://localhost:3333/mcp
 *  - https://ai.internal.zf.com/mcp
 */
export const mcp = new MCPClient(
  import.meta.env.VITE_MCP_ENDPOINT || "/mcp"
);
