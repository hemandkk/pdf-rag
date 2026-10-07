"use client";

import { useState } from "react";

import type { Conversation } from "@/lib/types/converstion";

interface ConversationSidebarProps {
  conversations: Conversation[];
  activeConversationId: string | null;
  isLoading: boolean;
  isCreating: boolean;
  onSelect: (conversationId: string) => void;
  onCreate: () => void;
}

function formatConversationDate(dateString: string): string {
  const date = new Date(dateString);

  if (Number.isNaN(date.getTime())) {
    return "";
  }

  return date.toLocaleDateString(undefined, {
    month: "short",
    day: "numeric",
  });
}

export function ConversationSidebar({
  conversations,
  activeConversationId,
  isLoading,
  isCreating,
  onSelect,
  onCreate,
}: ConversationSidebarProps) {
  const [isOpen, setIsOpen] = useState(true);

  return (
    <aside
      className={[
        "flex flex-col border-r bg-muted/30 transition-all",
        isOpen ? "w-72" : "w-14",
      ].join(" ")}
    >
      <div className="flex items-center justify-between border-b p-3">
        {isOpen && <h2 className="text-sm font-semibold">Conversations</h2>}

        <button
          type="button"
          onClick={() => setIsOpen((value) => !value)}
          className="rounded-md p-2 text-sm hover:bg-muted"
          aria-label={isOpen ? "Collapse sidebar" : "Expand sidebar"}
        >
          {isOpen ? "←" : "→"}
        </button>
      </div>

      {isOpen && (
        <>
          <div className="p-3">
            <button
              type="button"
              onClick={onCreate}
              disabled={isCreating}
              className="w-full rounded-lg border bg-background px-3 py-2 text-sm font-medium transition hover:bg-muted disabled:cursor-not-allowed disabled:opacity-50"
            >
              {isCreating ? "Creating..." : "+ New chat"}
            </button>
          </div>

          <div className="flex-1 overflow-y-auto px-2 pb-3">
            {isLoading ? (
              <div className="space-y-2 p-2">
                {Array.from({
                  length: 4,
                }).map((_, index) => (
                  <div
                    key={index}
                    className="h-12 animate-pulse rounded-lg bg-muted"
                  />
                ))}
              </div>
            ) : conversations.length === 0 ? (
              <div className="px-3 py-6 text-center">
                <p className="text-sm text-muted-foreground">
                  No conversations yet.
                </p>

                <p className="mt-1 text-xs text-muted-foreground">
                  Start a new chat to ask questions about this document.
                </p>
              </div>
            ) : (
              <div className="space-y-1">
                {conversations.map((conversation) => {
                  const isActive = conversation.id === activeConversationId;

                  return (
                    <button
                      key={conversation.id}
                      type="button"
                      onClick={() => onSelect(conversation.id)}
                      className={[
                        "w-full rounded-lg px-3 py-2.5 text-left transition",
                        isActive ? "bg-background shadow-sm" : "hover:bg-muted",
                      ].join(" ")}
                    >
                      <div className="flex items-start justify-between gap-2">
                        <span className="min-w-0 flex-1 truncate text-sm font-medium">
                          {conversation.title}
                        </span>

                        <span className="shrink-0 text-[11px] text-muted-foreground">
                          {formatConversationDate(conversation.updated_at)}
                        </span>
                      </div>
                    </button>
                  );
                })}
              </div>
            )}
          </div>
        </>
      )}
    </aside>
  );
}
