import { apiRequest } from "@/lib/api/client";
import type { ChatRequest, ChatResponse } from "@/lib/types/chat";

export async function chatWithDocument(
  request: ChatRequest,
): Promise<ChatResponse> {
  return apiRequest<ChatResponse>("/chat", {
    method: "POST",
    body: JSON.stringify(request),
  });
}
