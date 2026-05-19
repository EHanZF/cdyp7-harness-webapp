import { apiRequest } from "./client";
import type { DatasetType } from "./mcpService";

interface ImportResponse {
    success: boolean;
    message?: string;
}

export async function importData(
    dataset: DatasetType,
    file: File
): Promise<ImportResponse> {
    const formData = new FormData();
    formData.append("dataset", dataset);
    formData.append("file", file);

    return apiRequest<ImportResponse>("/api/mcp/import", {
        method: "POST",
        body: formData,
    });
}
