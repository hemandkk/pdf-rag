"use client";

import { useEffect, useState } from "react";

import { ConversationSidebar } from "@/components/chat/conversation-sidebar";

import { ChatWindow } from "@/components/chat/chat-window";

import { AppHeader } from "@/components/ui/app-header";

import { createConversation, getConversations } from "@/lib/api/coversations";

import type { Conversation } from "@/lib/types/converstion";

interface ChatPageProps {
  params: Promise<{
    documentId: string;
  }>;
}

export default function ChatPage({ params }: ChatPageProps) {
  const [documentId, setDocumentId] = useState<string | null>(null);

  const [conversations, setConversations] = useState<Conversation[]>([]);

  const [activeConversationId, setActiveConversationId] = useState<
    string | null
  >(null);

  const [isLoading, setIsLoading] = useState(true);

  const [isCreating, setIsCreating] = useState(false);

  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function initialize() {
      try {
        setIsLoading(true);
        setError(null);

        const resolvedParams = await params;

        const currentDocumentId = resolvedParams.documentId;

        if (cancelled) {
          return;
        }

        setDocumentId(currentDocumentId);

        const existingConversations = await getConversations(currentDocumentId);

        if (cancelled) {
          return;
        }

        if (existingConversations.length > 0) {
          setConversations(existingConversations);

          setActiveConversationId(existingConversations[0].id);

          return;
        }

        const newConversation = await createConversation({
          document_id: currentDocumentId,
          title: "New conversation",
        });

        if (cancelled) {
          return;
        }

        setConversations([newConversation]);

        setActiveConversationId(newConversation.id);
      } catch (initializationError) {
        if (cancelled) {
          return;
        }

        const message =
          initializationError instanceof Error
            ? initializationError.message
            : "Failed to load conversations.";

        setError(message);
      } finally {
        if (!cancelled) {
          setIsLoading(false);
        }
      }
    }

    initialize();

    return () => {
      cancelled = true;
    };
  }, [params]);

  const handleCreateConversation = async () => {
    if (!documentId || isCreating) {
      return;
    }

    try {
      setIsCreating(true);
      setError(null);

      const conversation = await createConversation({
        document_id: documentId,
        title: "New conversation",
      });

      setConversations((current) => [conversation, ...current]);

      setActiveConversationId(conversation.id);
    } catch (creationError) {
      const message =
        creationError instanceof Error
          ? creationError.message
          : "Failed to create conversation.";

      setError(message);
    } finally {
      setIsCreating(false);
    }
  };

  const handleSelectConversation = (conversationId: string) => {
    if (conversationId === activeConversationId) {
      return;
    }

    setActiveConversationId(conversationId);
  };

  if (isLoading) {
    return (
      <div className="flex min-h-screen flex-col">
        <AppHeader
          title="Document Chat"
          description="Ask questions about your PDF."
          backHref="/documents"
          backLabel="Documents"
        />

        <main className="flex flex-1 items-center justify-center">
          <div className="text-center">
            <div className="mx-auto h-6 w-6 animate-spin rounded-full border-2 border-muted border-t-foreground" />

            <p className="mt-3 text-sm text-muted-foreground">
              Loading conversations...
            </p>
          </div>
        </main>
      </div>
    );
  }

  if (error && !documentId) {
    return (
      <div className="flex min-h-screen flex-col">
        <AppHeader
          title="Document Chat"
          description="Ask questions about your PDF."
          backHref="/documents"
          backLabel="Documents"
        />

        <main className="flex flex-1 items-center justify-center p-6">
          <div className="w-full max-w-lg rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">
            <p className="font-medium">Failed to load conversations</p>

            <p className="mt-1">{error}</p>
          </div>
        </main>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen flex-col">
      <AppHeader
        title="Document Chat"
        description="Ask questions about your PDF."
        backHref="/documents"
        backLabel="Documents"
      />

      {error && (
        <div className="border-b px-4 py-2">
          <div className="mx-auto max-w-7xl rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">
            {error}
          </div>
        </div>
      )}

      <main className="flex min-h-0 flex-1">
        <ConversationSidebar
          conversations={conversations}
          activeConversationId={activeConversationId}
          isLoading={false}
          isCreating={isCreating}
          onSelect={handleSelectConversation}
          onCreate={handleCreateConversation}
        />

        <div className="min-w-0 flex-1">
          {activeConversationId && documentId ? (
            <ChatWindow
              key={activeConversationId}
              documentId={documentId}
              conversationId={activeConversationId}
            />
          ) : (
            <div className="flex h-full items-center justify-center">
              <p className="text-sm text-muted-foreground">
                Select a conversation.
              </p>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
