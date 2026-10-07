"use client";

import { useEffect, useRef, useState } from "react";

import {
  getConversation,
  streamConversationMessage,
} from "@/lib/api/coversations";

import type { ChatSource } from "@/lib/types/chat";

import { ChatInput } from "./chat-input";
import { ChatMessage } from "./chat-message";

interface ChatWindowProps {
  documentId: string;
  conversationId: string;
}

interface ChatMessageState {
  id: string;
  question: string;
  answer: string;
  sources: ChatSource[];
  isStreaming: boolean;
}

export function ChatWindow({ documentId, conversationId }: ChatWindowProps) {
  const [messages, setMessages] = useState<ChatMessageState[]>([]);

  const [isLoadingHistory, setIsLoadingHistory] = useState(true);

  const [error, setError] = useState<string | null>(null);

  const [isStreaming, setIsStreaming] = useState(false);

  const abortControllerRef = useRef<AbortController | null>(null);

  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function loadConversation() {
      setIsLoadingHistory(true);
      setError(null);

      try {
        const conversation = await getConversation(conversationId);

        if (cancelled) {
          return;
        }

        const restoredMessages: ChatMessageState[] = [];

        let pendingQuestion: string | null = null;

        for (const message of conversation.messages) {
          if (message.role === "user") {
            pendingQuestion = message.content;
            continue;
          }

          if (message.role === "assistant" && pendingQuestion !== null) {
            restoredMessages.push({
              id: message.id,
              question: pendingQuestion,
              answer: message.content,
              sources: [],
              isStreaming: false,
            });

            pendingQuestion = null;
          }
        }

        setMessages(restoredMessages);
      } catch (loadError) {
        if (cancelled) {
          return;
        }

        const message =
          loadError instanceof Error
            ? loadError.message
            : "Failed to load conversation.";

        setError(message);
      } finally {
        if (!cancelled) {
          setIsLoadingHistory(false);
        }
      }
    }

    loadConversation();

    return () => {
      cancelled = true;
    };
  }, [conversationId]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages]);

  const updateMessage = (
    id: string,
    updater: (message: ChatMessageState) => ChatMessageState,
  ) => {
    setMessages((current) =>
      current.map((message) =>
        message.id === id ? updater(message) : message,
      ),
    );
  };

  const handleSubmit = async (question: string) => {
    if (isStreaming) {
      return;
    }

    const trimmedQuestion = question.trim();

    if (!trimmedQuestion) {
      return;
    }

    if (!documentId) {
      setError("Document ID is missing.");
      return;
    }

    if (!conversationId) {
      setError("Conversation is not ready yet.");
      return;
    }

    setError(null);
    setIsStreaming(true);

    const messageId = crypto.randomUUID();

    setMessages((current) => [
      ...current,
      {
        id: messageId,
        question: trimmedQuestion,
        answer: "",
        sources: [],
        isStreaming: true,
      },
    ]);

    const controller = new AbortController();

    abortControllerRef.current = controller;

    try {
      await streamConversationMessage(
        conversationId,
        trimmedQuestion,
        {
          onToken: (text) => {
            updateMessage(messageId, (message) => ({
              ...message,
              answer: message.answer + text,
            }));
          },

          onSources: (sources) => {
            updateMessage(messageId, (message) => ({
              ...message,
              sources,
            }));
          },

          onDone: () => {
            updateMessage(messageId, (message) => ({
              ...message,
              isStreaming: false,
            }));
          },
        },
        controller.signal,
      );
    } catch (streamError) {
      if (
        streamError instanceof DOMException &&
        streamError.name === "AbortError"
      ) {
        return;
      }

      const message =
        streamError instanceof Error
          ? streamError.message
          : "Something went wrong while generating the answer.";

      setError(message);

      updateMessage(messageId, (current) => ({
        ...current,
        isStreaming: false,
      }));
    } finally {
      setIsStreaming(false);
      abortControllerRef.current = null;
    }
  };

  const handleStop = () => {
    abortControllerRef.current?.abort();

    abortControllerRef.current = null;

    setIsStreaming(false);

    setMessages((current) =>
      current.map((message) =>
        message.isStreaming
          ? {
              ...message,
              isStreaming: false,
            }
          : message,
      ),
    );
  };

  if (isLoadingHistory) {
    return (
      <div className="flex h-full min-h-[calc(100vh-73px)] items-center justify-center">
        <div className="text-center">
          <div className="mx-auto h-6 w-6 animate-spin rounded-full border-2 border-muted border-t-foreground" />

          <p className="mt-3 text-sm text-muted-foreground">
            Loading conversation...
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-full min-h-[calc(100vh-73px)] flex-col">
      <div className="flex-1 overflow-y-auto">
        {messages.length === 0 ? (
          <div className="flex min-h-[calc(100vh-220px)] items-center justify-center p-8">
            <div className="w-full max-w-xl text-center">
              <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl border bg-muted text-xl">
                ✦
              </div>

              <h2 className="mt-5 text-xl font-semibold tracking-tight">
                Ask a question about this document
              </h2>

              <p className="mt-2 text-sm leading-6 text-muted-foreground">
                Ask something specific and the answer will be generated from the
                relevant sections of your PDF.
              </p>

              <div className="mt-6 grid gap-2 text-left">
                {[
                  "What is this document about?",
                  "Summarize the main points.",
                  "What are the key conclusions?",
                ].map((suggestion) => (
                  <button
                    key={suggestion}
                    type="button"
                    onClick={() => handleSubmit(suggestion)}
                    disabled={isStreaming}
                    className="rounded-xl border bg-background p-3.5 text-sm transition hover:bg-muted disabled:cursor-not-allowed disabled:opacity-50"
                  >
                    {suggestion}
                  </button>
                ))}
              </div>
            </div>
          </div>
        ) : (
          <div className="mx-auto w-full max-w-4xl space-y-6 p-6">
            {messages.map((message) => (
              <ChatMessage
                key={message.id}
                question={message.question}
                answer={message.answer}
                sources={message.sources}
                isStreaming={message.isStreaming}
              />
            ))}

            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      {error && (
        <div className="border-t px-4 py-3">
          <div className="mx-auto max-w-4xl rounded-xl border border-red-200 bg-red-50 p-3 text-sm text-red-700">
            {error}
          </div>
        </div>
      )}

      <div className="border-t bg-background p-4">
        <div className="mx-auto max-w-4xl">
          {isStreaming && (
            <div className="mb-2 flex justify-end">
              <button
                type="button"
                onClick={handleStop}
                className="rounded-lg border px-3 py-1.5 text-sm font-medium transition hover:bg-muted"
              >
                Stop generating
              </button>
            </div>
          )}

          <ChatInput onSubmit={handleSubmit} disabled={isStreaming} />
        </div>
      </div>
    </div>
  );
}
