"use client";

import { useEffect, useRef, useState } from "react";

import { useMutation } from "@tanstack/react-query";

import { chatWithDocument } from "@/lib/api/chat";
import { ApiError } from "@/lib/api/client";
import type { ChatResponse } from "@/lib/types/chat";

import { ChatInput } from "@/components/chat/chat-input";
import { ChatMessage } from "@/components/chat/chat-message";

interface ChatWindowProps {
  documentId: string;
}

export function ChatWindow({ documentId }: ChatWindowProps) {
  const [messages, setMessages] = useState<ChatResponse[]>([]);

  const [error, setError] = useState<string | null>(null);

  const messagesEndRef = useRef<HTMLDivElement>(null);

  const chatMutation = useMutation({
    mutationFn: (question: string) =>
      chatWithDocument({
        document_id: documentId,
        question,
        top_k: 5,
      }),

    onSuccess: (response) => {
      setError(null);

      setMessages((currentMessages) => [...currentMessages, response]);
    },

    onError: (chatError: unknown) => {
      if (chatError instanceof ApiError) {
        setError(chatError.message);
        return;
      }

      if (chatError instanceof Error) {
        setError(chatError.message);
        return;
      }

      setError("Failed to get an answer.");
    },
  });

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, chatMutation.isPending]);

  function handleSubmit(question: string) {
    setError(null);
    chatMutation.mutate(question);
  }

  return (
    <div className="flex h-[calc(100vh-73px)] flex-col">
      <div className="flex-1 overflow-y-auto">
        <div className="mx-auto max-w-4xl px-6 py-8">
          {messages.length === 0 && (
            <div className="flex min-h-[50vh] items-center justify-center">
              <div className="max-w-xl text-center">
                <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-slate-900 text-2xl">
                  ✨
                </div>

                <h2 className="mt-5 text-2xl font-bold">
                  Ask about this document
                </h2>

                <p className="mt-3 text-sm leading-6 text-slate-400">
                  Ask a question and the RAG pipeline will retrieve relevant
                  sections from the PDF before generating an answer.
                </p>

                <div className="mt-6 grid gap-3 text-left sm:grid-cols-2">
                  {[
                    "What is this document about?",
                    "What are the main concepts?",
                    "Summarize the key points.",
                    "What does the document recommend?",
                  ].map((question) => (
                    <button
                      key={question}
                      type="button"
                      onClick={() => handleSubmit(question)}
                      disabled={chatMutation.isPending}
                      className="rounded-lg border border-slate-800 bg-slate-900 p-4 text-left text-sm text-slate-300 transition hover:border-slate-600 hover:bg-slate-800 disabled:opacity-50"
                    >
                      {question}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          )}

          {messages.length > 0 && (
            <div className="space-y-8">
              {messages.map((message, index) => (
                <ChatMessage
                  key={`${message.question}-${index}`}
                  response={message}
                />
              ))}
            </div>
          )}

          {chatMutation.isPending && (
            <div className="mt-8 flex justify-start">
              <div className="rounded-2xl rounded-bl-md border border-slate-800 bg-slate-900 px-5 py-4">
                <div className="flex items-center gap-3">
                  <div className="flex gap-1">
                    <span className="h-2 w-2 animate-bounce rounded-full bg-slate-500 [animation-delay:-0.3s]" />
                    <span className="h-2 w-2 animate-bounce rounded-full bg-slate-500 [animation-delay:-0.15s]" />
                    <span className="h-2 w-2 animate-bounce rounded-full bg-slate-500" />
                  </div>

                  <span className="text-sm text-slate-400">
                    Searching the document and generating an answer...
                  </span>
                </div>
              </div>
            </div>
          )}

          {error && (
            <div className="mt-6 rounded-lg border border-red-800 bg-red-950/40 p-4">
              <p className="text-sm text-red-300">{error}</p>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>

      <ChatInput onSubmit={handleSubmit} disabled={chatMutation.isPending} />
    </div>
  );
}
