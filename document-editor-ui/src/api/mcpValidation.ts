export type DatasetType =
    | "MCP_FEATURES"
    | "FEATURE_REQUIREMENT_TRACE"
    | "FEATURE_REQUIREMENT_VERIFICATION_GRAPH";

export interface ValidationResponse {
    valid: boolean;
    errors?: string[];
    error?: string;
}

export async function validateImport(dataset, file) {
  const formData = new FormData();
  formData.append("dataset", dataset);
  formData.append("file", file);

  const res = await fetch("/api/mcp/validate-import", {
    method: "POST",
    body: formData,
  });

  return res.json();
}
