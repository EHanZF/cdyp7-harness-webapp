// src/api/dataverse.ts
export async function importToDataverse(
    dataset: string,
    file: File
) {
    const form = new FormData();
    form.append("dataset", dataset);
    form.append("file", file);

    const res = await fetch("/api/dataverse/batch-import", {
        method: "POST",
        body: form,
    });

    if (!res.ok) throw new Error("Dataverse import failed");
}
