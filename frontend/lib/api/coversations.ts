import { apiRequest } from "@/lib/api/client";

import type { ChatSource } from "@/lib/types/chat";

import type {
  Conversation,
  ConversationDetail,
  CreateConversationRequest,
} from "@/lib/types/converstion";

export async function createConversation(
  request: CreateConversationRequest,
): Promise<Conversation> {
  return apiRequest<Conversation>("/conversations", {
    method: "POST",
    body: JSON.stringify(request),
  });
}

export async function getConversations(
  documentId: string,
): Promise<Conversation[]> {
  return apiRequest<Conversation[]>(`/conversations/document/${documentId}`);
}

export async function getConversation(
  conversationId: string,
): Promise<ConversationDetail> {
  return apiRequest<ConversationDetail>(`/conversations/${conversationId}`);
}

interface StreamHandlers {
  onToken: (text: string) => void;

  onSources: (sources: ChatSource[]) => void;

  onDone: () => void;
}

export async function streamConversationMessage(
  conversationId: string,
  question: string,
  handlers: StreamHandlers,
  signal?: AbortSignal,
): Promise<void> {
  const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL;

  if (!baseUrl) {
    throw new Error("NEXT_PUBLIC_API_BASE_URL is not configured.");
  }

  const url = `${baseUrl}/conversations/` + `${conversationId}/messages/stream`;

  const params = new URLSearchParams({
    question,
    top_k: "5",
  });

  const response = await fetch(`${url}?${params.toString()}`, {
    method: "POST",
    headers: {
      Accept: "text/event-stream",
    },
    signal,
  });

  if (!response.ok) {
    let message = `Request failed with status ${response.status}.`;

    try {
      const errorBody = await response.json();

      if (errorBody?.detail) {
        message =
          typeof errorBody.detail === "string" ? errorBody.detail : message;
      }
    } catch {
      // Keep default error message.
    }

    throw new Error(message);
  }

  if (!response.body) {
    throw new Error("Streaming response body is not available.");
  }

  const reader = response.body.getReader();

  const decoder = new TextDecoder("utf-8");

  let buffer = "";

  try {
    while (true) {
      const { value, done } = await reader.read();

      if (done) {
        break;
      }

      buffer += decoder.decode(value, { stream: true });

      const events = buffer.split("\n\n");

      buffer = events.pop() ?? "";

      for (const event of events) {
        processSSEEvent(event, handlers);
      }
    }

    buffer += decoder.decode();

    if (buffer.trim()) {
      processSSEEvent(buffer, handlers);
    }
  } finally {
    reader.releaseLock();
  }
}

function processSSEEvent(event: string, handlers: StreamHandlers): void {
  const lines = event.split("\n");

  let eventType = "message";
  let data = "";

  for (const line of lines) {
    if (line.startsWith("event:")) {
      eventType = line.slice("event:".length).trim();
    }

    if (line.startsWith("data:")) {
      data += line.slice("data:".length).trim();
    }
  }

  if (!data) {
    return;
  }

  const payload = JSON.parse(data);

  switch (eventType) {
    case "token":
      handlers.onToken(payload.text ?? "");
      break;

    case "sources":
      handlers.onSources(payload.sources ?? []);
      break;

    case "done":
      handlers.onDone();
      break;

    case "error":
      throw new Error(payload.message ?? "Streaming request failed.");

    default:
      break;
  }
}
