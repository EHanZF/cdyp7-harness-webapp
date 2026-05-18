import { http } from "./http";

export function uploadDocument(file: File) {
  const form = new FormData();
  form.append("file", file);
  return http<{ documentId: string }>("/api/documents/upload", {
    method: "POST",
    body: form,
  });
}

export function getStructuredDocument(id: string) {
  return http<any>(`/api/documents/${id}/structured`);
}
