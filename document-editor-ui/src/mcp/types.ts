export type MCPRequest = {
  jsonrpc: "2.0";
  id: string;
  method: string;
  params?: any;
};

export type MCPResponse<T = any> = {
  jsonrpc: "2.0";
  id: string;
  result?: T;
  error?: {
    code: number;
    message: string;
    data?: any;
  };
};

export type MCPToolCall = {
  name: string;
  arguments: Record<string, any>;
};
