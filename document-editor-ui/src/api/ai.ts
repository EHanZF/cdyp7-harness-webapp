import { http } from "./http";

export function aiSuggest(sectionId: string, instruction: string) {
  return http<any>("/api/ai/suggest", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ sectionId, instruction }),
  });
}
