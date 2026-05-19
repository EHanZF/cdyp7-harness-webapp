import { apiRequest } from "./client";
import type { ValidationResult } from "../types/ValidationResult";

export type DatasetType =
    | "MCP_FEATURES"
    | "FEATURE_REQUIREMENT_TRACE"
    | "FEATURE_REQUIREMENT_VERIFICATION_GRAPH";

export async function validateImport(
    dataset: DatasetType,
    file: File
): Promise<ValidationResult> {
    const formData = new FormData();
    formData.append("dataset", dataset);
    formData.append("file", file);

    return apiRequest<ValidationResult>("/api/mcp/validate-import", {
        method: "POST",
        body: formData,
    });
}
