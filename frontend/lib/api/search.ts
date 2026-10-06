import { apiRequest } from "@/lib/api/client";
import type { SearchRequest, SearchResponse } from "@/lib/types/search";

export async function searchDocument(
  request: SearchRequest,
): Promise<SearchResponse> {
  return apiRequest<SearchResponse>("/documents/search", {
    method: "POST",
    body: JSON.stringify(request),
  });
}
