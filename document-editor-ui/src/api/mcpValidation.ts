// src/api/mcpValidation.ts
export async function validateImport(
    dataset: string,
    file: File
): Promise<any> {
    const form = new FormData();
    form.append("dataset", dataset);
    form.append("file", file);

    const res = await fetch("/api/mcp/validate-import", {
        method: "POST",
        body: form,
    });

    return res.json();
}
